import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="JakU – Pantau Udara, Jaga Jakarta",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* Reset & base */
html, body, [class*="css"], .stApp {
    font-family: 'Poppins', sans-serif !important;
    background-color: #F8FAFC !important;
}

/* Hide default Streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E2E8F0;
    min-width: 220px !important;
    max-width: 220px !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
section[data-testid="stSidebar"] .stRadio > label { display: none; }
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    display: flex; flex-direction: column; gap: 4px;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    display: flex !important; align-items: center;
    padding: 10px 18px; border-radius: 10px;
    font-size: 14px; font-weight: 500; color: #64748B;
    cursor: pointer; transition: all 0.15s;
    margin: 0 12px; white-space: nowrap;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: #F1F5F9; color: #1E3A5F;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"],
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] input:checked + div {
    background: #EFF6FF; color: #2563EB; font-weight: 600;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span { display: none; }

/* Main content area */
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Cards */
.card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07), 0 4px 16px rgba(0,0,0,0.04);
    border: 1px solid #F1F5F9;
    margin-bottom: 16px;
}
.card-sm {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 2px 8px rgba(0,0,0,0.04);
    border: 1px solid #F1F5F9;
}

/* ISPU number */
.ispu-number { font-size: 64px; font-weight: 700; line-height: 1; }
.ispu-label { font-size: 13px; font-weight: 500; color: #94A3B8; margin-top: 4px; }

/* Status badges */
.badge {
    display: inline-block; padding: 4px 14px;
    border-radius: 999px; font-size: 13px; font-weight: 600;
}
.badge-baik    { background:#DCFCE7; color:#16A34A; }
.badge-sedang  { background:#DBEAFE; color:#2563EB; }
.badge-tidak   { background:#FEF9C3; color:#CA8A04; }
.badge-sangat  { background:#FEE2E2; color:#DC2626; }
.badge-berbahaya { background:#F3E8FF; color:#7C3AED; }

/* Status text colors */
.text-baik     { color: #22C55E; font-weight: 600; font-size: 22px; }
.text-sedang   { color: #2563EB; font-weight: 600; font-size: 22px; }
.text-tidak    { color: #F97316; font-weight: 600; font-size: 22px; }
.text-sangat   { color: #EF4444; font-weight: 600; font-size: 22px; }
.text-berbahaya{ color: #7C3AED; font-weight: 600; font-size: 22px; }

/* Section title */
.section-title {
    font-size: 16px; font-weight: 600; color: #1E293B; margin-bottom: 4px;
}
.section-sub {
    font-size: 13px; color: #94A3B8; margin-bottom: 16px;
}

/* Header bar */
.page-header {
    background: #FFFFFF;
    border-bottom: 1px solid #E2E8F0;
    padding: 18px 32px;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 24px;
}

/* Info note */
.info-note {
    background: #EFF6FF;
    border-left: 3px solid #2563EB;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px; color: #1E40AF;
}

/* Recommendation card */
.rec-card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    text-align: center;
    border: 1px solid #F1F5F9;
}
.rec-icon { font-size: 28px; margin-bottom: 8px; }
.rec-title { font-size: 13px; font-weight: 600; color: #334155; margin-bottom: 4px; }
.rec-status-aman    { color: #22C55E; font-weight: 700; font-size: 14px; }
.rec-status-disaran { color: #F97316; font-weight: 700; font-size: 14px; }
.rec-status-waspada { color: #FACC15; font-weight: 700; font-size: 14px; }
.rec-desc { font-size: 11px; color: #94A3B8; margin-top: 4px; }

/* Polutan bar */
.pol-bar-bg {
    background: #F1F5F9; border-radius: 4px; height: 4px; margin-top: 6px;
}
.pol-bar-fill {
    border-radius: 4px; height: 4px;
}

/* Tab style overrides */
.stTabs [data-baseweb="tab-list"] {
    gap: 0; background: #F1F5F9; border-radius: 10px;
    padding: 3px; border: none;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px; font-size: 13px; font-weight: 500;
    color: #64748B; background: transparent; border: none; padding: 8px 18px;
}
.stTabs [aria-selected="true"] {
    background: #FFFFFF !important; color: #2563EB !important;
    font-weight: 600; box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
.stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }

/* Metric overrides */
[data-testid="stMetric"] {
    background: #FFFFFF; border-radius: 12px; padding: 16px 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    border: 1px solid #F1F5F9;
}
[data-testid="stMetricLabel"] { font-size: 12px !important; color: #94A3B8 !important; }
[data-testid="stMetricValue"] { font-size: 28px !important; font-weight: 700 !important; color: #1E293B !important; }

/* Selectbox */
.stSelectbox > label { font-size: 13px; font-weight: 500; color: #64748B; }
[data-testid="stSelectbox"] > div > div {
    border-radius: 10px !important; border-color: #E2E8F0 !important;
    font-size: 13px !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Data Simulasi ────────────────────────────────────────────────────────────
DATE_LABELS = ["20 Mei", "21 Mei", "22 Mei", "23 Mei", "24 Mei", "25 Mei", "26 Mei"]
ISPU_TREND   = [62, 58, 45, 48, 54, 60, 78]

WILAYAH_DATA = {
    "Jakarta Pusat": {
        "ispu": 71, "status": "Sedang", "status_class": "text-sedang",
        "pm25": 24, "pm10": 41, "no2": 18, "so2": 7, "co": 0.6, "o3": 50,
        "trend": [65, 60, 46, 49, 55, 63, 71],
        "pred": {"besok": 78, "3hari": 85, "5hari": 92},
        "pred_status": {"besok": "Sedang", "3hari": "Sedang", "5hari": "Tidak Sehat"},
    },
    "Jakarta Utara": {
        "ispu": 65, "status": "Sedang", "status_class": "text-sedang",
        "pm25": 20, "pm10": 37, "no2": 15, "so2": 5, "co": 0.5, "o3": 45,
        "trend": [60, 56, 42, 44, 50, 57, 65],
        "pred": {"besok": 70, "3hari": 75, "5hari": 80},
        "pred_status": {"besok": "Sedang", "3hari": "Sedang", "5hari": "Sedang"},
    },
    "Jakarta Barat": {
        "ispu": 102, "status": "Tidak Sehat", "status_class": "text-tidak",
        "pm25": 35, "pm10": 60, "no2": 25, "so2": 10, "co": 0.9, "o3": 65,
        "trend": [80, 76, 68, 72, 85, 95, 102],
        "pred": {"besok": 105, "3hari": 112, "5hari": 98},
        "pred_status": {"besok": "Tidak Sehat", "3hari": "Tidak Sehat", "5hari": "Sedang"},
    },
    "Jakarta Selatan": {
        "ispu": 75, "status": "Sedang", "status_class": "text-sedang",
        "pm25": 26, "pm10": 44, "no2": 20, "so2": 8, "co": 0.7, "o3": 52,
        "trend": [68, 64, 50, 53, 60, 68, 75],
        "pred": {"besok": 80, "3hari": 88, "5hari": 95},
        "pred_status": {"besok": "Sedang", "3hari": "Sedang", "5hari": "Sedang"},
    },
    "Jakarta Timur": {
        "ispu": 68, "status": "Sedang", "status_class": "text-sedang",
        "pm25": 22, "pm10": 39, "no2": 16, "so2": 6, "co": 0.5, "o3": 47,
        "trend": [62, 58, 44, 47, 53, 60, 68],
        "pred": {"besok": 73, "3hari": 80, "5hari": 85},
        "pred_status": {"besok": "Sedang", "3hari": "Sedang", "5hari": "Sedang"},
    },
    "Kep. Seribu": {
        "ispu": 38, "status": "Baik", "status_class": "text-baik",
        "pm25": 10, "pm10": 18, "no2": 8, "so2": 3, "co": 0.2, "o3": 28,
        "trend": [40, 37, 32, 33, 36, 38, 38],
        "pred": {"besok": 40, "3hari": 42, "5hari": 38},
        "pred_status": {"besok": "Baik", "3hari": "Baik", "5hari": "Baik"},
    },
}

PRED_7HARI = {
    "dates":  ["27 Mei\nSel", "28 Mei\nRab", "29 Mei\nKam", "30 Mei\nJum",
               "31 Mei\nSab", "1 Jun\nMin", "2 Jun\nSen"],
    "values": [82, 85, 92, 108, 115, 98, 88],
    "lower":  [72, 75, 80, 95, 100, 85, 76],
    "upper":  [92, 95, 104, 121, 130, 111, 100],
    "status": ["Sedang","Sedang","Sedang","Tidak Sehat","Tidak Sehat","Sedang","Sedang"],
}

HOURLY_ISPU = [62,55,40,32,28,25,30,38,52,65,72,78,82,85,90,95,105,118,130,125,115,105,90,75]
HOURLY_PM25 = [20,18,14,11,9,8,10,13,17,21,23,25,27,28,29,30,34,38,42,40,37,34,29,24]

# ─── Helper: Plotly theme ──────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Poppins, sans-serif", size=12, color="#334155"),
    margin=dict(l=0, r=0, t=10, b=0),
    xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=11)),
    yaxis=dict(showgrid=True, gridcolor="#F1F5F9", zeroline=False, tickfont=dict(size=11)),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    hovermode="x unified",
)

def status_color(s):
    return {"Baik":"#22C55E","Sedang":"#2563EB","Tidak Sehat":"#F97316",
            "Sangat Tidak Sehat":"#EF4444","Berbahaya":"#7C3AED"}.get(s,"#94A3B8")

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:24px 20px 20px; border-bottom:1px solid #F1F5F9;">
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:36px;height:36px;background:linear-gradient(135deg,#2563EB,#22C55E);
                        border-radius:10px;display:flex;align-items:center;justify-content:center;
                        font-size:18px;">🌿</div>
            <div>
                <div style="font-size:22px;font-weight:700;color:#1E293B;line-height:1;">JakU</div>
                <div style="font-size:10px;color:#94A3B8;font-weight:400;">Pantau Udara, Jaga Jakarta</div>
            </div>
        </div>
    </div>
    <div style="padding:16px 8px 8px;">
        <div style="font-size:10px;font-weight:600;color:#CBD5E1;letter-spacing:0.08em;
                    padding:0 10px;margin-bottom:8px;">MENU</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "nav",
        ["🏠  Dashboard", "📍  Detail Wilayah", "📈  Prediksi & Analisis", "📚  Edukasi & Insight"],
        label_visibility="collapsed",
    )

    st.markdown("""
    <div style="position:absolute;bottom:0;left:0;right:0;padding:20px;
                border-top:1px solid #F1F5F9;background:#FAFBFC;">
        <div style="font-size:11px;font-weight:600;color:#2563EB;margin-bottom:6px;">
            ℹ️ Data tidak realtime
        </div>
        <div style="font-size:10.5px;color:#94A3B8;line-height:1.5;">
            Data yang ditampilkan berdasarkan sampel ISPU 2024 dan diperbarui secara berkala.
        </div>
        <div style="margin-top:12px;font-size:10px;color:#CBD5E1;">
            Terakhir diperbarui<br>
            <span style="color:#64748B;font-weight:500;">26 Mei 2025, 10:00 WIB</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── TOP HEADER ──────────────────────────────────────────────────────────────
def render_header(title, subtitle):
    page_name = page.split("  ")[1] if "  " in page else page
    is_dashboard = "Dashboard" in page_name
    st.markdown(f"""
    <div style="background:#FFFFFF;border-bottom:1px solid #E2E8F0;
                padding:18px 32px;display:flex;align-items:center;justify-content:space-between;
                margin-bottom:24px;">
        <div>
            <div style="font-size:22px;font-weight:700;color:#1E293B;">{title}</div>
            <div style="font-size:13px;color:#94A3B8;margin-top:2px;">{subtitle}</div>
        </div>
        <div style="display:flex;align-items:center;gap:16px;">
            <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;
                        padding:8px 16px;font-size:12px;color:#64748B;line-height:1.4;">
                <span style="color:#94A3B8;">📅 Data terakhir diperbarui</span><br>
                <strong style="color:#1E293B;">26 Mei 2025, 10:00 WIB</strong>
            </div>
            <div style="width:36px;height:36px;background:#F8FAFC;border:1px solid #E2E8F0;
                        border-radius:10px;display:flex;align-items:center;justify-content:center;
                        font-size:18px;cursor:pointer;">🔔</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── HALAMAN 1: DASHBOARD ─────────────────────────────────────────────────────
def page_dashboard():
    render_header("Halo, Selamat Pagi! 👋", "Berikut ringkasan kualitas udara di Provinsi DKI Jakarta.")

    pad = "padding: 0 32px;"
    st.markdown(f'<div style="{pad}">', unsafe_allow_html=True)

    # ── Row 1: Air Quality Card + Map Card ──────────────────────────────────
    c1, c2 = st.columns([1, 1], gap="large")

    with c1:
        st.markdown("""
        <div class="card" style="min-height:200px;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                    <div class="section-title">Kualitas Udara Jakarta (Rata-rata) ℹ️</div>
                    <div style="display:flex;align-items:flex-end;gap:16px;margin-top:16px;">
                        <div class="ispu-number" style="color:#2563EB;">78</div>
                        <div>
                            <div class="text-sedang" style="font-size:26px;">Sedang</div>
                            <div style="font-size:12px;color:#64748B;max-width:200px;margin-top:4px;">
                                Udara masih dapat diterima untuk beraktivitas di luar ruangan.
                            </div>
                        </div>
                    </div>
                    <div class="ispu-label" style="margin-top:12px;">ISPU</div>
                    <div style="margin-top:12px;">
                        <span style="font-size:13px;color:#22C55E;">🍃</span>
                        <span style="font-size:13px;color:#64748B;font-weight:500;"> Polutan dominan: <strong>PM2.5</strong></span>
                    </div>
                </div>
                <div style="font-size:80px;opacity:0.15;user-select:none;">🏙️</div>
            </div>
            <div style="margin-top:20px;text-align:right;">
                <span style="font-size:13px;color:#2563EB;font-weight:500;cursor:pointer;">
                    Lihat Selengkapnya →
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card" style="min-height:200px;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px;">
                <div class="section-title">Kualitas Udara per Wilayah ℹ️</div>
            </div>
        """, unsafe_allow_html=True)

        # Simple map using Plotly scatter
        map_data = {
            "Wilayah":   ["Jakarta Pusat","Jakarta Utara","Jakarta Barat","Jakarta Selatan","Jakarta Timur","Kep. Seribu"],
            "lat":       [-6.1924, -6.1565, -6.1881, -6.3296, -6.2864, -5.7400],
            "lon":       [106.8232, 106.9056, 106.7567, 106.8226, 106.9061, 106.5700],
            "ISPU":      [71, 65, 102, 75, 68, 38],
            "Status":    ["Sedang","Sedang","Tidak Sehat","Sedang","Sedang","Baik"],
            "Color":     ["#2563EB","#2563EB","#F97316","#2563EB","#2563EB","#22C55E"],
        }
        df_map = pd.DataFrame(map_data)

        fig_map = go.Figure()
        for _, row in df_map.iterrows():
            fig_map.add_trace(go.Scattermapbox(
                lat=[row["lat"]], lon=[row["lon"]],
                mode="markers+text",
                marker=dict(size=38, color=row["Color"], opacity=0.9),
                text=[str(row["ISPU"])],
                textfont=dict(color="white", size=13, family="Poppins"),
                textposition="middle center",
                hovertemplate=f"<b>{row['Wilayah']}</b><br>ISPU: {row['ISPU']}<br>Status: {row['Status']}<extra></extra>",
                name=row["Wilayah"],
                showlegend=False,
            ))

        fig_map.update_layout(
            mapbox=dict(
                style="carto-positron",
                center=dict(lat=-6.22, lon=106.82),
                zoom=9.0,
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=180,
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar": False})

        st.markdown("""
            <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:8px;">
                <span style="font-size:11px;display:flex;align-items:center;gap:4px;">
                    <span style="width:10px;height:10px;border-radius:50%;background:#22C55E;display:inline-block;"></span> Baik (0–50)
                </span>
                <span style="font-size:11px;display:flex;align-items:center;gap:4px;">
                    <span style="width:10px;height:10px;border-radius:50%;background:#2563EB;display:inline-block;"></span> Sedang (51–100)
                </span>
                <span style="font-size:11px;display:flex;align-items:center;gap:4px;">
                    <span style="width:10px;height:10px;border-radius:50%;background:#F97316;display:inline-block;"></span> Tidak Sehat (101–200)
                </span>
            </div>
            <div style="margin-top:12px;text-align:right;">
                <span style="font-size:13px;color:#2563EB;font-weight:500;cursor:pointer;">Lihat Peta Detail →</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Row 2: Trend chart + Prediction card ───────────────────────────────
    c3, c4 = st.columns([1, 1], gap="large")

    with c3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Tren ISPU Jakarta (7 Hari Terakhir)</div>', unsafe_allow_html=True)

        fig_trend = go.Figure()
        fig_trend.add_hrect(y0=0, y1=50, fillcolor="#DCFCE7", opacity=0.3, line_width=0)
        fig_trend.add_hrect(y0=50, y1=100, fillcolor="#DBEAFE", opacity=0.25, line_width=0)
        fig_trend.add_hrect(y0=100, y1=150, fillcolor="#FEF9C3", opacity=0.3, line_width=0)

        fig_trend.add_trace(go.Scatter(
            x=DATE_LABELS, y=ISPU_TREND,
            mode="lines+markers",
            line=dict(color="#2563EB", width=2.5),
            marker=dict(size=7, color="#2563EB", line=dict(color="white", width=2)),
            fill="tozeroy", fillcolor="rgba(37,99,235,0.07)",
            hovertemplate="%{x}: ISPU <b>%{y}</b><extra></extra>",
        ))

        # Last point callout
        fig_trend.add_annotation(
            x=DATE_LABELS[-1], y=ISPU_TREND[-1],
            text=f"<b>{ISPU_TREND[-1]}</b>",
            showarrow=False,
            bgcolor="#2563EB", font=dict(color="white", size=12),
            borderpad=4, borderradius=6, yshift=20,
        )

        # Threshold labels
        for label, y, color in [("Sangat Tidak Sehat","150","#EF4444"),
                                  ("Tidak Sehat","100","#F97316"),
                                  ("Sedang","50","#2563EB"),
                                  ("Baik","0","#22C55E")]:
            fig_trend.add_annotation(x=DATE_LABELS[-1], y=int(y),
                text=label, showarrow=False, xanchor="left",
                font=dict(size=10, color=color), xshift=8)
            fig_trend.add_shape(type="line", x0=DATE_LABELS[0], x1=DATE_LABELS[-1],
                y0=int(y), y1=int(y),
                line=dict(color=color, width=1, dash="dot"))

        fig_trend.update_layout(**{**PLOT_LAYOUT, "height": 220,
            "yaxis": dict(range=[0, 170], showgrid=False, zeroline=False)})
        st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("""
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <div class="section-title">Prediksi ISPU Jakarta ℹ️</div>
        </div>
        """, unsafe_allow_html=True)

        tab_pred1, tab_pred2 = st.tabs(["Besok", "3 Hari ke Depan"])

        with tab_pred1:
            fig_pred1 = go.Figure()
            pred_h = [70, 74, 78, 80, 82, 80, 78, 76]
            hours_p = ["Pagi","","","Siang","","Sore","","Malam"]
            fig_pred1.add_trace(go.Scatter(
                x=hours_p, y=pred_h,
                mode="lines+markers",
                line=dict(color="#2563EB", width=2.5),
                marker=dict(size=7, color="#2563EB"),
                fill="tozeroy", fillcolor="rgba(37,99,235,0.08)",
                hovertemplate="%{x}: ISPU <b>%{y}</b><extra></extra>",
            ))
            fig_pred1.update_layout(**{**PLOT_LAYOUT, "height": 140,
                "yaxis": dict(range=[50, 110], showgrid=True, gridcolor="#F1F5F9", zeroline=False)})
            col_pv, col_pc = st.columns([1, 1.8])
            with col_pv:
                st.markdown("""
                <div style="padding-top:8px;">
                    <div style="font-size:42px;font-weight:700;color:#2563EB;line-height:1;">82</div>
                    <div class="text-sedang" style="font-size:16px;">Sedang</div>
                    <div style="font-size:11px;color:#94A3B8;margin-top:4px;">27 Mei 2025</div>
                </div>
                """, unsafe_allow_html=True)
            with col_pc:
                st.plotly_chart(fig_pred1, use_container_width=True, config={"displayModeBar": False})

        with tab_pred2:
            pred_3d = [82, 85, 92]
            dates_3d = ["27 Mei", "28 Mei", "29 Mei"]
            fig_pred3 = go.Figure()
            fig_pred3.add_trace(go.Scatter(
                x=dates_3d, y=pred_3d,
                mode="lines+markers",
                line=dict(color="#2563EB", width=2.5),
                marker=dict(size=8, color="#2563EB"),
                fill="tozeroy", fillcolor="rgba(37,99,235,0.08)",
            ))
            fig_pred3.update_layout(**{**PLOT_LAYOUT, "height": 140,
                "yaxis": dict(range=[60, 110], showgrid=True, gridcolor="#F1F5F9", zeroline=False)})
            col_pv2, col_pc2 = st.columns([1, 1.8])
            with col_pv2:
                st.markdown("""
                <div style="padding-top:8px;">
                    <div style="font-size:42px;font-weight:700;color:#2563EB;line-height:1;">85</div>
                    <div class="text-sedang" style="font-size:16px;">Sedang</div>
                    <div style="font-size:11px;color:#94A3B8;margin-top:4px;">Rata-rata 3 hari</div>
                </div>
                """, unsafe_allow_html=True)
            with col_pc2:
                st.plotly_chart(fig_pred3, use_container_width=True, config={"displayModeBar": False})

        st.markdown("""
        <div class="info-note" style="margin-top:8px;">
            💡 Prediksi dibuat menggunakan model machine learning XGBoost berdasarkan data historis ISPU.
        </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Row 3: Rekomendasi Aktivitas ──────────────────────────────────────
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Rekomendasi Aktivitas</div>', unsafe_allow_html=True)

    recs = [
        ("🏃", "Olahraga Luar Ruangan", "Aman", "rec-status-aman",
         "Aktivitas luar ruangan aman dilakukan."),
        ("😷", "Gunakan Masker", "Disarankan", "rec-status-disaran",
         "Gunakan masker jika Anda sensitif terhadap polusi."),
        ("👴", "Kelompok Sensitif", "Waspada", "rec-status-waspada",
         "Jaga kesehatan dan hindari area dengan polusi tinggi."),
        ("🏡", "Buka Jendela", "Aman", "rec-status-aman",
         "Sirkulasi udara di dalam ruangan masih aman."),
    ]
    cols_rec = st.columns(4)
    for col, (icon, title, status, cls, desc) in zip(cols_rec, recs):
        with col:
            st.markdown(f"""
            <div class="rec-card">
                <div class="rec-icon">{icon}</div>
                <div class="rec-title">{title}</div>
                <div class="{cls}">{status}</div>
                <div class="rec-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ─── HALAMAN 2: DETAIL WILAYAH ────────────────────────────────────────────────
def page_detail():
    render_header("Detail Wilayah", "Pilih wilayah untuk melihat informasi kualitas udara lebih detail.")

    pad = "padding: 0 32px;"
    st.markdown(f'<div style="{pad}">', unsafe_allow_html=True)

    wilayah_list = list(WILAYAH_DATA.keys())
    tabs = st.tabs(wilayah_list)

    for tab, wilayah in zip(tabs, wilayah_list):
        with tab:
            d = WILAYAH_DATA[wilayah]

            # ── Card Kualitas Udara ──────────────────────────────────────
            c1, c2 = st.columns([1, 1], gap="large")

            with c1:
                st.markdown(f"""
                <div class="card">
                    <div class="section-title">Kualitas Udara {wilayah} ℹ️</div>
                    <div style="display:flex;align-items:flex-end;gap:14px;margin-top:16px;">
                        <div class="ispu-number" style="color:#2563EB;">{d['ispu']}</div>
                        <div>
                            <div class="{d['status_class']}" style="font-size:24px;">{d['status']}</div>
                            <div style="font-size:12px;color:#64748B;max-width:200px;margin-top:4px;">
                                Udara masih dapat diterima untuk beraktivitas di luar ruangan.
                            </div>
                        </div>
                    </div>
                    <div class="ispu-label">ISPU</div>
                    <div style="margin-top:10px;font-size:13px;color:#64748B;">
                        🍃 Polutan dominan: <strong>PM2.5 ({d['pm25']} µg/m³)</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Komposisi Polutan ℹ️</div>', unsafe_allow_html=True)

                pol_data = [
                    ("PM2.5",  d['pm25'], "µg/m³", "#2563EB", 50),
                    ("PM10",   d['pm10'],  "µg/m³", "#2563EB", 80),
                    ("NO₂",    d['no2'],   "µg/m³", "#22C55E", 40),
                    ("SO₂",    d['so2'],   "µg/m³", "#22C55E", 20),
                    ("CO",     d['co'],    "mg/m³", "#22C55E", 2),
                    ("O₃",     d['o3'],    "µg/m³", "#22C55E", 80),
                ]
                pcols = st.columns(6)
                for pc, (name, val, unit, color, maxval) in zip(pcols, pol_data):
                    pct = min(int(val / maxval * 100), 100)
                    with pc:
                        st.markdown(f"""
                        <div style="text-align:center;">
                            <div style="font-size:11px;font-weight:600;color:#94A3B8;">{name}</div>
                            <div style="font-size:18px;font-weight:700;color:#1E293B;margin:4px 0;">{val}</div>
                            <div style="font-size:10px;color:#CBD5E1;">{unit}</div>
                            <div class="pol-bar-bg">
                                <div class="pol-bar-fill" style="width:{pct}%;background:{color};"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown("""
                <div style="margin-top:12px;text-align:right;">
                    <span style="font-size:12px;color:#2563EB;cursor:pointer;">Lihat penjelasan parameter ∨</span>
                </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            # ── Charts Row ──────────────────────────────────────────────
            c3, c4 = st.columns([1, 1], gap="large")

            with c3:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f'<div class="section-title">Tren ISPU {wilayah} (7 Hari Terakhir)</div>', unsafe_allow_html=True)

                fig_t = go.Figure()
                fig_t.add_hrect(y0=50, y1=100, fillcolor="#DBEAFE", opacity=0.2, line_width=0)
                fig_t.add_trace(go.Scatter(
                    x=DATE_LABELS, y=d["trend"],
                    mode="lines+markers",
                    line=dict(color="#2563EB", width=2.5),
                    marker=dict(size=7, color="#2563EB", line=dict(color="white", width=2)),
                    fill="tozeroy", fillcolor="rgba(37,99,235,0.06)",
                    hovertemplate="%{x}: ISPU <b>%{y}</b><extra></extra>",
                ))
                fig_t.add_annotation(
                    x=DATE_LABELS[-1], y=d["trend"][-1],
                    text=f"<b>{d['trend'][-1]}</b>",
                    showarrow=False, bgcolor="#2563EB",
                    font=dict(color="white", size=11), borderpad=4, yshift=20,
                )
                for label, y, color in [("Sangat Tidak Sehat",150,"#EF4444"),
                                          ("Tidak Sehat",100,"#F97316"),
                                          ("Sedang",50,"#2563EB"),("Baik",0,"#22C55E")]:
                    fig_t.add_shape(type="line", x0=DATE_LABELS[0], x1=DATE_LABELS[-1],
                        y0=y, y1=y, line=dict(color=color, width=1, dash="dot"))
                    fig_t.add_annotation(x=DATE_LABELS[-1], y=y, text=label,
                        showarrow=False, xanchor="left", font=dict(size=10, color=color), xshift=8)

                fig_t.update_layout(**{**PLOT_LAYOUT, "height": 220,
                    "yaxis": dict(range=[0, 170], showgrid=False, zeroline=False)})
                st.plotly_chart(fig_t, use_container_width=True, config={"displayModeBar": False})
                st.markdown("</div>", unsafe_allow_html=True)

            with c4:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Pola Harian (Rata-rata) ℹ️</div>', unsafe_allow_html=True)
                hours = [f"{h:02d}:00" for h in range(0, 25, 1)]

                fig_h = go.Figure()
                # Color gradient effect: morning=green, afternoon=orange, evening=red
                colors_h = (["#22C55E"]*8 + ["#FACC15"]*4 + ["#F97316"]*4 +
                             ["#EF4444"]*4 + ["#F97316"]*4 + ["#22C55E"])[:24]
                fig_h.add_trace(go.Scatter(
                    x=[f"{i:02d}:00" for i in range(24)],
                    y=HOURLY_ISPU,
                    mode="lines+markers",
                    line=dict(color="#2563EB", width=2.5),
                    marker=dict(size=5, color="#2563EB"),
                    fill="tozeroy", fillcolor="rgba(37,99,235,0.07)",
                    hovertemplate="%{x}: ISPU <b>%{y}</b><extra></extra>",
                ))
                fig_h.add_annotation(x="19:00", y=130,
                    text="<b>Puncak Polusi<br>17:00 – 20:00</b>",
                    showarrow=True, arrowhead=2, arrowcolor="#EF4444",
                    bgcolor="white", bordercolor="#EF4444", borderpad=6,
                    font=dict(size=11, color="#EF4444"))
                fig_h.update_layout(**{**PLOT_LAYOUT, "height": 220,
                    "xaxis": dict(tickvals=["00:00","04:00","08:00","12:00","16:00","20:00","24:00"],
                                  tickfont=dict(size=10)),
                    "yaxis": dict(range=[0, 160], showgrid=True, gridcolor="#F1F5F9", zeroline=False)})
                st.plotly_chart(fig_h, use_container_width=True, config={"displayModeBar": False})
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

            # ── Prediksi + Rekomendasi ──────────────────────────────────
            c5, c6 = st.columns([1, 1], gap="large")

            with c5:
                st.markdown(f'<div class="card"><div class="section-title">Prediksi ISPU {wilayah} ℹ️</div>', unsafe_allow_html=True)
                pc1, pc2, pc3 = st.columns(3)
                pred_cards = [
                    ("Besok\n27 Mei 2025", d['pred']['besok'], d['pred_status']['besok']),
                    ("3 Hari ke Depan\n28 Mei 2025", d['pred']['3hari'], d['pred_status']['3hari']),
                    ("5 Hari ke Depan\n30 Mei 2025", d['pred']['5hari'], d['pred_status']['5hari']),
                ]
                for col, (lbl, val, stat) in zip([pc1, pc2, pc3], pred_cards):
                    sc = ("text-sedang" if stat == "Sedang"
                          else "text-tidak" if stat == "Tidak Sehat"
                          else "text-baik")
                    icon = "☀️" if stat == "Baik" else "🌤️" if stat == "Sedang" else "🌫️"
                    with col:
                        st.markdown(f"""
                        <div class="card-sm" style="text-align:center;">
                            <div style="font-size:11px;font-weight:600;color:#64748B;white-space:pre-line;">{lbl}</div>
                            <div style="font-size:26px;margin:6px 0;">{icon}</div>
                            <div style="font-size:24px;font-weight:700;color:#2563EB;">{val}</div>
                            <div class="{sc}" style="font-size:13px;">{stat}</div>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown("""
                <div class="info-note" style="margin-top:12px;">
                    💡 Prediksi ini dibuat menggunakan model machine learning berdasarkan data historis ISPU.
                </div></div>
                """, unsafe_allow_html=True)

            with c6:
                st.markdown('<div class="card"><div class="section-title">Rekomendasi untuk Wilayah Ini ℹ️</div>', unsafe_allow_html=True)
                recs_w = [
                    ("😷", "Gunakan Masker", "Disarankan menggunakan masker saat beraktivitas di luar ruangan."),
                    ("🏃", "Batasi Aktivitas Berat", "Kurangi aktivitas fisik intens di luar ruangan terutama sore hari."),
                    ("🪟", "Ventilasi Udara", "Buka jendela di pagi hari saat kualitas udara masih baik."),
                ]
                rcols = st.columns(3)
                for rc, (icon, title, desc) in zip(rcols, recs_w):
                    with rc:
                        st.markdown(f"""
                        <div style="text-align:center;">
                            <div style="font-size:28px;margin-bottom:8px;">{icon}</div>
                            <div style="font-size:12px;font-weight:600;color:#334155;">{title}</div>
                            <div style="font-size:11px;color:#94A3B8;margin-top:4px;">{desc}</div>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ─── HALAMAN 3: PREDIKSI & ANALISIS ─────────────────────────────────────────
def page_prediksi():
    render_header("Prediksi & Analisis",
                  "Analisis data historis dan prediksi kualitas udara di DKI Jakarta.")

    pad = "padding: 0 32px;"
    st.markdown(f'<div style="{pad}">', unsafe_allow_html=True)

    col_tab, col_sel = st.columns([3, 1])
    with col_sel:
        wilayah_sel = st.selectbox("Pilih Wilayah", ["DKI Jakarta (Rata-rata)"] + list(WILAYAH_DATA.keys()),
                                   label_visibility="collapsed")

    tab_pred, tab_pola = st.tabs(["Prediksi ISPU", "Analisis Pola"])

    with tab_pred:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # ── Prediction chart + side panel ──────────────────────────────
        c1, c2 = st.columns([2.5, 1], gap="large")

        with c1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Prediksi ISPU DKI Jakarta ℹ️</div>', unsafe_allow_html=True)

            sub_tab1, sub_tab2, sub_tab3 = st.tabs(["1 Hari ke Depan", "3 Hari ke Depan", "7 Hari ke Depan"])
            d_pred = PRED_7HARI

            for sub_tab, n_days in [(sub_tab1, 1), (sub_tab2, 3), (sub_tab3, 7)]:
                with sub_tab:
                    dates_s  = d_pred["dates"][:n_days]
                    values_s = d_pred["values"][:n_days]
                    lower_s  = d_pred["lower"][:n_days]
                    upper_s  = d_pred["upper"][:n_days]
                    status_s = d_pred["status"][:n_days]

                    if n_days == 1:
                        # Hourly prediction
                        hrs = ["Pagi","09:00","12:00","Siang","15:00","Sore","19:00","Malam"]
                        vals_1 = [70, 74, 78, 82, 88, 94, 82, 76]
                        fig_p1 = go.Figure()
                        fig_p1.add_trace(go.Scatter(
                            x=hrs, y=[v-8 for v in vals_1], mode="lines", showlegend=False,
                            line=dict(width=0), fillcolor="rgba(37,99,235,0.12)",
                        ))
                        fig_p1.add_trace(go.Scatter(
                            x=hrs, y=[v+8 for v in vals_1],
                            fill="tonexty", mode="lines", showlegend=True,
                            name="Rentang Kepercayaan (80%)",
                            line=dict(width=0), fillcolor="rgba(37,99,235,0.12)",
                        ))
                        fig_p1.add_trace(go.Scatter(
                            x=hrs, y=vals_1, mode="lines+markers",
                            name="Prediksi ISPU",
                            line=dict(color="#2563EB", width=2.5),
                            marker=dict(size=8, color="#2563EB"),
                        ))
                        fig_p1.update_layout(**{**PLOT_LAYOUT, "height": 260,
                            "legend": dict(orientation="h", y=1.12, x=0),
                            "yaxis": dict(range=[40, 130], showgrid=True, gridcolor="#F1F5F9", zeroline=False)})
                        st.plotly_chart(fig_p1, use_container_width=True, config={"displayModeBar": False})
                    else:
                        fig_pn = go.Figure()
                        fig_pn.add_trace(go.Scatter(
                            x=dates_s, y=lower_s, mode="lines", showlegend=False,
                            line=dict(width=0), fillcolor="rgba(37,99,235,0.10)",
                        ))
                        fig_pn.add_trace(go.Scatter(
                            x=dates_s, y=upper_s,
                            fill="tonexty", mode="lines", showlegend=True,
                            name="Rentang Kepercayaan (80%)",
                            line=dict(width=0), fillcolor="rgba(37,99,235,0.10)",
                        ))
                        fig_pn.add_trace(go.Scatter(
                            x=dates_s, y=values_s, mode="lines+markers",
                            name="Prediksi ISPU",
                            line=dict(color="#2563EB", width=2.5),
                            marker=dict(size=10, color="#2563EB", line=dict(color="white", width=2)),
                        ))
                        for x_v, y_v, stat_v in zip(dates_s, values_s, status_s):
                            col_ann = "#F97316" if stat_v == "Tidak Sehat" else "#2563EB"
                            fig_pn.add_annotation(x=x_v, y=y_v,
                                text=f"<b>{y_v}</b><br><span style='font-size:10px'>{stat_v}</span>",
                                showarrow=False, yshift=28, bgcolor=col_ann,
                                font=dict(color="white", size=11), borderpad=4)

                        fig_pn.add_shape(type="line", x0=0, x1=len(dates_s)-1,
                            y0=100, y1=100, line=dict(color="#F97316", width=1.5, dash="dot"),
                            xref="x", yref="y")
                        fig_pn.update_layout(**{**PLOT_LAYOUT, "height": 260,
                            "legend": dict(orientation="h", y=1.12, x=0),
                            "yaxis": dict(range=[40, 170], showgrid=True, gridcolor="#F1F5F9", zeroline=False)})
                        st.plotly_chart(fig_pn, use_container_width=True, config={"displayModeBar": False})

            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown("""
            <div class="card" style="text-align:center;">
                <div style="font-size:13px;color:#94A3B8;font-weight:500;">30 Mei 2025</div>
                <div style="font-size:68px;font-weight:700;color:#F97316;line-height:1;margin:8px 0;">108</div>
                <div style="font-size:22px;font-weight:700;color:#F97316;margin-bottom:12px;">Tidak Sehat</div>
                <div style="font-size:34px;margin:8px 0;">⛅</div>
                <div style="font-size:12px;color:#64748B;line-height:1.6;text-align:left;margin-top:12px;">
                    Kualitas udara diprediksi memburuk pada 30–31 Mei.
                    Disarankan untuk mengurangi aktivitas di luar ruangan.
                </div>
                <div style="margin-top:16px;padding-top:16px;border-top:1px solid #F1F5F9;text-align:left;">
                    <div style="font-size:12px;color:#64748B;margin-bottom:4px;">
                        <span style="color:#94A3B8;">Model:</span> <strong>XGBoost</strong>
                    </div>
                    <div style="font-size:12px;color:#64748B;">
                        <span style="color:#94A3B8;">Akurasi:</span> <strong>97.71%</strong>
                    </div>
                    <div style="font-size:12px;color:#64748B;margin-top:4px;">
                        <span style="color:#94A3B8;">RMSE:</span> <strong>12.45</strong>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        # ── Bottom Row: Pola Harian + Polutan + Korelasi ──────────────
        c3, c4, c5 = st.columns([1.1, 1, 1], gap="large")

        with c3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("""
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div class="section-title">Pola Harian (DKI Jakarta) ℹ️</div>
            </div>
            """, unsafe_allow_html=True)
            sub_ispu, sub_pm = st.tabs(["ISPU", "PM2.5"])

            with sub_ispu:
                fig_hr = go.Figure()
                fig_hr.add_trace(go.Scatter(
                    x=[f"{i:02d}:00" for i in range(24)], y=HOURLY_ISPU,
                    mode="lines+markers",
                    line=dict(color="#2563EB", width=2),
                    marker=dict(size=5, color="#2563EB"),
                    fill="tozeroy", fillcolor="rgba(37,99,235,0.07)",
                    hovertemplate="%{x}: <b>%{y}</b><extra></extra>",
                ))
                fig_hr.add_annotation(x="19:00", y=130, text="<b>Puncak Polusi<br>17:00–20:00</b>",
                    showarrow=True, arrowhead=2, arrowcolor="#EF4444", bgcolor="white",
                    bordercolor="#EF4444", borderpad=5, font=dict(size=10, color="#EF4444"))
                fig_hr.update_layout(**{**PLOT_LAYOUT, "height": 180,
                    "xaxis": dict(tickvals=["00:00","04:00","08:00","12:00","16:00","20:00"],
                                  tickfont=dict(size=9)),
                    "yaxis": dict(range=[0, 160], showgrid=True, gridcolor="#F1F5F9", zeroline=False)})
                st.plotly_chart(fig_hr, use_container_width=True, config={"displayModeBar": False})
            with sub_pm:
                fig_pm = go.Figure()
                fig_pm.add_trace(go.Scatter(
                    x=[f"{i:02d}:00" for i in range(24)], y=HOURLY_PM25,
                    mode="lines+markers",
                    line=dict(color="#22C55E", width=2),
                    marker=dict(size=5, color="#22C55E"),
                    fill="tozeroy", fillcolor="rgba(34,197,94,0.07)",
                ))
                fig_pm.update_layout(**{**PLOT_LAYOUT, "height": 180,
                    "xaxis": dict(tickvals=["00:00","04:00","08:00","12:00","16:00","20:00"],
                                  tickfont=dict(size=9)),
                    "yaxis": dict(range=[0, 55], showgrid=True, gridcolor="#F1F5F9", zeroline=False)})
                st.plotly_chart(fig_pm, use_container_width=True, config={"displayModeBar": False})

            st.markdown("""
            <div class="info-note" style="margin-top:6px;font-size:11px;">
                ℹ️ Polusi cenderung meningkat pada sore hingga malam hari.
            </div></div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown('<div class="card"><div class="section-title">Polutan Paling Berpengaruh ℹ️</div>', unsafe_allow_html=True)
            labels_pol = ["PM2.5","PM10","NO₂","O₃","SO₂","CO"]
            values_pol = [62, 18, 8, 6, 4, 2]
            colors_pol = ["#2563EB","#22C55E","#FACC15","#A78BFA","#F97316","#94A3B8"]

            fig_donut = go.Figure(go.Pie(
                labels=labels_pol, values=values_pol,
                hole=0.6, marker=dict(colors=colors_pol, line=dict(color="white", width=2)),
                textinfo="none",
                hovertemplate="<b>%{label}</b>: %{value}%<extra></extra>",
            ))
            fig_donut.add_annotation(text="<b>PM2.5</b><br><b>62%</b>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=13, color="#1E293B"), align="center")
            fig_donut.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=10, b=0), height=180,
                showlegend=True,
                legend=dict(orientation="v", yanchor="middle", y=0.5,
                            xanchor="right", x=1.3, font=dict(size=11)),
            )
            st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})
            st.markdown("""
            <div style="font-size:12px;color:#64748B;margin-top:4px;">
                PM2.5 adalah polutan yang paling berkontribusi terhadap ISPU di Jakarta.
            </div></div>
            """, unsafe_allow_html=True)

        with c5:
            st.markdown('<div class="card"><div class="section-title">Korelasi Parameter terhadap ISPU ℹ️</div>', unsafe_allow_html=True)
            params_cor = ["PM2.5","PM10","NO₂","O₃","SO₂","CO"]
            corr_vals  = [0.87, 0.68, 0.45, -0.28, 0.31, 0.22]
            colors_cor = ["#2563EB" if v > 0 else "#EF4444" for v in corr_vals]

            fig_corr = go.Figure(go.Bar(
                x=corr_vals, y=params_cor, orientation="h",
                marker_color=colors_cor,
                hovertemplate="<b>%{y}</b>: %{x}<extra></extra>",
            ))
            fig_corr.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=10, b=20), height=200,
                xaxis=dict(range=[-1, 1], showgrid=True, gridcolor="#F1F5F9",
                           tickvals=[-1, 0, 1], zeroline=True, zerolinecolor="#E2E8F0",
                           tickfont=dict(size=10)),
                yaxis=dict(showgrid=False, tickfont=dict(size=11)),
                font=dict(family="Poppins, sans-serif", size=11),
            )
            st.plotly_chart(fig_corr, use_container_width=True, config={"displayModeBar": False})
            st.markdown("""
            <div style="display:flex;gap:16px;font-size:11px;color:#94A3B8;margin-top:4px;">
                <span>← -1 (Negatif Kuat)</span><span style="margin-left:auto;">1 (Positif Kuat) →</span>
            </div></div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        # Insight cards
        st.markdown("""
        <div class="card">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;">
                <span style="font-size:18px;">💡</span>
                <div class="section-title" style="margin-bottom:0;">Insight Utama</div>
            </div>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;">
                <div class="card-sm">
                    <div style="font-size:24px;margin-bottom:8px;">📈</div>
                    <div style="font-size:13px;font-weight:600;color:#334155;margin-bottom:4px;">Tren Meningkat</div>
                    <div style="font-size:12px;color:#64748B;">Prediksi menunjukkan peningkatan ISPU pada 30–31 Mei, masuk kategori Tidak Sehat.</div>
                </div>
                <div class="card-sm">
                    <div style="font-size:24px;margin-bottom:8px;">🕔</div>
                    <div style="font-size:13px;font-weight:600;color:#334155;margin-bottom:4px;">Waktu Kritis</div>
                    <div style="font-size:12px;color:#64748B;">Polusi tertinggi terjadi pada sore hingga malam hari (17:00–20:00 WIB).</div>
                </div>
                <div class="card-sm">
                    <div style="font-size:24px;margin-bottom:8px;">😷</div>
                    <div style="font-size:13px;font-weight:600;color:#334155;margin-bottom:4px;">Polutan Utama</div>
                    <div style="font-size:12px;color:#64748B;">PM2.5 menjadi faktor dominan yang mempengaruhi kualitas udara di Jakarta.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab_pola:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2, gap="large")
        with c1:
            st.markdown('<div class="card"><div class="section-title">Rata-rata ISPU per Wilayah</div>', unsafe_allow_html=True)
            wil_names = list(WILAYAH_DATA.keys())
            wil_ispu  = [WILAYAH_DATA[w]["ispu"] for w in wil_names]
            wil_colors = [status_color(WILAYAH_DATA[w]["status"]) for w in wil_names]

            fig_bar = go.Figure(go.Bar(
                x=wil_names, y=wil_ispu, marker_color=wil_colors,
                text=wil_ispu, textposition="outside",
                hovertemplate="<b>%{x}</b>: ISPU %{y}<extra></extra>",
            ))
            fig_bar.update_layout(**{**PLOT_LAYOUT, "height": 240,
                "xaxis": dict(tickangle=-15, tickfont=dict(size=10)),
                "yaxis": dict(range=[0, 140], showgrid=True, gridcolor="#F1F5F9", zeroline=False)})
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="card"><div class="section-title">Distribusi Kategori ISPU (2024)</div>', unsafe_allow_html=True)
            cat_labels = ["BAIK", "SEDANG", "TIDAK SEHAT"]
            cat_values = [45.2, 42.8, 12.0]
            cat_colors = ["#22C55E", "#2563EB", "#F97316"]

            fig_cat = go.Figure(go.Pie(
                labels=cat_labels, values=cat_values,
                marker=dict(colors=cat_colors, line=dict(color="white", width=2)),
                hole=0.5, textinfo="percent+label",
                hovertemplate="<b>%{label}</b>: %{value}%<extra></extra>",
            ))
            fig_cat.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=10, b=0), height=240,
                legend=dict(orientation="h", y=-0.1),
                font=dict(family="Poppins, sans-serif"),
            )
            st.plotly_chart(fig_cat, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)

        # Model performance table
        st.markdown("""
        <div class="card">
            <div class="section-title">Performa Model Machine Learning</div>
            <div class="section-sub">Hasil evaluasi berdasarkan data ISPU DKI Jakarta 2024 (CRISP-DM)</div>
        """, unsafe_allow_html=True)

        model_df = pd.DataFrame({
            "Model": ["XGBoost ⭐", "Random Forest", "SVM"],
            "Test Accuracy": ["97.71%", "96.54%", "93.12%"],
            "Macro Precision": ["0.9714", "0.9608", "0.9241"],
            "Macro Recall": ["0.9556", "0.9423", "0.9085"],
            "Macro F1-Score": ["0.9634", "0.9515", "0.9162"],
            "CV Mean Accuracy": ["97.51%", "96.41%", "92.98%"],
        })
        st.dataframe(model_df, use_container_width=True, hide_index=True)
        st.markdown("""
        <div style="font-size:12px;color:#94A3B8;margin-top:8px;">
            ⭐ XGBoost dipilih sebagai model terbaik dengan akurasi tertinggi dan performa konsisten pada cross-validation 5-fold.
            Data simulasi berdasarkan sampel ISPU 2024.
        </div></div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ─── HALAMAN 4: EDUKASI & INSIGHT ────────────────────────────────────────────
def page_edukasi():
    render_header("Edukasi & Insight",
                  "Pahami kualitas udara dan dampaknya bagi kesehatan Anda.")

    pad = "padding: 0 32px;"
    st.markdown(f'<div style="{pad}">', unsafe_allow_html=True)

    # ── Kategori ISPU ──────────────────────────────────────────────────
    st.markdown("""
    <div class="card">
        <div class="section-title">Mengenal ISPU (Indeks Standar Pencemar Udara)</div>
        <div class="section-sub">ISPU digunakan untuk menggambarkan kualitas udara ambien di sekitar kita.</div>
    """, unsafe_allow_html=True)

    cats = [
        ("0 – 50",   "Baik",              "#22C55E", "#DCFCE7", "😊",
         "Udara bersih, aman untuk beraktivitas sehari-hari."),
        ("51 – 100",  "Sedang",            "#2563EB", "#DBEAFE", "😐",
         "Masih dapat diterima untuk beraktivitas luar ruangan."),
        ("101 – 200", "Tidak Sehat",       "#F97316", "#FEF3C7", "😟",
         "Kurangi aktivitas luar ruangan, terutama bagi kelompok sensitif."),
        ("201 – 300", "Sangat Tidak Sehat","#EF4444", "#FEE2E2", "😠",
         "Hindari aktivitas luar ruangan. Gunakan masker jika harus keluar."),
        ("≥ 301",     "Berbahaya",         "#7C3AED", "#F3E8FF", "😷",
         "Hindari semua aktivitas luar ruangan. Tetap di dalam ruangan."),
    ]

    cat_cols = st.columns(5)
    for col, (rng, label, color, bg, emoji, desc) in zip(cat_cols, cats):
        with col:
            st.markdown(f"""
            <div style="background:{bg};border-radius:14px;padding:18px 14px;text-align:center;">
                <div style="font-size:13px;font-weight:700;color:{color};">{rng}</div>
                <div style="font-size:15px;font-weight:700;color:{color};margin:4px 0;">{label}</div>
                <div style="font-size:32px;margin:8px 0;">{emoji}</div>
                <div style="font-size:11px;color:#64748B;line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Dampak & Sumber & Pola ──────────────────────────────────────────
    c1, c2, c3 = st.columns([1, 1, 1.1], gap="large")

    with c1:
        st.markdown("""
        <div class="card">
            <div class="section-title">Dampak Kualitas Udara terhadap Kesehatan ℹ️</div>
        """, unsafe_allow_html=True)
        impacts = [
            ("🫁", "Sistem Pernapasan",
             "Polusi udara dapat menyebabkan iritasi, batuk, sesak napas, dan memperparah asma."),
            ("❤️", "Sistem Kardiovaskular",
             "Paparan jangka panjang meningkatkan risiko penyakit jantung dan tekanan darah tinggi."),
            ("👧", "Anak-anak",
             "Anak lebih rentan terhadap infeksi pernapasan dan gangguan perkembangan paru-paru."),
            ("👴", "Lansia",
             "Risiko penyakit kronis meningkat, terutama jika memiliki riwayat penyakit."),
        ]
        for icon, title, desc in impacts:
            st.markdown(f"""
            <div style="display:flex;gap:12px;align-items:flex-start;padding:10px 0;
                        border-bottom:1px solid #F8FAFC;">
                <div style="font-size:26px;flex-shrink:0;">{icon}</div>
                <div>
                    <div style="font-size:13px;font-weight:600;color:#334155;">{title}</div>
                    <div style="font-size:11px;color:#64748B;margin-top:2px;line-height:1.5;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card"><div class="section-title">Sumber Polusi Udara di Jakarta ℹ️</div>', unsafe_allow_html=True)
        src_labels = ["Transportasi","Industri","Aktivitas Rumah Tangga","Konstruksi","Lainnya"]
        src_values = [45, 20, 15, 10, 10]
        src_colors = ["#2563EB","#22C55E","#FACC15","#EF4444","#A78BFA"]

        fig_src = go.Figure(go.Pie(
            labels=src_labels, values=src_values,
            marker=dict(colors=src_colors, line=dict(color="white", width=2)),
            hole=0.55,
            textinfo="percent",
            hovertemplate="<b>%{label}</b>: %{value}%<extra></extra>",
        ))
        fig_src.add_annotation(text="<b>Kontribusi</b><br><b>Sumber Polusi</b>",
            x=0.5, y=0.5, showarrow=False, font=dict(size=10, color="#1E293B"), align="center")
        fig_src.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0), height=220,
            legend=dict(orientation="v", yanchor="middle", y=0.5,
                        xanchor="right", x=1.4, font=dict(size=10)),
            font=dict(family="Poppins, sans-serif"),
        )
        st.plotly_chart(fig_src, use_container_width=True, config={"displayModeBar": False})
        st.markdown("""
        <div style="font-size:12px;color:#64748B;">
            Transportasi menjadi penyumbang polusi udara terbesar di Jakarta.
        </div></div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="card"><div class="section-title">Waktu dengan Kualitas Udara Terburuk ℹ️</div>', unsafe_allow_html=True)

        # Color by level
        seg_colors = (["#22C55E"]*8 + ["#FACC15"]*4 + ["#F97316"]*4 +
                      ["#EF4444"]*4 + ["#F97316"]*4)[:24]

        fig_worst = go.Figure()
        # Background zones
        fig_worst.add_hrect(y0=0, y1=50, fillcolor="rgba(34,197,94,0.08)", line_width=0)
        fig_worst.add_hrect(y0=50, y1=100, fillcolor="rgba(37,99,235,0.06)", line_width=0)
        fig_worst.add_hrect(y0=100, y1=200, fillcolor="rgba(249,115,22,0.06)", line_width=0)

        fig_worst.add_trace(go.Scatter(
            x=[f"{i:02d}:00" for i in range(24)],
            y=HOURLY_ISPU,
            mode="lines+markers",
            line=dict(color="#F97316", width=2.5),
            marker=dict(size=5, color=seg_colors),
            fill="tozeroy", fillcolor="rgba(249,115,22,0.07)",
            hovertemplate="%{x}: ISPU <b>%{y}</b><extra></extra>",
        ))
        fig_worst.add_annotation(x="19:00", y=130,
            text="<b>Puncak Polusi<br>17:00–20:00</b>",
            showarrow=True, arrowhead=2, arrowcolor="#EF4444",
            bgcolor="white", bordercolor="#EF4444", borderpad=5,
            font=dict(size=10, color="#EF4444"))

        fig_worst.update_layout(**{**PLOT_LAYOUT, "height": 220,
            "xaxis": dict(tickvals=["00:00","04:00","08:00","12:00","16:00","20:00","24:00"],
                          tickfont=dict(size=9)),
            "yaxis": dict(range=[0, 170], showgrid=True, gridcolor="#F1F5F9", zeroline=False)})
        st.plotly_chart(fig_worst, use_container_width=True, config={"displayModeBar": False})
        st.markdown("""
        <div class="info-note" style="font-size:11px;">
            💡 Kualitas udara cenderung memburuk pada sore hingga malam hari.
            Sebaiknya batasi aktivitas luar ruangan pada waktu tersebut.
        </div></div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Tips Kesehatan ──────────────────────────────────────────────────
    st.markdown("""
    <div class="card">
        <div class="section-title">Tips Menjaga Kesehatan Saat Kualitas Udara Tidak Sehat ℹ️</div>
    """, unsafe_allow_html=True)

    tips = [
        ("😷", "Gunakan Masker",
         "Gunakan masker berstandar untuk mengurangi paparan polusi udara."),
        ("🏃", "Batasi Aktivitas Luar",
         "Kurangi aktivitas fisik berat di luar ruangan, terutama saat sore hingga malam hari."),
        ("🪟", "Ventilasi yang Baik",
         "Tutup jendela saat polusi tinggi dan pastikan ventilasi rumah tetap berfungsi baik."),
        ("💧", "Perbanyak Minum Air",
         "Minum air putih yang cukup untuk menjaga kebersihan saluran pernapasan."),
        ("🌬️", "Gunakan Air Purifier",
         "Jika memungkinkan, gunakan alat penyaring udara di dalam ruangan untuk udara lebih bersih."),
    ]

    tip_cols = st.columns(5)
    for col, (icon, title, desc) in zip(tip_cols, tips):
        with col:
            st.markdown(f"""
            <div style="text-align:center;padding:8px 4px;">
                <div style="font-size:36px;margin-bottom:10px;">{icon}</div>
                <div style="font-size:13px;font-weight:600;color:#334155;margin-bottom:6px;">{title}</div>
                <div style="font-size:11px;color:#64748B;line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Footer ─────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#EFF6FF,#F0FDF4);border-radius:16px;
                padding:28px 32px;margin-top:8px;margin-bottom:32px;
                display:flex;align-items:center;justify-content:space-between;">
        <div>
            <div style="font-size:18px;font-weight:700;color:#2563EB;margin-bottom:6px;">
                🍃 Jaga udara, jaga kesehatan, jaga Jakarta.
            </div>
            <div style="font-size:13px;color:#64748B;">
                Langkah kecil hari ini untuk udara yang lebih baik di masa depan.
            </div>
        </div>
        <div style="font-size:64px;opacity:0.4;">🏙️</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ─── Router ───────────────────────────────────────────────────────────────────
if "Dashboard" in page:
    page_dashboard()
elif "Detail" in page:
    page_detail()
elif "Prediksi" in page:
    page_prediksi()
else:
    page_edukasi()
