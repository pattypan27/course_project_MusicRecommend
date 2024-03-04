import streamlit as st
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(page_title="Explore Music Library", page_icon="🔍")


# Load data
music_dict = pickle.load(open('music_content_dict.pkl','rb'))
music = pd.DataFrame(music_dict)

feature_matrix = pickle.load(open('feature_matrix.pkl','rb'))


# Prepare songs by cos sim
def recommend_songs(track_name, top_n=8):

    try:
        # Find the track ID corresponding to the user input
        track_id = music.loc[music['track_name'] == track_name, 'track_id'].values[0]
    except IndexError:
        return "Track name not found in the dataset."
    
    # Ensure the track_id is in the feature matrix
    if track_id not in feature_matrix.index:
        return "Track ID not found in the feature matrix."
    
    # Find the index of the track_id in the feature matrix
    track_index = feature_matrix.index.get_loc(track_id)
    
    # Calculate cosine similarity
    cosine_sim = cosine_similarity(feature_matrix)
    
    # Get similarity scores for the entered track with all tracks
    sim_scores = list(enumerate(cosine_sim[track_index]))
    
    # Sort the tracks based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the scores of the top_n most similar tracks (excluding the first one which is the track itself)
    top_indices = [i[0] for i in sim_scores[1: top_n + 1]]
    
    # Get the track IDs for the top similar tracks
    similar_track_ids = feature_matrix.iloc[top_indices].index.tolist()
    
    # Lookup the track names and artist names for the similar tracks
    recommendations = music[music['track_id'].isin(similar_track_ids)][['track_name', 'artist_name']].reset_index(drop=True)
    
    return recommendations


# Frontend

st.markdown("## Explore Music Library")
st.sidebar.markdown('**DVST - TEAM 6 - Final Project**')


# Add search panel and search button
options = st.selectbox('Which song do you like?', music['track_name'].values)

if st.button('Recommend'):
    recommendations = recommend_songs(options)
    st.write("#### ")
    st.write("Here are few Recommendations..")
    st.table(recommendations)



# Additional information
st.write("##")
tab1 ,tab2 = st.tabs(["About","Data"])

with tab1:
    st.caption('This a Content Based Movie Recommendation System')
with tab2:
    st.caption("It Contains Songs from *Spotify_1Million_Tracks*")