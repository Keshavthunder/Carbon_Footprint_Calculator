import streamlit as st
from manim import *
import os

# --- GLOBAL CONFIGURATION ---
config.quality = "low_quality" 
config.verbosity = "ERROR"     

class BlueSpheresScene(ThreeDScene):
    def __init__(self, count, **kwargs):
        self.count = int(max(1, count))
        super().__init__(**kwargs)

    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        
        spheres_group = Group()
        for _ in range(self.count):
            s = Sphere(radius=0.7, resolution=(12, 24)) 
            s.set_color(BLUE)
            s.set_sheen(0.3, direction=UP+LEFT) 
            spheres_group.add(s)

        spheres_group.arrange_in_grid(buff=0.8)

        title = Text(f"{self.count} Earths Needed", font_size=36)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP)

        self.play(Write(title, run_time=0.5))
        self.play(
            LaggedStartMap(GrowFromCenter, spheres_group, lag_ratio=0.1),
            run_time=1.0 
        )
        self.wait(1)

@st.cache_data
def render_video(planets):
    # FIX: Assign a unique filename so videos don't overwrite each other
    unique_name = f"Impact_{planets}_planets"
    config.output_file = unique_name
    
    scene = BlueSpheresScene(count=planets)
    scene.render()
    
    # Manim returns the absolute path to the newly created unique file
    return str(scene.renderer.file_writer.movie_file_path)

def main():
    st.title("Sustainable Living Visualizer")
    
    # User inputs
    score = st.slider("Select your impact level:", 1, 9, 4)

    if st.button("Generate Animation"):
        with st.spinner(f"Preparing visualization for {score} Earths..."):
            video_path = render_video(score)
            
            if os.path.exists(video_path):
                st.video(video_path)
            else:
                st.error("Video rendering failed.")

if __name__ == "__main__":
    main()