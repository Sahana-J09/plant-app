import streamlit as st 
from PIL import Image
from chat_ui import start_chat
import os

# how to put text on webpage


image = Image.open("plants.jpg")
st.image(image, caption="Lots of plants")

st.title("🌾 Smart Soil Compatibility App")
st.markdown('''> This application suggests crops suitable for your soil based on NPK, pH, and weather data.''')

st.sidebar.title("⚙️ Controls")
st.sidebar.write("Adjust or add features here later.")

os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=st.secrets['LANGCHAIN_API_KEY']
os.environ["LANGCHAIN_PROJECT"]="ChatImages"
os.environ['LANGCHAIN_ENDPOINT']="https://api.smith.langchain.com"


st.title("Chat with Images")
start_chat()