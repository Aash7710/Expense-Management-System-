import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://localhost:8000"

def analytics_months_tab():
    # Fetch monthly summary data from the backend
    try:
        response = requests.get(f"{API_URL}/monthly_summary/")  # Updated endpoint
        response.raise_for_status()  # Raises an error for bad responses
        monthly_summary = response.json()

        # Ensure that the response is in the correct format
        if isinstance(monthly_summary, list):  # Assuming it should be a list of dictionaries
            df = pd.DataFrame(monthly_summary)
        else:
            st.error("Unexpected response format.")
            return

        # Rename columns for clarity
        df.rename(columns={
            "expense_month": "Month Number",
            "month_name": "Month Name",
            "total": "Total"
        }, inplace=True)

        # Sort DataFrame by Month Number
        df_sorted = df.sort_values(by="Month Number", ascending=True)  # Sort in ascending order
        df_sorted.set_index("Month Number", inplace=True)

        # Display title and chart
        st.subheader("Expense Breakdown By Months")
        st.bar_chart(data=df_sorted.set_index("Month Name")['Total'], width=0, height=0, use_container_width=True)

        # Format total values to two decimal places
        df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)

        # Display the sorted DataFrame
        st.table(df_sorted.sort_index())

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
