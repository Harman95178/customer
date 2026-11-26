
import os
import pandas as pd
import pymysql
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv

# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD","blessyouharman8102004")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "customer_churn_db")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))


# ==========================================
# 2. STREAMLIT PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Customer Churn Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# 3. CUSTOM DASHBOARD DESIGN
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

.block-container, [data-testid="stMainBlockContainer"] { padding-top:5.25rem !important; }
.intro-shell { position:relative; isolation:isolate; overflow:hidden; padding:clamp(28px,5vw,64px); border:1px solid rgba(148,163,184,.16); border-radius:28px; color:#f8fafc; background:radial-gradient(ellipse at 82% 9%,rgba(59,130,246,.3),transparent 34%),radial-gradient(ellipse at 5% 100%,rgba(124,58,237,.22),transparent 40%),linear-gradient(125deg,#0d1728,#13213a 58%,#182640); background-size:180% 180%; animation:introGradient 20s ease-in-out infinite; box-shadow:0 26px 70px rgba(15,23,42,.15); font-family:'DM Sans',sans-serif; }
.intro-grid { display:grid; grid-template-columns:minmax(0,1.12fr) minmax(270px,.82fr); gap:42px; align-items:center; }
.intro-copy { position:relative;z-index:1; }
.intro-kicker { display:flex;align-items:center;gap:10px;margin-bottom:23px;color:#b7c8e3;font-size:11px;font-weight:700;letter-spacing:.16em;text-transform:uppercase; }
.intro-pulse { width:8px;height:8px;border-radius:50%;background:#60a5fa;box-shadow:0 0 16px #60a5fa;animation:pulseGlow 2.4s ease-in-out infinite; }
.intro-heading { margin:0;max-width:650px;color:#fff;font-family:'Manrope','DM Sans',sans-serif;font-size:clamp(40px,6vw,68px);font-weight:800;line-height:1.04;letter-spacing:-.06em; }
.intro-heading span { background:linear-gradient(100deg,#8bbcff,#d0c2ff,#8bbcff);background-size:220% auto;-webkit-background-clip:text;background-clip:text;color:transparent;animation:titleShimmer 6s linear infinite; }
.intro-description { max-width:545px;margin:20px 0 28px;color:#bac5d5;font-size:16px;line-height:1.75; }
.intro-cta { display:inline-flex;align-items:center;gap:13px;padding:14px 19px;border-radius:12px;background:#f8fafc;color:#111827!important;text-decoration:none!important;font-size:14px;font-weight:700;box-shadow:0 9px 24px rgba(0,0,0,.2);transition:transform .22s,box-shadow .22s; }
.intro-cta:hover { transform:translateY(-3px);box-shadow:0 15px 32px rgba(0,0,0,.3); }
.intro-cta span { display:inline-block;font-size:18px;transition:transform .22s; }.intro-cta:hover span { transform:translateX(4px); }
.intro-meta { margin-top:34px;color:#8493aa;font-size:10px;font-weight:600;letter-spacing:.14em; }
.preview-card { position:relative;min-height:280px;padding:22px;border:1px solid rgba(203,213,225,.16);border-radius:20px;background:linear-gradient(145deg,rgba(255,255,255,.11),rgba(255,255,255,.035));box-shadow:0 24px 65px rgba(0,0,0,.23);backdrop-filter:blur(14px);transition:transform .25s ease; }
.preview-header { display:flex;align-items:center;justify-content:space-between;color:#e6edf8;font-size:12px;font-weight:700; }
.preview-tag { padding:6px 9px;border:1px solid rgba(96,165,250,.28);border-radius:20px;color:#a6ccff;font-size:9px;letter-spacing:.08em; }
.focus-tabs { display:flex;gap:6px;margin-top:20px;padding:4px;border:1px solid rgba(203,213,225,.12);border-radius:11px;background:rgba(15,23,42,.28); }
.focus-tab { flex:1;padding:8px 6px;border:0;border-radius:8px;background:transparent;color:#aab7ca;font:600 11px 'DM Sans',sans-serif;cursor:pointer;transition:background .25s,color .25s,transform .25s,box-shadow .25s; }
.focus-tab:hover { color:#fff;transform:translateY(-1px); }
.focus-tab.active { background:rgba(96,165,250,.19);color:#dbeafe;box-shadow:inset 0 0 0 1px rgba(96,165,250,.2); }
.preview-title { margin:16px 0 5px;color:#fff;font:700 20px 'Manrope','DM Sans',sans-serif;letter-spacing:-.04em;transition:opacity .22s ease,transform .22s ease; }
.preview-subtitle { min-height:34px;color:#9eacc1;font-size:11px;line-height:1.5;transition:opacity .22s ease,transform .22s ease; }
.preview-title.is-changing,.preview-subtitle.is-changing { opacity:0;transform:translateY(5px); }
.preview-chart { display:flex;align-items:end;gap:9px;height:92px;margin-top:24px;padding:0 5px;border-bottom:1px solid rgba(203,213,225,.15); }
.preview-bar { flex:1;height:var(--height);border-radius:5px 5px 1px 1px;background:linear-gradient(180deg,#82bdff,#416eea);transform:scaleY(0);transform-origin:bottom;transition:height .5s cubic-bezier(.2,.8,.2,1),transform .8s cubic-bezier(.2,.8,.2,1);transition-delay:var(--delay); }
.preview-card.is-visible .preview-bar { transform:scaleY(1); }
.preview-labels { display:flex;justify-content:space-between;margin-top:8px;color:#8190a6;font-size:9px; }
.preview-float { position:absolute;right:-10px;bottom:18px;padding:9px 12px;border:1px solid rgba(255,255,255,.14);border-radius:11px;background:#1b2942;color:#dbeafe;font-size:10px;box-shadow:0 12px 28px rgba(0,0,0,.25);animation:floatNote 5s ease-in-out infinite; }
.preview-float b { color:#86efac; }
.intro-reveal { opacity:1;transform:none;transition:opacity .65s ease,transform .65s ease; }
.intro-animations .intro-reveal { opacity:0;transform:translateY(16px); }
.intro-animations .intro-reveal.is-visible { opacity:1;transform:translateY(0); }
@keyframes floatNote { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-8px); } }
@keyframes introGradient { 0%,100% { background-position:0% 50%; } 50% { background-position:100% 50%; } }
@keyframes pulseGlow { 0%,100% { box-shadow:0 0 8px #60a5fa; } 50% { box-shadow:0 0 19px #60a5fa; } }
@keyframes titleShimmer { to { background-position:220% center; } }
@media(max-width:760px) { .intro-grid { grid-template-columns:1fr;gap:30px; } .preview-card { max-width:520px;width:100%; } }
@media(max-width:520px) { .intro-shell { padding:28px 22px;border-radius:20px; } .intro-description { font-size:14px; } }
@media(max-width:520px) { .dashboard-heading { padding:20px; } }
@media(max-width:640px) { .block-container, [data-testid="stMainBlockContainer"] { padding-top:4.5rem !important; } }
@media(prefers-reduced-motion:reduce) { *,*:before,*:after { animation:none!important;transition:none!important;scroll-behavior:auto!important; } }
html { scroll-behavior:smooth; }

.stApp {
    background:linear-gradient(135deg,#F3F6FA 0%,#edf2f8 52%,#f6f8fb 100%);
    background-size:200% 200%;
    animation:dashboardGradient 32s ease infinite;
}
[data-testid="stAppViewContainer"], [data-testid="stMain"] { background:transparent; }

@keyframes dashboardGradient {
    0%,100% { background-position:0% 50%; }
    50% { background-position:100% 50%; }
}

header[data-testid="stHeader"] { background:rgba(243,246,250,.9); }
h1, h2, h3 { color:#142D4E; letter-spacing:-.035em; }
h1 { font-family:'Manrope','DM Sans',sans-serif; font-weight:800; }
h2, h3 { font-weight:700; }
h3 { margin-top:1.15rem!important;margin-bottom:.65rem!important;padding-left:11px;border-left:3px solid #237B8B;color:#142D4E; }
section[data-testid="stSidebar"] { background:linear-gradient(180deg,#eef3f8 0%,#e9eff6 58%,#f1f4f8 100%); border-right:1px solid #dfe6ee; }
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2 { color:#142D4E; }
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stCaptionContainer"] { color:#66788f; }
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { color:#4c6079; }
section[data-testid="stSidebar"] [data-baseweb="select"] > div { background:#fff;border-color:#d8e1eb;color:#142D4E; }
.dashboard-heading { margin:0 0 18px; padding:20px 26px; border:1px solid rgba(255,255,255,.14);
    border-radius:20px; background:linear-gradient(115deg,#142D4E 0%,#193b5e 58%,#237B8B 130%);
    box-shadow:0 14px 34px rgba(20,45,78,.16); }
.dashboard-eyebrow { margin-bottom:9px; color:#b6dce2; font-size:11px; font-weight:700; letter-spacing:.15em; text-transform:uppercase; }
.dashboard-title { margin:0; color:#fff; font-family:'Manrope','DM Sans',sans-serif; font-size:clamp(32px,3.6vw,42px);
    font-weight:800; line-height:1.08; letter-spacing:-.055em; }
.dashboard-title-accent { background:linear-gradient(100deg,#ffffff,#b9e7e7); -webkit-background-clip:text;
    background-clip:text; color:transparent; }
.dashboard-description { margin:8px 0 0; color:#d6e2ee; font-size:13px; line-height:1.6; }
.dashboard-reveal { opacity:1; transform:none; transition:opacity .55s ease,transform .55s ease,filter .55s ease; }
.dashboard-animations .dashboard-reveal { opacity:0; transform:translateY(12px); filter:blur(3px); }
.dashboard-animations .dashboard-reveal.is-visible { opacity:1; transform:translateY(0); filter:blur(0); }
div[data-testid="stMetric"] { min-height:112px; padding:17px 18px; border-radius:16px; border:1px solid #e1e8ef;border-top:3px solid #237B8B;
    background:#fff; box-shadow:0 7px 22px rgba(20,45,78,.065); transition:transform .2s,box-shadow .2s; }
div[data-testid="stMetric"]:hover { transform:translateY(-3px); box-shadow:0 13px 28px rgba(20,45,78,.12); }
div[data-testid="stMetricLabel"] { color:#63768d; font-size:13px; font-weight:600; }
div[data-testid="stMetricLabel"] p { overflow:visible;white-space:normal;font-size:12px;line-height:1.25; }
div[data-testid="stMetricValue"] { color:#142D4E; font-family:'Manrope','DM Sans',sans-serif; font-weight:800; letter-spacing:-.04em; }
div[data-testid="stPlotlyChart"] { overflow:hidden; border:1px solid #e1e8ef; border-radius:17px; background:#fff;
    box-shadow:0 7px 22px rgba(20,45,78,.055); padding:8px; }
div[data-testid="stDataFrame"] { overflow:hidden; border:1px solid #e1e8ef; border-radius:15px; background:#fff;box-shadow:0 7px 22px rgba(20,45,78,.055); }
div[data-testid="stButton"] button, div[data-testid="stDownloadButton"] button { min-height:42px; border-radius:10px; font-weight:650;background:#142D4E;border-color:#142D4E;color:#fff!important; }
div[data-testid="stButton"] button *, div[data-testid="stDownloadButton"] button * { color:#fff!important;opacity:1!important; }
div[data-testid="stButton"] button:hover, div[data-testid="stDownloadButton"] button:hover { background:#237B8B;border-color:#237B8B;color:#fff!important; }
[data-baseweb="tag"] { background:#237B8B!important;border-color:#237B8B!important;color:#fff!important; }
.st-key-open_dashboard div[data-testid="stButton"] button { margin-top:18px;min-height:50px;padding:0 24px;border:1px solid rgba(149,231,226,.55)!important;border-radius:13px;background:#237B8B!important;color:#fff!important;font-size:15px;font-weight:700;letter-spacing:.01em;box-shadow:0 9px 24px rgba(14,116,128,.24);transition:background-color .25s ease,transform .25s cubic-bezier(.2,.7,.2,1),box-shadow .25s ease,filter .25s ease; }
.st-key-open_dashboard div[data-testid="stButton"] button:hover { background:#2d96a0!important;color:#fff!important;transform:translateY(-3px);filter:saturate(1.12);box-shadow:0 15px 32px rgba(14,116,128,.36); }
.st-key-open_dashboard div[data-testid="stButton"] button:active { transform:translateY(-1px) scale(.985);box-shadow:0 6px 16px rgba(14,116,128,.26); }
.st-key-open_dashboard div[data-testid="stButton"] button:focus-visible { outline:3px solid #a6e5e1;outline-offset:3px; }
.dashboard-rise { animation:dashboardRise .62s cubic-bezier(.2,.7,.2,1) both; }
@keyframes dashboardRise { from { opacity:0;transform:translateY(12px); } to { opacity:1;transform:translateY(0); } }
@media(prefers-reduced-motion:reduce) { .dashboard-rise { animation:none!important; } }
hr { border-color:#e2e8f0; }

</style>
""", unsafe_allow_html=True)

px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = ["#237B8B", "#142D4E", "#27A879", "#E65B5B", "#69AEB8"]


def style_figure(fig):
    fig.update_layout(
        font={"family": "DM Sans, sans-serif", "size": 12, "color": "#53677f"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#ffffff",
        title={"font": {"size": 16, "color": "#142D4E"}, "x": 0.03, "xanchor": "left", "y": 0.98},
        margin={"l": 18, "r": 18, "t": 64, "b": 52},
        legend={"orientation": "h", "yanchor": "top", "y": -0.22, "x": 0.02}
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="#d7e0e9", tickfont={"color": "#53677f"})
    fig.update_yaxes(showgrid=True, gridcolor="#e9eef3", zeroline=False, tickfont={"color": "#53677f"})
    return fig


# ==========================================
# 3A. INTRODUCTION PAGE
# ==========================================

if "app_page" not in st.session_state:
    st.session_state.app_page = "intro"

INTRO_HTML = """
<section class="intro-shell" id="churn-intro">
  <div class="intro-grid">
    <div class="intro-copy">
      <div class="intro-kicker intro-reveal"><i class="intro-pulse"></i> Customer intelligence</div>
      <h1 class="intro-heading intro-reveal">Understand churn.<br><span>Improve retention.</span></h1>
      <p class="intro-description intro-reveal">This project explores why customers leave by analyzing contract type, tenure, internet service, and monthly charges. Use the dashboard to compare churn patterns, filter customer groups, and spot signals that can guide retention efforts.</p>
      <div class="intro-meta intro-reveal">CUSTOMER CHURN ANALYSIS&nbsp;&nbsp; · &nbsp;&nbsp;RETENTION INSIGHTS</div>
    </div>
    <div class="preview-card intro-reveal" id="retention-preview">
      <div class="preview-header"><span>Explore the analysis</span><span class="preview-tag">INTERACTIVE PREVIEW</span></div>
      <div class="focus-tabs" role="tablist" aria-label="Analysis focus">
        <button class="focus-tab active" type="button" role="tab" aria-selected="true" data-title="Churn patterns" data-copy="Compare customers who stay with those who leave." data-bars="38,58,47,76,63,88,71,96">Churn</button>
        <button class="focus-tab" type="button" role="tab" aria-selected="false" data-title="Contract & tenure" data-copy="Explore how commitment and time with the company relate to churn." data-bars="82,70,61,54,46,39,33,27">Contracts</button>
        <button class="focus-tab" type="button" role="tab" aria-selected="false" data-title="Charges & services" data-copy="Review monthly charges and service choices across customers." data-bars="29,43,57,49,72,65,83,92">Revenue</button>
      </div>
      <div class="preview-title" id="focus-title">Churn patterns</div>
      <div class="preview-subtitle" id="focus-copy">Compare customers who stay with those who leave.</div>
      <div class="preview-chart" aria-label="Illustrative visualization preview">
        <i class="preview-bar" style="--height:38%;--delay:.08s"></i><i class="preview-bar" style="--height:58%;--delay:.16s"></i>
        <i class="preview-bar" style="--height:47%;--delay:.24s"></i><i class="preview-bar" style="--height:76%;--delay:.32s"></i>
        <i class="preview-bar" style="--height:63%;--delay:.40s"></i><i class="preview-bar" style="--height:88%;--delay:.48s"></i>
        <i class="preview-bar" style="--height:71%;--delay:.56s"></i><i class="preview-bar" style="--height:96%;--delay:.64s"></i>
      </div>
      <div class="preview-labels"><span>LOWER</span><span>GROUP</span><span>COMPARISON</span><span>HIGHER</span></div>
      <div class="preview-float"><b>Explore</b>&nbsp; project insights</div>
    </div>
  </div>
</section>
<script>
(() => {
  const root = document.getElementById('churn-intro');
  if (!root || root.dataset.animated) return;
  root.dataset.animated = 'true';
  root.classList.add('intro-animations');
  root.querySelectorAll('.intro-reveal').forEach((item, index) => {
    window.setTimeout(() => item.classList.add('is-visible'), 100 + index * 110);
  });
  const tabs = root.querySelectorAll('.focus-tab');
  const bars = root.querySelectorAll('.preview-bar');
  const title = root.querySelector('#focus-title');
  const copy = root.querySelector('#focus-copy');
  tabs.forEach(tab => tab.addEventListener('click', () => {
    if (tab.classList.contains('active')) return;
    tabs.forEach(item => {
      item.classList.toggle('active', item === tab);
      item.setAttribute('aria-selected', item === tab ? 'true' : 'false');
    });
    title.classList.add('is-changing');
    copy.classList.add('is-changing');
    window.setTimeout(() => {
      title.textContent = tab.dataset.title;
      copy.textContent = tab.dataset.copy;
      tab.dataset.bars.split(',').forEach((height, index) => {
        if (bars[index]) bars[index].style.setProperty('--height', `${height}%`);
      });
      title.classList.remove('is-changing');
      copy.classList.remove('is-changing');
    }, 180);
  }));
  const card = root.querySelector('#retention-preview');
  if (card && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    root.addEventListener('pointermove', event => {
      const bounds = root.getBoundingClientRect();
      const x = (event.clientX - bounds.left) / bounds.width - .5;
      const y = (event.clientY - bounds.top) / bounds.height - .5;
      card.style.transform = `perspective(900px) rotateY(${x * 5}deg) rotateX(${-y * 4}deg)`;
    });
    root.addEventListener('pointerleave', () => card.style.transform = '');
  }
})();
</script>
"""

if st.session_state.app_page == "intro":
    st.html(INTRO_HTML, unsafe_allow_javascript=True)
    if st.button("Open the dashboard  →", key="open_dashboard"):
        st.session_state.app_page = "dashboard"
        st.rerun()
    st.stop()

if st.sidebar.button("← Introduction", key="back_to_intro"):
    st.session_state.app_page = "intro"
    st.rerun()


# ==========================================
# 4. MYSQL DATABASE CONNECTION
# ==========================================

def get_connection():

    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        port=MYSQL_PORT,
        charset="utf8mb4"
    )


# ==========================================
# 5. LOAD DATA FROM MYSQL
# ==========================================

@st.cache_data(ttl=60)
def load_data():

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM customers")

            columns = [
                col[0] for col in cursor.description
            ]

            rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=columns)

    finally:

        connection.close()

    # Clean column names
    df.columns = df.columns.astype(str).str.strip()

    # Convert numeric columns
    numeric_columns = [
        "MonthlyCharges",
        "TotalCharges",
        "tenure"
    ]

    for col in numeric_columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # Validate MonthlyCharges
    if "MonthlyCharges" not in df.columns:

        raise ValueError(
            "MonthlyCharges column not found."
        )

    if df["MonthlyCharges"].notna().sum() == 0:

        raise ValueError(
            "MonthlyCharges contains no valid numeric values."
        )

    return df


# ==========================================
# 6. DASHBOARD PAGE
# ==========================================

st.html("""
<section class="dashboard-heading" id="dashboard-heading">
  <div class="dashboard-eyebrow dashboard-reveal">Customer retention analytics</div>
  <h1 class="dashboard-title dashboard-reveal">Customer Churn <span class="dashboard-title-accent">Analytics</span></h1>
  <p class="dashboard-description dashboard-reveal">Monitor customer retention, service patterns, and revenue signals in one view.</p>
</section>
<script>
(() => {
  const heading = document.getElementById('dashboard-heading');
  if (!heading || heading.dataset.animated || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  heading.dataset.animated = 'true';
  heading.classList.add('dashboard-animations');
  heading.querySelectorAll('.dashboard-reveal').forEach((item, index) => {
    window.setTimeout(() => item.classList.add('is-visible'), 100 + index * 130);
  });
})();
</script>
""", unsafe_allow_javascript=True)


# ==========================================
# 7. REFRESH DATA
# ==========================================

if st.sidebar.button("🔄 Refresh Dashboard"):

    st.cache_data.clear()
    st.rerun()


# ==========================================
# 8. LOAD DATABASE DATA
# ==========================================

try:

    df = load_data()

    if df.empty:
        st.warning("No customer records found.")
        st.stop()

except Exception as e:

    st.error(f"Database Error: {e}")

    st.info(
        "Please check your .env file, MySQL connection "
        "and customers table."
    )

    st.stop()


# ==========================================
# 9. SIDEBAR FILTERS
# ==========================================

st.sidebar.title("Explore the data")
st.sidebar.caption("Adjust the filters to refine every metric and chart.")

filtered_df = df.copy()

if "gender" in df.columns:

    genders = sorted(
        df["gender"].dropna().unique().tolist()
    )

    selected_gender = st.sidebar.multiselect(
        "Select Gender",
        genders,
        default=genders
    )

    filtered_df = filtered_df[
        filtered_df["gender"].isin(selected_gender)
    ]


if "Contract" in df.columns:

    contracts = sorted(
        df["Contract"].dropna().unique().tolist()
    )

    selected_contract = st.sidebar.multiselect(
        "Select Contract",
        contracts,
        default=contracts
    )

    filtered_df = filtered_df[
        filtered_df["Contract"].isin(selected_contract)
    ]


if "InternetService" in df.columns:

    services = sorted(
        df["InternetService"].dropna().unique().tolist()
    )

    selected_service = st.sidebar.multiselect(
        "Internet Service",
        services,
        default=services
    )

    filtered_df = filtered_df[
        filtered_df["InternetService"].isin(selected_service)
    ]


if "Churn" in df.columns:

    churn_types = sorted(
        df["Churn"].dropna().unique().tolist()
    )

    selected_churn = st.sidebar.multiselect(
        "Churn Status",
        churn_types,
        default=churn_types
    )

    filtered_df = filtered_df[
        filtered_df["Churn"].isin(selected_churn)
    ]


# ==========================================
# 10. KPI CALCULATIONS
# ==========================================

total_customers = len(filtered_df)

if "Churn" in filtered_df.columns:

    churned_customers = (
        filtered_df["Churn"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("yes")
        .sum()
    )

else:

    churned_customers = 0


churn_rate = (
    churned_customers / total_customers * 100
    if total_customers > 0 else 0
)


avg_monthly_charges = (
    filtered_df["MonthlyCharges"].mean()
    if total_customers > 0 else 0
)


total_revenue = (
    filtered_df["TotalCharges"].sum()
    if "TotalCharges" in filtered_df.columns else 0
)


# ==========================================
# 11. KPI CARDS
# ==========================================

st.subheader("Performance snapshot")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Customers",
    f"{total_customers:,}"
)

col2.metric(
    "Churned",
    f"{churned_customers:,}"
)

col3.metric(
    "Churn rate",
    f"{churn_rate:.1f}%"
)

monthly_revenue_at_risk = (
    filtered_df.loc[
        filtered_df["Churn"].astype(str).str.strip().str.lower().eq("yes"),
        "MonthlyCharges"
    ].sum()
    if "Churn" in filtered_df.columns else 0
)

col4.metric(
    "Revenue at risk",
    f"${monthly_revenue_at_risk / 1000:.1f}K" if monthly_revenue_at_risk >= 1000 else f"${monthly_revenue_at_risk:,.0f}"
)

st.caption(f"Showing {total_customers:,} customers after filters · Average monthly charge: ${avg_monthly_charges:,.2f}")

st.html("""
<script>
(() => {
  const targets = document.querySelectorAll('[data-testid="stMetric"], [data-testid="stMain"] h3');
  targets.forEach((element, index) => {
    if (element.dataset.transitioned) return;
    element.dataset.transitioned = 'true';
    element.classList.add('dashboard-rise');
    element.style.animationDelay = `${Math.min(index * 90, 450)}ms`;
  });
})();
</script>
""", unsafe_allow_javascript=True)


# ==========================================
# 12. CUSTOMER CHURN ANALYSIS
# ==========================================

st.subheader("Churn & customer profile")

chart1, chart2 = st.columns(2)


# Churn Pie Chart
if "Churn" in filtered_df.columns:

    churn_data = (
        filtered_df["Churn"]
        .value_counts()
        .reset_index()
    )

    churn_data.columns = [
        "Churn",
        "Customers"
    ]

    with chart1:

        fig = px.pie(
            churn_data,
            names="Churn",
            values="Customers",
            hole=0.55,
            title="Customer Churn Distribution",
            color="Churn",
            color_discrete_map={
                "Yes": "#237B8B",
                "No": "#142D4E"
            }
        )

        st.plotly_chart(
            style_figure(fig),
            width="stretch"
        )


# Gender Bar Chart
if "gender" in filtered_df.columns:

    gender_data = (
        filtered_df["gender"]
        .value_counts()
        .reset_index()
    )

    gender_data.columns = [
        "Gender",
        "Customers"
    ]

    with chart2:

        fig = px.bar(
            gender_data,
            x="Gender",
            y="Customers",
            color="Gender",
            color_discrete_map={"Male": "#142D4E", "Female": "#237B8B"},
            title="Customers by Gender",
            text="Customers"
        )
        fig.update_layout(showlegend=False)

        st.plotly_chart(
            style_figure(fig),
            width="stretch"
        )


# ==========================================
# 13. CONTRACT ANALYSIS
# ==========================================

st.subheader("Contract mix and churn")

if "Contract" in filtered_df.columns and "Churn" in filtered_df.columns:

    contract_data = pd.crosstab(
        filtered_df["Contract"],
        filtered_df["Churn"]
    ).reset_index()

    contract_data = contract_data.melt(
        id_vars="Contract",
        var_name="Churn",
        value_name="Customers"
    )

    fig = px.bar(
        contract_data,
        x="Contract",
        y="Customers",
        color="Churn",
        barmode="group",
        title="Churn by contract type",
        color_discrete_map={
            "Yes": "#237B8B",
            "No": "#142D4E"
        }
    )

    st.plotly_chart(
        style_figure(fig),
        width="stretch"
    )


# ==========================================
# 14. REVENUE ANALYSIS
# ==========================================

st.subheader("Monthly charge insights")

rev1, rev2 = st.columns(2)


# Monthly Charges Distribution
with rev1:

    fig = px.histogram(
        filtered_df,
        x="MonthlyCharges",
        nbins=30,
        color_discrete_sequence=["#237B8B"],
        title="Monthly charges distribution"
    )

    st.plotly_chart(
        style_figure(fig),
        width="stretch"
    )


# Monthly Charges vs Churn
if "Churn" in filtered_df.columns:

    with rev2:

        fig = px.box(
            filtered_df,
            x="Churn",
            y="MonthlyCharges",
            color="Churn",
            color_discrete_map={"Yes": "#237B8B", "No": "#142D4E"},
            title="Monthly charges by churn status"
        )

        st.plotly_chart(
            style_figure(fig),
            width="stretch"
        )


# ==========================================
# 15. INTERNET SERVICE ANALYSIS
# ==========================================

st.subheader("Internet service mix")

if "InternetService" in filtered_df.columns:

    internet_data = (
        filtered_df["InternetService"]
        .value_counts()
        .reset_index()
    )

    internet_data.columns = [
        "Internet Service",
        "Customers"
    ]

    fig = px.bar(
        internet_data,
        x="Internet Service",
        y="Customers",
        color="Internet Service",
        text="Customers",
        title="Customers by internet service"
    )

    st.plotly_chart(
        style_figure(fig),
        width="stretch"
    )


# ==========================================
# 16. CUSTOMER DETAILS
# ==========================================

st.subheader("Customer records")

st.caption("Review filtered records or download the current customer selection.")

st.dataframe(
    filtered_df,
    width="stretch",
    hide_index=True
)


# ==========================================
# 17. DOWNLOAD CUSTOMER DATA
# ==========================================

csv = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Customer Data",
    data=csv,
    file_name="customer_churn_data.csv",
    mime="text/csv"
)


# ==========================================
# 18. FOOTER
# ==========================================

st.divider()

st.caption(
    "Customer churn analysis · Retention, service mix, and revenue insights"
)
