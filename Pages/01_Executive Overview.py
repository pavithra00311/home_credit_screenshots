import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Home Credit | Executive Overview",
    page_icon="💳",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.dashboard-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.dashboard-subtitle {
    color: #6b7280;
    font-size: 17px;
    margin-bottom: 25px;
}

.kpi-card {
    background-color: #ffffff !important;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    border: 1px solid #e5e7eb;
}

.kpi-title {
    color: #4b5563 !important;
    font-size: 14px;
    font-weight: 600;
}

.kpi-value {
    color: #111827 !important;
    font-size: 27px;
    font-weight: 800;
    margin-top: 7px;
}

.section-title {
    font-size: 24px;
    font-weight: 750;
    margin-top: 25px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():

    # Get the main project folder
    base_dir = Path(__file__).resolve().parent.parent

    # First location: project/data/application_train.csv
    data_path = base_dir / "data" / "application_train.csv"

    # Second location: project/application_train.csv
    if not data_path.exists():
        data_path = base_dir / "application_train.csv"

    # If file is still not found
    if not data_path.exists():
        st.error(
            "❌ application_train.csv was not found.\n\n"
            f"Python searched here:\n{data_path}"
        )
        st.stop()

    try:
        df = pd.read_csv(data_path)
        return df

    except Exception as e:
        st.error(
            f"❌ Error while reading the CSV file: {e}"
        )
        st.stop()


df = load_data()


# =========================================================
# CHECK REQUIRED COLUMNS
# =========================================================
required_columns = [
    "TARGET",
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        "❌ The following required columns are missing from the dataset:"
    )

    st.write(missing_columns)

    st.stop()


# =========================================================
# DATA CLEANING
# =========================================================
df["TARGET"] = pd.to_numeric(
    df["TARGET"],
    errors="coerce"
)

df["AMT_INCOME_TOTAL"] = pd.to_numeric(
    df["AMT_INCOME_TOTAL"],
    errors="coerce"
)

df["AMT_CREDIT"] = pd.to_numeric(
    df["AMT_CREDIT"],
    errors="coerce"
)

df["AMT_ANNUITY"] = pd.to_numeric(
    df["AMT_ANNUITY"],
    errors="coerce"
)


# =========================================================
# HEADER
# =========================================================
st.markdown(
    '<div class="dashboard-title">💳 Home Credit Risk Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Executive overview of customer applications, financial exposure and default risk'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# KPI CALCULATIONS
# =========================================================
total_applications = len(df)

default_customers = int(
    (df["TARGET"] == 1).sum()
)

non_default_customers = int(
    (df["TARGET"] == 0).sum()
)

default_rate = (
    default_customers / total_applications * 100
    if total_applications > 0
    else 0
)

average_income = df["AMT_INCOME_TOTAL"].mean()

average_credit = df["AMT_CREDIT"].mean()

average_annuity = df["AMT_ANNUITY"].mean()


# =========================================================
# KPI CARDS
# =========================================================
col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">TOTAL APPLICATIONS</div>
            <div class="kpi-value">{total_applications:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">DEFAULT CUSTOMERS</div>
            <div class="kpi-value">{default_customers:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">DEFAULT RATE</div>
            <div class="kpi-value">{default_rate:.2f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">NON-DEFAULT CUSTOMERS</div>
            <div class="kpi-value">{non_default_customers:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# FINANCIAL SUMMARY
# =========================================================
st.markdown(
    '<div class="section-title">💰 Financial Snapshot</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Average Income",
        f"{average_income:,.0f}"
    )

with col2:

    st.metric(
        "Average Credit",
        f"{average_credit:,.0f}"
    )

with col3:

    st.metric(
        "Average Annuity",
        f"{average_annuity:,.0f}"
    )


# =========================================================
# DEFAULT DISTRIBUTION
# =========================================================
st.markdown(
    '<div class="section-title">📊 Application Risk Distribution</div>',
    unsafe_allow_html=True
)

risk_data = pd.DataFrame({
    "Risk Status": [
        "Non-Default",
        "Default"
    ],
    "Customers": [
        non_default_customers,
        default_customers
    ]
})


fig_risk = px.pie(
    risk_data,
    names="Risk Status",
    values="Customers",
    hole=0.55,
    title="Default vs Non-Default Applications"
)

fig_risk.update_layout(
    height=420,
    showlegend=True
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)


# =========================================================
# 3D FINANCIAL RISK ANALYSIS
# =========================================================
st.markdown(
    '<div class="section-title">🌐 3D Financial Risk Landscape</div>',
    unsafe_allow_html=True
)

st.write(
    "Explore the relationship between customer income, credit amount "
    "and annuity while identifying default patterns."
)


# Sample data to prevent huge charts / Streamlit MessageSizeError
sample_size = min(
    5000,
    len(df)
)

df_sample = df.sample(
    n=sample_size,
    random_state=42
)


# Remove missing values for 3D visualization
df_sample = df_sample.dropna(
    subset=[
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY",
        "TARGET"
    ]
)


# Create 3D chart
fig_3d = px.scatter_3d(
    df_sample,
    x="AMT_INCOME_TOTAL",
    y="AMT_CREDIT",
    z="AMT_ANNUITY",
    color="TARGET",
    size="AMT_CREDIT",
    hover_data=[
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY",
        "TARGET"
    ],
    title="Income × Credit × Annuity Risk Map"
)


fig_3d.update_layout(
    height=700,
    scene=dict(
        xaxis_title="Income",
        yaxis_title="Credit Amount",
        zaxis_title="Annuity"
    )
)


st.plotly_chart(
    fig_3d,
    use_container_width=True
)


# =========================================================
# CREDIT DISTRIBUTION
# =========================================================
st.markdown(
    '<div class="section-title">💵 Credit Amount Distribution</div>',
    unsafe_allow_html=True
)

credit_data = df[
    ["AMT_CREDIT", "TARGET"]
].dropna()


credit_data = credit_data.sample(
    n=min(5000, len(credit_data)),
    random_state=42
)


fig_credit = px.histogram(
    credit_data,
    x="AMT_CREDIT",
    color="TARGET",
    nbins=40,
    title="Credit Amount Distribution by Risk"
)


fig_credit.update_layout(
    height=450
)


st.plotly_chart(
    fig_credit,
    use_container_width=True
)


# =========================================================
# INCOME VS DEFAULT
# =========================================================
st.markdown(
    '<div class="section-title">📈 Income vs Default Risk</div>',
    unsafe_allow_html=True
)


income_risk = (
    df.groupby("TARGET")["AMT_INCOME_TOTAL"]
    .mean()
    .reset_index()
)


income_risk["Risk Status"] = income_risk["TARGET"].map({
    0: "Non-Default",
    1: "Default"
})


fig_income = px.bar(
    income_risk,
    x="Risk Status",
    y="AMT_INCOME_TOTAL",
    text_auto=".0f",
    title="Average Income by Risk Status"
)


fig_income.update_layout(
    height=450,
    xaxis_title="Risk Status",
    yaxis_title="Average Income"
)


st.plotly_chart(
    fig_income,
    use_container_width=True
)


# =========================================================
# DATASET INFORMATION
# =========================================================
st.markdown(
    '<div class="section-title">📋 Dataset Overview</div>',
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Rows",
        f"{df.shape[0]:,}"
    )


with col2:

    st.metric(
        "Columns",
        f"{df.shape[1]:,}"
    )


with col3:

    st.metric(
        "Missing Values",
        f"{int(df.isna().sum().sum()):,}"
    )


# =========================================================
# EXECUTIVE INSIGHTS
# =========================================================
st.markdown(
    '<div class="section-title">🚀 Executive Insights</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# INSIGHT 1: DEFAULT RATE
# ---------------------------------------------------------
if default_rate >= 15:

    st.warning(
        f"⚠️ **High Portfolio Risk:** "
        f"The overall default rate is {default_rate:.2f}%. "
        "This indicates a relatively high level of credit risk and "
        "suggests that stronger credit-risk assessment may be required."
    )

elif default_rate >= 10:

    st.warning(
        f"⚠️ **Moderate Portfolio Risk:** "
        f"The overall default rate is {default_rate:.2f}%. "
        "Risk monitoring and customer-level affordability assessment "
        "remain important."
    )

else:

    st.success(
        f"✅ **Lower Portfolio Risk:** "
        f"The overall default rate is {default_rate:.2f}%. "
        "The observed default level is comparatively lower, although "
        "individual high-risk applications should still be monitored."
    )


# ---------------------------------------------------------
# INSIGHT 2: CREDIT VS INCOME
# ---------------------------------------------------------
credit_income_ratio = (
    average_credit / average_income
    if average_income and average_income > 0
    else 0
)


if credit_income_ratio >= 5:

    st.warning(
        f"💰 **Affordability Risk:** "
        f"The average credit amount is approximately "
        f"{credit_income_ratio:.1f} times the average annual income. "
        "This highlights a potentially significant affordability "
        "consideration for the lending portfolio."
    )

elif credit_income_ratio >= 3:

    st.info(
        f"💰 **Affordability Consideration:** "
        f"The average credit amount is approximately "
        f"{credit_income_ratio:.1f} times the average income. "
        "Affordability should therefore be considered carefully "
        "when evaluating applications."
    )

else:

    st.success(
        f"💰 **Credit-to-Income Position:** "
        f"The average credit amount is approximately "
        f"{credit_income_ratio:.1f} times the average income, "
        "indicating comparatively lower credit-to-income exposure."
    )


# ---------------------------------------------------------
# INSIGHT 3: CUSTOMER RISK PROFILE
# ---------------------------------------------------------
default_share = (
    default_customers / total_applications * 100
    if total_applications > 0
    else 0
)


st.info(
    f"👥 **Customer Risk Profile:** "
    f"{default_customers:,} customers are classified as default, "
    f"representing {default_share:.2f}% of the total application portfolio. "
    f"The remaining {non_default_customers:,} applications are classified "
    f"as non-default."
)


# ---------------------------------------------------------
# INSIGHT 4: INCOME AND DEFAULT
# ---------------------------------------------------------
income_by_risk = (
    df.groupby("TARGET")["AMT_INCOME_TOTAL"]
    .mean()
)


if 0 in income_by_risk.index and 1 in income_by_risk.index:

    non_default_income = income_by_risk[0]

    default_income = income_by_risk[1]

    income_difference = (
        non_default_income - default_income
    )

    if income_difference > 0:

        st.info(
            f"📊 **Income & Risk:** "
            f"Non-default customers have a higher average income "
            f"({non_default_income:,.0f}) compared with default customers "
            f"({default_income:,.0f}). "
            "This suggests that income level may be useful for "
            "risk segmentation."
        )

    elif income_difference < 0:

        st.warning(
            f"📊 **Income & Risk:** "
            f"Default customers have a higher average income "
            f"({default_income:,.0f}) compared with non-default customers "
            f"({non_default_income:,.0f}). "
            "This indicates that income alone may not explain "
            "default behavior."
        )

    else:

        st.info(
            "📊 **Income & Risk:** "
            "Average income is similar between default and non-default "
            "customers, suggesting that other customer and financial "
            "characteristics should also be considered."
        )


# ---------------------------------------------------------
# INSIGHT 5: REPAYMENT BURDEN
# ---------------------------------------------------------
annuity_income_ratio = (
    average_annuity / average_income * 100
    if average_income and average_income > 0
    else 0
)


st.info(
    f"💳 **Repayment Burden:** "
    f"The average annuity represents approximately "
    f"{annuity_income_ratio:.2f}% of the average annual income. "
    "This provides an additional perspective on customer repayment "
    "capacity and affordability."
)


# ---------------------------------------------------------
# INSIGHT 6: TOTAL CREDIT EXPOSURE
# ---------------------------------------------------------
total_credit_exposure = (
    df["AMT_CREDIT"].sum()
)


st.warning(
    f"🏦 **Credit Exposure:** "
    f"The total requested credit represented in the dataset is "
    f"approximately {total_credit_exposure:,.0f}. "
    "This represents the overall financial exposure associated with "
    "the applications in the dataset."
)


# ---------------------------------------------------------
# INSIGHT 7: AVERAGE FINANCIAL PROFILE
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">💡 Financial Profile Summary</div>',
    unsafe_allow_html=True
)


profile_col1, profile_col2, profile_col3 = st.columns(3)


with profile_col1:

    st.metric(
        "Credit / Income",
        f"{credit_income_ratio:.2f}x"
    )


with profile_col2:

    st.metric(
        "Annuity / Income",
        f"{annuity_income_ratio:.2f}%"
    )


with profile_col3:

    st.metric(
        "Total Credit Exposure",
        f"{total_credit_exposure:,.0f}"
    )


# ---------------------------------------------------------
# INSIGHT 8: DATA QUALITY
# ---------------------------------------------------------
total_missing = int(
    df.isna().sum().sum()
)


if total_missing == 0:

    st.success(
        "🧹 **Data Quality:** "
        "The dataset contains no missing values, providing a complete "
        "base for the current dashboard analysis."
    )

else:

    st.warning(
        f"🧹 **Data Quality:** "
        f"The dataset contains {total_missing:,} missing values. "
        "Additional data-quality handling may be required before using "
        "all available variables for advanced risk modeling."
    )


# =========================================================
# MANAGEMENT RECOMMENDATION
# =========================================================
st.markdown(
    '<div class="section-title">🎯 Management Recommendation</div>',
    unsafe_allow_html=True
)


st.write(
    """
    **Recommended focus areas for credit-risk management:**
    
    • Monitor the overall default rate and the number of customers 
    entering default.
    
    • Evaluate credit affordability by comparing requested credit 
    amounts with customer income.
    
    • Consider annuity obligations when assessing repayment capacity.
    
    • Avoid relying on income alone when identifying high-risk customers.
    
    • Use the relationship between income, credit amount and annuity 
    as part of a broader risk-segmentation strategy.
    
    • Continue monitoring portfolio-level credit exposure to support 
    responsible lending decisions.
    """
)


# =========================================================
# FINAL EXECUTIVE SUMMARY
# =========================================================
st.markdown(
    '<div class="section-title">📌 Executive Summary</div>',
    unsafe_allow_html=True
)


st.success(
    f"""
    **Overall Portfolio Assessment**

    The Home Credit portfolio contains **{total_applications:,} applications**, 
    with **{default_customers:,} default customers** and an overall 
    default rate of **{default_rate:.2f}%**.

    The average customer income is **{average_income:,.0f}**, while the 
    average credit amount is **{average_credit:,.0f}** and the average 
    annuity is **{average_annuity:,.0f}**.

    The analysis indicates that credit-risk assessment should focus on 
    **default behavior, affordability, repayment burden and overall 
    credit exposure** rather than relying on a single financial metric.
    """
)


# =========================================================
# FOOTER
# =========================================================
st.caption(
    "Home Credit Risk Dashboard • Executive Overview"
)
