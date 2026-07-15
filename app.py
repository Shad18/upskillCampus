import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TrafficIQ · Urban Command",
    page_icon="🚦",
    layout="wide",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

.stApp {
    background-color: #080C14;
    background-image:
        linear-gradient(180deg, rgba(245,158,11,0.04) 0%, transparent 35%);
}

#MainMenu, footer { visibility: hidden; }

.block-container {
    padding: 1.5rem 2.5rem 4rem;
    max-width: 1400px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #0D1321 !important;
    border-right: 1px solid rgba(245,158,11,0.12);
}
[data-testid="stSidebar"] * { color: #94a3b8 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stDateInput label,
[data-testid="stSidebar"] .stTimeInput label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.15em !important;
    color: #f59e0b !important;
    text-transform: uppercase !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="input"] > div,
[data-testid="stSidebar"] input {
    background-color: #131a2a !important;
    border-color: rgba(245,158,11,0.2) !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}

/* ── Sidebar stat badges ── */
.sidebar-stat {
    background: #0a1020;
    border: 1px solid rgba(245,158,11,0.18);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin: 0.4rem 0;
}
.sidebar-stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    color: #64748b;
    text-transform: uppercase;
}
.sidebar-stat-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.25rem;
    font-weight: 700;
    color: #f59e0b;
    margin-top: 0.1rem;
}
.sidebar-stat-sub {
    font-size: 0.7rem;
    color: #475569;
    margin-top: 0.1rem;
}

/* ── Header ── */
.app-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid rgba(245,158,11,0.12);
    margin-bottom: 1.75rem;
}
.header-left {}
.header-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.25em;
    color: #f59e0b;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.header-title {
    font-size: 1.85rem;
    font-weight: 700;
    color: #f1f5f9;
    line-height: 1.1;
    margin: 0;
}
.header-title span { color: #f59e0b; }
.header-sub {
    font-size: 0.83rem;
    color: #475569;
    margin-top: 0.3rem;
}
.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 999px;
    padding: 0.3rem 0.85rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    color: #10b981;
    text-transform: uppercase;
}
.live-dot {
    width: 6px;
    height: 6px;
    background: #10b981;
    border-radius: 50%;
    animation: pulse 1.8s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── Predict button ── */
.stButton > button {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
    color: #0a0f1a !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    transition: opacity 0.15s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
}

/* ── KPI cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}
.kpi-card {
    background: #0d1421;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1.25rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #f59e0b, transparent);
}
.kpi-card.green::before { background: linear-gradient(90deg, #10b981, transparent); }
.kpi-card.yellow::before { background: linear-gradient(90deg, #eab308, transparent); }
.kpi-card.orange::before { background: linear-gradient(90deg, #f97316, transparent); }
.kpi-card.red::before { background: linear-gradient(90deg, #ef4444, transparent); }

.kpi-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.63rem;
    letter-spacing: 0.2em;
    color: #475569;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #f1f5f9;
    line-height: 1;
}
.kpi-sub {
    font-size: 0.72rem;
    color: #475569;
    margin-top: 0.35rem;
}

/* ── Section header ── */
.section-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    color: #f59e0b;
    text-transform: uppercase;
    margin: 2rem 0 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(245,158,11,0.15);
}

/* ── Risk bar ── */
.risk-wrap {
    background: #0d1421;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.risk-meta {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.75rem;
}
.risk-title {
    font-size: 0.8rem;
    color: #64748b;
}
.risk-pct {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.5rem;
    font-weight: 700;
    color: #f1f5f9;
}
.risk-track {
    background: rgba(255,255,255,0.06);
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
}
.risk-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.6s ease;
}

/* ── Two-col summary ── */
.summary-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 1rem;
}
.summary-card {
    background: #0d1421;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1.3rem 1.5rem;
}
.summary-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.45rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.summary-row:last-child { border-bottom: none; }
.summary-key {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.summary-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    font-weight: 600;
    color: #cbd5e1;
}

/* ── Alert banner ── */
.alert-banner {
    border-radius: 12px;
    padding: 1rem 1.4rem;
    display: flex;
    align-items: center;
    gap: 0.85rem;
    font-size: 0.88rem;
    font-weight: 600;
    margin-bottom: 1rem;
}
.alert-banner.red    { background: rgba(239,68,68,0.1);  border: 1px solid rgba(239,68,68,0.3);  color: #fca5a5; }
.alert-banner.orange { background: rgba(249,115,22,0.1); border: 1px solid rgba(249,115,22,0.3); color: #fdba74; }
.alert-banner.green  { background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3); color: #6ee7b7; }
.alert-icon { font-size: 1.2rem; }

/* ── Recommendation cards ── */
.rec-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 0.75rem;
    margin-top: 0.5rem;
}
.rec-card {
    background: #0d1421;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 1rem 1.1rem;
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
}
.rec-card.urgent { border-color: rgba(239,68,68,0.25); }
.rec-card.warn   { border-color: rgba(249,115,22,0.25); }
.rec-card.ok     { border-color: rgba(16,185,129,0.2); }
.rec-icon { font-size: 1.1rem; flex-shrink: 0; margin-top: 0.05rem; }
.rec-text { font-size: 0.8rem; color: #94a3b8; line-height: 1.4; }

/* ── Feature table ── */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.06) !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #0d1421 !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 14px !important;
}
[data-testid="stExpander"] summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.15em !important;
    color: #64748b !important;
    text-transform: uppercase !important;
}

/* ── Footer ── */
.app-footer {
    margin-top: 3rem;
    padding-top: 1.25rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.footer-left {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.15em;
    color: #1e293b;
    text-transform: uppercase;
}
.footer-right {
    font-size: 0.72rem;
    color: #1e293b;
}

/* ── Idle state ── */
.idle-state {
    background: #0d1421;
    border: 1px dashed rgba(245,158,11,0.2);
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    margin: 1.5rem 0;
}
.idle-icon { font-size: 3rem; margin-bottom: 1rem; opacity: 0.4; }
.idle-text {
    font-size: 0.88rem;
    color: #334155;
}
</style>
""", unsafe_allow_html=True)


# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    with open("models/traffic_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 1.25rem;">
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                    letter-spacing:0.22em;color:#f59e0b;text-transform:uppercase;
                    margin-bottom:0.2rem;">Traffic Command</div>
        <div style="font-size:1.1rem;font-weight:700;color:#f1f5f9;">Control Panel</div>
    </div>
    """, unsafe_allow_html=True)

    junction = st.selectbox("Junction", [1, 2, 3, 4],
                            format_func=lambda x: f"Junction {x} — Sector {x*10}")
    selected_date = st.date_input("Date")
    selected_time = st.time_input("Time")

    st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

    run = st.button("Run Forecast →")

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                letter-spacing:0.2em;color:#334155;text-transform:uppercase;
                margin-bottom:0.6rem;">Model Performance</div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-stat">
        <div class="sidebar-stat-label">R² Score</div>
        <div class="sidebar-stat-value">0.969</div>
        <div class="sidebar-stat-sub">Regression accuracy</div>
    </div>
    <div class="sidebar-stat">
        <div class="sidebar-stat-label">Mean Abs. Error</div>
        <div class="sidebar-stat-value">2.37</div>
        <div class="sidebar-stat-sub">vehicles per prediction</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.75rem;color:#1e293b;line-height:1.5;">
        Configure junction, date, and time above, then run a forecast to see predicted vehicle
        counts, congestion level, and management recommendations.
    </div>
    """, unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="header-left">
        <div class="header-eyebrow">Urban Mobility · AI Forecasting</div>
        <div class="header-title">Traffic<span>IQ</span></div>
        <div class="header-sub">Smart City Traffic Intelligence — Junction monitoring & congestion prediction</div>
    </div>
    <div class="live-badge">
        <span class="live-dot"></span>System Online
    </div>
</div>
""", unsafe_allow_html=True)


# ── Feature engineering (always runs) ─────────────────────────────────────────
dt         = datetime.combine(selected_date, selected_time)
year       = dt.year
month      = dt.month
day        = dt.day
hour       = dt.hour
dayofweek  = dt.weekday()
is_weekend = 1 if dayofweek >= 5 else 0
weekofyear = dt.isocalendar().week
quarter    = ((month - 1) // 3) + 1
season     = {frozenset([12,1,2]): 0, frozenset([3,4,5]): 1,
              frozenset([6,7,8,9]): 2}.get(
              next((s for s in [frozenset([12,1,2]), frozenset([3,4,5]),
                                 frozenset([6,7,8,9])] if month in s), None), 3)
rushhour   = 1 if (8 <= hour <= 10) or (17 <= hour <= 20) else 0
holiday_dates = pd.to_datetime([
    "2015-01-26","2015-08-15","2015-10-02",
    "2016-01-26","2016-08-15","2016-10-02",
    "2017-01-26","2017-08-15"
])
is_holiday = int(pd.Timestamp(selected_date).normalize() in holiday_dates)


# ── Prediction ────────────────────────────────────────────────────────────────
if run:
    features = [[junction, year, month, day, hour, dayofweek,
                  is_weekend, is_holiday, weekofyear, quarter, season, rushhour]]
    prediction = model.predict(features)[0]
    risk_score = min(prediction / 50 * 100, 100)

    if prediction <= 10:
        level, level_color, top_color = "LOW",  "green",  "#10b981"
    elif prediction <= 20:
        level, level_color, top_color = "MEDIUM", "yellow", "#eab308"
    elif prediction <= 40:
        level, level_color, top_color = "HIGH",  "orange", "#f97316"
    else:
        level, level_color, top_color = "PEAK",  "red",    "#ef4444"

    day_names  = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    season_map = {0:"Winter", 1:"Spring", 2:"Summer", 3:"Autumn"}
    period     = "Rush Hour" if rushhour else ("Weekend" if is_weekend else "Off-peak")

    # ── KPI row ──────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Live Forecast</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "Predicted Vehicles", f"{prediction:.0f}", "vehicles at this junction", level_color),
        (c2, "Traffic Level",  level,    f"Threshold: {'10' if level=='LOW' else '20' if level=='MEDIUM' else '40'} veh", level_color),
        (c3, "Congestion Risk", f"{risk_score:.0f}%",  f"{'Critical' if risk_score>80 else 'Elevated' if risk_score>50 else 'Normal'} risk window", level_color),
        (c4, "Time Context",   period,   f"{day_names[dayofweek]} · {hour:02d}:00", ""),
    ]
    for col, label, value, sub, cls in cards:
        with col:
            st.markdown(f"""
            <div class="kpi-card {cls}">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Risk bar ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Congestion Risk Score</div>', unsafe_allow_html=True)
    bar_color = {"green":"#10b981","yellow":"#eab308","orange":"#f97316","red":"#ef4444"}[level_color]
    st.markdown(f"""
    <div class="risk-wrap">
        <div class="risk-meta">
            <span class="risk-title">Congestion risk index — Junction {junction}</span>
            <span class="risk-pct">{risk_score:.1f}%</span>
        </div>
        <div class="risk-track">
            <div class="risk-fill" style="width:{risk_score:.1f}%;
                 background:linear-gradient(90deg,{bar_color}aa,{bar_color});"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Summary ───────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Forecast Summary</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="summary-grid">
        <div class="summary-card">
            <div class="summary-row">
                <span class="summary-key">Junction</span>
                <span class="summary-val">Junction {junction}</span>
            </div>
            <div class="summary-row">
                <span class="summary-key">Date</span>
                <span class="summary-val">{selected_date.strftime('%d %b %Y')}</span>
            </div>
            <div class="summary-row">
                <span class="summary-key">Time</span>
                <span class="summary-val">{selected_time.strftime('%H:%M')}</span>
            </div>
            <div class="summary-row">
                <span class="summary-key">Season</span>
                <span class="summary-val">{season_map[season]}</span>
            </div>
            <div class="summary-row">
                <span class="summary-key">Holiday</span>
                <span class="summary-val">{'Yes' if is_holiday else 'No'}</span>
            </div>
        </div>
        <div class="summary-card">
            <div class="summary-row">
                <span class="summary-key">Predicted Vehicles</span>
                <span class="summary-val">{prediction:.0f}</span>
            </div>
            <div class="summary-row">
                <span class="summary-key">Traffic Level</span>
                <span class="summary-val" style="color:{bar_color}">{level}</span>
            </div>
            <div class="summary-row">
                <span class="summary-key">Risk Score</span>
                <span class="summary-val">{risk_score:.1f}%</span>
            </div>
            <div class="summary-row">
                <span class="summary-key">Rush Hour</span>
                <span class="summary-val">{'Active' if rushhour else 'Inactive'}</span>
            </div>
            <div class="summary-row">
                <span class="summary-key">Day Type</span>
                <span class="summary-val">{'Weekend' if is_weekend else 'Weekday'}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Alert ─────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">System Alert</div>', unsafe_allow_html=True)
    if prediction > 40:
        st.markdown('<div class="alert-banner red"><span class="alert-icon">🔴</span>Peak traffic expected — immediate action required at this junction.</div>', unsafe_allow_html=True)
    elif prediction > 20:
        st.markdown('<div class="alert-banner orange"><span class="alert-icon">🟠</span>High traffic expected — monitor conditions and prepare diversions.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-banner green"><span class="alert-icon">🟢</span>Normal traffic conditions — no intervention required.</div>', unsafe_allow_html=True)

    # ── Recommendations ───────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Management Recommendations</div>', unsafe_allow_html=True)
    if prediction > 40:
        recs = [
            ("🚔","urgent","Deploy traffic police to junction"),
            ("⏱","urgent","Extend signal green-phase duration"),
            ("🔀","urgent","Activate pre-planned alternate routes"),
            ("📢","urgent","Issue public congestion alert"),
        ]
    elif prediction > 20:
        recs = [
            ("📡","warn","Monitor traffic flow in real time"),
            ("🗺","warn","Prepare diversion plans for activation"),
            ("⚙️","warn","Optimise signal timing adaptively"),
        ]
    else:
        recs = [
            ("✅","ok","Normal operation — no action needed"),
            ("📊","ok","Continue passive monitoring"),
            ("📋","ok","Log data for baseline analysis"),
        ]
    rec_html = '<div class="rec-grid">'
    for icon, cls, text in recs:
        rec_html += f'<div class="rec-card {cls}"><div class="rec-icon">{icon}</div><div class="rec-text">{text}</div></div>'
    rec_html += '</div>'
    st.markdown(rec_html, unsafe_allow_html=True)

    # ── Feature viewer ────────────────────────────────────────────────────────
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    with st.expander("View Engineered Features"):
        feature_df = pd.DataFrame({
            "Feature": ["Junction","Year","Month","Day","Hour","DayOfWeek",
                        "IsWeekend","IsHoliday","WeekOfYear","Quarter","Season","RushHour"],
            "Value":   [junction, year, month, day, hour, dayofweek,
                        is_weekend, is_holiday, int(weekofyear), quarter, season, rushhour],
            "Description": [
                f"Junction {junction}","Calendar year","Calendar month","Day of month",
                f"{hour:02d}:00",day_names[dayofweek],
                "Weekend" if is_weekend else "Weekday",
                "Public holiday" if is_holiday else "Regular day",
                f"Week {int(weekofyear)} of year",f"Q{quarter}",
                season_map[season],"Active" if rushhour else "Inactive",
            ]
        })
        st.dataframe(feature_df, use_container_width=True, hide_index=True)

else:
    # ── Idle state ────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="idle-state">
        <div class="idle-icon">🚦</div>
        <div class="idle-text">
            Configure the junction, date, and time in the control panel,<br>
            then click <strong style="color:#f59e0b">Run Forecast</strong> to generate a prediction.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    <div class="footer-left">TrafficIQ &nbsp;·&nbsp; Smart City Traffic Intelligence</div>
    <div class="footer-right">YOLOv8 · Scikit-Learn · Streamlit · Python</div>
</div>
""", unsafe_allow_html=True)