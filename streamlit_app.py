import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration & Professional Branding
st.set_page_config(page_title="UNICEF Kenya: Upstream Results", layout="wide")

# Custom CSS for the high-fidelity 'Card' look
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border-left: 5px solid #0083C4;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    h1, h2, h3 { color: #0083C4 !important; font-family: 'Arial', sans-serif; }
    .stDivider { border-top: 2px solid #0083C4; }
    </style>
    """, unsafe_allow_html=True)

# 2. Establish External Snowflake Connection
# This uses the 'Secrets' you will set up in the Streamlit Cloud dashboard
conn = st.connection("snowflake")

# Helper function to fetch data from Snowflake with caching for performance
@st.cache_data(ttl=600)
def load_snowflake_data(query):
    return conn.query(query)

# --- HERO SECTION ---
st.title("🇰🇪 UNICEF Kenya: Upstream Results & Enabling Environment")
st.markdown("##### Strategic Monitoring & Results-Based Management Dashboard")
st.write("---")

# --- LAYER 1: NATIONAL IMPACT (The 'Why') ---
st.markdown("### **Layer 1: National Impact & Outcome Trends**")

# Query the Impact Trends table
impact_query = "SELECT * FROM UNICEF_PME.KENYA_DASHBOARD.IMPACT_TRENDS"
impact_df = load_snowflake_data(impact_query)

# Create 4 columns for KPIs
m1, m2, m3, m4 = st.columns(4)
metrics = [m1, m2, m3, m4]

for i, row in impact_df.iterrows():
    val = f"{row['CURRENT_VALUE']}{'%' if row['UNIT'] == 'Percentage' else ''}"
    metrics[i].metric(
        label=row['INDICATOR_NAME'], 
        value=val, 
        delta=row['TREND_DIRECTION'],
        help=f"SDG Target: {row['TARGET_VALUE']}"
    )

st.write("")

# --- LAYER 2: SYSTEMIC RESULTS (The 'Contribution') ---
st.markdown("### **Layer 2: Upstream Systemic Results (UNICEF Contribution)**")

col_a, col_b = st.columns([3, 2])

with col_a:
    st.markdown("#### **Pillar A: CRC & Children Act 2022 Accountability**")
    
    # Query the Policy Tracker table
    policy_query = "SELECT * FROM UNICEF_PME.KENYA_DASHBOARD.POLICY_TRACKER"
    policy_df = load_snowflake_data(policy_query)
    
    # Visual: Horizontal Accountability Bar Chart
    fig_policy = px.bar(
        policy_df, 
        y="CRC_PRINCIPLE", 
        x="PROGRESS_PCT", 
        orientation='h',
        color="PROGRESS_PCT",
        color_continuous_scale="Blues",
        text="CHILDREN_ACT_SECTION",
        labels={"PROGRESS_PCT": "Implementation %", "CRC_PRINCIPLE": ""},
        height=350
    )
    fig_policy.update_layout(margin=dict(l=0, r=0, t=10, b=10), showlegend=False)
    st.plotly_chart(fig_policy, use_container_width=True)

with col_b:
    st.markdown("#### **Pillar B: Systems & Bottlenecks**")
    st.error("**Exchequer Delays:** High impact on Turkana WASH projects.")
    st.warning("**Data Gap:** DHIS2 reporting lag in North Eastern region.")
    st.info("**Policy Milestone:** Section 20 guidelines successfully gazetted.")
    
    st.write("**National System Reporting Timeliness**")
    st.progress(0.94, text="94% Reporting (Target: 90%)")

# --- LAYER 3: CONTEXTUAL AUDIT ---
st.write("---")
with st.expander("🔎 Deep-Dive: Raw Results Data & Policy Sections"):
    st.dataframe(policy_df, use_container_width=True)
