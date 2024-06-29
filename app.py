import streamlit as st
import pickle
import pandas as pd
import numpy as np
from PIL import Image
import os

# Load the model and transformers
pipe = pickle.load(open('pipe.pkl', 'rb'))

# Define teams and cities
teams = ['Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa', 'England', 'West Indies', 'Afghanistan', 'Pakistan', 'Sri Lanka']
cities = ['Colombo', 'Mirpur', 'Johannesburg', 'Dubai', 'Auckland', 'Cape Town', 'London', 'Pallekele', 'Barbados', 'Sydney', 'Melbourne', 'Durban', 'St Lucia', 'Wellington', 'Lauderhill', 'Hamilton', 'Centurion', 'Manchester', 'Abu Dhabi', 'Mumbai', 'Nottingham', 'Southampton', 'Mount Maunganui', 'Chittagong', 'Kolkata', 'Lahore', 'Delhi', 'Nagpur', 'Chandigarh', 'Adelaide', 'Bangalore', 'St Kitts', 'Cardiff', 'Christchurch', 'Trinidad']

# Streamlit layout
st.set_page_config(layout="wide")

# Custom CSS to center the main content
st.markdown("""
    <style>
    .main-content {
        max-width: 800px;
        margin: auto;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Main content
main_content = st.container()

with main_content:
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    title ='ICC MEN T20 WORLD CUP SCORE PREDICTOR'
    st.markdown(f"<h1 style='text-align: center'>{title}</h1>", unsafe_allow_html=True)

    # Load and resize image
    image2 = Image.open("img2.jpg")
    image2 = image2.resize((800, 400))  # Adjust the size as needed (width, height)
    st.image(image2, use_column_width=True)

    # Input fields
    col1, col2 = st.columns(2)
    with col1:
        batting_team = st.selectbox('Select batting team', sorted(teams))
    with col2:
        bowling_team = st.selectbox('Select bowling team', sorted(teams))
    city = st.selectbox('Select city', sorted(cities))

    col3, col4, col5 = st.columns(3)
    with col3:
        current_score = st.number_input('Current Score')
    with col4:
        overs = st.number_input('Overs done (works for over > 5)')
    with col5:
        wickets = st.number_input('Wickets fallen')

    last_five = st.number_input('Runs scored in last 5 overs')

    if st.button('Predict Score'):
        balls_left = 120 - (overs * 6)
        wickets_left = 10 - wickets
        crr = current_score / overs if overs > 0 else 0

        # Create input DataFrame
        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [city],
            'current_score': [current_score],
            'balls_left': [balls_left],
            'wickets_left': [wickets_left],
            'crr': [crr],
            'last_five': [last_five]
        })

        # Predict score
        try:
            result = pipe.predict(input_df)
            st.header("Predicted Score - " + str(int(result[0])))
        except Exception as e:
            st.error("Prediction failed. Error: {}".format(e))

    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar with captain images
st.sidebar.title("Team Captains of T20 World Cup 2024")

captain_images_folder = "captain_images"
image_files = sorted([f for f in os.listdir(captain_images_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])

custom_captions = {
    "img1.png": "Rohit Sharma (India)",
    "img2.jpeg": "Wanindu Hasaranga (Srilanka)",
    "img3.jpeg": "Shakib Al Hasan (Bangladesh)",
    "img4.jpeg": "Kane Williamson (New Zealand)",
    "img5.jpeg": "Aiden Markaram (South Africa)",
    "img6.jpeg": "Jos BUttler (England)",
    "img7.jpeg": "Rovman Powell (West Indies)",
    "img8.jpeg": "Rashid Khan (Afghanistan)",
    "img9.jpeg": "Babar Azam (Pakistan)",
    "img10.jpeg": "Mtchell Marsh (Australia)"
}

for image_file in image_files:
    try:
        image_path = os.path.join(captain_images_folder, image_file)
        image = Image.open(image_path)
        
        # Use custom caption if available, otherwise use a default caption
        caption = custom_captions.get(image_file, f"Captain of {image_file.split('.')[0]}")
        
        st.sidebar.image(image, caption=caption, use_column_width=True)
    except Exception as e:
        st.sidebar.warning(f"Error loading image {image_file}: {str(e)}")