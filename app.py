import streamlit as st
import pandas as pd

st.set_page_config(page_title="スキル定義詳細", layout="centered")

# エラー修正1: データの読み込みを「関数化」してキャッシュを適用する
@st.cache_data
def load_data():
    return pd.read_csv("cards_master.csv")

# エラー修正2: 変数名を統一
df_cards = load_data()

# エラー修正3: デフォルト値を None にして、下のelseブロック（選択画面）が動くようにする
card_id = st.query_params.get("id", None)

if card_id:
    # マスターデータから該当のカード情報を抽出
    card_data = df_cards[df_cards["カードID"] == card_id]
    
    if not card_data.empty:
        row = card_data.iloc[0]
        
        # ヘッダー領域
        st.markdown(f"### {row['スート']} {row['番号']} ［{row['カテゴリ']}］")
        st.caption(f"フェーズ：{row['フェーズ']}")
        st.divider()

        # 導入ストーリー
        st.markdown("#### 💡 このフェーズにおける役割")
        st.info(row['導入メッセージ'])

        # 印字スキル詳細
        st.markdown("#### ◆ カードピックアップスキル")
        st.success(f"**{row['スキル1タイトル']}**\n\n{row['スキル1詳細']}")
        st.success(f"**{row['スキル2タイトル']}**\n\n{row['スキル2詳細']}")
        
    else:
        st.error(f"カードID「{card_id}」が見つかりませんでした。")
else:
    # URLにIDがない場合（トップページに直接アクセスされた場合）
    st.info("一覧から見たいカードを選択してください。")
    # エラー修正2: df を df_cards に変更
    selected_id = st.selectbox("カード選択", df_cards["カードID"].tolist())
    if st.button("詳細を表示"):
        st.query_params["id"] = selected_id
        st.rerun()

# st.markdown("#### 📚 関連スキル定義一覧（Deep Dive）")

# # マスターデータに書かれている「カテゴリ」の文字列を取得（例: "科学的解析の基礎"）
# # ジョーカーのように改行が含まれている場合（"【基盤】コンプライアンス\n【融合】データガバナンス"）は分割する
# categories = str(card_info['カテゴリ']).split('\n')

# for cat in categories:
#     # 全量データから、該当カテゴリのスキルだけを絞り込む
#     # （※実際の全量CSVの列名「スキルカテゴリ」等に合わせて調整）
#     deep_dive_skills = df_skills_full[df_skills_full['スキルカテゴリ'].str.contains(cat, na=False)]
    
#     if not deep_dive_skills.empty:
#         # カテゴリ名でアコーディオンを作成
#         with st.expander(f"🔽 {cat} （関連スキル一覧を展開）"):
#             for _, skill_row in deep_dive_skills.iterrows():
#                 # そのカテゴリに含まれる全スキルを箇条書きで出力
#                 level = skill_row['スキルレベル']
#                 text = skill_row['チェック項目']
#                 st.write(f"- **【{level}】** {text}")