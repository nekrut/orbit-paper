#!/usr/bin/env python3
"""
Generate publication-grade 42-panel compound Figure 4 for Section 3.3:
Continuous Manifold Alluvial Phylogenies Across 42 High-Priority Pathogen Cohorts.

Layout:
  Grid of 6 columns x 7 rows (42 panels).
  Each cell contains:
  - Header banner with cohort number, pathogen, author citation, and concordance badge.
  - The cropped Continuous Manifold Alluvial Phylogeny (Streamlines) fanning out from founder root
    across calendar time, color-coded by AutoClock evolutionary community, with 95% Fieller CI
    and BEAST 95% HPD bands.
  - Master header at top and explanatory legend bar at bottom.
"""

import os
import csv
from PIL import Image, ImageDraw, ImageFont
import numpy as np

SHORT_LABELS = {
    "00_ebola_sierraleone_gire2014": "01 · EBOV Sierra Leone (Gire 2014)",
    "01_ebola_makona_dudas2017": "02 · EBOV Makona (Dudas 2017)",
    "02_ebola_drc_kingebeni2020": "03 · EBOV DRC (Kingebeni 2020)",
    "03_chikungunya_brazil_naveca2019": "04 · CHIKV Brazil (Naveca 2019)",
    "04_dengue1_caribbean_siddle2023": "05 · DENV-1 Caribbean (Siddle 2023)",
    "05_dengue2_caribbean_siddle2023": "06 · DENV-2 Caribbean (Siddle 2023)",
    "06_zika_cuba_grubaugh2019": "07 · ZIKV Cuba (Grubaugh 2019)",
    "07_mumps_wa_moncla2021": "08 · Mumps Genotype G (Moncla 2021)",
    "08_zika_angola_faria2018": "09 · ZIKV Angola (Faria 2018)",
    "09_sarscov2_p1_faria2021": "10 · SARS-CoV-2 P.1 / Gamma (Faria 2021)",
    "10_chikungunya_rj_romero2023": "11 · CHIKV Rio de Janeiro (Romero 2023)",
    "11_dengue_polyepoch_suchard2020": "12 · DENV Polyprotein (Suchard 2020)",
    "12_yellow_fever_faria2018": "13 · Yellow Fever Brazil (Faria 2018)",
    "13_rymv_madagascar_suchard2020": "14 · RYMV Madagascar (Suchard 2020)",
    "14_zika_fiji_henderson2020": "15 · ZIKV Fiji (Henderson 2020)",
    "15_west_nile_pybus_suchard2020": "16 · West Nile Virus NA (Pybus 2012)",
    "16_rabies_northamerica_biek2007": "17 · Rabies Virus NA (Biek 2007)",
    "17_influenza_h3n2_bedford_suchard2020": "18 · Influenza H3N2 (Bedford 2015)",
    "18_lassa_andersen_suchard2020": "19 · Lassa Virus (Andersen 2015)",
    "19_avian_influenza_h7_baele2018": "20 · Avian Flu H7 (Baele 2018)",
    "20_avian_influenza_n7_baele2018": "21 · Avian Flu N7 (Baele 2018)",
    "21_hiv1_gill_suchard2013": "22 · HIV-1 RT / Protease (Gill 2013)",
    "22_chikungunya_bolivia_valdez2026": "23 · CHIKV Bolivia (Valdez 2026)",
    "23_dengue3_caribbean_siddle2023": "24 · DENV-3 Caribbean (Siddle 2023)",
    "24_dengue4_caribbean_siddle2023": "25 · DENV-4 Caribbean (Siddle 2023)",
    "25_fmdv_serotype_a_carvalho2013": "26 · FMDV Serotype A (Carvalho 2013)",
    "26_fmdv_serotype_o_carvalho2013": "27 · FMDV Serotype O (Carvalho 2013)",
    "27_hiv1_faria2014": "28 · HIV-1 Group M (Faria 2014)",
    "28_influenza_h1n1_2009_smith2009": "29 · Pandemic H1N1 2009 (Smith 2009)",
    "29_ypestis_blackdeath_spyrou2019": "30 · Y. pestis Black Death (Spyrou 2019)",
    "30_mpox_clade_ib_burundi2025": "31 · MPXV Clade Ib (Burundi 2025)",
    "31_rsv_a_trovao2025": "32 · RSV-A (Trovao 2025)",
    "32_usuv_netherlands_munger2026": "33 · Usutu Virus (Munger 2026)",
    "33_chikv_civ_klitting2024": "34 · CHIKV Côte d'Ivoire (Klitting 2024)",
    "34_asfv_europe_gambaro2025": "35 · ASFV Genotype II (Gambaro 2025)",
    "35_h3n2_ha_suchard2026": "36 · Influenza H5N1 HA (Suchard 2026)",
    "36_denv1_suchard2026": "37 · DENV-1 (Suchard 2026)",
    "37_measles_1912_dux2020": "38 · Measles / Rinderpest (Dux 2020)",
    "38_mab_commins2023": "39 · M. abscessus (Commins 2023)",
    "39_chikv_reunion_dellicour2020": "40 · CHIKV Multi-Wave (Dellicour 2020)",
    "40_hiv1_crf01ae_philippines2024": "41 · HIV-1 CRF01_AE (Philippines 2024)",
    "41_skygrid_rabies_gill2020": "42 · EBOV Skygrid (Gill 2020)",
}

def get_font(size, bold=False):
    # Try common font locations on macOS
    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFCompact.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    if bold:
        font_paths = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf",
            "/Library/Fonts/Arial Bold.ttf",
        ] + font_paths

    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return ImageFont.load_default()

def make_compound_figure():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_png = os.path.join(base_dir, "figure4_chronaeon_42cohorts.png")
    output_pdf = os.path.join(base_dir, "figure4_chronaeon_42cohorts.pdf")
    cache_dir = "/tmp/chronaeon_diagnostics_cache"

    # Load concordance data
    concordance_map = {}
    agg_path = "/Users/anton/git/beast-chrom/aggregate_benchmark_results.tsv"
    with open(agg_path) as f:
        reader = csv.DictReader(f, delimiter="\t")
        for r in reader:
            concordance_map[r["study_id"]] = r["concordance"]

    # Load cohort manifest
    manifest_path = "/Users/anton/git/beast-chrom/cohort_manifest.tsv"
    with open(manifest_path) as f:
        reader = csv.DictReader(f, delimiter="\t")
        studies = [row["study_id"] for row in reader if row.get("study_id")]

    # Grid config
    ncols = 6
    nrows = 7
    panel_w = 700
    panel_h = 515
    banner_h = 42
    cell_w = panel_w
    cell_h = panel_h + banner_h

    margin_x = 40
    header_h = 130
    footer_h = 100
    margin_bottom = 30

    total_w = margin_x * 2 + ncols * cell_w + (ncols - 1) * 20
    total_h = header_h + nrows * cell_h + (nrows - 1) * 25 + footer_h + margin_bottom

    print(f"Canvas dimensions: {total_w} x {total_h} px")
    master = Image.new("RGB", (total_w, total_h), color="#FFFFFF")
    draw = ImageDraw.Draw(master)

    # Fonts
    title_font = get_font(38, bold=True)
    subtitle_font = get_font(21, bold=False)
    banner_font = get_font(18, bold=True)
    badge_font = get_font(14, bold=True)
    footer_font = get_font(18, bold=False)
    footer_bold = get_font(18, bold=True)

    # Master Header
    draw.text((margin_x, 30), "Continuous Manifold Alluvial Phylogenies Across 42 High-Priority Pathogen Cohorts",
              fill="#0F172A", font=title_font)
    draw.text((margin_x, 82), "Transverse divergence manifolds fanning out from founder roots (tMRCA, diamonds) across calendar time, color-coded by AutoClock evolutionary communities with 95% Fieller CI (light blue) and BEAST 95% HPD (gold).",
              fill="#475569", font=subtitle_font)

    # Crop and place each panel
    for idx, sid in enumerate(studies):
        row = idx // ncols
        col = idx % ncols

        x0 = margin_x + col * (cell_w + 20)
        y0 = header_h + row * (cell_h + 25)

        img_path = os.path.join(cache_dir, f"{sid}.png")
        im = Image.open(img_path).convert("RGB")
        arr = np.array(im)
        h_im, w_im, _ = arr.shape
        sub = arr[h_im//2:h_im, 0:w_im//2]
        mask = (sub[:, :, 0] == 248) & (sub[:, :, 1] == 250) & (sub[:, :, 2] == 252)
        rows_m = np.where(mask.any(axis=1))[0]
        cols_m = np.where(mask.any(axis=0))[0]

        x_min, x_max = cols_m[0], cols_m[-1]
        y_min, y_max = rows_m[0] + h_im//2, rows_m[-1] + h_im//2

        left = max(0, x_min - 165)
        top = max(0, y_min - 6)
        right = min(w_im, x_max + 20)
        bottom = min(h_im, y_max + 105)

        panel = im.crop((left, top, right, bottom))
        panel_resized = panel.resize((panel_w, panel_h), Image.Resampling.LANCZOS)

        # Draw banner background
        draw.rectangle([x0, y0, x0 + cell_w, y0 + banner_h], fill="#F8FAFC", outline="#CBD5E1", width=1)

        # Title text
        label_text = SHORT_LABELS.get(sid, sid)
        draw.text((x0 + 12, y0 + 10), label_text, fill="#0F172A", font=banner_font)

        # Concordance Badge
        status = concordance_map.get(sid, "UNKNOWN")
        if status == "CONCORDANT":
            b_bg = "#DCFCE7"
            b_fg = "#15803D"
            b_edge = "#86EFAC"
            b_txt = "CONCORDANT"
        elif status == "DISCORDANT":
            b_bg = "#FEF3C7"
            b_fg = "#B45309"
            b_edge = "#FCD34D"
            b_txt = "DISCORDANT"
        else:
            b_bg = "#F1F5F9"
            b_fg = "#475569"
            b_edge = "#CBD5E1"
            b_txt = "BASELINE"

        # Badge dimensions
        bbox = draw.textbbox((0, 0), b_txt, font=badge_font)
        txt_w = bbox[2] - bbox[0]
        badge_w = txt_w + 16
        badge_h = 24
        bx = x0 + cell_w - badge_w - 10
        by = y0 + 9
        draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=4, fill=b_bg, outline=b_edge, width=1)
        draw.text((bx + 8, by + 4), b_txt, fill=b_fg, font=badge_font)

        # Paste panel
        master.paste(panel_resized, (x0, y0 + banner_h))

        # Cell border around image
        draw.rectangle([x0, y0 + banner_h, x0 + cell_w, y0 + banner_h + panel_h], outline="#CBD5E1", width=1)

    # Master Footer / Legend Bar
    footer_y = header_h + nrows * cell_h + (nrows - 1) * 25 + 20
    draw.rounded_rectangle([margin_x, footer_y, total_w - margin_x, footer_y + 80],
                           radius=8, fill="#F8FAFC", outline="#CBD5E1", width=1)

    # Legend elements inside footer
    leg_x = margin_x + 25
    leg_y = footer_y + 28

    # 1. Founder diamond
    draw.polygon([(leg_x, leg_y + 12), (leg_x + 12, leg_y), (leg_x + 24, leg_y + 12), (leg_x + 12, leg_y + 24)],
                 fill="#0284C7", outline="#082F49")
    draw.text((leg_x + 32, leg_y + 3), "Founder Origin (tMRCA)", fill="#0F172A", font=footer_font)

    # 2. Fieller CI
    f_x = leg_x + 300
    draw.rectangle([f_x, leg_y + 3, f_x + 28, leg_y + 21], fill="#BAE6FD", outline="#38BDF8", width=1)
    draw.text((f_x + 36, leg_y + 3), "ChronAeon 95% Fieller CI", fill="#0F172A", font=footer_font)

    # 3. BEAST HPD
    b_x = f_x + 320
    draw.rectangle([b_x, leg_y + 3, b_x + 28, leg_y + 21], fill="#FEF08A", outline="#FACC15", width=1)
    draw.text((b_x + 36, leg_y + 3), "Published BEAST 95% HPD", fill="#0F172A", font=footer_font)

    # 4. Streamlines
    s_x = b_x + 320
    draw.line([(s_x, leg_y + 12), (s_x + 30, leg_y + 12)], fill="#059669", width=4)
    draw.text((s_x + 38, leg_y + 3), "AutoClock Manifold Streamlines", fill="#0F172A", font=footer_font)

    # 5. Summary Stats
    stat_x = s_x + 370
    draw.text((stat_x, leg_y + 3), "Compendium Summary: 20 Concordant (47.6%)  |  19 Discordant (45.2%)  |  3 Novel Baselines (7.1%)",
              fill="#1E293B", font=footer_bold)

    print(f"Saving {output_png}...")
    master.save(output_png, quality=95)
    print(f"Saving {output_pdf}...")
    master.save(output_pdf, "PDF", resolution=200.0)
    print(f"Successfully generated 42-panel compound figure!")

if __name__ == "__main__":
    make_compound_figure()
