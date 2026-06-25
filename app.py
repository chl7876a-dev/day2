import streamlit as st
import pandas as pd
import altair as alt
import requests
from datetime import datetime

# ── 다크 테마 색상 토큰 ────────────────────────────────────────────────────────
BG         = "#12131F"
CARD       = "#1A1D2E"
SIDEBAR_BG = "#0E0F1A"
BORDER     = "#2A2D45"
TEXT       = "#E0E0E0"
MUTED      = "#8B97B5"
ACCENT     = "#818CF8"   # indigo-400
C_GREEN    = "#34D399"
C_AMBER    = "#FBBF24"
C_RED      = "#F87171"
C_PURPLE   = "#A78BFA"
C_CYAN     = "#22D3EE"
CHART_GRID = "#242740"
CHART_LBL  = "#8B97B5"
CHART_TTL  = "#C4C9E8"


def dark_chart(chart, height=280):
    """Altair 차트에 다크 테마를 일괄 적용."""
    return (
        chart
        .properties(height=height, background=CARD)
        .configure_view(stroke=None, fill=CARD)
        .configure_axis(
            grid=True, gridColor=CHART_GRID, domainColor=BORDER,
            labelColor=CHART_LBL, titleColor=CHART_TTL,
            labelFontSize=11, titleFontSize=11,
        )
        .configure_legend(
            labelColor=TEXT, titleColor=MUTED,
            labelFontSize=11, titleFontSize=10,
        )
    )


# ── 페이지 설정 ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="에코마케팅 광고 대시보드", layout="wide", page_icon="📊")

# ── 스타일 ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
/* ════ 기본 배경 ════ */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="block-container"],
.main .block-container {{
    background-color: {BG} !important;
    color: {TEXT} !important;
}}
[data-testid="stHeader"] {{ background: transparent !important; }}
.block-container {{ padding: 2rem 2.5rem 3rem !important; max-width: 1280px; }}
.main p, .main li {{ color: {TEXT} !important; }}
.main h1, .main h2, .main h3, .main h4 {{
    color: {TEXT} !important;
    font-weight: 700 !important;
}}

/* ════ Fade-in 전환 ════ */
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(8px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
.card     {{ animation: fadeIn 0.4s ease both; }}
.kpi-card {{ animation: fadeIn 0.35s ease both; }}

/* ════ Vega-Lite / Altair 툴팁 ════ */
.vg-tooltip {{
    background: #0A0B14 !important;
    border: 1px solid {ACCENT} !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    font-size: 0.82rem !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.7) !important;
    color: {TEXT} !important;
}}
.vg-tooltip * {{ color: {TEXT} !important; background: transparent !important; }}
.vg-tooltip td.key   {{ color: {ACCENT} !important; padding-right: 8px; }}
.vg-tooltip td.value {{ color: #FFFFFF !important; font-weight: 600; }}
.vg-tooltip table    {{ border-collapse: separate; border-spacing: 0 3px; }}

/* ════ Streamlit 툴팁 (? 아이콘) ════ */
[data-testid="stTooltipContent"],
[data-testid="stTooltipContent"] div,
[data-testid="stTooltipContent"] p,
[data-testid="stTooltipContent"] span {{
    background: #0A0B14 !important;
    color: {TEXT} !important;
}}

/* ════ 사이드바 ════ */
[data-testid="stSidebar"] {{
    background: {SIDEBAR_BG} !important;
    border-right: 1px solid {BORDER} !important;
}}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] div {{ color: {TEXT} !important; }}
[data-testid="stSidebar"] h2 {{
    color: {ACCENT} !important;
    font-size: 1rem !important;
    border-bottom: 2px solid {BORDER};
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}}

/* ════ 파일 업로더 ════ */
[data-testid="stFileUploader"] {{ background: transparent !important; }}
[data-testid="stFileUploaderDropzone"] {{
    background: rgba(129,140,248,0.05) !important;
    border: 2px dashed {ACCENT} !important;
    border-radius: 14px !important;
    min-height: 90px !important;
    transition: border-color 0.25s ease, background 0.25s ease !important;
}}
[data-testid="stFileUploaderDropzone"]:hover {{
    background: rgba(129,140,248,0.12) !important;
    border-color: #A5B4FC !important;
}}
[data-testid="stFileUploaderDropzoneInstructions"] small,
[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] p,
[data-testid="stFileUploaderDropzoneInstructions"] div {{
    color: #A5B4FC !important;
    font-weight: 600 !important;
}}
[data-testid="stFileUploaderFile"] span,
[data-testid="stFileUploaderFile"] p,
[data-testid="stFileUploaderFile"] div {{ color: {TEXT} !important; }}

/* ════ Multiselect / Select 드롭다운 ════ */
[data-baseweb="tag"] {{ background-color: {ACCENT} !important; border-radius: 6px !important; }}
[data-baseweb="tag"] span {{ color: #FFFFFF !important; }}
[data-baseweb="tag"] svg  {{ color: #FFFFFF !important; fill: #FFFFFF !important; }}
[data-baseweb="popover"],
[data-baseweb="menu"],
ul[data-baseweb="menu"] {{
    background: #1A1D30 !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.65) !important;
}}
[data-baseweb="option"] {{
    background: #1A1D30 !important;
    color: {TEXT} !important;
}}
[data-baseweb="option"]:hover,
[data-baseweb="option"][aria-selected="true"] {{
    background: rgba(129,140,248,0.18) !important;
    color: #A5B4FC !important;
}}
[data-baseweb="select"] > div,
[data-baseweb="input"] {{
    background: #1A1D30 !important;
    border-color: {BORDER} !important;
    color: {TEXT} !important;
    border-radius: 8px !important;
}}
[data-baseweb="select"] span,
[data-baseweb="select"] div {{ color: {TEXT} !important; }}

/* ════ 카드 ════ */
.card {{
    background: {CARD};
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    margin-bottom: 1.2rem;
    border: 1px solid {BORDER};
    transition: box-shadow 0.25s ease;
}}
.card:hover {{ box-shadow: 0 6px 28px rgba(0,0,0,0.55); }}
.card p, .card span, .card div, .card label {{ color: {TEXT} !important; }}

/* ════ KPI 카드 ════ */
.kpi-card {{
    background: {CARD};
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    border: 1px solid {BORDER};
    border-left: 5px solid {ACCENT};
    margin-bottom: 0.8rem;
    transition: box-shadow 0.25s ease, transform 0.2s ease;
}}
.kpi-card:hover {{ box-shadow: 0 6px 28px rgba(0,0,0,0.55); transform: translateY(-2px); }}
.kpi-icon  {{ font-size: 1.4rem; margin-bottom: 0.5rem; display: block; }}
.kpi-label {{
    font-size: 0.72rem !important; color: {MUTED} !important;
    font-weight: 700 !important; text-transform: uppercase;
    letter-spacing: 0.8px; margin-bottom: 0.3rem;
}}
.kpi-value {{
    font-size: 1.55rem !important; font-weight: 800 !important;
    color: #FFFFFF !important; line-height: 1.2; margin-bottom: 0.25rem;
}}
.kpi-sub {{ font-size: 0.73rem !important; color: {MUTED} !important; font-weight: 500 !important; }}

/* ════ 섹션 타이틀 ════ */
.section-title {{
    font-size: 1rem !important;
    font-weight: 700 !important;
    color: {TEXT} !important;
    margin-bottom: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}}

/* ════ 데이터프레임 ════ */
[data-testid="stDataFrame"] {{ border-radius: 10px; overflow: hidden; }}

/* ════ 다운로드 버튼 (항상 인디고 + 흰 글씨) ════ */
[data-testid="stDownloadButton"] > button {{
    background: #4F46E5 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.8rem !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 3px 12px rgba(79,70,229,0.45) !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}}
[data-testid="stDownloadButton"] > button:hover {{
    background: #6366F1 !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.65) !important;
    transform: translateY(-2px) !important;
    color: #FFFFFF !important;
}}
[data-testid="stDownloadButton"] > button p,
[data-testid="stDownloadButton"] > button span {{
    color: #FFFFFF !important;
    font-weight: 700 !important;
}}

/* ════ 알림 박스 ════ */
[data-testid="stAlert"] {{
    border-radius: 12px !important;
    border-left: 4px solid {ACCENT} !important;
    background-color: rgba(129,140,248,0.08) !important;
}}
[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
[data-testid="stAlert"] div {{ color: {TEXT} !important; }}
[data-testid="stNotification"] p,
[data-testid="stNotification"] span {{ color: {TEXT} !important; }}
</style>
""", unsafe_allow_html=True)

# ── 헤더 ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    background: linear-gradient(135deg, #1E1B4B 0%, #312E81 55%, #4C1D95 100%);
    border-radius: 18px;
    padding: 2rem 2.4rem;
    margin-bottom: 1.6rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.5);
    border: 1px solid rgba(129,140,248,0.25);
">
    <div style="font-size:2rem; font-weight:900; color:#FFFFFF; letter-spacing:-0.5px; margin-bottom:0.3rem;">
        📊 에코마케팅 광고 통합 대시보드
    </div>
    <div style="font-size:0.92rem; color:rgba(255,255,255,0.6); font-weight:500;">
        캠페인 운영현황 + 광고소재 성과를 하나의 뷰로 통합 분석합니다
    </div>
</div>
""", unsafe_allow_html=True)

# ── 서울 날씨 ──────────────────────────────────────────────────────────────────
@st.cache_data(ttl=600)
def fetch_seoul_weather():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=37.5665&longitude=126.9780"
        "&current=temperature_2m,weathercode"
        "&hourly=temperature_2m"
        "&timezone=Asia%2FSeoul&forecast_days=1"
    )
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    return r.json()

def weathercode_to_label(code):
    if code == 0:              return "맑음", "☀️"
    if code in (1, 2, 3):     return "구름", "🌤️"
    if code in range(51, 68): return "비", "🌧️"
    if code in range(71, 78): return "눈", "❄️"
    if code in range(80, 83): return "소나기", "🌦️"
    if code in (95, 96, 99):  return "뇌우", "⛈️"
    return "흐림", "🌥️"

try:
    weather_data = fetch_seoul_weather()
    current_temp = weather_data["current"]["temperature_2m"]
    weather_code = weather_data["current"]["weathercode"]
    weather_label, weather_icon = weathercode_to_label(weather_code)

    hourly_times = weather_data["hourly"]["time"]
    hourly_temps = weather_data["hourly"]["temperature_2m"]
    today_str = datetime.now().strftime("%Y-%m-%d")
    hourly_df = pd.DataFrame({
        "시간": [t for t in hourly_times if t.startswith(today_str)],
        "기온(°C)": [hourly_temps[i] for i, t in enumerate(hourly_times) if t.startswith(today_str)],
    })
    hourly_df["시간"] = pd.to_datetime(hourly_df["시간"]).dt.strftime("%H:%M")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🌡️ 서울 현재 날씨</div>', unsafe_allow_html=True)
    w_left, w_right = st.columns([1, 3])
    with w_left:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg,#1E1B4B,#312E81);
            border-radius:14px; padding:1.4rem 1.6rem;
            text-align:center;
            border: 1px solid rgba(129,140,248,0.3);
        ">
            <div style="font-size:2.8rem;">{weather_icon}</div>
            <div style="font-size:2.2rem; font-weight:900; margin:0.2rem 0; color:#FFFFFF;">{current_temp}°C</div>
            <div style="font-size:0.9rem; color:rgba(224,224,224,0.75);">{weather_label} · 서울</div>
        </div>
        """, unsafe_allow_html=True)
    with w_right:
        weather_line = (
            alt.Chart(hourly_df)
            .mark_line(
                point=alt.OverlayMarkDef(color=ACCENT, size=40),
                color=ACCENT, strokeWidth=2.5,
            )
            .encode(
                x=alt.X("시간:N", axis=alt.Axis(labelAngle=-45), title="시간"),
                y=alt.Y("기온(°C):Q", scale=alt.Scale(zero=False), title="기온 (°C)"),
                tooltip=[
                    alt.Tooltip("시간:N", title="시간"),
                    alt.Tooltip("기온(°C):Q", title="기온", format=".1f"),
                ],
            )
        )
        st.altair_chart(dark_chart(weather_line, height=180), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

except Exception:
    st.warning("날씨 정보를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.")

# ── 파일 업로드 ────────────────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📂 데이터 업로드</div>', unsafe_allow_html=True)
st.markdown(
    f"<p style='font-size:0.85rem; color:{MUTED} !important; margin-top:-0.5rem; margin-bottom:1rem;'>"
    f"두 엑셀 파일을 업로드하면 <b style='color:{ACCENT};'>캠페인ID</b> 기준으로 자동 병합되어 대시보드가 활성화됩니다.</p>",
    unsafe_allow_html=True,
)

col_up1, col_up2 = st.columns(2)
with col_up1:
    st.markdown(
        f"<div style='font-size:0.82rem; font-weight:700; color:{ACCENT}; margin-bottom:0.5rem;'>"
        "1️⃣ 캠페인 운영현황</div>"
        f"<div style='font-size:0.78rem; color:{MUTED}; margin-bottom:0.5rem;'>"
        "엑셀 파일을 드래그하거나 클릭하여 업로드하세요</div>",
        unsafe_allow_html=True,
    )
    campaign_file = st.file_uploader(
        "캠페인 운영현황 엑셀 (.xlsx)",
        type=["xlsx"],
        key="campaign",
        label_visibility="collapsed",
    )
with col_up2:
    st.markdown(
        f"<div style='font-size:0.82rem; font-weight:700; color:{C_GREEN}; margin-bottom:0.5rem;'>"
        "2️⃣ 광고소재 성과</div>"
        f"<div style='font-size:0.78rem; color:{MUTED}; margin-bottom:0.5rem;'>"
        "엑셀 파일을 드래그하거나 클릭하여 업로드하세요</div>",
        unsafe_allow_html=True,
    )
    creative_file = st.file_uploader(
        "광고소재 성과 엑셀 (.xlsx)",
        type=["xlsx"],
        key="creative",
        label_visibility="collapsed",
    )
st.markdown('</div>', unsafe_allow_html=True)

if not campaign_file or not creative_file:
    st.markdown(f"""
    <div style="
        background: rgba(129,140,248,0.08);
        border-left: 4px solid {ACCENT};
        border-radius: 12px;
        padding: 1rem 1.4rem;
        color: {TEXT};
        font-size: 0.9rem;
        margin-top: 0.5rem;
    ">
        ℹ️ &nbsp; <b style='color:#FFFFFF;'>두 파일을 모두 업로드</b>하면 통합 대시보드가 표시됩니다.
        <br><span style="color:{MUTED}; font-size:0.82rem;">
            에코마케팅_캠페인운영현황.xlsx &amp; 에코마케팅_광고소재성과.xlsx
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── 데이터 로드 & 머지 ──────────────────────────────────────────────────────────
@st.cache_data
def load_and_merge(camp_bytes, cre_bytes):
    df_camp = pd.read_excel(camp_bytes)
    df_cre  = pd.read_excel(cre_bytes)
    merged = pd.merge(df_cre, df_camp, on="캠페인ID", suffixes=("_소재", "_캠페인"))
    return df_camp, df_cre, merged

df_camp, df_cre, df = load_and_merge(campaign_file, creative_file)

# ── 사이드바 필터 ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 필터")

    platforms = sorted(df_camp["플랫폼"].dropna().unique())
    sel_platform = st.multiselect("플랫폼", platforms, default=platforms)

    statuses = sorted(df_camp["상태"].dropna().unique())
    sel_status = st.multiselect("캠페인 상태", statuses, default=statuses)

    creative_types = sorted(df_cre["소재유형"].dropna().unique())
    sel_ctype = st.multiselect("소재 유형", creative_types, default=creative_types)

    ab_groups = sorted(df_cre["A/B그룹"].dropna().unique())
    sel_ab = st.multiselect("A/B 그룹", ab_groups, default=ab_groups)

# 필터 적용
df_filt = df[
    df["플랫폼"].isin(sel_platform) &
    df["상태"].isin(sel_status) &
    df["소재유형"].isin(sel_ctype) &
    df["A/B그룹"].isin(sel_ab)
]

if df_filt.empty:
    st.warning("필터 조건에 맞는 데이터가 없습니다.")
    st.stop()

# ── KPI 계산 ───────────────────────────────────────────────────────────────────
total_spend  = df_filt["집행금액(원)_소재"].sum()
total_imp    = df_filt["노출수_소재"].sum()
total_click  = df_filt["클릭수_소재"].sum()
total_conv   = df_filt["전환수_소재"].sum()
avg_roas     = df_filt.drop_duplicates("캠페인ID")["ROAS"].mean()
avg_ctr      = df_filt["CTR(%)"].mean()
avg_cvr      = df_filt["CVR(%)"].mean()
n_campaigns  = df_filt["캠페인ID"].nunique()
budget_total = df_filt.drop_duplicates("캠페인ID")["총예산(원)"].sum()
exec_rate    = (
    df_filt.drop_duplicates("캠페인ID")["집행금액(원)_캠페인"].sum() / budget_total * 100
) if budget_total else 0

# ── KPI 카드 (3 + 3) ───────────────────────────────────────────────────────────
kpi_row1 = st.columns(3)
kpi_defs1 = [
    (kpi_row1[0], "💰", "총 집행금액",  f"₩{total_spend:,.0f}",  f"캠페인 {n_campaigns}개 합산", ACCENT),
    (kpi_row1[1], "👁️", "총 노출수",    f"{total_imp:,}",         "소재 기준 합산",               C_GREEN),
    (kpi_row1[2], "🖱️", "총 클릭수",    f"{total_click:,}",       f"평균 CTR {avg_ctr:.2f}%",    C_AMBER),
]
for col, icon, label, value, sub, color in kpi_defs1:
    with col:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color:{color};">
            <span class="kpi-icon">{icon}</span>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

kpi_row2 = st.columns(3)
kpi_defs2 = [
    (kpi_row2[0], "🎯", "총 전환수",   f"{total_conv:,}",       f"평균 CVR {avg_cvr:.2f}%",    C_RED),
    (kpi_row2[1], "📈", "평균 ROAS",   f"{avg_roas:.2f}x",      "캠페인 단위 평균",             C_PURPLE),
    (kpi_row2[2], "💳", "예산 집행률", f"{exec_rate:.1f}%",     f"총예산 ₩{budget_total:,.0f}", C_CYAN),
]
for col, icon, label, value, sub, color in kpi_defs2:
    with col:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color:{color};">
            <span class="kpi-icon">{icon}</span>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 차트 행 1: 플랫폼별 집행금액 | 캠페인 상태 분포 ────────────────────────────
ch1, ch2 = st.columns(2)

with ch1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📡 플랫폼별 집행금액</div>', unsafe_allow_html=True)
    plat_data = (
        df_filt.drop_duplicates("캠페인ID")
        .groupby("플랫폼")["집행금액(원)_캠페인"]
        .sum()
        .reset_index()
        .sort_values("집행금액(원)_캠페인", ascending=False)
    )
    bar_plat = (
        alt.Chart(plat_data)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X("플랫폼:N", sort="-y", axis=alt.Axis(labelAngle=-30), title=None),
            y=alt.Y("집행금액(원)_캠페인:Q", axis=alt.Axis(title="집행금액 (원)", format=",")),
            color=alt.Color("플랫폼:N", legend=None, scale=alt.Scale(scheme="tableau10")),
            tooltip=[
                alt.Tooltip("플랫폼:N", title="플랫폼"),
                alt.Tooltip("집행금액(원)_캠페인:Q", title="집행금액", format=","),
            ],
        )
    )
    st.altair_chart(dark_chart(bar_plat), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with ch2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔵 캠페인 상태 분포</div>', unsafe_allow_html=True)
    status_data = (
        df_filt.drop_duplicates("캠페인ID")["상태"]
        .value_counts()
        .reset_index()
        .rename(columns={"상태": "상태", "count": "캠페인수"})
    )
    pie = (
        alt.Chart(status_data)
        .mark_arc(innerRadius=50, outerRadius=110)
        .encode(
            theta=alt.Theta("캠페인수:Q"),
            color=alt.Color("상태:N",
                            scale=alt.Scale(scheme="tableau10"),
                            legend=alt.Legend(orient="right", labelFontSize=12)),
            tooltip=[
                alt.Tooltip("상태:N", title="상태"),
                alt.Tooltip("캠페인수:Q", title="캠페인수"),
            ],
        )
    )
    st.altair_chart(dark_chart(pie), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── 차트 행 2: 소재유형별 CTR/CVR | A/B 그룹 성과 ───────────────────────────────
ch3, ch4 = st.columns(2)

with ch3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎨 소재유형별 평균 CTR / CVR</div>', unsafe_allow_html=True)
    ctype_data = (
        df_filt.groupby("소재유형")[["CTR(%)", "CVR(%)"]]
        .mean()
        .reset_index()
        .melt(id_vars="소재유형", var_name="지표", value_name="값")
    )
    bar_ctype = (
        alt.Chart(ctype_data)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
        .encode(
            x=alt.X("소재유형:N", axis=alt.Axis(labelAngle=-20), title=None),
            y=alt.Y("값:Q", axis=alt.Axis(title="비율 (%)")),
            color=alt.Color("지표:N",
                            scale=alt.Scale(domain=["CTR(%)", "CVR(%)"],
                                            range=[ACCENT, C_GREEN]),
                            legend=alt.Legend(orient="top-right")),
            xOffset="지표:N",
            tooltip=[
                alt.Tooltip("소재유형:N", title="소재유형"),
                alt.Tooltip("지표:N", title="지표"),
                alt.Tooltip("값:Q", title="값 (%)", format=".2f"),
            ],
        )
    )
    st.altair_chart(dark_chart(bar_ctype), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with ch4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧪 A/B 그룹별 성과 비교</div>', unsafe_allow_html=True)
    ab_data = (
        df_filt.groupby("A/B그룹")
        .agg(
            평균CTR=("CTR(%)", "mean"),
            평균CVR=("CVR(%)", "mean"),
            총전환수=("전환수_소재", "sum"),
            평균CPA=("CPA(원)", "mean"),
        )
        .reset_index()
    )
    ab_melt = ab_data.melt(
        id_vars="A/B그룹",
        value_vars=["평균CTR", "평균CVR"],
        var_name="지표", value_name="값"
    )
    bar_ab = (
        alt.Chart(ab_melt)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, size=40)
        .encode(
            x=alt.X("A/B그룹:N", axis=alt.Axis(labelFontSize=13), title=None),
            y=alt.Y("값:Q", axis=alt.Axis(title="비율 (%)")),
            color=alt.Color("지표:N",
                            scale=alt.Scale(domain=["평균CTR", "평균CVR"],
                                            range=[C_AMBER, C_RED]),
                            legend=alt.Legend(orient="top-right")),
            xOffset="지표:N",
            tooltip=[
                alt.Tooltip("A/B그룹:N", title="그룹"),
                alt.Tooltip("지표:N", title="지표"),
                alt.Tooltip("값:Q", title="값 (%)", format=".2f"),
            ],
        )
    )
    st.altair_chart(dark_chart(bar_ab), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── 캠페인 상세 테이블 ─────────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📋 캠페인별 통합 현황</div>', unsafe_allow_html=True)
camp_summary = (
    df_filt.drop_duplicates("캠페인ID")[[
        "캠페인ID", "고객사", "캠페인명", "플랫폼", "광고유형",
        "캠페인목표", "상태", "총예산(원)", "집행금액(원)_캠페인",
        "ROAS", "담당자"
    ]]
    .sort_values("집행금액(원)_캠페인", ascending=False)
    .reset_index(drop=True)
)
camp_summary["예산집행률(%)"] = (
    camp_summary["집행금액(원)_캠페인"] / camp_summary["총예산(원)"] * 100
).round(1)

st.dataframe(
    camp_summary,
    use_container_width=True,
    hide_index=True,
    column_config={
        "캠페인ID":            st.column_config.TextColumn("캠페인ID"),
        "고객사":              st.column_config.TextColumn("고객사"),
        "캠페인명":            st.column_config.TextColumn("캠페인명", width="large"),
        "플랫폼":              st.column_config.TextColumn("플랫폼"),
        "광고유형":            st.column_config.TextColumn("광고유형"),
        "캠페인목표":          st.column_config.TextColumn("캠페인목표"),
        "상태":                st.column_config.TextColumn("상태"),
        "총예산(원)":          st.column_config.NumberColumn("총예산 (원)", format="₩%d"),
        "집행금액(원)_캠페인": st.column_config.NumberColumn("집행금액 (원)", format="₩%d"),
        "ROAS":                st.column_config.NumberColumn("ROAS", format="%.2fx"),
        "예산집행률(%)":       st.column_config.ProgressColumn("집행률", min_value=0, max_value=100, format="%.1f%%"),
        "담당자":              st.column_config.TextColumn("담당자"),
    },
)
st.markdown('</div>', unsafe_allow_html=True)

# ── 소재 성과 테이블 ───────────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🖼️ 광고소재 성과 상세</div>', unsafe_allow_html=True)
creative_table = (
    df_filt[[
        "소재ID", "소재명", "소재유형", "컨셉", "A/B그룹",
        "캠페인명", "플랫폼", "고객사",
        "노출수_소재", "클릭수_소재", "전환수_소재",
        "집행금액(원)_소재", "CTR(%)", "CVR(%)", "CPC(원)", "CPA(원)", "검수상태"
    ]]
    .sort_values("집행금액(원)_소재", ascending=False)
    .reset_index(drop=True)
)
st.dataframe(
    creative_table,
    use_container_width=True,
    hide_index=True,
    column_config={
        "소재ID":            st.column_config.TextColumn("소재ID"),
        "소재명":            st.column_config.TextColumn("소재명", width="large"),
        "소재유형":          st.column_config.TextColumn("소재유형"),
        "컨셉":              st.column_config.TextColumn("컨셉"),
        "A/B그룹":           st.column_config.TextColumn("A/B"),
        "캠페인명":          st.column_config.TextColumn("캠페인명", width="large"),
        "플랫폼":            st.column_config.TextColumn("플랫폼"),
        "고객사":            st.column_config.TextColumn("고객사"),
        "노출수_소재":       st.column_config.NumberColumn("노출수", format="%d"),
        "클릭수_소재":       st.column_config.NumberColumn("클릭수", format="%d"),
        "전환수_소재":       st.column_config.NumberColumn("전환수", format="%d"),
        "집행금액(원)_소재": st.column_config.NumberColumn("집행금액 (원)", format="₩%d"),
        "CTR(%)":            st.column_config.NumberColumn("CTR (%)", format="%.2f%%"),
        "CVR(%)":            st.column_config.NumberColumn("CVR (%)", format="%.2f%%"),
        "CPC(원)":           st.column_config.NumberColumn("CPC (원)", format="₩%d"),
        "CPA(원)":           st.column_config.NumberColumn("CPA (원)", format="₩%d"),
        "검수상태":          st.column_config.TextColumn("검수상태"),
    },
)
st.markdown('</div>', unsafe_allow_html=True)

# ── 통합 데이터 다운로드 ───────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">⬇️ 통합 데이터 내보내기</div>', unsafe_allow_html=True)
dl_col, info_col = st.columns([1, 3])
with dl_col:
    csv = df_filt.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="📥  CSV 다운로드",
        data=csv,
        file_name="에코마케팅_통합분석.csv",
        mime="text/csv",
        use_container_width=True,
    )
with info_col:
    st.markdown(
        f"<p style='color:{MUTED} !important; font-size:0.85rem; margin-top:0.6rem;'>"
        f"현재 필터 기준 <b style='color:{ACCENT};'>{len(df_filt)}개 소재</b> · "
        f"<b style='color:{ACCENT};'>{n_campaigns}개 캠페인</b> 데이터가 포함됩니다.</p>",
        unsafe_allow_html=True,
    )
st.markdown('</div>', unsafe_allow_html=True)
