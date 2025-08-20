import streamlit as st
import pandas as pd

st.title("💬 Employee Engagement Agent")

st.write("Analyze engagement levels and suggest actions.")

# Manual Entry
name = st.text_input("Employee Name")
engagement = st.slider("Engagement Level (1=Low, 5=High)", 1, 5, 3)
feedback = st.text_area("Feedback (optional)")

if st.button("Analyze Engagement"):
    st.subheader(f"Engagement Analysis for {name if name else 'Employee'}")
    if engagement <= 2:
        st.write("⚠️ Disengaged: Schedule one-on-one and provide support.")
    elif engagement == 3:
        st.write("🙂 Neutral: Encourage participation in team activities.")
    else:
        st.write("✅ Highly Engaged: Recognize and reward performance.")

# Bulk Upload
st.subheader("Upload Engagement Survey (CSV)")
uploaded_file = st.file_uploader("Upload file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    def analyze(row):
        if row["Engagement"] <= 2:
            return "Disengaged"
        elif row["Engagement"] == 3:
            return "Neutral"
        else:
            return "Engaged"

    df["Analysis"] = df.apply(analyze, axis=1)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Engagement Report", data=csv, file_name="engagement_report.csv")
