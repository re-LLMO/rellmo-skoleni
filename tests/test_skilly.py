"""test_skilly.py — formální správnost všech skillů."""
import re
from pathlib import Path

PLUGIN_ROOT = Path(__file__).parent.parent


def _frontmatter(cesta):
    text = cesta.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, f"{cesta} nemá frontmatter"
    return m.group(1), text


def test_skill_ma_frontmatter_s_nazvem_a_popisem():
    for slozka in (PLUGIN_ROOT / "skills").iterdir():
        if not slozka.is_dir():
            continue
        fm, _ = _frontmatter(slozka / "SKILL.md")
        assert re.search(r"^name:\s*\S+", fm, re.M), slozka.name
        assert re.search(r"^description:\s*\S+", fm, re.M), slozka.name


def test_nazev_v_frontmatteru_odpovida_slozce():
    for slozka in (PLUGIN_ROOT / "skills").iterdir():
        if not slozka.is_dir():
            continue
        fm, _ = _frontmatter(slozka / "SKILL.md")
        assert re.search(rf"^name:\s*{re.escape(slozka.name)}\s*$", fm, re.M), slozka.name


def test_skripty_pluginu_se_volaji_pres_promennou():
    """Skripty se volají absolutní cestou přes proměnnou, nikdy relativně.

    Na Windows leží plugin pod uživatelským profilem a relativní cesta vyvolá
    dotaz na citlivý soubor při každém zápisu. Skripty tohohle pluginu se
    volají přes `${CLAUDE_PLUGIN_ROOT}`; skripty ve složce účastníka (třeba
    vlastní skill účastníka) přes `${CLAUDE_PROJECT_DIR}` — obojí je platná
    absolutní cesta, jen k jinému kořeni.

    Kontrolují se jen řádky se skutečným voláním (obsahují `python3`), ne
    výklad o tom, kam si má účastník uložit vlastní skript — to skill o automatizaci
    potřebuje vysvětlit a je to něco jiného.
    """
    for slozka in (PLUGIN_ROOT / "skills").iterdir():
        if not slozka.is_dir():
            continue
        _, text = _frontmatter(slozka / "SKILL.md")
        for radek in text.splitlines():
            if "python3" not in radek:
                continue
            for odkaz in re.findall(r"[\w./${}]*scripts/\w+\.py", radek):
                assert any(p in odkaz for p in ("CLAUDE_PLUGIN_ROOT", "CLAUDE_PROJECT_DIR")), (
                    f"{slozka.name}: {odkaz} — skript se volá absolutní cestou přes "
                    f"proměnnou, ne relativně"
                )


OCEKAVANE = {
    "skoleni-start", "skoleni-automatizace", "skoleni-brandkit", "skoleni-napoveda", "skoleni-shrnuti",
}


def test_plugin_ma_presne_ctyri_skilly():
    nalezene = {s.name for s in (PLUGIN_ROOT / "skills").iterdir() if s.is_dir()}
    assert nalezene == OCEKAVANE


def test_prikazy_slibene_v_readme_maji_svuj_skill():
    """README slibuje čtyři příkazy. Slash command vzniká z názvu skillu,
    takže rozpor mezi README a složkou skills/ znamená slib, který nikdo
    nesplní — a projeví se to až u účastníka, který ten příkaz napíše."""
    readme = (PLUGIN_ROOT / "README.md").read_text(encoding="utf-8")
    slibene = set(re.findall(r"`/(skoleni-[a-z-]+)`", readme))
    assert slibene == OCEKAVANE, f"README slibuje {slibene - OCEKAVANE}, chybí {OCEKAVANE - slibene}"


def test_cesty_pluginu_se_neberou_z_promennych_prostredi():
    """`${CLAUDE_PLUGIN_ROOT}` a `${CLAUDE_PROJECT_DIR}` dosazuje Claude Code
    do obsahu skillu, ne shell a ne běhové prostředí skriptu.

    Podle reference pluginů se obě hodnoty exportují jako proměnné prostředí
    jen hookům a podprocesům MCP a LSP serverů; do obsahu skillu se dosazují
    inline, kdekoli se zástupný text objeví. `os.environ["CLAUDE_PLUGIN_ROOT"]`
    uvnitř snippetu proto spoléhá na něco, co v prostředí volaného pythonu
    být nemusí — a spadne to až u účastníka.

    Vzniklo z opravného kola: nezávislý oponent tenhle tvar navrhl jako
    opravu domnělé vady heredocu a bylo to naopak.
    """
    for slozka in (PLUGIN_ROOT / "skills").iterdir():
        if not slozka.is_dir():
            continue
        text = (slozka / "SKILL.md").read_text(encoding="utf-8")
        nalezy = re.findall(r'os\.environ\[[\'"]CLAUDE_(?:PLUGIN_ROOT|PROJECT_DIR)[\'"]\]', text)
        assert not nalezy, (
            f"{slozka.name}: {nalezy[0]} — cesty se píšou jako "
            f"${{CLAUDE_PLUGIN_ROOT}}, dosazuje je Claude Code"
        )


def test_odkazane_soubory_v_pluginu_existuji():
    """Rozpor mezi odkazem ve skillu a skutečností se v ostatních testech
    neprojeví a v sále se ukáže až u záchranné brzdy — tedy ve chvíli, kdy
    někdo potřebuje pomoc."""
    vzor = re.compile(r'\$\{CLAUDE_PLUGIN_ROOT\}/((?:references|assets)/[A-Za-z0-9_.*/-]*)')
    chybi = []
    for slozka in (PLUGIN_ROOT / "skills").iterdir():
        if not slozka.is_dir():
            continue
        text = (slozka / "SKILL.md").read_text(encoding="utf-8")
        for rel in set(vzor.findall(text)):
            rel = rel.rstrip("/.,`")
            if not rel:
                continue
            # Odkazy se v textu píšou i jako maska (…_d1_*.json) — ta musí
            # něco najít, jinak by záchranná brzda selhala se stejnou chybou,
            # jako by soubor vůbec neexistoval.
            if "*" in rel:
                if not list(PLUGIN_ROOT.glob(rel)):
                    chybi.append(f"{slozka.name} → {rel}")
            elif not (PLUGIN_ROOT / rel).exists():
                chybi.append(f"{slozka.name} → {rel}")
    assert not chybi, "odkazy bez souboru: " + ", ".join(sorted(chybi))


def test_python_bloky_ve_skillech_jsou_syntakticky_platne():
    """Snippet, který se nedá spustit, spadne až u účastníka.

    Zástupné cesty dosazuje Claude Code do obsahu skillu, takže se před
    kontrolou nahradí jakoukoli platnou cestou — kontroluje se syntaxe,
    ne existence složek.
    """
    import ast

    blok = re.compile(r"```bash\n(.*?)```", re.S)
    heredoc = re.compile(r"python3\s*(?:-\s*\"[^\"]*\"\s*)?<<'PY'\n(.*?)\nPY", re.S)

    chyby = []
    for slozka in (PLUGIN_ROOT / "skills").iterdir():
        if not slozka.is_dir():
            continue
        text = (slozka / "SKILL.md").read_text(encoding="utf-8")
        for kus in blok.findall(text):
            for kod in heredoc.findall(kus):
                kod = (kod.replace("${CLAUDE_PLUGIN_ROOT}", "/tmp/plugin")
                          .replace("${CLAUDE_PROJECT_DIR}", "/tmp/projekt"))
                try:
                    ast.parse(kod)
                except SyntaxError as e:
                    chyby.append(f"{slozka.name}: řádek {e.lineno}: {e.msg}")
    assert not chyby, "; ".join(chyby)


def test_popis_se_vejde_do_limitu_a_ma_spoustec_vpredu():
    """`description` je jediné, podle čeho se model rozhoduje.

    Limit je 1 024 znaků, ale ve výpisech je vidět zhruba prvních 250 —
    spouštěcí fráze musí být v nich, jinak skill nikdo neobjeví.
    """
    for slozka in (PLUGIN_ROOT / "skills").iterdir():
        if not slozka.is_dir():
            continue
        fm, _ = _frontmatter(slozka / "SKILL.md")
        popis = re.search(r"^description:\s*(.+)$", fm, re.M).group(1).strip()
        assert len(popis) <= 1024, f"{slozka.name}: popis má {len(popis)} znaků"
        assert "Použij" in popis[:400] or "použij" in popis[:400], (
            f"{slozka.name}: v prvních 400 znacích chybí věta o tom, KDY skill použít"
        )


def test_prikazy_v_tele_skillu_jsou_v_allowed_tools():
    """Skill, který v těle používá příkaz, na který nemá povolení, vyvolá
    uprostřed běhu dotaz na oprávnění — a účastník netuší, co odpovědět.

    Tuhle chybu už jednou udělal tenhle plugin (`Edit` chybějící v hlavičce),
    takže to hlídá test, ne poznámka.
    """
    sledovane = ("cp", "mkdir", "git", "gh", "python3")
    for slozka in (PLUGIN_ROOT / "skills").iterdir():
        if not slozka.is_dir():
            continue
        fm, text = _frontmatter(slozka / "SKILL.md")
        radek = re.search(r"^allowed-tools:\s*(.+)$", fm, re.M)
        if not radek:
            continue
        povolene = radek.group(1)
        # hledáme jen skutečná volání v blocích ```bash, ne zmínky v textu
        for blok in re.findall(r"```bash\n(.*?)```", text, re.S):
            for radka in blok.splitlines():
                radka = radka.strip()
                for prikaz in sledovane:
                    if re.match(rf"{prikaz}\b", radka):
                        assert f"Bash({prikaz}:" in povolene, (
                            f"{slozka.name}: tělo volá `{prikaz}`, ale "
                            f"allowed-tools ho nemá"
                        )


def test_skilly_odkazuji_jen_na_existujici_prikazy_a_kroky():
    """Odkaz na `/skoleni-analyzy` nebo krok `sdileni` ze srpnového pluginu by
    účastníka poslal za něčím, co v tomhle pluginu není."""
    import stav
    for slozka in (PLUGIN_ROOT / "skills").iterdir():
        if not slozka.is_dir():
            continue
        text = (slozka / "SKILL.md").read_text(encoding="utf-8")
        for prikaz in set(re.findall(r"/(skoleni-[a-z-]+)", text)):
            assert prikaz in OCEKAVANE, f"{slozka.name} odkazuje na /{prikaz}"
        for krok in set(re.findall(r'\["kroky"\]\["([a-z-]+)"\]', text)):
            assert krok in stav.KROKY, f"{slozka.name} čte krok {krok}"
        for krok in set(re.findall(r'(?:nastav_krok|pridej_artefakt)\(s, "([a-z-]+)"', text)):
            assert krok in stav.KROKY, f"{slozka.name} zapisuje krok {krok}"
