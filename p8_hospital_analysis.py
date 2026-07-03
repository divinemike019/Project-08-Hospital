# ============================================================
#  PROJECT 8 — HOSPITAL OPERATIONS ANALYTICS
#  Dataset  : Hospital Admissions Data — Ashish Sahani (Kaggle)
#  Tool     : Python 3.x | Pandas, Matplotlib, Seaborn
#  Author   : Charlie | TheBuild Data Analysis Programme
#  Date     : June 2026
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

sns.set_theme(style="whitegrid")
plt.rcParams.update({"font.family": "Arial", "figure.dpi": 150})

OUTPUT_DIR = "outputs/charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── 1. LOAD & CLEAN ──────────────────────────────────────────────────────────
df = pd.read_csv("data/hospital_admissions.csv",
                 parse_dates=["admission_date", "discharge_date"])

df.drop_duplicates(inplace=True)
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df = df[df["Age"].between(0, 120)]
df["Gender"]   = df["Gender"].str.strip().str.upper()
df["Department"] = df["Department"].str.strip().str.title()

df["length_of_stay"] = (df["discharge_date"] - df["admission_date"]).dt.days
df = df[df["length_of_stay"].between(0, 365)]

df["month"]  = df["admission_date"].dt.to_period("M")
df["year"]   = df["admission_date"].dt.year
df["quarter"]= df["admission_date"].dt.quarter
df["season"] = df["admission_date"].dt.month.map({
    12:"Winter",1:"Winter",2:"Winter",
    3:"Spring",4:"Spring",5:"Spring",
    6:"Summer",7:"Summer",8:"Summer",
    9:"Autumn",10:"Autumn",11:"Autumn"
})
df["age_group"] = pd.cut(df["Age"],
    bins=[0, 17, 34, 54, 69, 120],
    labels=["Child","Young Adult","Adult","Senior","Elderly"])

print(f"Records after cleaning: {len(df):,}")

# ── 2. SEASONAL ADMISSIONS ────────────────────────────────────────────────────
season_order = ["Winter","Spring","Summer","Autumn"]
season_stats = (df.groupby("season", observed=True)
                .agg(admissions=("admission_id","count"),
                     readmissions=(df.columns[df.columns.str.contains("readmit",case=False)][0]
                                   if any("readmit" in c.lower() for c in df.columns)
                                   else "length_of_stay","count"))
                .reindex(season_order)).fillna(0)

# safer: recount using actual column name
readmit_col = next((c for c in df.columns if "readmit" in c.lower()), None)
season_stats = (df.groupby("season")
                .agg(admissions=("Age","count"),
                     avg_los=("length_of_stay","mean"))
                .reindex(season_order).reset_index())

fig, ax = plt.subplots(figsize=(9, 5))
colors_s = ["#1B3A6B","#0D7377","#14BDBD","#E8A020"]
bars = ax.bar(season_stats["season"], season_stats["admissions"],
              color=colors_s, edgecolor="white", width=0.55)
ax.bar_label(bars, fmt="{:,.0f}", padding=4, fontsize=11)
ax.set_title("Hospital Admissions by Season", fontweight="bold", fontsize=13)
ax.set_ylabel("Number of Admissions")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/15_seasonal_admissions.png"); plt.close()

# ── 3. DEPARTMENT ANALYSIS ────────────────────────────────────────────────────
dept_stats = (df.groupby("Department")
              .agg(admissions=("Age","count"),
                   avg_los=("length_of_stay","mean"))
              .sort_values("admissions", ascending=False).head(8).reset_index())

fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()
x = range(len(dept_stats))
ax1.bar([i-0.2 for i in x], dept_stats["admissions"], width=0.35,
        color="#1B3A6B", label="Admissions", edgecolor="white")
ax2.bar([i+0.2 for i in x], dept_stats["avg_los"], width=0.35,
        color="#0D7377", alpha=0.8, label="Avg LOS (days)", edgecolor="white")
ax1.set_xticks(list(x))
ax1.set_xticklabels(dept_stats["Department"], rotation=20, ha="right", fontsize=10)
ax1.set_ylabel("Total Admissions", color="#1B3A6B")
ax2.set_ylabel("Avg Length of Stay (days)", color="#0D7377")
ax1.set_title("Department Admissions & Average Length of Stay", fontweight="bold", fontsize=13)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, loc="upper right")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/16_dept_analysis.png"); plt.close()

# ── 4. AGE GROUP DISTRIBUTION ─────────────────────────────────────────────────
age_stats = (df.groupby("age_group", observed=True)
             .agg(count=("Age","count"), avg_los=("length_of_stay","mean"))
             .reset_index())

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(age_stats["age_group"].astype(str), age_stats["count"],
              color=["#1B3A6B","#0D7377","#14BDBD","#E8A020","#C0392B"],
              edgecolor="white")
ax.bar_label(bars, fmt="{:,.0f}", padding=4, fontsize=10)
ax.set_title("Admissions by Patient Age Group", fontweight="bold", fontsize=13)
ax.set_ylabel("Number of Admissions"); ax.set_xlabel("Age Group")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/17_age_distribution.png"); plt.close()

# ── 5. LOS DISTRIBUTION (BOXPLOT) ─────────────────────────────────────────────
top_depts = dept_stats["Department"].tolist()[:6]
los_data  = df[df["Department"].isin(top_depts)]

fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=los_data, x="Department", y="length_of_stay",
            palette=["#1B3A6B","#0D7377","#14BDBD","#E8A020","#C0392B","#4C51BF"],
            ax=ax, order=top_depts)
ax.set_title("Length of Stay Distribution by Department (Boxplot)", fontweight="bold", fontsize=13)
ax.set_xlabel("Department"); ax.set_ylabel("Length of Stay (days)")
plt.xticks(rotation=15, ha="right")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/18_los_boxplot.png"); plt.close()

# ── 6. SUMMARY ───────────────────────────────────────────────────────────────
print("\n─── PROJECT 8 SUMMARY ───────────────────────────────")
print(f"Total clean records    : {len(df):,}")
print(f"Avg length of stay     : {df['length_of_stay'].mean():.2f} days")
print(f"Busiest season         : {season_stats.loc[season_stats['admissions'].idxmax(),'season']}")
print(f"Busiest department     : {dept_stats.iloc[0]['Department']}")
print("─────────────────────────────────────────────────────")
