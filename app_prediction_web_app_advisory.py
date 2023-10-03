import streamlit as st
import numpy as np
import pickle


# Load the trained model
loaded_model = pickle.load(open('trained_model.sav', 'rb'))


def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp  {{
             height: 100vh;
             background-image: url("https://png.pngtree.com/thumb_back/fh260/background/20201012/pngtree-white-cloud-on-blue-sky-weather-background-image_410050.jpg");
             background-size: cover;
             
             }}
         </style>
         """,
         unsafe_allow_html=True
     )


# Function to get the AQI and health advisory
def get_aqi_advisory(so2, no2, rspm, pm2_5):
    prediction = loaded_model.predict([[so2, no2, rspm, pm2_5]])

    # Get the AQI category
    if isinstance(prediction, int):
        if prediction <= 50:
            aqi_category = "Good"
        elif prediction <= 100:
            aqi_category = "Moderate"
        elif prediction <= 200:
            aqi_category = "Unhealthy"
        elif prediction <= 300:
            aqi_category = "Very Unhealthy"
        else:
            aqi_category = "Hazardous"
    else:
        aqi_category = prediction

    # Get the health advisory
    if aqi_category == "Good":
        health_advisory = "Air quality is satisfactory, and air pollution poses little or no risk."
    elif aqi_category == "Moderate":
        health_advisory = "Air quality is acceptable. However, there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution."
    elif aqi_category == "Unhealthy":
        health_advisory = "Members of sensitive groups may experience health effects. The general public is less likely to be affected."
    elif aqi_category == "Very Unhealthy":
        health_advisory = "Health warnings of emergency conditions. The entire population is more likely to be affected."
    else:
        health_advisory = "Health alert: everyone may experience more serious health effects."

    return aqi_category, health_advisory


def welcome():
    add_bg_from_url() 
    st.image("mansi2304.gif")
    
    st.write("""
    # Welcome to the Air Quality Prediction and Health Advisory website
    This app uses a machine learning model to predict the Air Quality Index (AQI) based on various pollutants in the air. 
    The AQI category and health advisory is displayed based on the AQI value.
    """)
    st.image("plant.gif",width=700)
    st.markdown("<h1 style='text-align: center; color: red;'>Plant as many as you can.</h1>", unsafe_allow_html=True)


def main():
    add_bg_from_url() 
    st.sidebar.title("Navigation")
    pages = ["Welcome", "Prediction"]
    choice = st.sidebar.radio("Go to", pages)

    if choice == "Welcome":
        welcome()
    elif choice == "Prediction":
        st.title("Air Quality Prediction and Health Advisory")
        st.write("Enter the following parameters to get the AQI category and health advisory:")

        # Get the input values from the user
        so2 = st.number_input("Enter SO2 value")
        no2 = st.number_input("Enter NO2 value")
        rspm = st.number_input("Enter RSPM value")
        pm2_5 = st.number_input("Enter PM2.5 value")

        # Get the AQI category and health advisory using the get_aqi_advisory() function
        aqi_category, health_advisory = get_aqi_advisory(so2, no2, rspm, pm2_5)

        # Display the AQI category and health advisory
        st.markdown("## AQI Category: {}".format(aqi_category))
        st.markdown('<p style="color:#000220;font-size:24px;">Health Advisory: {}</p>'.format(health_advisory), unsafe_allow_html=True)

        st.image("anj.gif",width=700)
        st.markdown("<h1 style='text-align: center; color: red;'>This will save us.</h1>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()