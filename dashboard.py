import streamlit as st
# Branding / Header
st.set_page_config(page_title="Asset Operations Dashboard", layout="wide")
st.title("Asset Operations Dashboard")
st.caption("Built by Carlos Castro • For AAM interview purposes with John Spratley")
st.markdown("---")

import pandas as pd
import plotly.express as px

# Set the title
st.title("Asset Operations Dashboard")

# Sidebar Navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to:", ("Financial", "Performance", "Compliance", "Operational"))

# --- Financial Section ---
if section == "Financial":
    st.header("💵 Financial Analysis & Support")

    uploaded_file = st.file_uploader("Upload Financial Data (Excel)", type=["xlsx", "xls"], key="financial_upload")

    if uploaded_file is not None:
        try:
            df_financial = pd.read_excel(uploaded_file)
            st.session_state["financial_df"] = df_financial
            st.success("✅ File uploaded and saved in memory.")
        except Exception as e:
            st.error(f"❌ Could not read file: {e}")

    if "financial_df" in st.session_state:
        df_financial = st.session_state["financial_df"]

        st.subheader("📊 Edit Financial Table")
        edited_df = st.data_editor(df_financial, num_rows="dynamic", use_container_width=True, key="financial_editor")

        if "RSCR" in edited_df.columns and "DSCR" in edited_df.columns:
            st.metric(
                label="Avg RSCR",
                value=f"{edited_df['RSCR'].mean():.2f}",
                help="Reserve Service Coverage Ratio"
            )
            st.metric(
                label="Avg DSCR",
                value=f"{edited_df['DSCR'].mean():.2f}",
                help="Debt Service Coverage Ratio"
            )

        if "Cash Flow" in edited_df.columns:
            st.metric(
                label="Total Cash Flow",
                value=f"${edited_df['Cash Flow'].sum():,.0f}",
                help="Total project-level cash flow"
            )

        # Download Button
        csv = edited_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Edited Financial Data as CSV",
            data=csv,
            file_name="financial_data.csv",
            mime='text/csv'
        )
    else:
        st.info("Upload a financial Excel file to get started.")

# --- Performance Section ---
elif section == "Performance":
    st.header("📈 Performance Monitoring Support")

    uploaded_perf = st.file_uploader("Upload Performance Data (Excel)", type=["xlsx", "xls"], key="performance_upload")

    if uploaded_perf is not None:
        try:
            df_perf = pd.read_excel(uploaded_perf)
            st.session_state["performance_df"] = df_perf
            st.success("✅ File uploaded and saved in memory.")
        except Exception as e:
            st.error(f"❌ Could not read file: {e}")

    if "performance_df" in st.session_state:
        df_perf = st.session_state["performance_df"]

        st.subheader("📊 Edit Generation Data")
        edited_df = st.data_editor(df_perf, num_rows="dynamic", use_container_width=True, key="performance_editor")

        if "Actual Generation (MWh)" in edited_df.columns and "Forecasted Generation (MWh)" in edited_df.columns:
            accuracy = 100 * (edited_df["Actual Generation (MWh)"] / edited_df["Forecasted Generation (MWh)"]).mean()
            st.metric("Average Forecast Accuracy", f"{accuracy:.1f}%", help="Higher is better. 100% = actual matches forecast.")

            st.subheader("📈 Actual vs Forecasted")
            fig = px.line(edited_df, x=edited_df.columns[0], y=["Actual Generation (MWh)", "Forecasted Generation (MWh)"])
            st.plotly_chart(fig)

        # Download Button
        csv = edited_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Edited Performance Data as CSV",
            data=csv,
            file_name="performance_data.csv",
            mime='text/csv'
        )
    else:
        st.info("Upload an Excel file to view generation performance.")

# --- Compliance Section ---
elif section == "Compliance":
    st.header("📋 Contract & Regulatory Compliance")

    uploaded_compliance = st.file_uploader("Upload Compliance Tracker (Excel)", type=["xlsx", "xls"], key="compliance_upload")

    if uploaded_compliance is not None:
        try:
            df_compliance = pd.read_excel(uploaded_compliance)
            st.session_state["compliance_df"] = df_compliance
            st.success("✅ Compliance tracker loaded and stored.")
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")

    if "compliance_df" in st.session_state:
        df_compliance = st.session_state["compliance_df"]

        st.subheader("📝 Edit Compliance Items")
        edited_df = st.data_editor(df_compliance, num_rows="dynamic", use_container_width=True, key="compliance_editor")

        if "Status" in edited_df.columns:
            completed = (edited_df["Status"] == "Completed").sum()
            total = len(edited_df)
            percent = 100 * completed / total
            st.metric("Completion Rate", f"{percent:.1f}%", help="Percentage of compliance tasks marked as Completed.")

        # Download Button
        csv = edited_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Edited Compliance Data as CSV",
            data=csv,
            file_name="compliance_data.csv",
            mime='text/csv'
        )
    else:
        st.info("Upload an Excel file to track compliance deadlines.")

# --- Operational Section ---
elif section == "Operational":
    st.header("⚙️ Operational Awareness")

    uploaded_ops = st.file_uploader("Upload Outage & Availability Data (Excel)", type=["xlsx", "xls"], key="operational_upload")

    if uploaded_ops is not None:
        try:
            df_ops = pd.read_excel(uploaded_ops)
            st.session_state["operational_df"] = df_ops
            st.success("✅ Operational data uploaded and saved.")
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")

    if "operational_df" in st.session_state:
        df_ops = st.session_state["operational_df"]

        st.subheader("🔧 Edit Outage Records")
        edited_df = st.data_editor(df_ops, num_rows="dynamic", use_container_width=True, key="operational_editor")

        if "Availability (%)" in edited_df.columns:
            avg_avail = edited_df["Availability (%)"].mean()
            st.metric("Avg Availability", f"{avg_avail:.2f}%", help="Average operational availability across all entries.")

        if "Duration (hours)" in edited_df.columns:
            total_downtime = edited_df["Duration (hours)"].sum()
            st.metric("Total Downtime", f"{total_downtime:.1f} hrs", help="Sum of all recorded outages.")

        # Download Button
        csv = edited_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Edited Operational Data as CSV",
            data=csv,
            file_name="operational_data.csv",
            mime='text/csv'
        )
    else:
        st.info("Upload outage and availability data to track operations.")

# Footer
st.write("---")
st.write("Made by Carlos Castro")
