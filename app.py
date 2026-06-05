
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# Konfigurasi halaman
# ============================================================

st.set_page_config(
    page_title="Dashboard AI Student Impact",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# Tema visual: colorful, clean, dan teks kontras
# ============================================================

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #F8FBFF 0%, #EEF4FF 100%);
        color: #111827 !important;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1280px;
    }

    html, body, [class*="css"] {
        color: #111827 !important;
    }

    p, div, span, label {
        color: #374151 !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #111827 !important;
        font-weight: 800 !important;
    }

    .hero-card {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #EC4899 100%);
        border-radius: 24px;
        padding: 28px 32px;
        margin-bottom: 20px;
        box-shadow: 0 16px 40px rgba(79, 70, 229, 0.25);
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 900;
        color: #FFFFFF !important;
        margin-bottom: 0.25rem;
        letter-spacing: -0.03em;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #EEF2FF !important;
        margin-bottom: 0;
        line-height: 1.55;
    }

    .section-title {
        font-size: 1.65rem;
        font-weight: 850;
        color: #111827 !important;
        margin-top: 0.25rem;
        margin-bottom: 0.35rem;
    }

    .section-subtitle {
        font-size: 1rem;
        color: #64748B !important;
        margin-bottom: 1rem;
    }

    .kpi-card {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 18px 20px;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
        border: 1px solid #E5E7EB;
        min-height: 118px;
    }

    .kpi-label {
        font-size: 0.92rem;
        color: #64748B !important;
        font-weight: 650;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 2rem;
        font-weight: 900;
        color: #111827 !important;
        letter-spacing: -0.03em;
    }

    .kpi-note {
        font-size: 0.78rem;
        color: #94A3B8 !important;
        margin-top: 6px;
    }

    .insight-box {
        background: #FFFFFF;
        border-left: 6px solid #4F46E5;
        border-radius: 16px;
        padding: 16px 18px;
        margin: 14px 0 20px 0;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    }

    .insight-box b {
        color: #111827 !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }

    section[data-testid="stSidebar"] label {
        color: #E2E8F0 !important;
        font-weight: 650 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: #CBD5E1 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-color: #CBD5E1 !important;
        color: #111827 !important;
    }

    div[data-baseweb="select"] span {
        color: #111827 !important;
    }

    div[data-baseweb="popover"] * {
        color: #111827 !important;
    }

    button[data-baseweb="tab"] {
        color: #475569 !important;
        font-weight: 750 !important;
        border-radius: 16px !important;
        padding: 12px 20px !important;
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        margin-right: 8px !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid #7C3AED !important;
        box-shadow: 0 10px 24px rgba(79, 70, 229, 0.24);
    }

    button[data-baseweb="tab"][aria-selected="true"] p,
    button[data-baseweb="tab"][aria-selected="true"] div,
    button[data-baseweb="tab"][aria-selected="true"] span {
        color: #FFFFFF !important;
    }

    [data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricValue"] {
        color: #111827 !important;
        font-weight: 900 !important;
    }

    [data-testid="stDataFrame"] {
        background: #FFFFFF !important;
        border-radius: 18px !important;
        border: 1px solid #E5E7EB !important;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
    }

    .stAlert {
        background: #FFFFFF !important;
        border-radius: 16px !important;
        color: #111827 !important;
    }

    .stMarkdown, .stMarkdown p {
        color: #374151 !important;
    }

    hr {
        border: none;
        border-top: 1px solid #E5E7EB;
        margin: 1.25rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Palet warna
# ============================================================

SEGMENT_COLORS = {
    "Light User (0-5 jam/minggu)": "#10B981",
    "Moderate User (5-15 jam/minggu)": "#F59E0B",
    "Heavy User (>15 jam/minggu)": "#EF4444",
}

BURNOUT_COLORS = {
    "Low": "#22C55E",
    "Medium": "#F59E0B",
    "High": "#EF4444",
}

RISK_COLORS = {
    "Risiko Rendah / Normal": "#22C55E",
    "Risiko Sedang - Dependency": "#F59E0B",
    "Risiko Tinggi - Well-being": "#EF4444",
    "Risiko Tinggi - Dependency dan Burnout": "#7C3AED",
}

CATEGORICAL_COLORS = [
    "#4F46E5", "#06B6D4", "#10B981", "#F59E0B", "#EF4444",
    "#8B5CF6", "#EC4899", "#14B8A6", "#F97316", "#64748B"
]

def apply_chart_style(fig, title=None):
    fig.update_layout(
        title=title,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#1F2937", size=13),
        title_font=dict(color="#111827", size=20),
        legend=dict(
            font=dict(color="#1F2937"),
            bgcolor="rgba(255,255,255,0.88)",
            bordercolor="#E5E7EB",
            borderwidth=1
        ),
        margin=dict(l=32, r=22, t=64, b=50),
    )
    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor="#CBD5E1",
        gridcolor="#E5E7EB",
        tickfont=dict(color="#475569"),
        title_font=dict(color="#111827")
    )
    fig.update_yaxes(
        showline=True,
        linewidth=1,
        linecolor="#CBD5E1",
        gridcolor="#E5E7EB",
        tickfont=dict(color="#475569"),
        title_font=dict(color="#111827")
    )
    return fig

def metric_card(label, value, note="", accent="#4F46E5"):
    st.markdown(
        f"""
        <div class="kpi-card" style="border-top: 5px solid {accent};">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def section_header(title, subtitle):
    st.markdown(
        f"""
        <div class="section-title">{title}</div>
        <div class="section-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True
    )

def insight(text, color="#4F46E5"):
    st.markdown(
        f"""
        <div class="insight-box" style="border-left-color:{color};">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# Load data
# ============================================================

@st.cache_data
def load_data():
    candidates = [
        Path("data/Analytical Dataset.csv"),
        Path("Analytical Dataset.csv"),
        Path("Clean Dataset.csv"),
        Path("ai_student_impact_dataset.csv"),
    ]

    data_path = None
    for candidate in candidates:
        if candidate.exists():
            data_path = candidate
            break

    if data_path is None:
        raise FileNotFoundError("Dataset tidak ditemukan. Letakkan 'Analytical Dataset.csv' di folder data/.")

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

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">📊 Modul 6 - Business Intelligence Dashboard</div>
        <div class="hero-subtitle">
            AI Impact on Students: Academic Performance, Knowledge Retention, and Well-being Risk.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

with st.expander("Keterkaitan dengan Modul 1-5", expanded=False):
    st.markdown("""
    Dashboard ini disusun berdasarkan alur proyek:

    - **Modul 1 BRD:** dashboard menjawab 7 pertanyaan analitik dan kebutuhan stakeholder.
    - **Modul 2 Data Profiling:** dashboard memakai variabel yang sudah didefinisikan dalam data dictionary.
    - **Modul 3 EDA:** visualisasi dashboard mengikuti pola temuan EDA: GPA, retention, burnout, dependency, dan policy.
    - **Modul 4 Cleaning:** dashboard memakai dataset yang sudah divalidasi dan dibersihkan.
    - **Modul 5 Objek Data:** dashboard memakai `AI Usage Segment`, `GPA Change`, dan `Risk Profile`.
    """)

# ============================================================
# Sidebar filter
# ============================================================

st.sidebar.title("🎛️ Filter Interaktif")
st.sidebar.caption("Gunakan filter ini untuk mengeksplorasi segmen mahasiswa.")

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
# KPI cards
# ============================================================

total_students = len(filtered)
avg_gpa = filtered["Post_Semester_GPA"].mean()
avg_retention = filtered["Skill_Retention_Score"].mean()
high_burnout_pct = filtered["Burnout_Risk_Level"].eq("High").mean() * 100
avg_dependency = filtered["Perceived_AI_Dependency"].mean()

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    metric_card("Jumlah Mahasiswa", f"{total_students:,}", "setelah filter", "#4F46E5")
with kpi2:
    metric_card("Rata-rata GPA", f"{avg_gpa:.3f}", "Post Semester GPA", "#06B6D4")
with kpi3:
    metric_card("Skill Retention", f"{avg_retention:.2f}", "rata-rata skor", "#10B981")
with kpi4:
    metric_card("High Burnout", f"{high_burnout_pct:.2f}%", "proporsi risiko tinggi", "#EF4444")
with kpi5:
    metric_card("AI Dependency", f"{avg_dependency:.2f}", "rata-rata persepsi", "#F59E0B")

st.markdown("---")

# ============================================================
# Tabs
# ============================================================

tab_overview, tab_ai, tab_mental, tab_retention, tab_risk, tab_brd = st.tabs([
    "📌 Overview",
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
    section_header(
        "Overview Mahasiswa",
        "Distribusi mahasiswa per bidang studi, jenjang, dan kebijakan institusi."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        major_count = filtered["Major_Category"].value_counts().reset_index()
        major_count.columns = ["Major_Category", "Jumlah Mahasiswa"]

        fig = px.bar(
            major_count,
            x="Major_Category",
            y="Jumlah Mahasiswa",
            color="Major_Category",
            color_discrete_sequence=CATEGORICAL_COLORS,
            text="Jumlah Mahasiswa"
        )
        fig.update_traces(marker_line_color="white", marker_line_width=1.2, textposition="outside")
        st.plotly_chart(apply_chart_style(fig, "Distribusi Mahasiswa per Major Category"), use_container_width=True)

    with c2:
        year_order = ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"]
        year_count = filtered["Year_of_Study"].value_counts().reindex(year_order).dropna().reset_index()
        year_count.columns = ["Year_of_Study", "Jumlah Mahasiswa"]

        fig = px.bar(
            year_count,
            x="Year_of_Study",
            y="Jumlah Mahasiswa",
            color="Year_of_Study",
            color_discrete_sequence=CATEGORICAL_COLORS,
            text="Jumlah Mahasiswa"
        )
        fig.update_traces(marker_line_color="white", marker_line_width=1.2, textposition="outside")
        st.plotly_chart(apply_chart_style(fig, "Distribusi Mahasiswa per Year of Study"), use_container_width=True)

    with c3:
        policy_count = filtered["Institutional_Policy"].value_counts().reset_index()
        policy_count.columns = ["Institutional_Policy", "Jumlah Mahasiswa"]

        fig = px.bar(
            policy_count,
            x="Institutional_Policy",
            y="Jumlah Mahasiswa",
            color="Institutional_Policy",
            color_discrete_sequence=CATEGORICAL_COLORS,
            text="Jumlah Mahasiswa"
        )
        fig.update_traces(marker_line_color="white", marker_line_width=1.2, textposition="outside")
        st.plotly_chart(apply_chart_style(fig, "Distribusi Mahasiswa per Institutional Policy"), use_container_width=True)

    insight("<b>Insight:</b> overview membantu memvalidasi bahwa dashboard mencakup bidang studi, jenjang, dan kebijakan institusi yang relevan untuk kebutuhan BRD.", "#4F46E5")

# ============================================================
# Dampak AI
# ============================================================

with tab_ai:
    section_header(
        "Dampak AI terhadap GPA",
        "Perubahan GPA rata-rata dibandingkan dengan segmentasi Light, Moderate, dan Heavy User."
    )

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
            marker=dict(color="#93C5FD", line=dict(color="white", width=1.2)),
            text=[f"{v:.3f}" for v in gpa_segment["Rata_Rata_Pre_GPA"]],
            textposition="outside"
        ))
        fig.add_trace(go.Bar(
            x=gpa_segment["AI Usage Segment"],
            y=gpa_segment["Rata_Rata_Post_GPA"],
            name="Post GPA",
            marker=dict(color="#7C3AED", line=dict(color="white", width=1.2)),
            text=[f"{v:.3f}" for v in gpa_segment["Rata_Rata_Post_GPA"]],
            textposition="outside"
        ))
        fig.update_layout(barmode="group")
        st.plotly_chart(apply_chart_style(fig, "Rata-rata GPA Pre vs Post per Segment"), use_container_width=True)

    with c2:
        fig = px.bar(
            gpa_segment,
            x="AI Usage Segment",
            y="Rata_Rata_GPA_Change",
            color="AI Usage Segment",
            color_discrete_map=SEGMENT_COLORS,
            text="Rata_Rata_GPA_Change"
        )
        fig.update_traces(marker_line_color="white", marker_line_width=1.2, texttemplate="%{text:.3f}", textposition="outside")
        st.plotly_chart(apply_chart_style(fig, "Rata-rata GPA Change per Segment"), use_container_width=True)

    st.dataframe(gpa_segment, use_container_width=True)
    insight("<b>Insight:</b> tab ini menjawab pertanyaan BRD tentang keterkaitan penggunaan AI dengan performa akademik.", "#06B6D4")

# ============================================================
# Kesehatan Mental
# ============================================================

with tab_mental:
    section_header(
        "Kesehatan Mental",
        "Distribusi Burnout Risk Level dan rata-rata anxiety berdasarkan kebijakan institusi."
    )

    c1, c2 = st.columns(2)

    with c1:
        burnout_policy = filtered.groupby(["Institutional_Policy", "Burnout_Risk_Level"]).size().reset_index(name="Jumlah Mahasiswa")

        fig = px.bar(
            burnout_policy,
            x="Institutional_Policy",
            y="Jumlah Mahasiswa",
            color="Burnout_Risk_Level",
            barmode="stack",
            color_discrete_map=BURNOUT_COLORS,
            text="Jumlah Mahasiswa"
        )
        fig.update_traces(marker_line_color="white", marker_line_width=1.1)
        st.plotly_chart(apply_chart_style(fig, "Burnout Risk per Institutional Policy"), use_container_width=True)

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
            marker=dict(color="#EC4899", line=dict(color="white", width=1.2)),
            text=[f"{v:.2f}" for v in anxiety_policy["Rata_Rata_Anxiety"]],
            textposition="outside"
        ))
        fig.add_trace(go.Bar(
            x=anxiety_policy["Institutional_Policy"],
            y=anxiety_policy["Rata_Rata_Dependency"],
            name="AI Dependency",
            marker=dict(color="#F59E0B", line=dict(color="white", width=1.2)),
            text=[f"{v:.2f}" for v in anxiety_policy["Rata_Rata_Dependency"]],
            textposition="outside"
        ))
        fig.update_layout(barmode="group")
        st.plotly_chart(apply_chart_style(fig, "Anxiety dan Dependency per Policy"), use_container_width=True)

    insight("<b>Insight:</b> tab ini menghubungkan kebijakan institusi dengan indikator well-being mahasiswa.", "#EC4899")

# ============================================================
# Retensi Pengetahuan
# ============================================================

with tab_retention:
    section_header(
        "Retensi Pengetahuan",
        "Hubungan Skill Retention Score dengan Perceived AI Dependency."
    )

    c1, c2 = st.columns([2, 1])

    with c1:
        fig = px.scatter(
            filtered,
            x="Perceived_AI_Dependency",
            y="Skill_Retention_Score",
            color="AI Usage Segment",
            opacity=0.50,
            color_discrete_map=SEGMENT_COLORS,
            hover_data=["Major_Category", "Year_of_Study", "Institutional_Policy", "Burnout_Risk_Level"],
            trendline="ols"
        )
        fig.update_traces(marker=dict(size=7, line=dict(width=0.4, color="white")))
        st.plotly_chart(apply_chart_style(fig, "Skill Retention Score vs AI Dependency"), use_container_width=True)

    with c2:
        corr_retention_dependency = filtered["Skill_Retention_Score"].corr(filtered["Perceived_AI_Dependency"])
        corr_retention_hours = filtered["Skill_Retention_Score"].corr(filtered["Weekly_GenAI_Hours"])

        metric_card("Retention vs Dependency", f"{corr_retention_dependency:.4f}", "Pearson correlation", "#7C3AED")
        st.write("")
        metric_card("Retention vs GenAI Hours", f"{corr_retention_hours:.4f}", "Pearson correlation", "#10B981")

    insight("<b>Insight:</b> korelasi digunakan sebagai indikasi awal hubungan, bukan bukti kausalitas.", "#7C3AED")

# ============================================================
# Profil Risiko
# ============================================================

with tab_risk:
    section_header(
        "Profil Risiko Mahasiswa",
        "Segmentasi mahasiswa berdasarkan kombinasi AI dependency dan burnout risk."
    )

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
        fig.update_traces(marker_line_color="white", marker_line_width=1.2, textposition="outside")
        st.plotly_chart(apply_chart_style(fig, "Jumlah Mahasiswa berdasarkan Risk Profile"), use_container_width=True)

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
        fig.update_traces(marker_line_color="white", marker_line_width=1.1)
        st.plotly_chart(apply_chart_style(fig, "Risk Profile per AI Usage Segment"), use_container_width=True)

    risk_table = filtered.groupby(["Risk Profile", "Burnout_Risk_Level"], as_index=False).agg(
        Jumlah_Mahasiswa=("Student_ID", "count"),
        Rata_Rata_Dependency=("Perceived_AI_Dependency", "mean"),
        Rata_Rata_Anxiety=("Anxiety_Level_During_Exams", "mean"),
        Rata_Rata_Post_GPA=("Post_Semester_GPA", "mean"),
        Rata_Rata_Skill_Retention=("Skill_Retention_Score", "mean")
    )

    st.dataframe(risk_table, use_container_width=True)
    insight("<b>Insight:</b> Risk Profile dapat digunakan untuk menentukan kelompok prioritas intervensi akademik dan well-being.", "#EF4444")

# ============================================================
# BRD Mapping
# ============================================================

with tab_brd:
    section_header(
        "Mapping Dashboard ke 7 Pertanyaan Analitik BRD",
        "Memastikan setiap visualisasi dashboard terhubung dengan kebutuhan bisnis pada Modul 1."
    )

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
    insight("<b>Catatan:</b> Dashboard ini fokus pada visualisasi interaktif dan KPI. Analisis model formal dapat dijelaskan pada Modul 7.", "#4F46E5")

# ============================================================
# Export filtered data
# ============================================================

st.markdown("---")
section_header("Export Data Terfilter", "Unduh data sesuai kombinasi filter yang sedang aktif.")

csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download data terfilter sebagai CSV",
    data=csv,
    file_name="filtered_dashboard_data.csv",
    mime="text/csv"
)
