import streamlit as st
import pandas as pd

st.set_page_config(page_title="スキル定義詳細", layout="centered")

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

df_cards = load_data("cards_master.csv")
df_skills_full = load_data("skill_list.csv")

card_id = st.query_params.get("id", None)

if card_id:
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
        
        # ---------------------------------------------------------
        # ▼ 修正ポイント: Deep Diveの処理をこの if ブロックの中に移動
        # ---------------------------------------------------------
        st.markdown("#### 📚 関連スキル定義一覧（Deep Dive）")

        # row['カテゴリ']から文字列を取得
        categories = str(row['カテゴリ']).split('\n')

        for cat in categories:
            # 検索がヒットしやすいように【基盤】【融合】などを取り除いて純粋なカテゴリ名にする
            search_word = cat.replace("【基盤】", "").replace("【融合】", "").strip()
            
            # 全量データから該当カテゴリを検索（部分一致）
            deep_dive_skills = df_skills_full[df_skills_full['スキルカテゴリ'].str.contains(search_word, na=False)]
            
            if not deep_dive_skills.empty:
                # カテゴリ名でアコーディオンを作成
                with st.expander(f"🔽 {cat} （関連スキル一覧を展開）"):
                    for _, skill_row in deep_dive_skills.iterrows():
                        # そのカテゴリに含まれる全スキルを箇条書きで出力
                        level = skill_row['スキルレベル']
                        text = skill_row['チェック項目']
                        st.write(f"- **【{level}】** {text}")
            else:
                # もし一致するスキルが見つからなかった場合のデバッグ用メッセージ（不要なら削除可）
                st.caption(f"※「{search_word}」に関連するスキルリストは見つかりませんでした。")
                
    else:
        st.error(f"カードID「{card_id}」が見つかりませんでした。")
else:
    # URLにIDがない場合（トップページに直接アクセスされた場合）
    st.info("一覧から見たいカードを選択してください。")
    selected_id = st.selectbox("カード選択", df_cards["カードID"].tolist())
    if st.button("詳細を表示"):
        st.query_params["id"] = selected_id
        st.rerun()