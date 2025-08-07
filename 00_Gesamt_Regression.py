import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# ===========================
# KONFIGURATION
# ===========================
CSV_PATH = "Befragungsstudie.csv"
SEP = ";"
ENCODING = "cp1252"
COL_AGE = "Alter"
COL_GENDER = "Geschlecht"
BE_PREFIXES = [f"BE{str(i).zfill(2)}" for i in range(2, 25)]
SUFFIXES = ['_01', '_02', '_03']
EXPORT_XLSX = "mittelwerte_nach_geschlecht.xlsx"

# ===========================
# DATEN LADEN
# ===========================
df = pd.read_csv(CSV_PATH, sep=SEP, encoding=ENCODING)
df[COL_AGE] = pd.to_numeric(df[COL_AGE], errors='coerce')
df = df[df[COL_AGE] > 1]
df = df[df[COL_GENDER].isin([1, 2])]

# ===========================
# BE-SPALTEN SAMMELN
# ===========================
all_items = []
for prefix in BE_PREFIXES:
    for suf in SUFFIXES:
        col = f"{prefix}{suf}"
        if col in df.columns:
            all_items.append(col)

if not all_items:
    raise ValueError("Keine gültigen BE-Spalten gefunden!")

# ===========================
# MITTELWERT PRO PERSON
# ===========================
df_person = df[[COL_AGE, COL_GENDER] + all_items].copy()
df_person["Mittelwert_Bewertung"] = df_person[all_items].apply(
    lambda row: row[row.isin([1, 2, 3, 4, 5])].mean(), axis=1
)
df_person = df_person.dropna(subset=["Mittelwert_Bewertung"])

# ===========================
# REGRESSION
# ===========================
df_person["Geschlecht_txt"] = df_person[COL_GENDER].map({1: "Frau", 2: "Mann"})

model = smf.ols(formula="Mittelwert_Bewertung ~ Alter + C(Geschlecht_txt)", data=df_person).fit()
print("\n📊 LINEARE REGRESSION: Mittelwert ~ Alter + Geschlecht")
print(model.summary())

# ===========================
# PLOT: REGRESSIONSVISUALISIERUNG
# ===========================
plt.figure(figsize=(12, 6))

color_female = "#e74c3c"
color_male = "#2980b9"
palette = {1: color_female, 2: color_male}

# Scatterplot
sns.scatterplot(
    data=df_person,
    x=COL_AGE,
    y="Mittelwert_Bewertung",
    hue="Geschlecht_txt",
    palette={"Frau": color_female, "Mann": color_male},
    alpha=0.5,
    s=50
)

# Regressionen mit Konfidenzintervall
sns.regplot(
    data=df_person[df_person["Geschlecht_txt"] == "Frau"],
    x=COL_AGE,
    y="Mittelwert_Bewertung",
    scatter=False,
    color=color_female,
    label="Regression Frauen"
)
sns.regplot(
    data=df_person[df_person["Geschlecht_txt"] == "Mann"],
    x=COL_AGE,
    y="Mittelwert_Bewertung",
    scatter=False,
    color=color_male,
    label="Regression Männer"
)

# Manuelle Legende ergänzen
custom_legend = [
    Line2D([0], [0], marker='o', color='w', label='Ø Bewertung je Person – Frauen', markerfacecolor=color_female, markersize=8, alpha=0.5),
    Line2D([0], [0], marker='o', color='w', label='Ø Bewertung je Person – Männer', markerfacecolor=color_male, markersize=8, alpha=0.5),
    Line2D([0], [0], color=color_female, lw=2, label='Lineare Regression Frauen'),
    Line2D([0], [0], color=color_male, lw=2, label='Lineare Regression Männer'),
    Patch(facecolor=color_female, edgecolor='none', alpha=0.2, label='95 %-Konfidenzintervall Frauen'),
    Patch(facecolor=color_male, edgecolor='none', alpha=0.2, label='95 %-Konfidenzintervall Männer')
]

plt.legend(handles=custom_legend, title="")
plt.ylim(0.8, 5.2)
plt.xlabel("Alter")
plt.ylabel("Ø Bewertung (über alle Thesen)")
plt.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()
