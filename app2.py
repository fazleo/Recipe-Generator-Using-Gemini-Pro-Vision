
from dotenv import load_dotenv
import os
from PIL import Image

#loading environment variables
load_dotenv()


import streamlit as st
import google.generativeai as genai



genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro-vision')



def get_gemini_response(prompt, image):
    response = model.generate_content([prompt,image])
    return response.text

def input_image(uploaded_file):
    # give me codd to open and convert to byte image

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No image uploaded")



#setting streamlit ui 

st.set_page_config(page_title="Recipe Generator: ", page_icon="🎨")

st.header("Recipe Generator Using Image: ")
# input_text = st.text_input("Enter the prompt for asking in the pdf ?", key="input_text")

uploaded_file = st.file_uploader("Upload the Image of invoice: ..",type=['jpg','jpeg','png','webp'],key="file")

image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Submit")

system_prompt = """
You are a food image recognition and recipe generation assistant. Your goal is to analyze an image of a prepared dish and:

1. **Identify the main ingredients and their quantities.**
2. **Suggest a recipe for the dish based on the identified ingredients.**
3. **Consider the user's dietary preferences, allergies, or any additional information provided.**

Use your knowledge of food identification, recipe databases, and dietary restrictions to provide accurate and helpful suggestions. Be informative, engaging, and offer variations or substitutions when possible.
"""

if submit:
    image_data = input_image(uploaded_file)
    response = get_gemini_response(system_prompt, image)
    st.subheader("Response: ...")
    st.write(response)