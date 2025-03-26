import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Streamlit page configuration
st.set_page_config(page_title="Traditional Companies vs. Startups Dashboard", layout="wide")

# Title and Introduction
st.title("Traditional Companies vs. Startups - Competitive Strategy Tracker")
st.markdown("Monitor strategies for traditional businesses to compete with startups in India, based on Indian Startup Funding data.")

# Load and Process Dataset
@st.cache_data
def load_and_process_data():
    df = pd.read_csv("startup_funding.csv")
    
    # Clean and convert AmountInUSD to Rs Lakh
    df["AmountInUSD"] = df["AmountInUSD"].str.replace(",", "").fillna(0).astype(float)
    df["AmountInRsLakh"] = df["AmountInUSD"] / 100000 * 83  # 1 USD = 83 Rs, 1M USD = 830 Lakh
    
    # Fix date column and extract month-year
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
    df["MonthYear"] = df["Date"].dt.strftime("%b %Y")
    
    # 1. Go Digital
    tech_df = df[df["IndustryVertical"].str.contains("Tech|E-commerce", case=False, na=False)]
    digital_data = pd.DataFrame({
        "Metric": ["App Cost (Rs Lakh)", "Sales Growth (%)", "Customer Reach"],
        "Value": [tech_df["AmountInRsLakh"].mean(), 12, len(tech_df)]  # 12% growth assumed
    })

    # 2. Cut Costs (assumed savings, e-commerce revenue)
    ecomm_df = df[df["IndustryVertical"].str.contains("E-commerce", case=False, na=False)]
    cost_data = pd.DataFrame({
        "Category": ["Rent", "Staff", "Inventory", "Pop-Up Sales"],
        "Cost Savings (%)": [20, 15, 10, 0],  # Assumed from PPT
        "Revenue (Rs Lakh)": [0, 0, 0, ecomm_df["AmountInRsLakh"].mean()]
    })

    # 3. Unique Value (trends over 4 months)
    monthly_df = df.groupby("MonthYear").agg({"AmountInRsLakh": "sum"}).reset_index().head(4)
    unique_value_data = pd.DataFrame({
        "Month": monthly_df["MonthYear"],
        "Retention Rate (%)": [70, 72, 75, 78],  # Simulated growth
        "Satisfaction Score": [4.2, 4.3, 4.5, 4.6]  # Simulated
    })

    # 4. Collaborate (top 2 investors)
    collab_df = df.groupby("InvestorsName").agg({"AmountInRsLakh": "sum"}).nlargest(2, "AmountInRsLakh").reset_index()
    collab_data = pd.DataFrame({
        "Partner": collab_df["InvestorsName"],
        "Revenue Share (Rs Lakh)": collab_df["AmountInRsLakh"],
        "Cost Savings (Rs Lakh)": collab_df["AmountInRsLakh"] * 0.1  # 10% savings assumed
    })

    # 5. Start Small (Delhi and Bangalore)
    pilot_df = df[df["CityLocation"].isin(["Delhi", "Bangalore"])].groupby("CityLocation").agg({"AmountInRsLakh": "mean"}).reset_index()
    pilot_data = pd.DataFrame({
        "City": pilot_df["CityLocation"],
        "Sales Growth (%)": [15, 10],  # Assumed from PPT
        "Pilot Cost (Rs Lakh)": pilot_df["AmountInRsLakh"]
    })

    return digital_data, cost_data, unique_value_data, collab_data, pilot_data

digital_data, cost_data, unique_value_data, collab_data, pilot_data = load_and_process_data()

# Sidebar Filters (placeholders)
st.sidebar.header("Filters")
time_period = st.sidebar.selectbox("Time Period", ["Monthly", "Quarterly"])
city = st.sidebar.selectbox("City", ["All", "Delhi", "Bangalore"])
industry = st.sidebar.selectbox("Industry", ["All", "Taxis", "Retail", "Hotels"])

# Dashboard Layout
col1, col2 = st.columns(2)

# Go Digital
with col1:
    st.subheader("1. Go Digital")
    st.write("Track adoption and impact of digital tools.")
    fig_digital = px.bar(digital_data[digital_data["Metric"] != "Customer Reach"], 
                         x="Metric", y="Value", title="Cost vs. Sales Growth")
    st.plotly_chart(fig_digital, use_container_width=True)
    st.write(f"Customer Reach: {int(digital_data.loc[2, 'Value'])} startups")

# Cut Costs
with col2:
    st.subheader("2. Cut Costs")
    st.write("Monitor cost-saving measures.")
    fig_cost = px.pie(cost_data[cost_data["Cost Savings (%)"] > 0], 
                      values="Cost Savings (%)", names="Category", title="Cost Savings Breakdown")
    st.plotly_chart(fig_cost, use_container_width=True)
    st.write(f"Pop-Up Sales Revenue: Rs {cost_data.loc[3, 'Revenue (Rs Lakh)']:.2f} Lakh")

# Unique Value
with col1:
    st.subheader("3. Unique Value")
    st.write("Measure personalized service impact.")
    fig_retention = px.line(unique_value_data, x="Month", y="Retention Rate (%)", 
                            title="Customer Retention Over Time")
    st.plotly_chart(fig_retention, use_container_width=True)
    latest_satisfaction = unique_value_data["Satisfaction Score"].iloc[-1]
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number", value=latest_satisfaction, 
        title={'text': "Customer Satisfaction (Latest)"}, 
        gauge={'axis': {'range': [0, 5]}, 'bar': {'color': "darkblue"}}
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

# Collaborate
with col2:
    st.subheader("4. Collaborate")
    st.write("Track partnerships with startups.")
    fig_collab = px.pie(collab_data, values="Revenue Share (Rs Lakh)", names="Partner", 
                        title="Revenue Share from Collaborations", hole=0.3)
    st.plotly_chart(fig_collab, use_container_width=True)
    st.dataframe(collab_data)

# Start Small
st.subheader("5. Start Small")
st.write("Evaluate pilot projects in one city.")
col3, col4 = st.columns(2)

with col3:
    fig_pilot = px.bar(pilot_data, x="City", y="Sales Growth (%)", title="Sales Growth in Pilot Cities")
    st.plotly_chart(fig_pilot, use_container_width=True)

with col4:
    readiness_score = 75  # Static for now
    st.write("Expansion Readiness Score")
    st.progress(readiness_score / 100)
    st.write(f"{readiness_score}% Ready")

# Key Takeaways
st.subheader("Key Takeaways")
st.markdown("""
- **Digital is Key**: Embrace digital tools.
- **Unique Value Matters**: Focus on what startups can't offer.
- **Start Small**: Test in one city.
- **Compete Smart**: Grow without huge funds.
""")

# Footer
st.markdown("---")
st.write("Built with Streamlit by [Your Team Name] | Data as of March 25, 2025 | Source: Indian Startup Funding (Kaggle)")
