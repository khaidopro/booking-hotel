import pickle
import streamlit as st
import requests
import base64
from streamlit_option_menu import option_menu
import altair as alt
import pandas as pd
import plotly.express as px
import itertools
from pmdarima.arima import auto_arima
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(max_features=1000)

from sklearn.metrics.pairwise import cosine_similarity

from background_style import set_background

# Enable wide mode
st.set_page_config(
    layout="wide",  # Enable wide mode
)

# Set the background
set_background(
    main_bg_url="https://ik.imagekit.io/tvlk/image/imageResource/2025/01/05/1736039153373-64c979a852c7ec9063c6f2104bcf58dd.png?tr=q-75",
    sidebar_img_path="background.webp"
)

# st.set_page_config(layout="wide")
if "selected_hotel_index" not in st.session_state:
    st.session_state.selected_hotel_index = None

# Chatbot Integration (this will always run)
chatbot_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coze Chat</title>
</head>
<body>
    <!-- Coze Chat Integration -->
    <script src="https://sf-cdn.coze.com/obj/unpkg-va/flow-platform/chat-app-sdk/1.1.0-beta.0/libs/oversea/index.js"></script>
    <script>
        new CozeWebSDK.WebChatClient({
            config: {
                bot_id: '7460460940891275282', // Replace with your bot ID if necessary
            },
            componentProps: {
                title: 'Coze', // Title of the chat window
            },
        });
    </script>
</body>
</html>
"""

one = st.empty()
two = st.empty()
three = st.empty()

df_final = pd.read_pickle("data.pkl")

def fetch_poster(movie_id):
    url = "https://ik.imagekit.io/tvlk/apr-asset/dgXfoyh24ryQLRcGq00cIdKHRmotrWLNlvG-TxlcLxGkiDwaUSggleJNPRgIHCX6/hotel/asset/{}".format(movie_id)
    return url

def recommend(city , starrating , roomtype):
    
    ## filtering the dataframe to the requirements of the user
    filtered_df = df_final[
        (df_final['city'] == city)
    ]

    ## creating a temporary dataframe so that we recommend hotels only from the speicified country and city rather than using the entire df which
    ## could lead to results from different cities and countries
    temp = df_final[
        (df_final['city'] == city) 
    ]

    ## indices of the hotels of user requirements
    idx1 = filtered_df['index'].tolist()

    ## reseting index because we need to search for the indices in idx1 in temp
    temp.reset_index(inplace = True)

    ## extracting the index(of the dataframe) of the specified hotels 
    idx2 = temp[temp['index'].isin(idx1)].index.tolist()
    
    ## creating similarity matrix
    vector = tfidf.fit_transform(temp['tags']).toarray()
    similarity = cosine_similarity(vector)

    recommended_hotel = []
    recommended_hotel_posters = []
    ## traverse each user specified hotel and extract top recommend hotels for each specified hotel
    for i in idx2:
        similar_hotels = sorted(list(enumerate(similarity[i])),key = lambda x:x[1],reverse = True)[0:7]
        for hotel in similar_hotels:
            if (int(temp.loc[hotel[0]].starrating) >= starrating) or (temp.loc[hotel[0]].roomtype[0] == roomtype) :
                url_image = temp.loc[hotel[0]].url_image
                recommended_hotel.append(temp.loc[hotel[0]])
                recommended_hotel_posters.append(fetch_poster(url_image))
            else:
                continue
                
    return recommended_hotel , recommended_hotel_posters

# Save booking data to an Excel file
def save_booking_to_excel(data):
    df = pd.DataFrame(data)
    try:
        # Append to the file if it exists, otherwise create it
        file_name = "bookings.xlsx"
        with pd.ExcelWriter(file_name, mode="a", if_sheet_exists="overlay", engine="openpyxl") as writer:
            startrow = writer.sheets['Sheet1'].max_row if 'Sheet1' in writer.sheets else 0
            df.to_excel(writer, index=False, header=startrow == 0, startrow=startrow)
    except FileNotFoundError:
        df.to_excel("bookings.xlsx", index=False)

import streamlit.components.v1 as components

st.header('Hotel Recommender System')
col1, col2 = st.columns([1, 0.5])
date = datetime.datetime.now().date()
with col1:
    st.write('Nhập ngày nhận phòng và ngày trả phòng')
with col2:
    st.button(f"Today's Date 🗓️ {date}")

col5, col6 = st.columns(2)
with col5:
    checkin = st.date_input('Enter Check-in Date🗓️')
with col6:
    checkout = st.date_input('Enter Check-out Date🗓️')

# Initialize session state variables
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
if "recommended_hotels" not in st.session_state:
    st.session_state.recommended_hotels = []
    st.session_state.recommended_posters = []

city_list = df_final['city'].unique()
roomtype_list = df_final['roomtype'].unique()

# Form for user input
with st.form("user_input_form"):
    cname = st.selectbox("Type or select a city from the dropdown", city_list)
    starrating = int(st.number_input('Số sao khách sạn', step=1))
    roomtype = st.selectbox("Loại phòng", roomtype_list)
    submitted = st.form_submit_button("Submit")

# Handle form submission
if submitted:
    recommended_hotel, recommended_hotel_posters = recommend(cname, starrating , roomtype)
    st.session_state.recommended_hotels = recommended_hotel
    st.session_state.recommended_posters = recommended_hotel_posters
    st.session_state.form_submitted = True

# Define a function to display the booking form
def booking_form(hotel):
    st.title(f"Booking {hotel['hotelname']}")
    st.write(f"Location: {hotel['city']}, {hotel['country']}")
    st.write(f"Room Type: {hotel['roomtype']}")
    st.write(f"Price: ${hotel['max']}")

    with st.form("booking_form"):
        full_name = st.text_input("Full Name")
        phone_number = st.text_input("Phone Number")
        email = st.text_input("Email Address")
        number_people = st.text_input("Number Of People:")
        special_requests = st.text_area("Special Requests (optional)")

        # Submit button
        submitted = st.form_submit_button("Complete Booking")

        if submitted:
            if not full_name or not phone_number or not email:
                st.error("Please fill in all the required fields!")
            else:
                # Save booking details to Excel
                booking_data = {
                    "Hotel Name": [hotel["hotelname"]],
                    "City": [hotel["city"]],
                    "Country": [hotel["country"]],
                    "Room Type": [hotel["roomtype"]],
                    "Price": [hotel["max"]],
                    "Full Name": [full_name],
                    "Phone Number": [phone_number],
                    "Email Address": [email],
                    "Number Of People": [number_people],
                    "Special Requests": [special_requests],
                }
                save_booking_to_excel(booking_data)
                st.success("Booking completed successfully! Your details have been saved.")

# Use the booking form within the hotel selection process
if st.session_state.form_submitted:
    recommended_hotel = st.session_state.recommended_hotels
    recommended_hotel_posters = st.session_state.recommended_posters

    st.write("---")
    st.header('Select Room')

    for i, hotel in enumerate(recommended_hotel):
        if i >= 5:  # Limit displayed hotels
            break
        with st.container():
            col1, col2 = st.columns([0.5, 1])
            with col1:
                st.image(recommended_hotel_posters[i])
            with col2:
                st.write(f'Country: {hotel["country"]}')
                st.write(f'City: {hotel["city"]}')
                st.write(f'Hotel Name: {hotel["hotelname"]} || Address: {hotel["address"]}')
                st.write(f'Room Type: {hotel["roomtype"]}')
                st.write(f'Room Amenities: {hotel["roomamenities"]}')
                st.write(f'Rate Description: {hotel["ratedescription"]}')
                st.write('Price:', hotel["max"])
                st.write('Star Rating:', hotel["starrating"])

                # Button to display booking form for the selected hotel
                if st.button(f"Book {hotel['hotelname']}", key=f"book_button_{i}"):
                    st.session_state.selected_hotel_index = i

            st.write("---")

        # Display the booking form when a hotel is selected
        if st.session_state.selected_hotel_index == i:
            booking_form(hotel)