import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ─── Daten einlesen & performance_pct berechnen ───────────────────────────────
df = pd.read_csv('deine_daten.csv', sep=';', encoding='cp1252', engine='python')

# ─── Manuelle Liste mit genau 12 Item-Spalten ──────────────────────────────────
item_cols = [
    '1.1 Ballon', '1.2 Wüste', '1.3 Strand',
    '2.1 Giraffe', '2.2 Hund',   '2.3 Katze',
    '3.1 Mercedes','3.2 Lambo',  '3.3 Beetle',
    '4.1 Kuchen',  '4.2 Bowl',   '4.3 Burger'
]
n_items = len(item_cols)  # = 12

# ─── Performance berechnen ─────────────────────────────────────────────────────
df['correct_count']   = df[item_cols].eq(1).sum(axis=1)
df['performance_pct'] = df['correct_count'] / n_items * 100

# ─── Funktionen & Farben ───────────────────────────────────────────────────────
def cohens_d(x, y):
    nx, ny = len(x), len(y)
    pooled_std = np.sqrt(((nx - 1)*x.std(ddof=1)**2 + (ny - 1)*y.std(ddof=1)**2)/(nx + ny - 2))
    return (x.mean() - y.mean()) / pooled_std

clr_all = 'skyblue'
clr_m   = 'tab:blue'
clr_w   = 'tab:orange'
clr_y   = 'tab:green'
clr_o   = 'tab:red'

# ─── 1) 1-Sample t-Test gegen 33,3 % ──────────────────────────────────────────
hyp_mean = 33.33
t1, p1   = stats.ttest_1samp(df['performance_pct'], popmean=hyp_mean)
print(f"1-Sample t-Test: t={t1:.2f}, p={p1:.3f}")

# ─── Histogramm Gesamt über correct_count ─────────────────────────────────────
counts_all = df['correct_count'].value_counts().sort_index()

plt.figure(figsize=(6,4))
plt.bar(counts_all.index, counts_all.values, color=clr_all, edgecolor='white')
plt.xticks(counts_all.index, [f"{i}/12" for i in counts_all.index])
plt.xlabel('Anzahl richtig erkannter Bilder (k/12)')
plt.ylabel('Anzahl Proband:innen')
plt.title('Verteilung der Probanden-Scores (k/12)')
plt.show()

# ─── 2) Welch's t-Test: männlich vs. weiblich ────────────────────────────────
grp_w = df.loc[df['Geschlecht']==1, 'performance_pct']
grp_m = df.loc[df['Geschlecht']==2, 'performance_pct']
t2, p2 = stats.ttest_ind(grp_m, grp_w, equal_var=False, nan_policy='omit')
d2     = cohens_d(grp_m, grp_w)
print(f"Welch t-Test m vs w: t={t2:.2f}, p={p2:.3f}, Cohen's d={d2:.2f}")

# Histogramm nach Geschlecht
cnt_m = df.loc[df['Geschlecht']==2, 'correct_count'].value_counts().sort_index()
cnt_w = df.loc[df['Geschlecht']==1, 'correct_count'].value_counts().sort_index()

plt.figure(figsize=(6,4))
plt.bar(cnt_m.index - 0.2, cnt_m.values, width=0.4, label='männlich', color=clr_m, edgecolor='white')
plt.bar(cnt_w.index + 0.2, cnt_w.values, width=0.4, label='weiblich', color=clr_w, edgecolor='white')
plt.xticks(counts_all.index, [f"{i}/12" for i in counts_all.index])
plt.xlabel('Anzahl richtig erkannter Bilder (k/12)')
plt.ylabel('Anzahl Proband:innen')
plt.title('Scores nach Geschlecht')
plt.legend()
plt.show()

# ─── 3) Welch's t-Test: Alter <38 vs. Alter ≥38 ───────────────────────────────
grp_y = df.loc[df['Alter']<38, 'performance_pct']
grp_o = df.loc[df['Alter']>=38, 'performance_pct']
t3, p3 = stats.ttest_ind(grp_o, grp_y, equal_var=False, nan_policy='omit')
d3     = cohens_d(grp_o, grp_y)
print(f"Welch t-Test Alt<38 vs ≥38: t={t3:.2f}, p={p3:.3f}, Cohen's d={d3:.2f}")

# Histogramm nach Altersgruppe
cnt_y = df.loc[df['Alter']<38, 'correct_count'].value_counts().sort_index()
cnt_o = df.loc[df['Alter']>=38, 'correct_count'].value_counts().sort_index()

plt.figure(figsize=(6,4))
plt.bar(cnt_y.index - 0.2, cnt_y.values, width=0.4, label='Alter < 38', color=clr_y, edgecolor='white')
plt.bar(cnt_o.index + 0.2, cnt_o.values, width=0.4, label='Alter ≥ 38', color=clr_o, edgecolor='white')
plt.xticks(counts_all.index, [f"{i}/12" for i in counts_all.index])
plt.xlabel('Anzahl richtig erkannter Bilder (k/12)')
plt.ylabel('Anzahl Proband:innen')
plt.title('Scores nach Altersgruppe')
plt.legend()
plt.show()

# ─── Ergebnisse Tabelle (Tests) ────────────────────────────────────────────────
results = pd.DataFrame({
    "Test": ["1-Sample t-Test (33,3%)",
             "Welch t-Test (m vs w)",
             "Welch t-Test (Alter)"],
    "t-Wert": [f"{t1:.2f}", f"{t2:.2f}", f"{t3:.2f}"],
    "p-Wert": [f"{p1:.3f}", f"{p2:.3f}", f"{p3:.3f}"],
    "Cohen's d": ["–", f"{d2:.2f}", f"{d3:.2f}"]
})
print("\nErgebnisse der t-Tests:\n", results.to_string(index=False))

# ─── Histogramm-Daten zu DataFrame hinzufügen und exportieren ─────────────────
hist_df = pd.DataFrame({
    "Bin":          [f"{i}/12" for i in counts_all.index],
    "Gesamt":       counts_all.values,
    "Männer":       cnt_m.reindex(counts_all.index, fill_value=0).values,
    "Frauen":       cnt_w.reindex(counts_all.index, fill_value=0).values,
    "Alter<38":     cnt_y.reindex(counts_all.index, fill_value=0).values,
    "Alter>=38":    cnt_o.reindex(counts_all.index, fill_value=0).values
})
hist_df.to_csv("t-test_statistik.csv", sep=';', index=False)
print("\nHistogramm-Daten und Testergebnisse wurden in 't-test_statistik.csv' gespeichert.")
