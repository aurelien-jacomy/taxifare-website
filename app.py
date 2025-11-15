import streamlit as st
import datetime
import requests
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

'''
# TaxiFareModel 
'''
st.write("Hello!")
#url = 'https://taxifare.lewagon.ai/predict'

url = 'https://taxifare-495542883015.southamerica-east1.run.app/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')


# Forms to input data
with st.form(key='my_taxifare'):
    date = st.date_input(
        "Select your pickup date",
        value=datetime.date.today(),
        min_value=datetime.date(1990, 1, 1),
        max_value=datetime.date.today()
    )
    time = st.time_input("Select your pickup time")
    pickup_address = st.text_input("Enter pickup address")
    dropoff_address = st.text_input("Enter dropoff address")
    passenger_count = st.number_input("Number of passenger", value=1, min_value=1, max_value=8)
    
    submitted = st.form_submit_button(label='Calculate my taxifare')

# Show Result    
if submitted:
   # Instantiate Geolocator and get lat long of pickup and dropoff
    geolocator = Nominatim(user_agent="taxifare")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    pickup_location = geocode(pickup_address)
    dropoff_location = geocode(dropoff_address)
    
    # Show response to user
    if (pickup_location and dropoff_location):
        # Get taxifare from API
        request_url = url+f"?pickup_datetime={date}%20{time}&pickup_longitude={pickup_location.longitude}&pickup_latitude={pickup_location.latitude}&dropoff_longitude={dropoff_location.longitude}&dropoff_latitude={dropoff_location.latitude}&passenger_count={passenger_count}"
        response = requests.get(request_url)
        st.text("")
        st.write(f'#### 🚖 Your taxi fare will cost around {round(response.json()['fare'], 2)} USD.')
        
        # Show map with pickup and dropoff locations
        df = pd.DataFrame({'lat': [pickup_location.latitude, dropoff_location.latitude], 'lon': [pickup_location.longitude, dropoff_location.longitude]})
        st.map(df)
        
    else:
        st.write("Couldn't find pickup or dropoff address")