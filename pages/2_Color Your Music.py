import streamlit as st
import pickle
from streamlit_extras.stylable_container import stylable_container
import pandas as pd

st.set_page_config(page_title="Color Your Music", page_icon="🎨")

# Load data
music_mood_dict = pickle.load(open('music_mood_dict.pkl', 'rb'))
music_mood = pd.DataFrame(music_mood_dict)

color_to_mood = {
    'yellow': 'Happy',
    'blue': 'Sad',
    'green': 'Relaxed',
    'red': 'Angry' 
}

# Prepare top songs by mood
top_songs_by_mood = {}

for mood in music_mood['mood'].unique():
    top_songs = music_mood[music_mood['mood'] == mood].nlargest(200, 'popularity')
    top_songs_by_mood[mood] = top_songs

def recommend_song_by_color(color):
    mood = color_to_mood.get(color)
    if mood and not top_songs_by_mood[mood].empty:
        return top_songs_by_mood[mood].sample(8)
    else:
        return None

# Frontend
st.sidebar.markdown('**DVST - TEAM 6 - Final Project**')

st.write("## What Color Represents You Today?")

# Dictionary for button colors
button_colors = {
    'red': '#FF6347',
    'yellow': '#FFD700',
    'blue': '#1E90FF',
    'green': '#2E8B57'
}

# Buttons for color selection
col1, col2 = st.columns(2)
colors = ['red', 'blue', 'yellow', 'green']
for i, color in enumerate(colors):
    col = col1 if i < 2 else col2
    with col:
        with stylable_container(
            color,
            css_styles=f"""
                button {{
                    background-color: {button_colors[color]};
                    color: #F5F5F5;
                    border-radius: 20px;
                    border: 1px solid;
                    font-size: 26px;
                    width: 200px;
                    height: 150px;
                    line-height: 25px;
                }}
            """
        ):
            if st.button(color.capitalize(), key=color):
                # Store the selected color in session state
                st.session_state['selected_color'] = color
                # Flag that a new song selection is ready to be shown
                st.session_state['show_selection'] = True

# Define the placeholder for the recommendations after the buttons
recommended_songs_header_placeholder = st.empty()
recommended_songs_placeholder = st.empty()

# Check if a color button has been clicked and display the recommendations
if 'show_selection' in st.session_state and st.session_state['show_selection']:
    selected_songs = recommend_song_by_color(st.session_state['selected_color'])
    if selected_songs is not None:
        recommended_songs_header_placeholder.markdown(" Here are a few Recommendations..")
        recommended_songs_placeholder.table(selected_songs[['track_name', 'artist_name']].reset_index(drop=True))
    else:
        recommended_songs_placeholder.write(f"No songs found for {st.session_state['selected_color']} mood.")
    # Reset the flag to prevent the selection from showing again until the next button press
    st.session_state['show_selection'] = False

# Additional information
st.write("##")
tab1, tab2 = st.tabs(["About", "Data"])
with tab1:
    st.caption('This is an Emotion-Based Music Recommendation System')
with tab2:
    st.caption("It Contains Songs from *Spotify_1Million_Tracks*")
