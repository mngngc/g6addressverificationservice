import streamlit as st
import pandas as pd
from geopy.geocoders import GoogleV3
from geopy.distance import geodesic
from fuzzywuzzy import fuzz

st.title("Address Verification Service")
google_api_key = "AIzaSyDFKimABSxzNoxKUrjtsoLzatpLDeqMxBk"

# Read the Excel database of addresses into a DataFrame
database_df = pd.read_excel('Project_2_Addresses_mp.xlsx')

# Initialize GoogleV3 geocoder
geolocator = GoogleV3(api_key=google_api_key)

# Get the user-inputted address
text_input = st.text_input(
        "Enter Address To Verify",
        key="placeholder"
)

if text_input:
    st.write("You entered:", text_input)
user_address = text_input
    
# Geocode the user-inputted address
user_location = geolocator.geocode(user_address)

# Iterate through the rows of the DataFrame and check for exact or fuzzy matches
for index, row in database_df.iterrows():
    if str(row['Address 2']) != "nan":
        current_address = f"{row['Address 1']} {str(row['Address 2'])} {row['City']} {row['State']} {str(row['Zip'])}"
    else:
        current_address = f"{row['Address 1']} {row['City']} {row['State']} {str(row['Zip'])}"

    if user_address.lower() == current_address.lower():
      st.write("Exact match found: " + current_address)
      quit()

    whole_address_ratio = fuzz.ratio(user_address.lower(), current_address.lower())
    street_address_ratio = fuzz.ratio(user_address.lower(), row['Address 1'].lower())

    if whole_address_ratio > 80 or street_address_ratio > 80:
      st.write("Possible match found: " + current_address)
      quit()

print("No match found in database, checking against Google...")

# Geocode the user-inputted address
user_location = geolocator.geocode(user_address)
user_location_is_partial_match = False

# Check if the user-inputted address was geocoded
if hasattr(user_location, "address"):
    raw_user_location = user_location.raw
    user_location_is_partial_match = "partial_match" in raw_user_location and raw_user_location["partial_match"] == True

# Iterate through the rows of the DataFrame and check Google for matches
for index, row in database_df.iterrows():
    if str(row['Address 2']) != "nan":
        current_address = f"{row['Address 1']} {str(row['Address 2'])} {row['City']} {row['State']} {str(row['Zip'])}"
    else:
        current_address = f"{row['Address 1']} {row['City']} {row['State']} {str(row['Zip'])}"

    if not hasattr(user_location, "address"):
      continue

    test_location = geolocator.geocode(current_address)
    test_location_is_partial_match = False

    # Check if the test address was geocoded
    if hasattr(test_location, "address"):
      raw_test_location = test_location.raw
      test_location_is_partial_match = "partial_match" in raw_test_location and raw_test_location["partial_match"] == True

    # print(f"Test location: {test_location} (partial match: {test_location_is_partial_match})")

    if user_location == test_location:
      if user_location_is_partial_match or test_location_is_partial_match:
        st.write(f"{user_address} is a partial match for {current_address}")
        quit()
      else:
        st.write(f"{user_address} is similar to {current_address}. Did you mean {current_address}?")
        quit()
else:
    st.write("No match found in database or Google. Try providing a more complete address.")
