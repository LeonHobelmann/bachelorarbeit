import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ===========================
# KONFIGURATION
# ===========================
CSV_PATH = "Befragungsstudie.csv"
SEP = ";"
ENCODING = "cp1252"
COL_AGE = "Alter"
COL_GENDER = "Geschlecht"
BE_TARGETS = ["BE19_03", "BE20_03", "BE21_03"]
EXPORT_XLSX = "mittelwerte_nach_geschlecht.xlsx"

# ===========================
# DATEN LADEN
# ===========================
df = pd.read_csv(CSV_PATH, sep=SEP, encoding=ENCODING)
df[COL_AGE] = pd.to_numeric(df[COL_AGE], errors='coerce')
df = df[df[COL_AGE] > 1]
df = df[df[COL_GENDER].isin([1, 2])]

# ===========================
# BE-SPALTEN FILTERN
# ===========================
all_items = [col for col in BE_TARGETS if col in df.columns]

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
# EXCEL-DATEI: NACH ALTER GRUPPIEREN
# ===========================
grouped = df_person.groupby([COL_AGE, COL_GENDER])["Mittelwert_Bewertung"].mean().unstack()
grouped.columns = ["Mittelwert_Frauen" if col == 1 else "Mittelwert_Männer" for col in grouped.columns]
grouped = grouped.reset_index()
grouped.to_excel(EXPORT_XLSX, index=False)
print(f"✅ Excel-Datei gespeichert unter: {EXPORT_XLSX}")

# ===========================
# PLOT: INDIVIDUELLE PUNKTE + TRENDLINIEN
# ===========================
plt.figure(figsize=(10, 6))

# Farben definieren
color_female = "#e74c3c"
color_male = "#2980b9"
palette = {1: color_female, 2: color_male}

# Punktwolke
sns.scatterplot(
    data=df_person,
    x=COL_AGE,
    y="Mittelwert_Bewertung",
    hue=COL_GENDER,
    palette=palette,
    alpha=0.5,
    s=50,
    legend=False
)

# Trendlinien nach Geschlecht
for gender, color, label in [(1, color_female, "Trend Frauen"), (2, color_male, "Trend Männer")]:
    sns.regplot(
        data=df_person[df_person[COL_GENDER] == gender],
        x=COL_AGE,
        y="Mittelwert_Bewertung",
        scatter=False,
        lowess=True,
        color=color,
        label=label
    )

# Achsen und Layout
plt.ylim(0.8, 5.2)
plt.xlabel("Alter")
plt.ylabel("Ø Bewertung - Vorher/Nachher_03")
plt.grid(True, linestyle="--", alpha=0.3)
plt.legend(title="")
plt.tight_layout()
plt.show()
