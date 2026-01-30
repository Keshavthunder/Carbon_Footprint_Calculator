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

def q4(q,min_val, max_val, default_val):
    rating = st.slider(q,min_val, max_val, format = "compact", value=default_val)
    
    return rating
def main():

# Sliders are used for inputting the amount of carbon footprint in different areas of life

    st.title("Carbon Footprint Visulaizer")
    
    st.write("This tool allows you to see the future of Earth in 10 years if every person on Earth, i.e. 8 billion people, lived a lifestyle similar to yours.")
    st.write("""For this magic, you will need to enter your household's carbon footprint in 4 areas of life:  
                             1. Housing  
                             2. Transportation  
                             3. Food  
                             4. Shopping""")

    st.header("Housing")
    
    c1, c2 = st.columns(2)
    with c1:
        adults = q4("How many adults in your household?", 0, 10, 2)
        dishwasher = st.selectbox("Do you use a dishwasher?", ["Yes", "No"], key="dw_1")
    with c2:
        kids = q4("How many kids in your household?", 0, 10, 1)
        washing_machine = st.selectbox("Do you use a washing machine?", ["Yes", "No"], key="wm_1")
    
    
    st.markdown("---")
    c3, c4 = st.columns(2)
    with c3:
        energy = q4("Household Monthly Energy Consumption (kWh)?", 20, 1500, 450)
    with c4:
        e_energy = q2("What portion of Monthly Energy is renewable energy?")

    energy_conservation = st.selectbox("Do you practice energy conservation methods (e.g. turning off lights when not in use)?", ["Yes", "No"])
    
    st.header("Transportation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        car = q4("Car driven per week (km)?", 0, 3000, 500)
        car_type = st.selectbox(
            "Car Engine Type", 
            ["Gasoline", "Diesel", "Hybrid", "Electric"], 
            key="car" 
        )
    
    with col2:
        bike = q4("Bike driven per week (km)?", 0, 500, 0)
        bike_type = st.selectbox(
            "Bike Type", 
            ["Regular", "Electric"], 
            key="bike" 
        )
    
    st.markdown("---")
    col3, col4 = st.columns(2)
    
    with col3:
        d_flight = q4("No. of Domestic flights/year? (Consider roundtrip as 2)", 0, 50, 2)
    
    with col4:
        
        i_flight = q4("No. of International flights/year? (Consider roundtrip as 2)", 0, 20, 1)
    public = q4("How many kilometers do you use public transportation per week?", 0, 2000, 200)


    st.header("Food")
    st.subheader("Dietary Habits")
    st.write("How often do you consume:")
    food_col1, food_col2 = st.columns(2)
    
    with food_col1:
        veg = q1("Vegetarian meal?")
        poultry = q1("Poultry?")
        seafood = q1("Seafood?")
    
    with food_col2:
        red_meat = q1("Red meat?")
        dairy = q1("Dairy products?")
        out = q1("Takeout?")
    
    st.markdown("---")

    locally = q2("What portion of your diet is grown locally (within 250kms)?")
    
        
    st.header("Shopping")

    clothes = q3("How many clothing items do you purchase per month?", 0, 40, 8, 0, 50)
    electronics = q3("How many electronic items do you purchase per year? (Ex. Phones, laptops, TVs)", 0, 20, 2, 0, 20)
    waste = q3("How much waste do you generate per week (in kgs)?", 0, 50, 10, 0, 50)
    recycle = q2("What portion of your waste do you recycle or compost?")






    

    if st.button("Render Your World"):
        # Housing Totals
        total_people = max(1, (adults + 0.7*kids))
        annual_energy_co2 = (energy * 12) * 0.3 * (1 - (e_energy / 300))
        appliance_co2 = 0
        if dishwasher == "Yes":
            appliance_co2 += 10
        if washing_machine == "Yes":
            appliance_co2 += 10
        housing_subtotal = annual_energy_co2 + appliance_co2
        if energy_conservation == "Yes":
            housing_subtotal *= 0.85

        housing_per_person = housing_subtotal / total_people
        st.metric("Housing Footprint", f"{housing_per_person:.2f} kg CO2e/year")
        #Transportation Totals

        car_factors = {
            "Gasoline": 0.19,
            "Diesel": 0.17,
            "Hybrid": 0.11,
            "Electric": 0.05
        }
        car_annual = (car * 52) * car_factors[car_type]
        bike_annual = (bike * 52) * 0.01
        public_annual = (public * 52) * 0.07
        flights_annual = (d_flight * 150) + (i_flight * 800)
        transport_total = car_annual + bike_annual + public_annual + flights_annual
    
        st.metric("Transport Footprint", f"{transport_total:,.0f} kg CO2e/year")

        #Food Totals
        def get_intensity(val):
            return (val - 20) / 80.0

        meat_co2    = get_intensity(red_meat) * 2500
        dairy_co2   = get_intensity(dairy) * 900
        poultry_co2 = get_intensity(poultry) * 550
        seafood_co2 = get_intensity(seafood) * 600
        veg_co2     = get_intensity(veg) * 400
        takeout_co2 = get_intensity(out) * 600

        base_food_total = meat_co2 + dairy_co2 + poultry_co2 + seafood_co2 + veg_co2 + takeout_co2

        local_offset = (locally / 100.0) * 0.10
        food_total = base_food_total * (1 - local_offset)

        st.metric("Food Footprint", f"{food_total:,.0f} kg CO2e/year")
        
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
