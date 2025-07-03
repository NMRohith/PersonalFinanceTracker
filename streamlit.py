import streamlit as st
import pandas as pd

st.set_page_config(page_title="💰 Personal Finance Tracker", layout="wide")

st.markdown("""
    <style>
        .title-style {
            font-size:36px;
            font-weight:bold;
            color:#4B8BBE;
        }
        .card {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-style">💸 Personal Finance & Expense Tracker</div>', unsafe_allow_html=True)
st.markdown("Track your spending, filter transactions, and visualize your financial habits 📊")
st.markdown("---")

category = st.sidebar.selectbox("📂 Choose Category", ['Rent / Housing', 'Groceries', 'Utilities (Electricity, Water, Gas)','Internet & Mobile','Transportation (Fuel, Bus, Metro, Auto)'])
name = st.sidebar.text_input("👤 Enter Name")
number = st.sidebar.number_input("💵 Enter Amount", min_value=0.0)
date = st.sidebar.date_input("📅 Enter Date")
Payment = st.sidebar.radio("💳 Payment Method", ["💸 Cash on Delivery", "📲 UPI", "💳 Card"])

if "form_data" not in st.session_state:
    st.session_state.form_data = []

if st.sidebar.button("✅ Submit"):
    if name.strip() == "":
        st.sidebar.warning("⚠️ Name cannot be empty.")
    else:
        new_entry = {
            "Name": name,
            "Category": category,
            "Amount": number,
            "Date": date,
            "Payment Method": Payment
        }
        st.session_state.form_data.append(new_entry)

if st.session_state.form_data:
    df = pd.DataFrame(st.session_state.form_data)

    st.subheader("🧾 All Expense Entries")
    st.dataframe(df, use_container_width=True)

    with st.expander("🎛️ Filter Options"):
        selected_date = st.date_input("📅 Filter by Date", max_value=df["Date"].max(), min_value=df["Date"].min())
        selected_rate = st.slider("📈 Max Amount Filter", 0, 100, 50)
        selected_name = st.multiselect("👥 Filter by Name", df["Name"].unique())

    datafilter = df[
        (df["Date"] == selected_date) &
        (df["Amount"] <= selected_rate)
    ]
    if selected_name:
        datafilter = datafilter[datafilter["Name"].isin(selected_name)]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔎 Filtered Results")
    st.dataframe(datafilter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("💰 Total Amount", f"₹{datafilter['Amount'].sum():.2f}", delta="5%")
    with col2:
        st.metric("🧾 Total Entries", len(datafilter))

    st.subheader("📊 Expenses by Category")
    st.bar_chart(datafilter.groupby("Category")["Amount"].sum(), use_container_width=True)

    st.subheader("📉 Spending Trend Over Time")
    st.line_chart(datafilter.groupby("Date")["Amount"].sum(), use_container_width=True)

    st.markdown("---")
    st.caption("🚀 Built with ❤️ using Streamlit")

else:
    st.info("🚫 No entries yet. Submit your first expense using the form on the left.")
