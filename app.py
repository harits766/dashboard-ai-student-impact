
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# Page config
# ============================================================

st.set_page_config(
    page_title="AI Student Impact Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# Theme and CSS
# ============================================================

PRIMARY = "#2563EB"
SECONDARY = "#7C3AED"
ACCENT = "#06B6D4"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
DANGER = "#EF4444"
INK = "#111827"
MUTED = "#6B7280"
CARD = "#FFFFFF"
BG = "#F6F8FC"

PALETTE = [
    "#2563EB", "#7C3AED", "#06B6D4", "#10B981", "#F59E0B",
    "#EF4444", "#EC4899", "#14B8A6", "#6366F1", "#84CC16"
]

SEGMENT_COLORS = {
    "Light User (0-5 jam/minggu)": "#10B981",
    "Moderate User (5-15 jam/minggu)": "#F59E0B",
    "Heavy User (>15 jam/minggu)": "#EF4444"
}

BURNOUT_COLORS = {
    "Low": "#10B981",
    "Medium": "#F59E0B",
    "High": "#EF4444"
}

RISK_COLORS = {
    "Risiko Rendah / Normal": "#10B981",
    "Risiko Sedang - Dependency": "#F59E0B",
    "Risiko Tinggi - Well-being": "#EF4444",
    "Risiko Tinggi - Dependency dan Burnout": "#7C2D12"
}

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background:
            radial-gradient(circle at top left, rgba(37, 99, 235, 0.12), transparent 28%),
            radial-gradient(circle at top right, rgba(124, 58, 237, 0.12), transparent 25%),
            linear-gradient(180deg, #F8FAFC 0%, #EEF2FF 100%);
    }}

    .block-container {{
        padding-top: 1.4rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }}

    section[data-testid="stSidebar"] * {{
        color: #F8FAFC !important;
    }}

    section[data-testid="stSidebar"] div[data-baseweb="select"] span {{
        color: #111827 !important;
    }}

    .hero {{
        padding: 1.6rem 1.8rem;
        border-radius: 24px;
        color: white;
        background:
            linear-gradient(135deg, rgba(37,99,235,0.98) 0%, rgba(124,58,237,0.96) 55%, rgba(6,182,212,0.92) 100%);
        box-shadow: 0 22px 50px rgba(37, 99, 235, 0.28);
        margin-bottom: 1.2rem;
    }}

    .hero h1 {{
        color: white;
        font-weight: 800;
        margin-bottom: 0.2rem;
        letter-spacing: -0.03em;
        font-size: 2.3rem;
    }}

    .hero p {{
        color: rgba(255,255,255,0.88);
        font-size: 1.02rem;
        margin-bottom: 0;
    }}

    .section-card {{
        background: rgba(255,255,255,0.88);
        border: 1px solid rgba(148, 163, 184, 0.32);
        border-radius: 20px;
        padding: 1rem 1.1rem;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
        margin-bottom: 1rem;
    }}

    div[data-testid="stMetric"] {{
        background: rgba(255,255,255,0.95);
        border: 1px solid rgba(148, 163, 184, 0.28);
        border-radius: 18px;
        padding: 1rem 1rem;
        box-shadow: 0 12px 26px rgba(15, 23, 42, 0.08);
        min-height: 112px;
    }}

    div[data-testid="stMetricLabel"] {{
        color: #64748B !important;
        font-size: 0.86rem !important;
        font-weight: 700 !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: {INK} !important;
        font-size: 1.62rem !important;
        font-weight: 800 !important;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background: rgba(255,255,255,0.72);
        padding: 0.45rem;
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.28);
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 12px;
        padding: 0.65rem 1rem;
        font-weight: 700;
        color: #334155;
    }}

    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #2563EB, #7C3AED);
        color: white !important;
    }}

    .stDataFrame {{
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(148, 163, 184, 0.25);
    }}

    .insight {{
        padding: 0.85rem 1rem;
        border-radius: 14px;
        background: linear-gradient(135deg, rgba(37,99,235,0.09), rgba(6,182,212,0.10));
        border-left: 5px solid #2563EB;
        color: #0F172A;
        margin: 0.5rem 0 1rem 0;
    }}

    .small-note {{
        color: #64748B;
        font-size: 0.92rem;
    }}

    h2, h3 {{
        color: #0F172A;
        font-weight: 800;
        letter-spacing: -0.02em;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================
# Plot helpers
# ============================================================

def style_fig(fig, title=None, height=430):
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color=INK, family="Inter"), x=0.02),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(color=INK, family="Inter"),
        legend=dict(
            bgcolor="rgba(255,255,255,0.72)",
            bordercolor="rgba(148,163,184,0.25)",
            borderwidth=1,
            font=dict(color=INK, size=12)
        ),
        margin=dict(l=34, r=24, t=58, b=48),
        height=height,
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter", font_color=INK),
    )
    fig.update_xaxes(
        showline=False,
        gridcolor="rgba(148,163,184,0.25)",
        zeroline=False,
        tickfont=dict(color="#475569"),
        title_font=dict(color="#334155")
    )
    fig.update_yaxes(
        showline=False,
        gridcolor="rgba(148,163,184,0.25)",
        zeroline=False,
        tickfont=dict(color="#475569"),
        title_font=dict(color="#334155")
    )
    return fig

def make_bar(df_plot, x, y, color=None, title=None, text=None, height=430):
    fig = px.bar(
        df_plot,
        x=x,
        y=y,
        color=color,
        text=text,
        color_discrete_sequence=PALETTE
    )
    fig.update_traces(
        marker_line_color="rgba(15,23,42,0.45)",
        marker_line_width=0.8,
        opacity=0.92,
        textposition="outside"
    )
    return style_fig(fig, title=title, height=height)

# ============================================================
# Load data
# ============================================================

@st.cache_data
def load_data():
    candidates = [
        Path("data/Analytical Dataset.csv"),
        Path("Analytical Dataset.csv"),
        Path("Clean Dataset.csv"),
        Path("ai_student_impact_dataset.csv")
    ]

    data_path = None
    for candidate in candidates:
        if candidate.exists():
            data_path = candidate
            break

    if data_path is None:
        raise FileNotFoundError("Dataset tidak ditemukan. Letakkan Analytical Dataset.csv di folder data/.")

    data = pd.read_csv(data_path)

    if "AI Usage Segment" not in data.columns:
        def segmentasi_ai(jam):
            if pd.isna(jam):
                return np.nan
            if jam <= 5:
                return "Light User (0-5 jam/minggu)"
            if jam <= 15:
                return "Moderate User (5-15 jam/minggu)"
            return "Heavy User (>15 jam/minggu)"
        data["AI Usage Segment"] = data["Weekly_GenAI_Hours"].apply(segmentasi_ai)

    if "GPA Change" not in data.columns:
        data["GPA Change"] = data["Post_Semester_GPA"] - data["Pre_Semester_GPA"]

    if "Risk Profile" not in data.columns:
        def profil_risiko(row):
            if row["Perceived_AI_Dependency"] >= 7 and row["Burnout_Risk_Level"] == "High":
                return "Risiko Tinggi - Dependency dan Burnout"
            if row["Burnout_Risk_Level"] == "High" or row["Anxiety_Level_During_Exams"] >= 8:
                return "Risiko Tinggi - Well-being"
            if row["Perceived_AI_Dependency"] >= 7:
                return "Risiko Sedang - Dependency"
            return "Risiko Rendah / Normal"
        data["Risk Profile"] = data.apply(profil_risiko, axis=1)

    return data

df = load_data()

# ============================================================
# Header
# ============================================================

st.markdown("""
<div class="hero">
    <h1>🎓 AI Student Impact Dashboard</h1>
    <p>Business Intelligence Dashboard untuk menganalisis performa akademik, retensi pengetahuan, kebijakan institusi, dan risiko well-being mahasiswa.</p>
</div>
""", unsafe_allow_html=True)

with st.expander("Keterkaitan dengan Modul 1-5", expanded=False):
    st.markdown("""
    - **Modul 1 BRD:** dashboard menjawab 7 pertanyaan analitik.
    - **Modul 2 Data Profiling:** dashboard memakai variabel yang sudah didefinisikan.
    - **Modul 3 EDA:** visualisasi mengikuti pola EDA.
    - **Modul 4 Cleaning:** dashboard memakai dataset yang sudah divalidasi.
    - **Modul 5 Objek Data:** dashboard memakai `AI Usage Segment`, `GPA Change`, dan `Risk Profile`.
    """)

# ============================================================
# Sidebar filter
# ============================================================

st.sidebar.markdown("## 🎛️ Filter Interaktif")
st.sidebar.caption("Gunakan filter ini untuk drill-down analisis.")

def sidebar_multiselect(label, column):
    values = sorted([x for x in df[column].dropna().unique()])
    return st.sidebar.multiselect(label, values, default=values)

selected_major = sidebar_multiselect("Major Category", "Major_Category")
selected_year = sidebar_multiselect("Year of Study", "Year_of_Study")
selected_policy = sidebar_multiselect("Institutional Policy", "Institutional_Policy")
selected_segment = sidebar_multiselect("AI Usage Segment", "AI Usage Segment")
selected_burnout = sidebar_multiselect("Burnout Risk Level", "Burnout_Risk_Level")

filtered = df[
    df["Major_Category"].isin(selected_major)
    & df["Year_of_Study"].isin(selected_year)
    & df["Institutional_Policy"].isin(selected_policy)
    & df["AI Usage Segment"].isin(selected_segment)
    & df["Burnout_Risk_Level"].isin(selected_burnout)
].copy()

st.sidebar.markdown("---")
st.sidebar.metric("Mahasiswa Terfilter", f"{len(filtered):,}")
st.sidebar.metric("Total Dataset", f"{len(df):,}")

if filtered.empty:
    st.error("Tidak ada data untuk kombinasi filter yang dipilih.")
    st.stop()

# ============================================================
# KPI
# ============================================================

total_students = len(filtered)
avg_gpa = filtered["Post_Semester_GPA"].mean()
avg_retention = filtered["Skill_Retention_Score"].mean()
high_burnout_pct = filtered["Burnout_Risk_Level"].eq("High").mean() * 100
avg_dependency = filtered["Perceived_AI_Dependency"].mean()

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("👥 Jumlah Mahasiswa", f"{total_students:,}")
kpi2.metric("🎯 Rata-rata GPA", f"{avg_gpa:.3f}")
kpi3.metric("🧠 Skill Retention", f"{avg_retention:.2f}")
kpi4.metric("🔥 High Burnout Risk", f"{high_burnout_pct:.2f}%")
kpi5.metric("🤖 AI Dependency", f"{avg_dependency:.2f}")

st.markdown("")

# ============================================================
# Tabs
# ============================================================

tab_overview, tab_ai, tab_mental, tab_retention, tab_risk, tab_brd = st.tabs([
    "🌍 Overview",
    "🚀 Dampak AI",
    "🧘 Kesehatan Mental",
    "🧠 Retensi Pengetahuan",
    "⚠️ Profil Risiko",
    "🧭 BRD Mapping"
])

# ============================================================
# Overview
# ============================================================

with tab_overview:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Overview Mahasiswa")
    st.markdown('<p class="small-note">Distribusi mahasiswa per bidang studi, jenjang, dan kebijakan institusi.</p>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        major_count = filtered["Major_Category"].value_counts().reset_index()
        major_count.columns = ["Major_Category", "Jumlah Mahasiswa"]
        fig = make_bar(
            major_count,
            x="Major_Category",
            y="Jumlah Mahasiswa",
            color="Major_Category",
            title="Distribusi per Major Category",
            text="Jumlah Mahasiswa"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        year_order = ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"]
        year_count = filtered["Year_of_Study"].value_counts().reindex(year_order).dropna().reset_index()
        year_count.columns = ["Year_of_Study", "Jumlah Mahasiswa"]
        fig = make_bar(
            year_count,
            x="Year_of_Study",
            y="Jumlah Mahasiswa",
            color="Year_of_Study",
            title="Distribusi per Year of Study",
            text="Jumlah Mahasiswa"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        policy_count = filtered["Institutional_Policy"].value_counts().reset_index()
        policy_count.columns = ["Institutional_Policy", "Jumlah Mahasiswa"]
        fig = make_bar(
            policy_count,
            x="Institutional_Policy",
            y="Jumlah Mahasiswa",
            color="Institutional_Policy",
            title="Distribusi per Policy",
            text="Jumlah Mahasiswa"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="insight">Insight: tab overview memastikan komposisi data dapat dicek sebelum membaca dampak AI, burnout, dan retensi.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# Dampak AI
# ============================================================

with tab_ai:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Dampak AI terhadap GPA")
    st.markdown('<p class="small-note">Perubahan GPA rata-rata dibandingkan dengan segmentasi Light, Moderate, dan Heavy User.</p>', unsafe_allow_html=True)

    seg_order = ["Light User (0-5 jam/minggu)", "Moderate User (5-15 jam/minggu)", "Heavy User (>15 jam/minggu)"]
    gpa_segment = filtered.groupby("AI Usage Segment", as_index=False).agg(
        Rata_Rata_Pre_GPA=("Pre_Semester_GPA", "mean"),
        Rata_Rata_Post_GPA=("Post_Semester_GPA", "mean"),
        Rata_Rata_GPA_Change=("GPA Change", "mean"),
        Jumlah_Mahasiswa=("Student_ID", "count")
    )
    gpa_segment["AI Usage Segment"] = pd.Categorical(gpa_segment["AI Usage Segment"], categories=seg_order, ordered=True)
    gpa_segment = gpa_segment.sort_values("AI Usage Segment")

    c1, c2 = st.columns(2)

    with c1:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=gpa_segment["AI Usage Segment"],
            y=gpa_segment["Rata_Rata_Pre_GPA"],
            name="Pre GPA",
            marker=dict(color="#93C5FD", line=dict(color="#1D4ED8", width=1))
        ))
        fig.add_trace(go.Bar(
            x=gpa_segment["AI Usage Segment"],
            y=gpa_segment["Rata_Rata_Post_GPA"],
            name="Post GPA",
            marker=dict(color="#7C3AED", line=dict(color="#4C1D95", width=1))
        ))
        fig.update_layout(barmode="group")
        st.plotly_chart(style_fig(fig, "Rata-rata GPA Pre vs Post per Segment"), use_container_width=True)

    with c2:
        fig = px.bar(
            gpa_segment,
            x="AI Usage Segment",
            y="Rata_Rata_GPA_Change",
            color="AI Usage Segment",
            color_discrete_map=SEGMENT_COLORS,
            text="Rata_Rata_GPA_Change"
        )
        fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        st.plotly_chart(style_fig(fig, "Rata-rata GPA Change per Segment"), use_container_width=True)

    st.dataframe(gpa_segment, use_container_width=True)
    st.markdown('<div class="insight">Insight: segmentasi AI membantu membandingkan apakah intensitas penggunaan AI berkaitan dengan perubahan GPA.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# Kesehatan Mental
# ============================================================

with tab_mental:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Kesehatan Mental")
    st.markdown('<p class="small-note">Distribusi burnout dan rata-rata anxiety/dependency per kebijakan institusi.</p>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        burnout_policy = filtered.groupby(["Institutional_Policy", "Burnout_Risk_Level"]).size().reset_index(name="Jumlah Mahasiswa")
        fig = px.bar(
            burnout_policy,
            x="Institutional_Policy",
            y="Jumlah Mahasiswa",
            color="Burnout_Risk_Level",
            barmode="stack",
            color_discrete_map=BURNOUT_COLORS
        )
        st.plotly_chart(style_fig(fig, "Burnout Risk per Institutional Policy"), use_container_width=True)

    with c2:
        anxiety_policy = filtered.groupby("Institutional_Policy", as_index=False).agg(
            Rata_Rata_Anxiety=("Anxiety_Level_During_Exams", "mean"),
            Rata_Rata_Dependency=("Perceived_AI_Dependency", "mean")
        )
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=anxiety_policy["Institutional_Policy"],
            y=anxiety_policy["Rata_Rata_Anxiety"],
            name="Anxiety",
            marker=dict(color="#F59E0B")
        ))
        fig.add_trace(go.Bar(
            x=anxiety_policy["Institutional_Policy"],
            y=anxiety_policy["Rata_Rata_Dependency"],
            name="AI Dependency",
            marker=dict(color="#EF4444")
        ))
        fig.update_layout(barmode="group")
        st.plotly_chart(style_fig(fig, "Anxiety dan AI Dependency per Policy"), use_container_width=True)

    st.markdown('<div class="insight">Insight: kebijakan institusi dapat dibandingkan terhadap burnout, anxiety, dan dependency untuk evaluasi kebijakan AI.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# Retensi Pengetahuan
# ============================================================

with tab_retention:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Retensi Pengetahuan")
    st.markdown('<p class="small-note">Hubungan Skill Retention Score dengan Perceived AI Dependency.</p>', unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])

    with c1:
        fig = px.scatter(
            filtered,
            x="Perceived_AI_Dependency",
            y="Skill_Retention_Score",
            color="AI Usage Segment",
            opacity=0.48,
            color_discrete_map=SEGMENT_COLORS,
            hover_data=["Major_Category", "Year_of_Study", "Institutional_Policy", "Burnout_Risk_Level"],
            trendline="ols"
        )
        fig.update_traces(marker=dict(size=7, line=dict(width=0.4, color="white")))
        st.plotly_chart(style_fig(fig, "Skill Retention vs AI Dependency"), use_container_width=True)

    with c2:
        corr_retention_dependency = filtered["Skill_Retention_Score"].corr(filtered["Perceived_AI_Dependency"])
        corr_retention_hours = filtered["Skill_Retention_Score"].corr(filtered["Weekly_GenAI_Hours"])
        st.metric("Retention vs Dependency", f"{corr_retention_dependency:.4f}")
        st.metric("Retention vs GenAI Hours", f"{corr_retention_hours:.4f}")
        st.markdown('<p class="small-note">Nilai korelasi menunjukkan arah hubungan awal, bukan kausalitas.</p>', unsafe_allow_html=True)

    st.markdown('<div class="insight">Insight: scatterplot dan trendline membantu membaca apakah dependency terhadap AI berkaitan dengan retensi pengetahuan.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# Profil Risiko
# ============================================================

with tab_risk:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Profil Risiko")
    st.markdown('<p class="small-note">Segmentasi mahasiswa berdasarkan AI dependency dan burnout risk.</p>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        risk_count = filtered["Risk Profile"].value_counts().reset_index()
        risk_count.columns = ["Risk Profile", "Jumlah Mahasiswa"]
        fig = px.bar(
            risk_count,
            x="Risk Profile",
            y="Jumlah Mahasiswa",
            color="Risk Profile",
            color_discrete_map=RISK_COLORS,
            text="Jumlah Mahasiswa"
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(style_fig(fig, "Jumlah Mahasiswa berdasarkan Risk Profile"), use_container_width=True)

    with c2:
        risk_by_segment = filtered.groupby(["AI Usage Segment", "Risk Profile"]).size().reset_index(name="Jumlah Mahasiswa")
        fig = px.bar(
            risk_by_segment,
            x="AI Usage Segment",
            y="Jumlah Mahasiswa",
            color="Risk Profile",
            barmode="stack",
            color_discrete_map=RISK_COLORS
        )
        st.plotly_chart(style_fig(fig, "Risk Profile per AI Usage Segment"), use_container_width=True)

    risk_table = filtered.groupby(["Risk Profile", "Burnout_Risk_Level"], as_index=False).agg(
        Jumlah_Mahasiswa=("Student_ID", "count"),
        Rata_Rata_Dependency=("Perceived_AI_Dependency", "mean"),
        Rata_Rata_Anxiety=("Anxiety_Level_During_Exams", "mean"),
        Rata_Rata_Post_GPA=("Post_Semester_GPA", "mean"),
        Rata_Rata_Skill_Retention=("Skill_Retention_Score", "mean")
    )
    st.dataframe(risk_table, use_container_width=True)
    st.markdown('<div class="insight">Insight: Risk Profile membantu menentukan kelompok prioritas intervensi akademik dan well-being.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# BRD Mapping
# ============================================================

with tab_brd:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Mapping Dashboard ke 7 Pertanyaan Analitik BRD")

    brd_mapping = pd.DataFrame([
        ["1", "Penggunaan AI dan performa akademik", "Dampak AI", "Post_Semester_GPA, GPA Change, AI Usage Segment"],
        ["2", "AI dependency dan retensi pengetahuan", "Retensi Pengetahuan", "Skill_Retention_Score, Perceived_AI_Dependency"],
        ["3", "AI usage dan burnout", "Kesehatan Mental, Profil Risiko", "Burnout_Risk_Level, AI Usage Segment, Risk Profile"],
        ["4", "Kebijakan institusi dan performa/well-being", "Overview, Kesehatan Mental", "Institutional_Policy"],
        ["5", "Pola AI berdasarkan bidang dan jenjang studi", "Overview, Dampak AI", "Major_Category, Year_of_Study"],
        ["6", "Prompt engineering dan performa/retensi", "Pengembangan lanjutan", "Prompt_Engineering_Skill"],
        ["7", "Prioritas intervensi akademik dan well-being", "Profil Risiko", "Risk Profile, High Burnout Risk"],
    ], columns=["No", "Pertanyaan BRD", "Tab Dashboard", "Peubah Terkait"])

    st.dataframe(brd_mapping, use_container_width=True)
    st.markdown('<div class="insight">Catatan: dashboard ini fokus pada visualisasi interaktif dan KPI, bukan model regresi/klasifikasi final.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# Export filtered data
# ============================================================

st.markdown("---")
st.subheader("📥 Export Data Terfilter")
csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download data terfilter sebagai CSV",
    data=csv,
    file_name="filtered_dashboard_data.csv",
    mime="text/csv",
    use_container_width=True
)

