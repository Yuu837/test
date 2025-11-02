# カテゴリ別抽出
df_food = df[df["概要"].str.contains("食費", na=False)].copy()
df_goods = df[df["概要"].str.contains("日用品", na=False)].copy()
df_util = df[df["概要"].str.contains("光熱費|電気|ガス|水道", na=False)].copy()  # 光熱費関係

# 月別集計
monthly_total = df.groupby("YearMonth")["Amount"].sum().sort_index()
monthly_food = df_food.groupby("YearMonth")["Amount"].sum().sort_index()
monthly_goods = df_goods.groupby("YearMonth")["Amount"].sum().sort_index()
monthly_util = df_util.groupby("YearMonth")["Amount"].sum().sort_index()

# 合計・平均の表
monthly_summary = pd.DataFrame({
    "合計": monthly_total,
    "食費": monthly_food,
    "日用品": monthly_goods,
    "光熱費": monthly_util
}).fillna(0)

monthly_summary["平均"] = monthly_summary[["食費", "日用品", "光熱費"]].mean(axis=1)
