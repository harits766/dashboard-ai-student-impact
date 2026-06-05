
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Modul 6 Dashboard BI - AI Student Impact",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {background-color: #FFFFFF; color: #000000;}
    h1, h2, h3, h4, h5, h6, p, div, span {color: #000000;}
    [data-testid="stMetricValue"] {color: #000000;}
    [data-testid="stMetricLabel"] {color: #000000;}
    .block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
</style>
""", unsafe_allow_html=True)

BW_COLORS = ["#111111", "#444444", "#777777", "#AAAAAA", "#DDDDDD", "#FFFFFF"]

def apply_bw_layout(fig, title=None):
    fig.update_layout(
        title=title,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="black"),
        legend=dict(font=dict(color="black")),
        margin=dict(l=30, r=20, t=50, b=45)
    )
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black", gridcolor="#D9D9D9")
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black", gridcolor="#D9D9D9")
    return fig

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

st.title("Modul 6 - Business Intelligence Dashboard")
st.caption("AI Impact on Students - Academic & Well-being Dataset")

with st.expander("Keterkaitan dengan Modul 1-5", expanded=False):
    st.markdown("""
    - **Modul 1 BRD:** dashboard menjawab 7 pertanyaan analitik.
    - **Modul 2 Data Profiling:** dashboard memakai variabel yang sudah didefinisikan.
    - **Modul 3 EDA:** dashboard mengikuti pola EDA.
    - **Modul 4 Cleaning:** dashboard memakai data yang sudah divalidasi.
    - **Modul 5 Objek Data:** dashboard memakai AI Usage Segment, GPA Change, dan Risk Profile.
    """)

st.sidebar.header("Filter Interaktif")

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
st.sidebar.metric("Jumlah Mahasiswa Terfilter", f"{len(filtered):,}")
st.sidebar.metric("Total Dataset", f"{len(df):,}")

if filtered.empty:
    st.error("Tidak ada data untuk kombinasi filter yang dipilih.")
    st.stop()

total_students = len(filtered)
avg_gpa = filtered["Post_Semester_GPA"].mean()
avg_retention = filtered["Skill_Retention_Score"].mean()
high_burnout_pct = filtered["Burnout_Risk_Level"].eq("High").mean() * 100
avg_dependency = filtered["Perceived_AI_Dependency"].mean()

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Jumlah Mahasiswa", f"{total_students:,}")
kpi2.metric("Rata-rata GPA", f"{avg_gpa:.3f}")
kpi3.metric("Rata-rata Skill Retention", f"{avg_retention:.2f}")
kpi4.metric("% High Burnout Risk", f"{high_burnout_pct:.2f}%")
kpi5.metric("Rata-rata AI Dependency", f"{avg_dependency:.2f}")

st.markdown("---")

tab_overview, tab_ai, tab_mental, tab_retention, tab_risk, tab_brd = st.tabs([
    "Overview",
    "Dampak AI",
    "Kesehatan Mental",
    "Retensi Pengetahuan",
    "Profil Risiko",
    "BRD Mapping"
])

with tab_overview:
    st.subheader("Overview Mahasiswa")
    c1, c2, c3 = st.columns(3)

    with c1:
        major_count = filtered["Major_Category"].value_counts().reset_index()
        major_count.columns = ["Major_Category", "Jumlah Mahasiswa"]
        fig = px.bar(major_count, x="Major_Category", y="Jumlah Mahasiswa", color="Major_Category", color_discrete_sequence=BW_COLORS)
        fig.update_traces(marker_line_color="black", marker_line_width=1)
        st.plotly_chart(apply_bw_layout(fig, "Distribusi Mahasiswa per Major Category"), use_container_width=True)

    with c2:
        year_order = ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"]
        year_count = filtered["Year_of_Study"].value_counts().reindex(year_order).dropna().reset_index()
        year_count.columns = ["Year_of_Study", "Jumlah Mahasiswa"]
        fig = px.bar(year_count, x="Year_of_Study", y="Jumlah Mahasiswa", color="Year_of_Study", color_discrete_sequence=BW_COLORS)
        fig.update_traces(marker_line_color="black", marker_line_width=1)
        st.plotly_chart(apply_bw_layout(fig, "Distribusi Mahasiswa per Year of Study"), use_container_width=True)

    with c3:
        policy_count = filtered["Institutional_Policy"].value_counts().reset_index()
        policy_count.columns = ["Institutional_Policy", "Jumlah Mahasiswa"]
        fig = px.bar(policy_count, x="Institutional_Policy", y="Jumlah Mahasiswa", color="Institutional_Policy", color_discrete_sequence=BW_COLORS)
        fig.update_traces(marker_line_color="black", marker_line_width=1)
        st.plotly_chart(apply_bw_layout(fig, "Distribusi Mahasiswa per Institutional Policy"), use_container_width=True)

with tab_ai:
    st.subheader("Dampak AI terhadap GPA")
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
        fig.add_trace(go.Bar(x=gpa_segment["AI Usage Segment"], y=gpa_segment["Rata_Rata_Pre_GPA"], name="Pre GPA", marker=dict(color="white", line=dict(color="black", width=1))))
        fig.add_trace(go.Bar(x=gpa_segment["AI Usage Segment"], y=gpa_segment["Rata_Rata_Post_GPA"], name="Post GPA", marker=dict(color="#999999", line=dict(color="black", width=1))))
        fig.update_layout(barmode="group")
        st.plotly_chart(apply_bw_layout(fig, "Rata-rata GPA Pre vs Post per AI Usage Segment"), use_container_width=True)

    with c2:
        fig = px.bar(gpa_segment, x="AI Usage Segment", y="Rata_Rata_GPA_Change", color="AI Usage Segment", color_discrete_sequence=BW_COLORS, text="Rata_Rata_GPA_Change")
        fig.update_traces(marker_line_color="black", marker_line_width=1, texttemplate="%{text:.3f}", textposition="outside")
        st.plotly_chart(apply_bw_layout(fig, "Rata-rata GPA Change per AI Usage Segment"), use_container_width=True)

    st.dataframe(gpa_segment, use_container_width=True)

with tab_mental:
    st.subheader("Kesehatan Mental")
    c1, c2 = st.columns(2)

    with c1:
        burnout_policy = filtered.groupby(["Institutional_Policy", "Burnout_Risk_Level"]).size().reset_index(name="Jumlah Mahasiswa")
        fig = px.bar(burnout_policy, x="Institutional_Policy", y="Jumlah Mahasiswa", color="Burnout_Risk_Level", barmode="stack", color_discrete_sequence=BW_COLORS)
        fig.update_traces(marker_line_color="black", marker_line_width=1)
        st.plotly_chart(apply_bw_layout(fig, "Distribusi Burnout Risk per Institutional Policy"), use_container_width=True)

    with c2:
        anxiety_policy = filtered.groupby("Institutional_Policy", as_index=False).agg(
            Rata_Rata_Anxiety=("Anxiety_Level_During_Exams", "mean"),
            Rata_Rata_Dependency=("Perceived_AI_Dependency", "mean")
        )
        fig = go.Figure()
        fig.add_trace(go.Bar(x=anxiety_policy["Institutional_Policy"], y=anxiety_policy["Rata_Rata_Anxiety"], name="Anxiety", marker=dict(color="white", line=dict(color="black", width=1))))
        fig.add_trace(go.Bar(x=anxiety_policy["Institutional_Policy"], y=anxiety_policy["Rata_Rata_Dependency"], name="AI Dependency", marker=dict(color="#888888", line=dict(color="black", width=1))))
        fig.update_layout(barmode="group")
        st.plotly_chart(apply_bw_layout(fig, "Rata-rata Anxiety dan Dependency per Policy"), use_container_width=True)

with tab_retention:
    st.subheader("Retensi Pengetahuan")
    c1, c2 = st.columns([2, 1])

    with c1:
        fig = px.scatter(
            filtered,
            x="Perceived_AI_Dependency",
            y="Skill_Retention_Score",
            color="AI Usage Segment",
            opacity=0.35,
            color_discrete_sequence=BW_COLORS,
            hover_data=["Major_Category", "Year_of_Study", "Institutional_Policy", "Burnout_Risk_Level"]
        )
        fig.update_traces(marker=dict(line=dict(width=0.5, color="black")))
        st.plotly_chart(apply_bw_layout(fig, "Skill Retention Score vs AI Dependency"), use_container_width=True)

    with c2:
        corr_retention_dependency = filtered["Skill_Retention_Score"].corr(filtered["Perceived_AI_Dependency"])
        corr_retention_hours = filtered["Skill_Retention_Score"].corr(filtered["Weekly_GenAI_Hours"])
        st.metric("Korelasi Retention vs Dependency", f"{corr_retention_dependency:.4f}")
        st.metric("Korelasi Retention vs GenAI Hours", f"{corr_retention_hours:.4f}")

with tab_risk:
    st.subheader("Profil Risiko")
    c1, c2 = st.columns(2)

    with c1:
        risk_count = filtered["Risk Profile"].value_counts().reset_index()
        risk_count.columns = ["Risk Profile", "Jumlah Mahasiswa"]
        fig = px.bar(risk_count, x="Risk Profile", y="Jumlah Mahasiswa", color="Risk Profile", color_discrete_sequence=BW_COLORS)
        fig.update_traces(marker_line_color="black", marker_line_width=1)
        st.plotly_chart(apply_bw_layout(fig, "Jumlah Mahasiswa berdasarkan Risk Profile"), use_container_width=True)

    with c2:
        risk_by_segment = filtered.groupby(["AI Usage Segment", "Risk Profile"]).size().reset_index(name="Jumlah Mahasiswa")
        fig = px.bar(risk_by_segment, x="AI Usage Segment", y="Jumlah Mahasiswa", color="Risk Profile", barmode="stack", color_discrete_sequence=BW_COLORS)
        fig.update_traces(marker_line_color="black", marker_line_width=1)
        st.plotly_chart(apply_bw_layout(fig, "Risk Profile per AI Usage Segment"), use_container_width=True)

with tab_brd:
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

st.markdown("---")
st.subheader("Export Data Terfilter")
csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download data terfilter sebagai CSV",
    data=csv,
    file_name="filtered_dashboard_data.csv",
    mime="text/csv"
)
