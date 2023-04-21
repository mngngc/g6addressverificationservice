import streamlit as st
import pandas as pd
from geopy.geocoders import GoogleV3
from geopy.distance import geodesic

pip.main (["install","openpyxl"])
st.title("AVS6")
google_api_key = "AIzaSyDFKimABSxzNoxKUrjtsoLzatpLDeqMxBk"

# Read the Excel database of addresses into a DataFrame
database_df = pd.read_excel('Project_2_Addresses_mp.xlsx')

# Initialize GoogleV3 geocoder
geolocator = GoogleV3(api_key=google_api_key)

# Get the user-inputted address

col1, col2 = st.columns(2)
with col1:
    st.text_input(
        "your address",
        key="placeholder"
    )

with col2:
    text_input = st.text_input(
        "Enter address to verify",
        label_visibility=st.session_state.visibiity,
        disabled=st.session_state.disabled,
        placeholder=st.session_state.placeholer,
    )
if text_input:
    st.write("You entered:", text_input)
    user_address = text_input
    
# Geocode the user-inputted address
user_location = geolocator.geocode(user_address)


# Iterate through the rows of the DataFrame and check for matches or close proximity
for index, row in database_df.iterrows():
    if str(row['Address 2']) != "nan":
        current_address = f"{row['Address 1']} {str(row['Address 2'])} {row['City']} {row['State']} {str(row['Zip'])}"
    else:
        current_address = f"{row['Address 1']} {row['City']} {row['State']} {str(row['Zip'])}"

    if user_address.lower() == current_address.lower():
        print("Exact match found: " + current_address)
        break

    if not hasattr(user_location, "address"):
      print("Address not found in Google.")
      quit()

    test_location = geolocator.geocode(current_address)
    distance = geodesic((user_location.latitude, user_location.longitude), (test_location.latitude, test_location.longitude)).miles

    if distance < 0.5: # If the distance between two addresses is less than 0.5 km, consider it a match
        print(f"{user_address} is a match for {current_address}")
        break
    elif distance < 5: # If the distance is less than 5 km, suggest a correction
        print(f"{user_address} is close to {current_address}. Did you mean {current_address}?")
        break
else:
    print("No match found.")
