import streamlit as st
import base64

from background_style import set_background

# Enable wide mode
st.set_page_config(
    layout="wide",  # Enable wide mode
)

set_background(
    main_bg_url="https://ik.imagekit.io/tvlk/image/imageResource/2025/01/05/1736039153373-64c979a852c7ec9063c6f2104bcf58dd.png?tr=q-75",
    sidebar_img_path="background.webp"
)


# Add background image
image_url = "background.webp"
def add_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Add running text
def add_marquee_text(text, color="#FFFFFF"):
    st.markdown(
        f"""
        <style>
        .marquee {{
            overflow: hidden;
            white-space: nowrap;
            box-sizing: border-box;
            width: 100%;
            animation: marquee 10s linear infinite;
            color: {color};
            font-size: 24px;
            font-weight: bold;
        }}
        @keyframes marquee {{
            0%   {{ transform: translateX(100%); }}
            100% {{ transform: translateX(-100%); }}
        }}
        </style>
        <div class="marquee">{text}</div>
        """,
        unsafe_allow_html=True,
    )

# Add background image (Replace the URL with your own image link)
add_background("https://source.unsplash.com/1600x900/?hotel,resort,travel")

# Add running text
add_marquee_text("🌟 Find Your Perfect Hotel Stay Today! 🌟")

# Main Header
st.header("🏨 Welcome to the Ultimate Hotel Search App")
st.write("""
Discover a seamless and hassle-free way to search for the best hotels around the world.
With our intuitive interface and powerful search algorithms, you can find the perfect accommodation for your next adventure.
""")

# About Section
st.subheader("About This App")
st.write("""
This application is designed for travelers seeking top-notch hotel recommendations. 
With real-time filters, personalized suggestions, and a user-friendly interface, our tool simplifies the hotel search process.
Developed by travel enthusiasts, it aims to make your planning smooth and enjoyable.
""")
