import streamlit as st
import os
import numpy as np

# Get the absolute path to the folder where this script lives
script_dir = os.path.dirname(os.path.abspath(__file__))
def scale_number(unscaled, to_min, to_max, from_min, from_max):
    return (to_max-to_min)*(unscaled-from_min)/(from_max-from_min)+to_min

def q1(q):
    options_list = ['Never', 'Occasionally', 'Regularly', 'Frequently', 'Always']
    rating = st.select_slider(q, options=options_list)
    #t.write("Your rating is", rating)
    return (20*(1+options_list.index(rating)))

def q2(q):
    rating = st.slider(q, 0.00, 1.00, format = "percent",)

    return (100*rating)

def q3(q,min_val, max_val, default_val,avg_min, avg_max):
    rating = st.slider(q,min_val, max_val, format = "compact", value=default_val)
    
    return scale_number(rating, 0, 100, avg_min, avg_max)
def main():

# Sliders are used for inputting the amount of carbon footprint in different areas of life

    st.title("Carbon Footprint Visulaizer")
    
    st.write("This tool allows you to see the future of Earth in 10 years if every person on Earth, i.e. 8 billion people, lived a lifestyle similar to yours.")
    st.write("""For this magic, you will need to enter your carbon footprint in 4 areas of your life:  
                             1. Housing  
                             2. Transportation  
                             3. Food  
                             4. Shopping""")

    st.header("Housing")
    
    c1, c2 = st.columns(2)
    with c1:
        adults = q3("How many adults in your household?", 0, 10, 2, 0, 10)
        dishwasher = st.selectbox("Do you use a dishwasher?", ["Yes", "No"], key="dw_1")
    with c2:
        kids = q3("How many kids in your household?", 0, 10, 1, 0, 10)
        washing_machine = st.selectbox("Do you use a washing machine?", ["Yes", "No"], key="wm_1")
    
    
    st.markdown("---")
    c3, c4 = st.columns(2)
    with c3:
        energy = q3("Household Monthly Energy Consumption (kWh)?", 5000, 13700, 11000, 8772, 13700)
    with c4:
        e_energy = q2("What portion of Monthly Energy is renewable energy?")

    energy_conservation = st.selectbox("Do you practice energy conservation methods (e.g. turning off lights when not in use)?", ["Yes", "No"])
    
    st.header("Transportation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        car = q3("Car driven per week (km)?", 0, 3000, 500, 0, 3000)
        car_type = st.selectbox(
            "Car Engine Type", 
            ["Gasoline", "Diesel", "Hybrid", "Electric"], 
            key="car" 
        )
    
    with col2:
        bike = q3("Bike driven per week (km)?", 0, 500, 0, 0, 500)
        bike_type = st.selectbox(
            "Bike Type", 
            ["Regular", "Electric"], 
            key="bike" 
        )
    
    st.markdown("---")
    col3, col4 = st.columns(2)
    
    with col3:
        d_flight = q3("No. of Domestic flights/year? (Consider roundtrip as 2)", 0, 50, 2, 0, 50)
    
    with col4:
        
        i_flight = q3("No. of International flights/year? (Consider roundtrip as 2)", 0, 20, 1, 0, 20)
    public = q3("How many kilometers do you use public transportation per week?", 0, 2000, 200, 0, 2000)


    st.header("Food")
    st.subheader("Dietary Habits")
    st.write("How often do you consume:")
    food_col1, food_col2 = st.columns(2)
    
    with food_col1:
        veg = q1("Vegetarian meal?", key="veg_q")
        poultry = q1("Poultry?", key="poultry_q")
        seafood = q1("Seafood?", key="seafood_q")
    
    with food_col2:
        red_meat = q1("Red meat?", key="meat_q")
        dairy = q1("Dairy products?", key="dairy_q")
        out = q1("Takeout?", key="takeout_q")
    
    st.markdown("---")

    locally = q2("What portion of your diet is grown locally (within 250kms)?", key="local_food_pct")
    
        
    st.header("Shopping")

    clothes = q3("How many clothing items do you purchase per month?", 0, 40, 8, 0, 50)
    electronics = q3("How many electronic items do you purchase per year?", 0, 20, 2, 0, 20)
    waste = q3("How much waste do you generate per week (in kgs)?", 0, 50, 10, 0, 50)
    recycle = q2("What portion of your waste do you recycle or compost?")




    if st.button("Render Your World"):
        st.write("To BE CONTINUED")


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
