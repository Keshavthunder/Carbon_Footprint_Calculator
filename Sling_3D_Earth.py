import streamlit as st
import os

# Get the absolute path to the folder where this script lives
script_dir = os.path.dirname(os.path.abspath(__file__))

def main():
    st.title("Sustainable Living Visualizer")
    
    score = st.slider("Select your impact level:", 1, 9, 4)
    st.subheader(f"If everyone lived like you, we would need {score} Earths:")

    # Construct the path to the video file
    video_path = os.path.join(script_dir, "videos", f"{score}.mp4")

    if os.path.exists(video_path):
        # Open and read the video file as binary
        with open(video_path, 'rb') as video_file:
            video_bytes = video_file.read()
        
        # ADDED: format="video/mp4" tells the browser how to play it
        st.video(video_bytes, format="video/mp4")
    else:
        st.error(f"Video '{score}.mp4' not found in the videos folder.")
        st.info("Make sure you have uploaded all videos (1.mp4 through 9.mp4) to GitHub.")

if __name__ == "__main__":
    main()
