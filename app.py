import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- PAGE CONFIG ---
st.set_page_config(page_title="💬 Employee Engagement Agent", layout="wide")

# --- TITLE & DESCRIPTION ---
st.title("💬 Employee Engagement Agent")
st.write("Analyze employee engagement, get actionable suggestions, and explore interactive visual dashboards.")

# --- MANUAL ENTRY ---
st.header("Manual Entry")
name = st.text_input("Employee Name")
engagement = st.slider("Engagement Level (1=Low, 5=High)", 1, 5, 3)
feedback = st.text_area("Feedback (optional)")

if st.button("Analyze Engagement"):
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
st.header("Bulk Upload & Interactive Dashboard")
st.write("Upload a CSV file with columns: `Name`, `Engagement`, and optionally `Department` or `Team`.")

uploaded_file = st.file_uploader("Upload Engagement Survey CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Validate required columns
    if "Engagement" not in df.columns:
        st.error("CSV must contain an 'Engagement' column.")
    else:
        # Optional department column
        if "Department" not in df.columns:
            df["Department"] = "All"

        # Analysis function
        def analyze(row):
            if row["Engagement"] <= 2:
                return "Disengaged"
            elif row["Engagement"] == 3:
                return "Neutral"
            else:
                return "Engaged"

        df["Analysis"] = df.apply(analyze, axis=1)

        st.subheader("Survey Data")
        st.dataframe(df)

        # Download button
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Engagement Report",
            data=csv,
            file_name="engagement_report.csv",
            mime="text/csv"
        )

        # --- INTERACTIVE FILTER ---
        st.subheader("Filter by Department/Team")
        departments = ["All"] + sorted(df["Department"].unique().tolist())
        selected_dept = st.selectbox("Select Department/Team", departments)
        if selected_dept != "All":
            filtered_df = df[df["Department"] == selected_dept]
        else:
            filtered_df = df

        st.write(f"Showing {len(filtered_df)} employees in {selected_dept} department/team.")
        st.dataframe(filtered_df)

        # --- ENGAGEMENT BAR CHART ---
        st.subheader("Engagement Distribution")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.countplot(x="Analysis", data=filtered_df, palette="Set2",
                      order=["Disengaged", "Neutral", "Engaged"], ax=ax)
        ax.set_title("Employee Engagement Distribution")
        ax.set_xlabel("Engagement Level")
        ax.set_ylabel("Number of Employees")
        for p in ax.patches:
            ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', fontsize=12)
        st.pyplot(fig)

        # --- PIE CHART ---
        st.subheader("Engagement Breakdown (Pie Chart)")
        pie_data = filtered_df["Analysis"].value_counts()
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', colors=["#FF6F61", "#FFD700", "#4CAF50"], startangle=140)
        ax2.set_title("Engagement Categories")
        st.pyplot(fig2)

        # --- METRICS ---
        st.subheader("Key Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Engagement", f"{filtered_df['Engagement'].mean():.2f} / 5")
        col2.metric("Disengaged Count", str(len(filtered_df[filtered_df['Analysis'] == "Disengaged"])))
        col3.metric("Highly Engaged Count", str(len(filtered_df[filtered_df['Analysis'] == "Engaged"])))
