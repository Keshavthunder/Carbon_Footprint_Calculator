import streamlit as st
import os

def main():
    st.title("Sustainable Living Visualizer")
    
    # 1. User selects the number of Earths
    score = st.slider("Select your impact level:", 1, 9, 4)

    # 2. Map the score to the pre-rendered video file
    video_path = f"videos/{score}.mp4"

    st.subheader(f"If everyone lived like you, we would need {score} Earths:")

    # 3. Play the video immediately
    if os.path.exists(video_path):
        st.video(video_path)
    else:
        st.error("Video file not found in the repository.")

if __name__ == "__main__":
    main()
