import pandas as pd
import matplotlib.pyplot as plt

# 日本語フォント設定（Windows用）
plt.rcParams['font.family'] = 'Meiryo'   # または 'Yu Gothic', 'MS Gothic', 'MS Mincho'
plt.rcParams['axes.unicode_minus'] = False  # マイナス記号が文字化けしないように


#データ読み込み＆前処理
input_path = r"C:\Users\97110\Downloads\_2025-11-01_export.csv"
df = pd.read_csv(input_path)
df["Date"] = pd.to_datetime(df["日付"])
df["Amount"] = pd.to_numeric(df["費用"], errors='coerce')
df["YearMonth"] = df["Date"].dt.to_period("M")

df_food = df[df["概要"].str.contains("食費", na=False)].copy()
df_goods = df[df["概要"].str.contains("日用品", na=False)].copy()

monthly_total = df.groupby("YearMonth")["Amount"].sum().sort_index(ascending=True)
monthly_food = df_food.groupby("YearMonth")["Amount"].sum().sort_index(ascending=True)
monthly_goods = df_goods.groupby("YearMonth")["Amount"].sum().sort_index(ascending=True)

monthly_summary = pd.DataFrame({
    "Total": monthly_total,
    "Food": monthly_food,
    "Goods": monthly_goods
}).fillna(0)

#上から下に時系列順
monthly_summary_sorted = monthly_summary[::-1]

#Y軸用のインデックス
y_pos = range(len(monthly_summary_sorted))

#数字だけの月ラベル
labels = [f"{x.month:02d}" for x in monthly_summary_sorted.index]

plt.figure(figsize=(8, 5))

#横棒積み上げグラフ
plt.barh(y_pos, monthly_summary_sorted["Food"], color="skyblue", label="食費")
plt.barh(y_pos, monthly_summary_sorted["Goods"], left=monthly_summary_sorted["Food"], color="lightgreen", label="日用品")
plt.barh(y_pos, monthly_summary_sorted["Total"] - monthly_summary_sorted["Food"] - monthly_summary_sorted["Goods"],
         left=monthly_summary_sorted["Food"] + monthly_summary_sorted["Goods"], color="lightgrey", label="その他")

#Y軸ラベルに数字を設定
plt.yticks(y_pos, labels)

#棒の中にそれぞれの内訳額を表示
for i in y_pos:
    plt.text(monthly_summary_sorted["Food"].iloc[i] / 2, i,
             f"{int(monthly_summary_sorted['Food'].iloc[i])}",
             va = "center", ha="center", color="black", fontsize=9, fontweight="bold")
    plt.text(monthly_summary_sorted["Food"].iloc[i] + monthly_summary_sorted["Goods"].iloc[i] / 2, i,
             f"{int(monthly_summary_sorted['Goods'].iloc[i])}",
             va = "center", ha="center", color="black", fontsize=9, fontweight="bold")
    others_val = monthly_summary_sorted["Total"].iloc[i] - monthly_summary_sorted["Food"].iloc[i] - monthly_summary_sorted["Goods"].iloc[i]
    if others_val > 0:
        plt.text(monthly_summary_sorted["Food"].iloc[i] + monthly_summary_sorted["Goods"].iloc[i] + others_val / 2, i,
                 f"{int(others_val)}",
                 va = "center", ha="center", color="black", fontsize=9, fontweight="bold")
        
#月ごとの合計値を右上に表示
total_text = "合計(月ごと):\n" + "\n".join([f"{x.month:02d}: {int(v)}"
                                            for x, v in zip(monthly_summary_sorted.index[::-1], monthly_summary_sorted["Total"][::-1])])
plt.text(1.02, 1.0, total_text, transform=plt.gca().transAxes,
         fontsize=10, va="top", ha="left", color="red", fontweight="bold")

#グラフ装飾
plt.xlabel("金額")
plt.ylabel("月")
plt.title("月別支出内訳")
plt.legend(loc="best")
plt.tight_layout()
output_path = r"C:\Users\97110\Projects\2025_AI_Scheduler\result\monthly_expense_breakdown.png"
plt.savefig(output_path, bbox_inches="tight")
plt.show()