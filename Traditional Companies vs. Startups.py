import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Traditional Companies vs. Startups Dashboard", layout="wide")

st.title("Traditional Companies vs. Startups - Competitive Strategy Tracker")
st.markdown("Monitor strategies for traditional businesses to compete with startups in India and beyond.")

digital_data = pd.DataFrame({
    "Metric": ["App Cost (Rs Lakh)", "Sales Growth (%)", "Customer Reach"],
    "Value": [4, 12, 5000]
})

cost_data = pd.DataFrame({
    "Category": ["Rent", "Staff", "Inventory", "Pop-Up Sales"],
    "Cost Savings (%)": [20, 15, 10, 0],
    "Revenue (Rs Lakh)": [0, 0, 0, 3]
})

unique_value_data = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr"],
    "Retention Rate (%)": [70, 72, 75, 78],
    "Satisfaction Score": [4.2, 4.3, 4.5, 4.6]
})

collab_data = pd.DataFrame({
    "Partner": ["Startup A", "Startup B"],
    "Revenue Share (Rs Lakh)": [5, 3],
    "Cost Savings (Rs Lakh)": [1, 0.5]
})

pilot_data = pd.DataFrame({
    "City": ["Delhi", "Bangalore"],
    "Sales Growth (%)": [15, 10],
    "Pilot Cost (Rs Lakh)": [2, 1.5]
})

st.sidebar.header("Filters")
time_period = st.sidebar.selectbox("Time Period", ["Monthly", "Quarterly"])
city = st.sidebar.selectbox("City", ["All", "Delhi", "Bangalore"])
industry = st.sidebar.selectbox("Industry", ["All", "Taxis", "Retail", "Hotels"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Go Digital")
    st.write("Track adoption and impact of digital tools.")
    fig_digital = px.bar(digital_data[digital_data["Metric"] != "Customer Reach"], 
                         x="Metric", y="Value", title="Cost vs. Sales Growth")
    st.plotly_chart(fig_digital, use_container_width=True)
    st.write(f"Customer Reach: {digital_data.loc[2, 'Value']} users")

with col2:
    st.subheader("2. Cut Costs")
    st.write("Monitor cost-saving measures.")
    fig_cost = px.pie(cost_data[cost_data["Cost Savings (%)"] > 0], 
                      values="Cost Savings (%)", names="Category", title="Cost Savings Breakdown")
    st.plotly_chart(fig_cost, use_container_width=True)
    st.write(f"Pop-Up Sales Revenue: Rs {cost_data.loc[3, 'Revenue (Rs Lakh)']} Lakh")

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

with col2:
    st.subheader("4. Collaborate")
    st.write("Track partnerships with startups.")
    fig_collab = px.pie(collab_data, values="Revenue Share (Rs Lakh)", names="Partner", 
                        title="Revenue Share from Collaborations", hole=0.3)
    st.plotly_chart(fig_collab, use_container_width=True)
    st.dataframe(collab_data)

st.subheader("5. Start Small")
st.write("Evaluate pilot projects in one city.")
col3, col4 = st.columns(2)

with col3:
    fig_pilot = px.bar(pilot_data, x="City", y="Sales Growth (%)", title="Sales Growth in Pilot Cities")
    st.plotly_chart(fig_pilot, use_container_width=True)

with col4:
    readiness_score = 75
    st.write("Expansion Readiness Score")
    st.progress(readiness_score / 100)
    st.write(f"{readiness_score}% Ready")

st.subheader("Key Takeaways")
st.markdown("""
- **Digital is Key**: Embrace digital tools.
- **Unique Value Matters**: Focus on what startups can't offer.
- **Start Small**: Test in one city.
- **Compete Smart**: Grow without huge funds.
""")

st.markdown("---")
st.write("Built with Streamlit by [Your Team Name] | Data as of March 25, 2025")
