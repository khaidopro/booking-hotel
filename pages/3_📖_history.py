import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Booking History",
    page_icon="📖",
    layout="wide",
)

# Function to load booking history
def load_booking_history(file_path):
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        st.error("No booking history found. Make sure 'bookings.xlsx' exists.")
        return None

# Display the booking history
st.title("📖 Booking History")

# Load the booking data
file_path = "bookings.xlsx"
booking_history = load_booking_history(file_path)

if booking_history is not None:
    st.subheader("Here is your booking history:")
    
    # Display data as a table
    st.dataframe(booking_history, use_container_width=True)

    # Add some insights (optional)
    st.markdown("### Insights:")
    st.write(f"**Total Bookings:** {len(booking_history)}")
    if "Price" in booking_history.columns:
        total_spent = booking_history["Price"].sum()
        st.write(f"**Total Spent:** ${total_spent:,.2f}")
else:
    st.write("You have no booking history at the moment.")