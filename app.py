import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="💬 Employee Engagement Agent", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
    }
    .main {
        background: #ffffffcc;
        padding: 20px;
        border-radius: 15px;
    }
    h1, h2, h3 {
        color: #333333 !important;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton button {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        border-radius: 10px;
        height: 3em;
        font-size: 16px;
        font-weight: bold;
    }
    .stMetric {
        background: #f0f8ff;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- TITLE & DESCRIPTION ---
st.title("💬 Employee Engagement Agent")
st.write("✨ Analyze employee engagement, get actionable suggestions, and explore colorful interactive dashboards.")

# --- MANUAL ENTRY ---
st.header("📝 Manual Entry")
name = st.text_input("Employee Name")
engagement = st.slider("Engagement Level (1=Low, 5=High)", 1, 5, 3)
feedback = st.text_area("Feedback (optional)")

if st.button("🔍 Analyze Engagement"):
    st.subheader(f"Engagement Analysis for {name if name else 'Employee'}")
    if engagement <= 2:
        st.error("⚠️ Disengaged: Schedule one-on-one and provide support.")
    elif engagement == 3:
        st.info("🙂 Neutral: Encourage participation in team activities.")
    else:
        st.success("✅ Highly Engaged: Recognize and reward performance.")
    if feedback:
        st.write(f"📝 Feedback noted: {feedback}")

# --- BULK UPLOAD ---
st.header("📊 Bulk Upload & Interactive Dashboard")
st.write("Upload a CSV file with columns: `Name`, `Engagement`, and optionally `Department`, `Team`, or `Date`.")

uploaded_file = st.file_uploader("📂 Upload Engagement Survey CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Validate required columns
    if "Engagement" not in df.columns:
        st.error("CSV must contain an 'Engagement' column.")
    else:
        if "Department" not in df.columns:
            df["Department"] = "All"

        def analyze(row):
            if row["Engagement"] <= 2:
                return "Disengaged"
            elif row["Engagement"] == 3:
                return "Neutral"
            else:
                return "Engaged"

        df["Analysis"] = df.apply(analyze, axis=1)

        st.subheader("📋 Survey Data")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Engagement Report", csv, "engagement_report.csv", "text/csv")

        # --- INTERACTIVE FILTER ---
        st.subheader("🎯 Filter by Department/Team")
        departments = ["All"] + sorted(df["Department"].unique().tolist())
        selected_dept = st.selectbox("Select Department/Team", departments)
        if selected_dept != "All":
            filtered_df = df[df["Department"] == selected_dept]
        else:
            filtered_df = df

        st.write(f"Showing {len(filtered_df)} employees in {selected_dept} department/team.")
        st.dataframe(filtered_df)

        # --- ENGAGEMENT DISTRIBUTION (BAR) ---
        st.subheader("📊 Engagement Distribution")
        fig1 = px.histogram(filtered_df, x="Analysis", color="Analysis",
                            category_orders={"Analysis": ["Disengaged", "Neutral", "Engaged"]},
                            color_discrete_map={"Disengaged": "#FF6F61", "Neutral": "#FFD700", "Engaged": "#4CAF50"},
                            text_auto=True)
        fig1.update_layout(title="Employee Engagement Distribution", xaxis_title="Engagement Level", yaxis_title="Count")
        st.plotly_chart(fig1, use_container_width=True)

        # --- PIE CHART ---
        st.subheader("🥧 Engagement Breakdown")
        pie_data = filtered_df["Analysis"].value_counts().reset_index()
        fig2 = px.pie(pie_data, values="Analysis", names="index",
                      color="index", color_discrete_map={"Disengaged": "#FF6F61", "Neutral": "#FFD700", "Engaged": "#4CAF50"},
                      hole=0.3)
        fig2.update_traces(textinfo="percent+label")
        st.plotly_chart(fig2, use_container_width=True)

        # --- METRICS ---
        st.subheader("📌 Key Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("🌟 Avg Engagement", f"{filtered_df['Engagement'].mean():.2f} / 5")
        col2.metric("⚠️ Disengaged", str(len(filtered_df[filtered_df['Analysis'] == "Disengaged"])))
        col3.metric("✅ Engaged", str(len(filtered_df[filtered_df['Analysis'] == "Engaged"])))

        # --- AVG ENGAGEMENT BY DEPARTMENT ---
        st.subheader("🏢 Average Engagement by Department/Team")
        dept_avg = filtered_df.groupby("Department")["Engagement"].mean().reset_index()
        fig3 = px.bar(dept_avg, x="Department", y="Engagement", color="Engagement",
                      color_continuous_scale="Viridis", text_auto=True)
        fig3.update_layout(title="Average Engagement per Department")
        st.plotly_chart(fig3, use_container_width=True)

        # --- HEATMAP ---
        st.subheader("🔥 Engagement Heatmap (Departments vs Levels)")
        heatmap_data = pd.crosstab(filtered_df["Department"], filtered_df["Analysis"])
        fig4 = px.imshow(heatmap_data, text_auto=True, color_continuous_scale="Blues")
        fig4.update_layout(title="Engagement Levels Across Departments")
        st.plotly_chart(fig4, use_container_width=True)

        # --- TRENDS (if Date column exists) ---
        if "Date" in df.columns:
            st.subheader("📈 Engagement Trends Over Time")
            try:
                df["Date"] = pd.to_datetime(df["Date"])
                trend_df = df.groupby(["Date", "Department"])["Engagement"].mean().reset_index()
                fig5 = px.line(trend_df, x="Date", y="Engagement", color="Department", markers=True)
                fig5.update_layout(title="Engagement Trends by Department", yaxis_title="Avg Engagement Score")
                st.plotly_chart(fig5, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not plot trends: {e}")
