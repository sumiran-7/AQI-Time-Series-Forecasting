import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.live_aqi import get_current_conditions, get_hourly_forecast


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Delhi Air Intelligence",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
    <style>
    /* ---------- APP ---------- */
    .stApp {
        background:
            radial-gradient(circle at 90% 0%, rgba(20,184,166,.10), transparent 25%),
            radial-gradient(circle at 0% 100%, rgba(14,165,233,.08), transparent 25%),
            #07111f;
    }

    [data-testid="stHeader"] {
        background: rgba(7,17,31,0);
    }

    [data-testid="stAppViewContainer"] {
        background: transparent;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ---------- TEXT ---------- */
    h1, h2, h3, p, label {
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .brand {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: #f8fafc;
        margin-bottom: .25rem;
    }

    .brand span {
        color: #2dd4bf;
    }

    .subtitle {
        color: #8fa5b8;
        font-size: .92rem;
        margin-bottom: 1.5rem;
    }

    .live-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 7px 13px;
        border-radius: 999px;
        color: #5eead4;
        background: rgba(20,184,166,.10);
        border: 1px solid rgba(45,212,191,.25);
        font-size: .72rem;
        font-weight: 800;
        letter-spacing: .08em;
    }

    .live-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #34d399;
        box-shadow: 0 0 12px #34d399;
    }

    /* ---------- HERO ---------- */
    .hero {
        border: 1px solid rgba(148,163,184,.13);
        border-radius: 24px;
        padding: 28px 30px;
        margin: .5rem 0 1.2rem 0;
        background: linear-gradient(135deg, rgba(15,35,52,.96), rgba(8,28,42,.94));
        box-shadow: 0 20px 60px rgba(0,0,0,.20);
    }

    .hero-kicker {
        color: #6ee7d1;
        font-size: .70rem;
        font-weight: 800;
        letter-spacing: .15em;
        text-transform: uppercase;
    }

    .hero-title {
        color: #f8fafc;
        font-size: 2.5rem;
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -.045em;
        margin: 8px 0;
    }

    .hero-copy {
        color: #94aabd;
        font-size: .92rem;
        max-width: 760px;
        line-height: 1.6;
    }

    /* ---------- METRICS ---------- */
    div[data-testid="stMetric"] {
        background: rgba(15,31,47,.88);
        border: 1px solid rgba(148,163,184,.12);
        border-radius: 18px;
        padding: 18px 20px;
        min-height: 118px;
        box-shadow: 0 10px 30px rgba(0,0,0,.13);
    }

    div[data-testid="stMetricLabel"] {
        color: #8298aa !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }

    /* ---------- SECTION ---------- */
    .section-title {
        color: #edf5fa;
        font-size: 1.15rem;
        font-weight: 800;
        margin-top: 1.8rem;
        margin-bottom: .15rem;
    }

    .section-subtitle {
        color: #71879a;
        font-size: .78rem;
        margin-bottom: .7rem;
    }

    /* ---------- INFO ---------- */
    .info-box {
        background: rgba(15,31,47,.78);
        border: 1px solid rgba(148,163,184,.10);
        border-radius: 18px;
        padding: 20px;
    }

    .info-title {
        color: #dce9f2;
        font-size: .92rem;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .pollutant {
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #8fa5b8;
        font-size: .80rem;
        padding: 10px 0;
        border-bottom: 1px solid rgba(148,163,184,.07);
    }

    .pollutant:last-child {
        border-bottom: 0;
    }

    .pollutant strong {
        color: #edf5fa;
    }

    .model-box {
        background: linear-gradient(135deg, rgba(12,42,52,.92), rgba(11,29,43,.92));
        border: 1px solid rgba(45,212,191,.15);
        border-radius: 20px;
        padding: 24px;
        margin-top: 1.4rem;
    }

    .badge {
        display: inline-block;
        padding: 5px 9px;
        border-radius: 7px;
        color: #5eead4;
        background: rgba(45,212,191,.10);
        font-size: .68rem;
        font-weight: 800;
        letter-spacing: .1em;
    }

    .model-title {
        color: #f8fafc;
        font-size: 1.3rem;
        font-weight: 800;
        margin-top: 10px;
    }

    .model-copy {
        color: #8fa5b8;
        font-size: .82rem;
        line-height: 1.65;
    }

    .notice {
        background: rgba(15,31,47,.60);
        border: 1px solid rgba(148,163,184,.08);
        border-radius: 14px;
        padding: 15px 18px;
        color: #8298aa;
        font-size: .78rem;
        line-height: 1.6;
        margin-top: 1rem;
    }

    /* ---------- BUTTON ---------- */
    .stButton > button {
        border-radius: 10px;
        border: 1px solid rgba(45,212,191,.28);
        background: rgba(20,184,166,.08);
        color: #99f6e4;
        font-weight: 700;
    }

    .stButton > button:hover {
        border-color: rgba(45,212,191,.55);
        color: #ccfbf1;
    }

    /* ---------- FOOTER ---------- */
    .footer {
        text-align: center;
        color: #60788b;
        font-size: .70rem;
        padding-top: 2rem;
        margin-top: 2.5rem;
        border-top: 1px solid rgba(148,163,184,.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA
# ============================================================

@st.cache_data(ttl=300, show_spinner=False)
def load_current():
    return get_current_conditions()


@st.cache_data(ttl=300, show_spinner=False)
def load_forecast():
    return get_hourly_forecast()


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns([5, 1])

with header_left:
    st.markdown(
        '<div class="brand">🌫️ DELHI <span>AIR INTELLIGENCE</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="subtitle">Real-time air quality monitoring · '
        'Time-series forecasting · Machine Learning</div>',
        unsafe_allow_html=True,
    )

with header_right:
    st.markdown(
        '<div style="text-align:right;margin-top:8px">'
        '<span class="live-pill"><span class="live-dot"></span> LIVE DATA</span>'
        '</div>',
        unsafe_allow_html=True,
    )

refresh_col, _ = st.columns([1, 5])
with refresh_col:
    if st.button("↻ Refresh data", width="stretch"):
        load_current.clear()
        load_forecast.clear()
        st.rerun()


# ============================================================
# FETCH DATA
# ============================================================

try:
    current = load_current()
    forecast = load_forecast()
except Exception as e:
    st.error(f"Unable to fetch live AQI data: {e}")
    st.info("Check your internet connection and try Refresh data again.")
    st.stop()


required_current = ["aqi", "pm2_5", "pm10", "no2", "co", "o3", "timestamp"]
missing = [x for x in required_current if x not in current]

if missing:
    st.error(f"Live API response is missing: {', '.join(missing)}")
    st.stop()

aqi = float(current["aqi"])
pm25 = float(current["pm2_5"])
pm10 = float(current["pm10"])
no2 = float(current["no2"])
co = float(current["co"])
o3 = float(current["o3"])
timestamp = str(current["timestamp"])


def aqi_category(value):
    if value <= 50:
        return "Good"
    if value <= 100:
        return "Moderate"
    if value <= 150:
        return "Unhealthy for Sensitive Groups"
    if value <= 200:
        return "Unhealthy"
    if value <= 300:
        return "Very Unhealthy"
    return "Hazardous"


category = aqi_category(aqi)


# ============================================================
# HERO
# ============================================================

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-kicker">DELHI · CURRENT AIR QUALITY</div>
        <div class="hero-title">Air quality at a glance.</div>
        <div class="hero-copy">
            Live atmospheric observations combined with a predictive
            time-series forecasting pipeline.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Current AQI", f"{aqi:.0f}")
    st.markdown(
        f'<div class="metric-caption">{category}</div>',
        unsafe_allow_html=True,
    )

with c2:
    st.metric("PM2.5", f"{pm25:.1f}")
    st.markdown(
        '<div class="metric-caption">μg/m³</div>',
        unsafe_allow_html=True,
    )

with c3:
    st.metric("PM10", f"{pm10:.1f}")
    st.markdown(
        '<div class="metric-caption">μg/m³</div>',
        unsafe_allow_html=True,
    )

with c4:
    try:
        formatted_date = pd.Timestamp(timestamp).strftime("%d %b %Y")
        formatted_time = pd.Timestamp(timestamp).strftime("%H:%M")
    except Exception:
        formatted_date = timestamp[:10]
        formatted_time = timestamp[11:16] if len(timestamp) >= 16 else timestamp

    st.metric("Last Updated", formatted_time)
    st.markdown(
        f'<div class="metric-caption">{formatted_date} · IST</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# FORECAST CHART
# ============================================================

st.markdown(
    '<div class="section-title">📈 48-Hour Air Quality Forecast</div>'
    '<div class="section-subtitle">Live API forecast · Hourly AQI outlook</div>',
    unsafe_allow_html=True,
)

try:
    forecast_df = forecast.copy()
    forecast_df["datetime"] = pd.to_datetime(forecast_df["datetime"])
    forecast_df["aqi"] = pd.to_numeric(forecast_df["aqi"], errors="coerce")
    forecast_df = forecast_df.dropna(subset=["datetime", "aqi"])

    current_time = pd.to_datetime(timestamp)
    future_df = forecast_df[forecast_df["datetime"] >= current_time].head(48)

    if future_df.empty:
        future_df = forecast_df.head(48)

except Exception as e:
    st.error(f"Could not prepare forecast chart: {e}")
    future_df = pd.DataFrame()


if not future_df.empty:
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=future_df["datetime"],
            y=future_df["aqi"],
            mode="lines+markers",
            name="AQI",
            line=dict(color="#2dd4bf", width=3),
            marker=dict(size=5, color="#5eead4"),
            fill="tozeroy",
            fillcolor="rgba(45,212,191,.06)",
            hovertemplate="<b>%{x|%d %b %H:%M}</b><br>AQI: %{y:.0f}<extra></extra>",
        )
    )

    fig.add_hline(
        y=150,
        line_dash="dot",
        line_color="#f59e0b",
        annotation_text="Unhealthy threshold",
        annotation_position="top left",
    )

    fig.update_layout(
        height=390,
        margin=dict(l=10, r=10, t=25, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8fa5b8"),
        xaxis=dict(
            showgrid=False,
            title="",
            tickformat="%d %b\n%H:%M",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(148,163,184,.08)",
            title="AQI",
            zeroline=False,
        ),
        hovermode="x unified",
        showlegend=False,
    )

    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


# ============================================================
# POLLUTANTS + OUTLOOK
# ============================================================

left, right = st.columns([1.05, 1])


with left:
    st.markdown(
        '<div class="info-box"><div class="info-title">🧪 Pollutant Profile</div>',
        unsafe_allow_html=True,
    )

    pollutant_values = [
        ("PM2.5", pm25, "µg/m³"),
        ("PM10", pm10, "µg/m³"),
        ("NO₂", no2, "µg/m³"),
        ("CO", co, "µg/m³"),
        ("O₃", o3, "µg/m³"),
    ]

    rows = ""
    for name, value, unit in pollutant_values:
        rows += (
            f'<div class="pollutant">'
            f'<span>{name}</span>'
            f'<strong>{value:.1f} {unit}</strong>'
            f'</div>'
        )

    st.markdown(rows + "</div>", unsafe_allow_html=True)


with right:
    st.markdown(
        '<div class="info-box"><div class="info-title">🔮 Next Few Hours</div>',
        unsafe_allow_html=True,
    )

    if not future_df.empty:
        outlook = future_df.head(5)

        for _, row in outlook.iterrows():
            dt = row["datetime"].strftime("%d %b · %H:%M")
            value = int(round(row["aqi"]))

            st.markdown(
                f"""
                <div class="pollutant">
                    <span>{dt}</span>
                    <strong>AQI {value}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="pollutant"><span>No forecast available</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# MODEL SECTION
# ============================================================

st.markdown(
    """
    <div class="model-box">
        <div class="badge">MACHINE LEARNING</div>
        <div class="model-title">LSTM Time-Series Forecasting</div>
        <div class="model-copy">
            The forecasting pipeline uses a 30-day lookback window to learn
            temporal dependencies from historical Delhi AQI observations.
            Live API observations are displayed separately from the trained
            forecasting model.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Model", "LSTM")

with m2:
    st.metric("Lookback", "30 Days")

with m3:
    st.metric("Test MAE", "34.73")

with m4:
    st.metric("Test RMSE", "46.74")


# ============================================================
# MODEL NOTE
# ============================================================

st.markdown(
    """
    <div class="notice">
        <b style="color:#cbd5e1;">Model context:</b>
        The LSTM was trained using historical Delhi AQI observations
        from 2015–2020. Live air-quality observations are obtained
        separately through the live air-quality API.
        <br><br>
        <b style="color:#cbd5e1;">AQI scale:</b>
        Live AQI values shown here use the US AQI scale returned by
        the live API.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        DELHI AIR INTELLIGENCE · Live Air Quality · LSTM Forecasting · Time-Series Analytics
    </div>
    """,
    unsafe_allow_html=True,
)