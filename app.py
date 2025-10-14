import streamlit as st 
from PIL import Image

# how to put text on webpage

image = Image.open("plants.jpg")
st.image(image, caption = "Lots of plants")

st.title("Plant App")
st.write("blah blah")
st.markdown('''>This application will give you suggestions on crops''')

# uploaded_file = st.file_uploader("upload soil report", type = ["pdf", "jpeg", "png", "csv"])

# if (uploaded_file != None):

#     image = Image.open(uploaded_file)
#     st.image(image, caption = "This is your uploaded file")



st.sidebar.title("Controls")
