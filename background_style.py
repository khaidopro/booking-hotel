import base64
import streamlit as st

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(main_bg_url, sidebar_img_path):
    # Convert the sidebar image to base64
    img = get_img_as_base64(sidebar_img_path)

    # Define background styling
    page_bg_img = f"""
    <style>
    /* Apply background to the entire page */
    [data-testid="stAppViewContainer"] {{
        background-image: url("{main_bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        padding: 0;
    }}

    /* Spread content to fill the width */
    [data-testid="block-container"] {{
        max-width: 100%;
        padding-left: 2rem;
        padding-right: 2rem;
    }}

    /* Add sidebar background */
    [data-testid="stSidebar"] > div:first-child {{
        background-image: url("data:image/png;base64,{img}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Hide header */
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
        visibility: hidden;
    }}

    /* Style toolbar (optional) */
    [data-testid="stToolbar"] {{
        right: 2rem;
    }}
    </style>
    """

    # Apply the CSS styles
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Example usage of the function
set_background(
    main_bg_url="https://ik.imagekit.io/tvlk/image/imageResource/2025/01/05/1736039153373-64c979a852c7ec9063c6f2104bcf58dd.png?tr=q-75",
    sidebar_img_path="background.webp"
)

# Example content
st.title("Welcome to the Expanded Layout")
st.write("Your content now spreads out to the sides instead of being centered!")
