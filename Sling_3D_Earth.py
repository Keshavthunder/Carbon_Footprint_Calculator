import streamlit as st
import os

# Get the directory where the current script is located
script_dir = os.path.dirname(__file__)

def main():
    st.title("Sustainable Living Visualizer")
    
    # 1. User selects the number of Earths
    score = st.slider("Select your impact level:", 1, 9, 4)

    st.subheader(f"If everyone lived like you, we would need {score} Earths:")

    # 2. Construct the absolute path to the video
    # This helps Streamlit Cloud find the 'videos' folder correctly
    video_filename = f"{score}.mp4"
    video_path = os.path.join(script_dir, "videos", video_filename)

    # 3. Display the video
    if os.path.exists(video_path):
        with open(video_path, 'rb') as v_file:
            video_bytes = v_file.read()
        st.video(video_bytes)
    else:
        st.error(f"Video for {score} Earths is not yet uploaded to the 'videos' folder.")
        st.info("Check your GitHub to ensure 'videos/4.mp4' exists!")

if __name__ == "__main__":
    main()
