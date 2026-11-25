from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "mango_chatbot_dataset_scored.csv"
OUT = ROOT / "outputs"
FIG = ROOT / "figures"
CHARTS = ROOT / "charts"
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)
CHARTS.mkdir(exist_ok=True)

score_cols = ["accuracy_score", "relevance_score", "language_score", "tone_score", "complexity_score"]
criterion_names = {
    "accuracy_score": "Exactitud y fiabilidad",
    "relevance_score": "Relevancia y resolución",
    "language_score": "Calidad lingüística",
    "tone_score": "Tono y adecuación comunicativa",
    "complexity_score": "Gestión de consultas complejas",
}
category_names = {
    "shipping": "Envíos", "returns": "Devoluciones", "orders": "Pedidos",
    "products": "Productos", "payments": "Pagos", "availability": "Disponibilidad",
    "complaints": "Reclamaciones", "complex_queries": "Consultas complejas",
}
labels = ["Insuficiente", "Mejorable", "Bueno", "Excelente"]

df = pd.read_csv(DATA, sep=";", encoding="utf-8-sig")
required = ["id", "category", "user_query", "assistant_response", "test_date", *score_cols, "notes"]
missing = [c for c in required if c not in df.columns]
if missing:
    raise ValueError(f"Faltan columnas: {missing}")
for col in score_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
if df[score_cols].isna().any().any():
    raise ValueError("Hay puntuaciones vacías: completa las cinco notas por interacción.")
if not df[score_cols].apply(lambda s: s.between(1, 4).all()).all():
    raise ValueError("Las puntuaciones deben estar entre 1 y 4.")
if df["assistant_response"].fillna("").str.strip().eq("").any():
    raise ValueError("Hay respuestas vacías en assistant_response.")

df["total_score"] = df[score_cols].sum(axis=1)
df["performance_level"] = pd.cut(df["total_score"], bins=[0, 9, 14, 18, 20], labels=labels, include_lowest=True)
criterion = pd.DataFrame({"criterion": [criterion_names[c] for c in score_cols], "n": [df[c].count() for c in score_cols], "mean": [df[c].mean() for c in score_cols]})
category = df.groupby("category")["total_score"].agg(["count", "mean", "min", "max"]).reset_index()
category["category_label"] = category["category"].map(category_names)
levels = df["performance_level"].value_counts().reindex(labels, fill_value=0).rename_axis("level").reset_index(name="count")
levels["percentage"] = levels["count"] / len(df) * 100

criterion.to_csv(OUT / "criterion_summary.csv", index=False, sep=";", encoding="utf-8-sig")
category.to_csv(OUT / "category_summary.csv", index=False, sep=";", encoding="utf-8-sig")
levels.to_csv(OUT / "performance_distribution.csv", index=False, sep=";", encoding="utf-8-sig")
df[["id", "category", "total_score", "performance_level"]].to_csv(OUT / "interaction_scores.csv", index=False, sep=";", encoding="utf-8-sig")

plt.rcParams.update({"font.size": 10, "axes.titlesize": 13, "axes.labelsize": 10})
# Figure 1: mean score by criterion
cs = criterion.sort_values("mean")
fig, ax = plt.subplots(figsize=(9, 5.2))
bars = ax.barh(cs["criterion"], cs["mean"])
ax.set(title="Evaluación del chatbot por criterio", xlabel="Puntuación media (sobre 4)", ylabel="Criterio", xlim=(0, 4.35))
ax.grid(axis="x", alpha=.25)
for bar, value in zip(bars, cs["mean"]): ax.text(value + .04, bar.get_y() + bar.get_height()/2, f"{value:.2f}", va="center", fontsize=9)
fig.tight_layout(); fig.savefig(FIG / "01_criterios.png", dpi=220, bbox_inches="tight"); plt.close(fig)
# Figure 2: mean score by category
cat_plot = category.sort_values("mean").copy()
cat_plot["label"] = cat_plot["category_label"] + " (n=" + cat_plot["count"].astype(str) + ")"
fig, ax = plt.subplots(figsize=(9, 5.4))
bars = ax.barh(cat_plot["label"], cat_plot["mean"])
ax.set(title="Puntuación media por categoría", xlabel="Puntuación media total (sobre 20)", ylabel="Categoría", xlim=(0, 22))
ax.grid(axis="x", alpha=.25)
for bar, value in zip(bars, cat_plot["mean"]): ax.text(value + .12, bar.get_y() + bar.get_height()/2, f"{value:.2f}", va="center", fontsize=9)
fig.tight_layout(); fig.savefig(FIG / "02_categorias.png", dpi=220, bbox_inches="tight"); plt.close(fig)
# Figure 3: score band distribution
fig, ax = plt.subplots(figsize=(8.5, 5))
bars = ax.bar(levels["level"], levels["count"])
ax.set(title="Distribución de las interacciones por nivel de rendimiento", xlabel="Nivel de rendimiento", ylabel="Número de interacciones", ylim=(0, max(levels["count"]) + 3))
ax.grid(axis="y", alpha=.25)
for bar, count, pct in zip(bars, levels["count"], levels["percentage"]): ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+.12, f"{int(count)} ({pct:.1f}%)", ha="center", va="bottom", fontsize=9)
fig.tight_layout(); fig.savefig(FIG / "03_distribucion.png", dpi=220, bbox_inches="tight"); plt.close(fig)

print(f"Interacciones analizadas: {len(df)}")
print(f"Puntuación media global: {df['total_score'].mean():.2f}/20")
print("\\nMedia por criterio:")
print(criterion.to_string(index=False, formatters={"mean": "{:.2f}".format}))
print("\\nMedia por categoría:")
print(category[["category_label", "count", "mean"]].sort_values("mean", ascending=False).to_string(index=False, formatters={"mean": "{:.2f}".format}))
print("\\nDistribución:")
print(levels.to_string(index=False, formatters={"percentage": "{:.1f}%".format}))
print("\\nFiguras guardadas en:", FIG)


# Three complementary charts supplied by the author. They present simpler alternative
# views of the same pandas aggregates used above; they are not additional observations.
criterion_simple = df[score_cols].mean().rename(index=criterion_names).sort_values()
plt.figure(figsize=(9, 5))
criterion_simple.plot(kind="barh")
plt.title("Evaluación del chatbot por criterio")
plt.xlabel("Puntuación media (sobre 4)")
plt.ylabel("Criterio")
plt.xlim(0, 4)
plt.tight_layout()
plt.savefig(CHARTS / "grafico_01_criterios.png", dpi=240)
plt.close()

category_simple = (df.groupby("category")["total_score"].mean()
                   .rename(index=category_names).sort_values())
plt.figure(figsize=(9, 5))
category_simple.plot(kind="barh")
plt.title("Rendimiento del chatbot por categoría")
plt.xlabel("Puntuación media (sobre 20)")
plt.ylabel("Categoría")
plt.xlim(0, 20)
plt.tight_layout()
plt.savefig(CHARTS / "grafico_02_categorias.png", dpi=240)
plt.close()

plt.figure(figsize=(8, 5))
levels.set_index("level")["count"].plot(kind="bar")
plt.xlabel("Nivel de rendimiento")
plt.ylabel("Número de interacciones")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(CHARTS / "grafico_03_distribucion.png", dpi=240)
plt.close()

print("Gráficos complementarios guardados en:", CHARTS)
