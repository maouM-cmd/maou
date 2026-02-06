import streamlit as st
import feedparser
from urllib.parse import quote
from datetime import datetime
import time

# ページ設定
st.set_page_config(
    page_title="🐦 シマエナガAIニュース",
    page_icon="🐦",
    layout="wide"
)

# シマエナガ×クリスマスカラーCSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;700&display=swap');
    
    * {
        font-family: 'M PLUS Rounded 1c', sans-serif !important;
    }
    
    /* メインコンテナ - クリスマスカラー背景 */
    .main {
        background: linear-gradient(180deg, #1a472a 0%, #2d5a3d 50%, #1a472a 100%);
    }
    
    .stApp {
        background: linear-gradient(180deg, #1a472a 0%, #2d5a3d 50%, #1a472a 100%);
    }
    
    /* 雪の結晶エフェクト */
    .stApp::before {
        content: "❄️ 🐦 ❄️ 🐦 ❄️ 🐦 ❄️ 🐦 ❄️";
        position: fixed;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 1.5rem;
        opacity: 0.6;
        z-index: 1000;
        letter-spacing: 20px;
    }
    
    /* ニュースカード - クリック可能 */
    .news-card-link {
        text-decoration: none !important;
        display: block;
    }
    
    .news-card {
        background: linear-gradient(145deg, #ffffff 0%, #fff5f5 100%);
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 20px;
        border: 3px solid #c41e3a;
        box-shadow: 0 8px 32px rgba(196, 30, 58, 0.2), 
                    inset 0 0 20px rgba(255, 255, 255, 0.5);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .news-card::before {
        content: "🐦";
        position: absolute;
        top: -10px;
        right: 10px;
        font-size: 2.5rem;
        opacity: 0.3;
        transition: all 0.3s ease;
    }
    
    .news-card::after {
        content: "✨";
        position: absolute;
        bottom: 5px;
        left: 15px;
        font-size: 1.2rem;
        opacity: 0.4;
    }
    
    /* ホバー効果 - 色変化 */
    .news-card:hover {
        transform: translateY(-8px) scale(1.02);
        background: linear-gradient(145deg, #ffe4e6 0%, #ffd1d4 100%);
        border-color: #ff6b7a;
        box-shadow: 0 16px 48px rgba(255, 107, 122, 0.4),
                    0 0 30px rgba(255, 215, 0, 0.3);
    }
    
    .news-card:hover::before {
        opacity: 1;
        transform: rotate(15deg) scale(1.2);
    }
    
    /* カードタイトル */
    .card-title {
        color: #2d5a3d;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 12px;
        line-height: 1.5;
        padding-right: 40px;
    }
    
    .news-card:hover .card-title {
        color: #c41e3a;
    }
    
    /* 日付バッジ */
    .date-badge {
        display: inline-block;
        background: linear-gradient(90deg, #c41e3a 0%, #ff6b7a 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 14px;
        box-shadow: 0 4px 12px rgba(196, 30, 58, 0.3);
    }
    
    /* 要約テキスト */
    .summary-text {
        color: #4a5568;
        font-size: 0.95rem;
        line-height: 1.8;
        margin-bottom: 15px;
    }
    
    /* リンクヒント */
    .link-hint {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(90deg, #2d5a3d 0%, #3d7a4d 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.9rem;
        box-shadow: 0 4px 15px rgba(45, 90, 61, 0.3);
        transition: all 0.3s ease;
    }
    
    .news-card:hover .link-hint {
        background: linear-gradient(90deg, #c41e3a 0%, #ff6b7a 100%);
        box-shadow: 0 6px 20px rgba(196, 30, 58, 0.4);
    }
    
    /* ヘッダー */
    .header-container {
        text-align: center;
        padding: 30px 0 40px 0;
        position: relative;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3),
                     0 0 30px rgba(255, 215, 0, 0.5);
        margin-bottom: 10px;
    }
    
    .subtitle {
        color: #a8d5ba;
        font-size: 1.2rem;
        font-weight: 500;
    }
    
    .shimaenaga-parade {
        font-size: 2.5rem;
        margin: 15px 0;
        letter-spacing: 10px;
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* サイドバー */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #c41e3a 0%, #8b1538 100%) !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] h2 {
        color: #ffd700 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    section[data-testid="stSidebar"] h3 {
        color: #ffe4b5 !important;
    }
    
    section[data-testid="stSidebar"] p {
        color: #fff5f5 !important;
    }
    
    /* 記事カウント */
    .article-count {
        text-align: center;
        color: #ffffff;
        font-size: 1.1rem;
        margin-bottom: 30px;
        padding: 15px 20px;
        background: linear-gradient(90deg, rgba(196, 30, 58, 0.3) 0%, rgba(255, 107, 122, 0.2) 50%, rgba(196, 30, 58, 0.3) 100%);
        border-radius: 15px;
        border: 2px solid rgba(255, 215, 0, 0.3);
    }
    
    /* シマエナガ装飾 */
    .shimaenaga-deco {
        position: fixed;
        font-size: 3rem;
        opacity: 0.2;
        z-index: 0;
        pointer-events: none;
    }
    
    .shimaenaga-left {
        left: 20px;
        top: 50%;
    }
    
    .shimaenaga-right {
        right: 20px;
        top: 30%;
    }
    
    /* サイドバーシマエナガ */
    .sidebar-shimaenaga {
        text-align: center;
        font-size: 4rem;
        margin: 20px 0;
        animation: sway 3s ease-in-out infinite;
    }
    
    @keyframes sway {
        0%, 100% { transform: rotate(-5deg); }
        50% { transform: rotate(5deg); }
    }
    
    /* クリスマス装飾 */
    .xmas-deco {
        text-align: center;
        font-size: 1.8rem;
        letter-spacing: 15px;
        margin: 10px 0;
        opacity: 0.8;
    }
</style>

<div class="shimaenaga-deco shimaenaga-left">🐦</div>
<div class="shimaenaga-deco shimaenaga-right">🐦</div>
""", unsafe_allow_html=True)

def get_google_news_rss_url(query: str) -> str:
    """検索クエリからGoogle News RSSのURLを生成"""
    encoded_query = quote(query)
    return f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"

def parse_date(date_str: str) -> str:
    """日付文字列をフォーマット"""
    try:
        parsed = datetime(*time.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")[:6])
        return parsed.strftime("%Y年%m月%d日 %H:%M")
    except:
        try:
            parsed = datetime(*time.strptime(date_str, "%a, %d %b %Y %H:%M:%S GMT")[:6])
            return parsed.strftime("%Y年%m月%d日 %H:%M")
        except:
            return date_str

def clean_summary(summary: str) -> str:
    """要約テキストをクリーンアップ"""
    import re
    clean = re.sub(r'<[^>]+>', '', summary)
    clean = re.sub(r'\s+', ' ', clean).strip()
    if len(clean) > 250:
        clean = clean[:247] + "..."
    return clean

def fetch_news(query: str):
    """Google News RSSからニュースを取得"""
    url = get_google_news_rss_url(query)
    feed = feedparser.parse(url)
    return feed.entries

def render_news_card(entry):
    """ニュースカードをレンダリング（カード全体がクリック可能）"""
    title = entry.get('title', 'タイトルなし')
    link = entry.get('link', '#')
    published = entry.get('published', '日付不明')
    summary = entry.get('summary', '要約なし')
    
    formatted_date = parse_date(published)
    clean_text = clean_summary(summary)
    
    # カード全体をリンクに
    card_html = f"""
    <a href="{link}" target="_blank" class="news-card-link">
        <div class="news-card">
            <h3 class="card-title">{title}</h3>
            <div class="date-badge">🎄 {formatted_date}</div>
            <p class="summary-text">{clean_text}</p>
            <span class="link-hint">� 記事を読む →</span>
        </div>
    </a>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def main():
    # ヘッダー
    st.markdown("""
    <div class="header-container">
        <div class="xmas-deco">🎄 ❄️ 🎁 ❄️ 🎄</div>
        <div class="shimaenaga-parade">🐦🐦🐦🐦🐦</div>
        <h1 class="main-title">🐦 シマエナガAIニュース 🐦</h1>
        <p class="subtitle">もふもふシマエナガと一緒に最新AIニュースをチェック！</p>
        <div class="xmas-deco">🌟 ❄️ 🎅 ❄️ 🌟</div>
    </div>
    """, unsafe_allow_html=True)
    
    # サイドバー
    with st.sidebar:
        st.markdown('<div class="sidebar-shimaenaga">🐦</div>', unsafe_allow_html=True)
        st.markdown("## 🔍 検索設定")
        st.markdown("---")
        
        search_query = st.text_input(
            "キーワードを入力してね 🐦",
            value="Artificial Intelligence",
            placeholder="検索したいワードを入力...",
            help="Google Newsから検索するキーワードを入力してください"
        )
        
        st.markdown("---")
        st.markdown("### 📊 データソース")
        st.info("🌐 Google News RSS")
        
        st.markdown("---")
        st.markdown("### 🐦 使い方")
        st.markdown("""
        1️⃣ 検索ボックスにキーワード入力  
        2️⃣ Enterで検索開始！  
        3️⃣ カードをクリックで記事へ  
        """)
        
        if st.button("🔄 ニュースを更新", use_container_width=True):
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🐦 シマエナガとは？")
        st.markdown("""
        北海道に生息する  
        まんまるでもふもふの  
        かわいい小鳥です！  
        
        🐦❄️🐦❄️🐦
        """)
    
    # ニュース取得・表示
    if search_query:
        with st.spinner("🐦 シマエナガがニュースを集めています..."):
            news_entries = fetch_news(search_query)
        
        if news_entries:
            st.markdown(f"""
            <div class="article-count">
                � 「{search_query}」のニュースを <strong>{len(news_entries)}</strong> 件見つけたよ！🎄
            </div>
            """, unsafe_allow_html=True)
            
            # 2カラムレイアウト
            col1, col2 = st.columns(2)
            
            for i, entry in enumerate(news_entries):
                with col1 if i % 2 == 0 else col2:
                    render_news_card(entry)
        else:
            st.warning("🐦 ニュースが見つからなかったよ...別のキーワードで検索してみてね！")
    else:
        st.info("🐦 検索キーワードを入力してね！")

if __name__ == "__main__":
    main()
