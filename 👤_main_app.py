import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
import base64
import streamlit as st
import base64
from background_style import set_background
import pandas as pd
import re
import pickle


# Set the background
set_background(
    main_bg_url="https://ik.imagekit.io/tvlk/image/imageResource/2025/01/05/1736039153373-64c979a852c7ec9063c6f2104bcf58dd.png?tr=q-75",
    sidebar_img_path="background.webp"
)

st.title("Welcome to the Hotel Search App")
st.write("This app helps you find the best hotels with ease!")

# Initialize the login widget
__login__obj = __login__(
    auth_token="courier_auth_token",
    company_name="Shims",
    width=200,
    height=250,
    logout_button_name='Logout',
    hide_menu_bool=False,
    hide_footer_bool=False,
    lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json'
)

# Build the login UI and check the login state
LOGGED_IN = __login__obj.build_login_ui()

def transform(text):
    return re.sub(r'Room size: \d+ m²/\d+ ft², ','',text)

def remove_whitespace(text):
   return  text.replace(' ','')

# Show application content if the user is logged in
if LOGGED_IN:
    st.markdown("### Add Hotel Information")
    
    # Form for adding hotel information
    with st.form("add_hotel_form"):
        hotelname = st.text_input("Hotel Name")
        roomtype = st.text_input("Room Type")
        country = st.text_input("Country")
        city = st.text_input("City")
        propertytype = st.text_input("Property Type")
        url_image = st.text_input("Image URL")
        roomamenities = st.text_input("Room Amenities")
        ratedescription = st.text_area("Rate Description")
        address = st.text_area("Address")
        min_price = st.number_input("Min Price", min_value=0, step=1)
        max_price = st.number_input("Max Price", min_value=0, step=1)
        starrating = st.number_input("Star Rating", min_value=1, max_value=5, step=1)
        
        # Submit button
        submitted = st.form_submit_button("Add Hotel")
        
        if submitted:
            if not (hotelname and roomtype and country and city and address):
                st.error("Please fill in all required fields!")
            else:
                # Create a DataFrame with the new hotel data
                new_hotel_data = {
                    "hotelname": [hotelname],
                    "roomtype": [roomtype],
                    "country": [country],
                    "city": [city],
                    "propertytype": [propertytype],
                    "url_image": [url_image],
                    "roomamenities": [roomamenities],
                    "ratedescription": [ratedescription],
                    "address": [address],
                    "min": [min_price],
                    "max": [max_price],
                    "starrating": [starrating],
                }
                new_hotel_df = pd.DataFrame(new_hotel_data)

                new_hotel_df['roomamenities_tag'] = new_hotel_df['roomamenities'].apply(lambda x:x.replace(': ;',','))
                new_hotel_df['roomamenities_tag'] = new_hotel_df['roomamenities_tag'].apply(remove_whitespace)
                new_hotel_df['roomamenities_tag'] = new_hotel_df['roomamenities_tag'].apply(lambda x:x.split(','))

                new_hotel_df['roomtype_tag'] = new_hotel_df['roomtype'].apply(remove_whitespace)
                new_hotel_df['roomtype_tag'] =  new_hotel_df['roomtype_tag'].apply(lambda x:[x])

                new_hotel_df['ratedescription_tag'] = new_hotel_df['ratedescription'].apply(transform)
                new_hotel_df['ratedescription_tag'] = new_hotel_df['ratedescription_tag'].apply(remove_whitespace)
                new_hotel_df['ratedescription_tag'] = new_hotel_df['ratedescription_tag'].apply(lambda x:x.split(','))

                new_hotel_df['address'].nunique()
                new_hotel_df['address_tag'] = new_hotel_df['address'].apply(remove_whitespace)
                new_hotel_df['address_tag'] = new_hotel_df['address_tag'].apply(lambda x:x.split())

                new_hotel_df['city_tag'] = new_hotel_df['city'].apply(remove_whitespace)
                new_hotel_df['city_tag'] = new_hotel_df['city_tag'].apply(lambda x:x.split())

                new_hotel_df['country_tag'] = new_hotel_df['country'].apply(remove_whitespace)
                new_hotel_df['country_tag'] = new_hotel_df['country_tag'].apply(lambda x:x.split())

                new_hotel_df['propertytype_tag'] = new_hotel_df['propertytype'].apply(remove_whitespace)
                new_hotel_df['propertytype_tag'] = new_hotel_df['propertytype_tag'].apply(lambda x:x.split())

                new_hotel_df['tags'] = new_hotel_df['roomamenities_tag'] + new_hotel_df['roomtype_tag'] + new_hotel_df['ratedescription_tag'] + new_hotel_df['address_tag'] + new_hotel_df['city_tag'] + new_hotel_df['country_tag'] + new_hotel_df['propertytype_tag']
                new_hotel_df['tags'] = new_hotel_df['tags'].apply(lambda x:" ".join(x))

                df_final = new_hotel_df[['hotelname','tags','roomtype','country','city','propertytype' , 'url_image' , 'roomamenities' , 'ratedescription', 'address' , 'min', 'max' , 'starrating']]

                # Load the existing data from data.csv
                try:
                    existing_data = pd.read_csv("data.csv")
                    # Append the new data to the existing data
                    updated_data = pd.concat([existing_data, df_final], ignore_index=True)
                except FileNotFoundError:
                    # If the file does not exist, start a new DataFrame
                    updated_data = df_final
                
                # Save the updated data back to data.csv
                updated_data.to_csv("data.csv", index=False)
                
                pickle.dump(updated_data,open('data.pkl','wb'))

                st.success("Hotel information added successfully!")
                st.dataframe(updated_data)  # Display the updated data