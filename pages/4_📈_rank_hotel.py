import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    layout="wide",
)

# Load data from bookings.xlsx
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        st.error("The bookings.xlsx file was not found.")
        return pd.DataFrame()

# Load the dataset
file_path = "bookings.xlsx"  # Update this path if needed
bookings_data = load_data(file_path)

# Check if data is loaded successfully
if not bookings_data.empty:
    st.title("Most Booked Hotels Ranking")

    # Ensure necessary columns exist in the dataset
    required_columns = ["Hotel Name", "City", "Country", "Room Type", "Price"]
    missing_columns = [col for col in required_columns if col not in bookings_data.columns]

    if missing_columns:
        st.error(f"The dataset is missing the following columns: {', '.join(missing_columns)}")
    else:
        # Group by hotel and aggregate data
        hotel_ranking = (
            bookings_data.groupby(["Hotel Name", "City", "Country", "Room Type"])
            .agg(
                Bookings=("Hotel Name", "count"),
                Average_Price=("Price", "mean")
            )
            .reset_index()
            .sort_values(by="Bookings", ascending=False)
        )

        # Display the ranking
        st.subheader("Top Booked Hotels")
        st.dataframe(hotel_ranking)

        # Add a bar chart for visualization
        st.subheader("Bookings by Hotel")
        st.bar_chart(hotel_ranking.set_index("Hotel Name")["Bookings"])

else:
    st.error("No data available to display rankings.")
