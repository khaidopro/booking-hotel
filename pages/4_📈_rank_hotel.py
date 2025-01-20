import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    layout="wide",
)

# Load data from bookings.pkl
@st.cache_data(ttl=300)  # Cache data for 300 seconds (5 minutes)
def load_data(file_path):
    try:
        df = pd.read_pickle(file_path)
        return df
    except FileNotFoundError:
        st.error("The bookings.pkl file was not found.")
        return pd.DataFrame()

# File path
file_path = "bookings.pkl"  # Update this path if needed

# Add a refresh button to reload data
if st.button("Refresh Data"):
    st.cache_data.clear()

# Load the dataset
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
