import streamlit as st 
from PIL import Image
import chat_ui

# how to put text on webpage


image = Image.open("plants.jpg")
st.image(image, caption="Lots of plants")

st.title("🌾 Smart Soil Compatibility App")
st.markdown('''> This application suggests crops suitable for your soil based on NPK, pH, and weather data.''')

st.sidebar.title("⚙️ Controls")
st.sidebar.write("Adjust or add features here later.")

uploaded_file = st.file_uploader("Upload soil report or type it in!", type = ["pdf", "jpeg", "png", "csv"])


if (uploaded_file != None):

    image = Image.open(uploaded_file)
    st.image(image, caption = "This is your uploaded file")

st.header("💬 Soil Compatibility Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Enter your soil details or crop question...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response from chatbot
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_ui.chat_response(st.session_state.messages)
            output = ""
            for item in response:
                output += item.content
                
            st.markdown(output)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})


st.sidebar.title("Controls")