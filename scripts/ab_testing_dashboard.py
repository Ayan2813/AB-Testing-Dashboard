import streamlit as st
import mysql.connector
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import os

st.set_page_config(page_title="A/B Testing Dashboard", layout="wide")
st.title("A/B Testing Experiment Dashboard")

# --- Load Data from MySQL ---
@st.cache_data
def load_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Minu1981",
        database="ab_testing_db"
    )
    query = "SELECT * FROM experiment_data;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = load_data()

# --- Detect Date Column ---
date_col_candidates = ['date', 'created_at', 'timestamp', 'experiment_date']
date_col = None
for col in date_col_candidates:
    if col in df.columns:
        date_col = col
        df[date_col] = pd.to_datetime(df[col])
        break

# --- Sidebar ---
with st.sidebar.expander("Filter & Data Options", expanded=True):
    # CSV Upload
    st.subheader("Upload New Experiment Data")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        try:
            new_data = pd.read_csv(uploaded_file)
            required_cols = ['group_name', 'converted', 'device', 'country', 'traffic_source']
            if not all(col in new_data.columns for col in required_cols):
                st.error(f"CSV must include columns: {', '.join(required_cols)}")
            else:
                date_col_in_csv = [c for c in ['date','created_at','timestamp','experiment_date'] if c in new_data.columns]
                if date_col_in_csv:
                    new_data[date_col_in_csv[0]] = pd.to_datetime(new_data[date_col_in_csv[0]])
                    date_col = date_col_in_csv[0]
                df = new_data.copy()
                st.success("CSV loaded successfully!")
        except Exception as e:
            st.error(f"Error loading CSV: {e}")

    # Date filter
    if date_col:
        start_date, end_date = st.date_input(
            "Select Date Range",
            [df[date_col].min(), df[date_col].max()]
        )
    else:
        start_date = end_date = None
        st.info("No date column found in the data")

    # Device filter
    device_options = ['All'] + list(df['device'].unique())
    selected_device = st.selectbox("Select Device", device_options)

    # Country filter
    country_options = ['All'] + list(df['country'].unique())
    selected_country = st.selectbox("Select Country", country_options)

    # Traffic Source filter
    traffic_options = ['All'] + list(df['traffic_source'].unique())
    selected_traffic = st.selectbox("Select Traffic Source", traffic_options)

    # Group filter
    groups = st.multiselect("Select Groups", options=df['group_name'].unique(), default=list(df['group_name'].unique()))

# --- Apply Filters ---
filtered_df = df.copy()
if date_col:
    filtered_df = filtered_df[
        (filtered_df[date_col] >= pd.to_datetime(start_date)) &
        (filtered_df[date_col] <= pd.to_datetime(end_date))
    ]
if selected_device != 'All':
    filtered_df = filtered_df[filtered_df['device'] == selected_device]
if selected_country != 'All':
    filtered_df = filtered_df[filtered_df['country'] == selected_country]
if selected_traffic != 'All':
    filtered_df = filtered_df[filtered_df['traffic_source'] == selected_traffic]
filtered_df = filtered_df[filtered_df['group_name'].isin(groups)]

# --- Metrics Calculation ---
metrics = filtered_df.groupby('group_name')['converted'].agg(['count','sum']).rename(columns={'count':'total_users','sum':'conversions'})
metrics['conversion_rate'] = metrics['conversions'] / metrics['total_users']

if len(metrics) == 2:
    uplift = metrics.iloc[1]['conversion_rate'] - metrics.iloc[0]['conversion_rate']
    count = metrics['conversions'].values
    nobs = metrics['total_users'].values
    z_stat, p_value = proportions_ztest(count, nobs)
    significance = "Variant B Wins" if (p_value < 0.05 and uplift > 0) else "No Significant Difference"
    hypothesis_text = f"Variant {'B' if uplift > 0 else 'A'} beats {'A' if uplift > 0 else 'B'} (p = {p_value:.4f})"
else:
    uplift = z_stat = p_value = None
    significance = "N/A"
    hypothesis_text = "N/A"

# --- Display Metrics ---
st.subheader("Experiment Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Uplift (B - A)", f"{uplift:.2%}" if uplift is not None else "N/A")
col2.metric("Z-statistic", f"{z_stat:.4f}" if z_stat is not None else "N/A")
col3.metric("P-value", f"{p_value:.4f}" if p_value is not None else "N/A")
col4.metric("Significance", significance)
st.markdown(f"**Hypothesis Summary:** {hypothesis_text}")
st.dataframe(metrics.style.format({"conversion_rate": "{:.2%}"}))

# --- Visualization ---
st.subheader("Conversion Rate by Group")
fig, ax = plt.subplots()
sns.barplot(x=metrics.index, y=metrics['conversion_rate']*100, palette="viridis", ax=ax)
ax.set_ylabel("Conversion Rate (%)")
ax.set_xlabel("Group Name")
st.pyplot(fig)

# --- Export Options ---
st.sidebar.subheader("Export Report")

# CSV download
csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("Download Filtered Data as CSV", data=csv_data, file_name="filtered_experiment_data.csv", mime="text/csv")

# PDF download
def generate_pdf(metrics, significance, hypothesis_text, chart_path='chart.png'):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "A/B Test Report", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Significance: {significance}", ln=True)
    pdf.cell(0, 10, f"Hypothesis: {hypothesis_text}", ln=True)
    pdf.ln(5)
    for idx, row in metrics.iterrows():
        pdf.cell(0, 8, f"{idx} - Users: {row['total_users']}, Conversions: {row['conversions']}, Conversion Rate: {row['conversion_rate']:.2%}", ln=True)
    if os.path.exists(chart_path):
        pdf.image(chart_path, x=10, y=None, w=180)
    pdf_file = "ab_test_report.pdf"
    pdf.output(pdf_file)
    return pdf_file

# Save chart and generate PDF
fig.savefig("chart.png")
pdf_file = generate_pdf(metrics, significance, hypothesis_text)
with open(pdf_file, "rb") as f:
    st.sidebar.download_button("Download Report as PDF", f, file_name="ab_test_report.pdf", mime="application/pdf")
