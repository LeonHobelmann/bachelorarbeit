#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy import stats

# ============================
# Einstellungen
# ============================
CSV_PATH = "Befragungsstudie.csv"
SEP = ";"
ENC = "cp1252"
AGE_CUT = 38
COL_LIKERT = "BE25_05"
COL_GENDER = "Geschlecht"
COL_AGE = "Alter"

# Likert-Skala inklusive Enthaltung
LIKERT_ORDER = [-1, 1, 2, 3, 4, 5]
GENDER_LABELS = {1: "Frau", 2: "Mann"}

# ============================
# Hilfsfunktionen
# ============================
def likert_counts(series, order):
    counts = series.value_counts(sort=False).reindex(order, fill_value=0)
    return counts

def plot_likert_bar(counts, title, ylabel="Anzahl", color="tab:blue", annotate=True, save=None):
    fig, ax = plt.subplots(figsize=(6, 4))
    x_labels = [str(x) if x != -1 else "Enthaltung" for x in counts.index]
    ax.bar(x_labels, counts.values, color=color, edgecolor="white")
    ax.set_title(title)
    ax.set_xlabel("Likert-Stufe")
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, max(counts.values) * 1.15 if len(counts) else 1)
    if annotate:
        for x, v in zip(range(len(counts)), counts.values):
            ax.text(x, v, f"{int(v)}", ha="center", va="bottom", fontsize=9)
    plt.tight_layout()
    if save:
        safe_name = "".join([c if c.isalnum() or c in ['.', '_'] else "_" for c in save])
        fig.savefig(safe_name, dpi=300)
    plt.show()

def plot_group_comparison(df_grp, title, ylabel="Anzahl", save=None):
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.arange(len(df_grp.columns))
    bar_width = 0.35 if len(df_grp.index) == 2 else 0.2

    for i, (grp_name, row) in enumerate(df_grp.iterrows()):
        ax.bar(x + i * bar_width, row.values, bar_width, label=grp_name)
        for xi, v in zip(x + i * bar_width, row.values):
            ax.text(xi, v, f"{int(v)}", ha="center", va="bottom", fontsize=8, rotation=90)

    x_labels = [str(c) if c != -1 else "Enthaltung" for c in df_grp.columns]
    ax.set_xticks(x + bar_width * (len(df_grp.index)-1)/2)
    ax.set_xticklabels(x_labels)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    if save:
        safe_name = "".join([c if c.isalnum() or c in ['.', '_'] else "_" for c in save])
        fig.savefig(safe_name, dpi=300)
    plt.show()

def cohens_d(x, y):
    nx, ny = len(x), len(y)
    pooled_std = np.sqrt(((nx - 1) * x.std(ddof=1) ** 2 + (ny - 1) * y.std(ddof=1) ** 2) / (nx + ny - 2))
    return (x.mean() - y.mean()) / pooled_std

# ============================
# Daten laden & vorbereiten
# ============================
df = pd.read_csv(CSV_PATH, sep=SEP, encoding=ENC, engine="python")

# ============================
# 1) Overall
# ============================
counts_all = likert_counts(df[COL_LIKERT], LIKERT_ORDER)
print("\n=== Overall (Nach_Fr_04) ===")
print("Absolute Häufigkeiten:\n", counts_all.to_string())

plot_likert_bar(
    counts_all,
    title="Selbsteinschätzung (Nach_Fr_04) – Overall",
    color="skyblue",
    save="plot_overall.png"
)

# ============================
# 2) Nach Geschlecht (1=Frau, 2=Mann)
# ============================
df_gender = df[df[COL_GENDER].isin(GENDER_LABELS.keys())].copy()
gender_frames = []
for g_code, g_name in GENDER_LABELS.items():
    c = likert_counts(df_gender.loc[df_gender[COL_GENDER] == g_code, COL_LIKERT], LIKERT_ORDER)
    gender_frames.append(pd.DataFrame({"Gruppe": g_name, **c.to_dict()}, index=[0]))

counts_by_gender = pd.concat(gender_frames, ignore_index=True).set_index("Gruppe")
print("\n=== Nach Geschlecht (absolute Zahlen) ===")
print(counts_by_gender.to_string())

plot_group_comparison(
    counts_by_gender,
    title="Selbsteinschätzung (Nach_Fr_04) – Geschlecht",
    save="plot_gender_comparison.png"
)

# Welch’s t-Test für Geschlecht (Enthaltungen -1 ausgeschlossen)
grp_w = df.loc[(df['Geschlecht'] == 1) & (df[COL_LIKERT] != -1), COL_LIKERT].dropna()
grp_m = df.loc[(df['Geschlecht'] == 2) & (df[COL_LIKERT] != -1), COL_LIKERT].dropna()

t_gender, p_gender = stats.ttest_ind(grp_m, grp_w, equal_var=False)
d_gender = cohens_d(grp_m, grp_w)

print("\n=== Welch t-Test: Geschlecht (m vs w) ===")
print(f"Mean Männer: {grp_m.mean():.2f} (n={len(grp_m)}, SD={grp_m.std():.2f})")
print(f"Mean Frauen: {grp_w.mean():.2f} (n={len(grp_w)}, SD={grp_w.std():.2f})")
print(f"t = {t_gender:.2f}, p = {p_gender:.3f}, Cohen's d = {d_gender:.2f}")

# ============================
# 3) Nach Alter (< AGE_CUT vs. >= AGE_CUT)
# ============================
df_age = df.copy()
df_age["age_group"] = np.where(df_age[COL_AGE] < AGE_CUT, f"unter_{AGE_CUT}", f"ab_{AGE_CUT}")

age_frames = []
for grp in df_age["age_group"].unique():
    c = likert_counts(df_age.loc[df_age["age_group"] == grp, COL_LIKERT], LIKERT_ORDER)
    age_frames.append(pd.DataFrame({"Gruppe": grp, **c.to_dict()}, index=[0]))

counts_by_age = pd.concat(age_frames, ignore_index=True).set_index("Gruppe")
print("\n=== Nach Alter (absolute Zahlen) ===")
print(counts_by_age.to_string())

plot_group_comparison(
    counts_by_age,
    title=f"Selbsteinschätzung (Nach_Fr_04) – Alter (<{AGE_CUT} vs. ≥{AGE_CUT})",
    save="plot_age_comparison.png"
)

# Welch’s t-Test für Alter (Enthaltungen -1 ausgeschlossen)
grp_young = df.loc[(df['Alter'] < AGE_CUT) & (df[COL_LIKERT] != -1), COL_LIKERT].dropna()
grp_old = df.loc[(df['Alter'] >= AGE_CUT) & (df[COL_LIKERT] != -1), COL_LIKERT].dropna()

t_age, p_age = stats.ttest_ind(grp_old, grp_young, equal_var=False)
d_age = cohens_d(grp_old, grp_young)

print("\n=== Welch t-Test: Alter (<38 vs >=38) ===")
print(f"Mean <38: {grp_young.mean():.2f} (n={len(grp_young)}, SD={grp_young.std():.2f})")
print(f"Mean >=38: {grp_old.mean():.2f} (n={len(grp_old)}, SD={grp_old.std():.2f})")
print(f"t = {t_age:.2f}, p = {p_age:.3f}, Cohen's d = {d_age:.2f}")

# ============================
# 4) Übersichtstabellen speichern
# ============================
out_dir = Path(".")
tables = {
    "overall_abs.csv": counts_all,
    "gender_abs.csv": counts_by_gender,
    "age_abs.csv": counts_by_age
}
for name, table in tables.items():
    path = out_dir / name
    if isinstance(table, pd.Series):
        table.to_csv(path, header=True)
    else:
        table.to_csv(path)
    print(f"Gespeichert: {path}")

print("\nFertig. Plots, Tabellen und Welch-Tests ausgegeben.")
