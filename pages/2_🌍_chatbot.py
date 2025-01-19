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
import streamlit.components.v1 as components
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
              bot_id: '7461250636273762322',
            },
            componentProps: {
              title: 'Coze',
            },
          });
    </script>
</body>
</html>
"""

components.html(chatbot_html, height=800 , width=1000, scrolling=True)