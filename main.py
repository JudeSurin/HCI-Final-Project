# FINAL PROJECT

import streamlit as st
import requests
import folium
import polyline
import pandas as pd
from datetime import datetime
from streamlit_folium import folium_static




st.title("Lease Mile Manager App")
st.header("Streamlit and Google Maps API")
api_key = "AIzaSyAbR45vcfyN2rn57SzXJZEA_pxMUJEXv4g"


def calculate_original_mileage_data(mileage_contracted, months_contracted):
    # Constants for time conversion factors
    days_per_year = 365.242199  # Average number of days in a year to account for leap years
    months_per_year = 12  # Number of months in a year
    weeks_per_year = 52.143  # Average number of weeks in a year

    # Calculate yearly mileage based on total contracted mileage and months of the contract
    yearly_mileage = mileage_contracted / (months_contracted / months_per_year)

    # Calculate monthly mileage by dividing the yearly mileage by the number of months in a year
    monthly_mileage = yearly_mileage / months_per_year

    # Calculate weekly mileage by dividing the yearly mileage by the number of weeks in a year
    weekly_mileage = yearly_mileage / weeks_per_year

    # Calculate daily mileage by dividing the yearly mileage by the number of days in a year
    daily_mileage = yearly_mileage / days_per_year

    # Return the calculated mileages as a list for yearly, monthly, weekly, and daily periods
    return [yearly_mileage, monthly_mileage, weekly_mileage, daily_mileage]


def calculate_remaining_mileage_data(mileage_contracted, lease_end_date, current_mileage):
    # Constants for time conversion factors
    days_per_year = 365.242199  # Average number of days in a year to account for leap years
    days_per_month = 30.417     # Average number of days in a month
    days_per_week = 7           # Number of days in a week

    # Calculate the remaining mileage by subtracting the current mileage from the contracted mileage
    remaining_mileage = mileage_contracted - current_mileage
    # Calculate the number of days left until the lease ends
    remaining_days = (lease_end_date - datetime.now().date()).days

    # Check if the lease has already ended or ends today
    if remaining_days <= 0:
        return [0, 0, 0, 0]  # No days left in the lease, so no mileage left to allocate

    # Calculate daily mileage allowed from now to the end of the lease
    daily_mileage = remaining_mileage / remaining_days

    # Calculate weekly, monthly, and yearly mileage based on the daily mileage
    weekly_mileage = daily_mileage * days_per_week
    monthly_mileage = daily_mileage * days_per_month
    yearly_mileage = daily_mileage * days_per_year

    # Determine the appropriate mileage data to return based on the remaining lease duration
    if remaining_days >= days_per_year:
        # If more than a year remains, return all calculated mileages
        return [yearly_mileage, monthly_mileage, weekly_mileage, daily_mileage]
    elif remaining_days >= days_per_month:
        # If less than a year but more than a month remains, exclude yearly mileage
        return [0, monthly_mileage, weekly_mileage, daily_mileage]
    elif remaining_days >= days_per_week:
        # If less than a month but more than a week remains, exclude yearly and monthly mileage
        return [0, 0, weekly_mileage, daily_mileage]
    else:
        # If less than a week remains, only provide daily mileage
        return [0, 0, 0, daily_mileage]


def display_mileage_info_current():
    # Calculate original contracted yearly, monthly, weekly, and daily mileage
    mileage_contracted_year, mileage_contracted_month, mileage_contracted_week, mileage_contracted_day = (
        calculate_original_mileage_data(mileage_contracted, months_contracted))

    # Calculate remaining mileage allowances based on the current mileage and the lease end date
    current_mileage_yearly, current_mileage_month, current_mileage_week, current_mileage_day = (
        calculate_remaining_mileage_data(mileage_contracted, lease_end_date, current_mileage))

    # Calculate the remaining mileage by subtracting current mileage from contracted mileage
    remaining_mileage = mileage_contracted - current_mileage

    # Calculate the number of days left until the lease ends
    remaining_days = (lease_end_date - datetime.now().date()).days

    # Prepare data for display: compiling original and current mileage details
    data = {
        "Original": ["Contracted Mileage", "Original Yearly Mileage",
                     "Monthly Mileage", "Weekly Mileage", "Daily Mileage"],
        "Original Mileage": [
            mileage_contracted,  # Original Contracted Miles
            mileage_contracted_year,  # Original Yearly Mileage
            mileage_contracted_month,  # Monthly Mileage
            mileage_contracted_week,  # Weekly Mileage
            mileage_contracted_day,  # Daily Mileage
        ],
        "Current": ["Remaining Mileage", "Current yearly mileage", "Current Monthly Mileage",
                    "Current Weekly Mileage", "Current Daily Mileage"],
        "Current Mileage": [
            remaining_mileage,  # Remaining Mileage
            current_mileage_yearly,  # Current Yearly Mileage
            current_mileage_month,  # Current Monthly Mileage
            current_mileage_week,  # Current Weekly Mileage
            current_mileage_day  # Current Daily Mileage
        ]
    }

    # Create a DataFrame from the data dictionary and display it using Streamlit
    df = pd.DataFrame(data)
    st.info(f"You have {remaining_days} days left in this lease")
    st.dataframe(df)

    # Display a success message if there is no excess mileage yet
    st.success(f"You do not have any excess mileage yet")


def display_mileage_info_future():
    # Constants for time conversion factors
    months_per_year = 12  # Number of months in a year
    weeks_per_year = 52.143  # Average number of weeks in a year to accommodate fractional weeks
    days_per_year = 365.242199  # Average number of days in a year accounting for leap years

    # Calculate the total mileage for the entire contract duration
    total_contract_mileage = (lease_length / months_per_year) * lease_mileage

    # Calculate yearly, monthly, weekly, and daily mileage based on the annual lease mileage
    total_yearly_mileage = lease_mileage  # Yearly mileage is the lease mileage
    total_monthly_mileage = lease_mileage / months_per_year  # Divide the yearly mileage by the number of months
    total_weekly_mileage = lease_mileage / weeks_per_year  # Divide the yearly mileage by the number of weeks
    total_daily_mileage = lease_mileage / days_per_year  # Divide the yearly mileage by the number of days

    # Prepare data for display: compiling mileage information
    data = {
        "Original": ["Contract's total mileage", "Contract's yearly mileage",
                     "Contract's monthly mileage", "Contract's weekly mileage", "Contract's daily mileage"],
        "Original Mileage": [
            total_contract_mileage,  # Total mileage for the contract duration
            total_yearly_mileage,  # Yearly mileage
            total_monthly_mileage,  # Monthly mileage
            total_weekly_mileage,  # Weekly mileage
            total_daily_mileage,  # Daily mileage
        ]
    }

    # Create a DataFrame from the data dictionary and display it using Streamlit
    df = pd.DataFrame(data)
    st.text("You will have: ")
    st.dataframe(df)


def excess_fee_amount(excess_fee, current_mileage, mileage_contracted):
    # Calculate the number of miles the user is over their contracted mileage limit
    excess_miles = current_mileage - mileage_contracted

    # Calculate the total fee for the excess miles by multiplying by the per mile excess fee
    excess_miles_fee = excess_miles * excess_fee

    # Display an error message in the Streamlit app showing the number of excess miles and the total excess fee
    st.error(f"You are {excess_miles} miles over your contracted miles. "
             f"Your current fee is {excess_miles_fee}")


def calculate_route(start, end, api_key):
    # Construct the URL for the Google Maps Directions API with the specified parameters.
    # `origin` is the start location, `destination` is the end location,
    # `mode` specifies the type of transportation, which is driving in this case, and `key` is the API key.
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start}&destination={end}&mode=driving&key={api_key}"

    # Send a request to the Google Maps Directions API and store the response.
    response = requests.get(url)

    # Parse the JSON response into a dictionary.
    directions = response.json()

    # Check if the API query was successful.
    if directions['status'] == 'OK':
        # Extract the encoded polyline from the response. The polyline describes the route's shape.
        enc_polyline = directions['routes'][0]['overview_polyline']['points']

        # Decode the polyline to get a list of latitude and longitude points that describe the route.
        path = polyline.decode(enc_polyline)

        # Extract the distance and duration of the route from the response.
        # These are generally in human-readable format (e.g., '14.5 km', '12 mins').
        distance = directions['routes'][0]['legs'][0]['distance']['text']
        duration = directions['routes'][0]['legs'][0]['duration']['text']

        # Extract the starting and ending GPS coordinates of the route.
        start_location = directions['routes'][0]['legs'][0]['start_location']
        end_location = directions['routes'][0]['legs'][0]['end_location']

        # Return the decoded path along with distance, duration, start, and end locations.
        return path, distance, duration, start_location, end_location
    else:
        # If the API query was not successful, return None for all fields.
        return None, None, None, None, None


def display_map(path, start_location, end_location):
    # Create a new Folium Map object. The map is centered at the start location's coordinates.
    # `zoom_start` specifies the initial zoom level for the map.
    map = folium.Map(location=[start_location['lat'], start_location['lng']], zoom_start=13)

    # Add a polyline to the map using the list of (lat, lng) tuples in `path`.
    # This polyline represents the route between the start and end locations.
    folium.PolyLine(path).add_to(map)

    # Add a marker to the map at the start location.
    # `tooltip` is a text that appears when the mouse hovers over the marker.
    folium.Marker([start_location['lat'], start_location['lng']], tooltip='Start').add_to(map)

    # Add a marker to the map at the end location with a tooltip.
    folium.Marker([end_location['lat'], end_location['lng']], tooltip='End').add_to(map)

    # Display the map in the Streamlit app using the `folium_static` function from streamlit_folium.
    # This function renders a Folium map as a static image within a Streamlit page.
    folium_static(map)


def create_account_form():
    # Request the user's email via a text input widget in the sidebar.
    # The function st.sidebar.text_input displays a text box in the sidebar where users can enter their email.
    email = st.sidebar.text_input("Enter your email")

    # Create a button in the sidebar that users can click to submit their email and create an account.
    # The function st.sidebar.button returns True when the button is clicked, triggering the conditional.
    if st.sidebar.button("Create account"):
        # Check if the email variable contains any text, which indicates that the user has entered something.
        if email:
            # If an email is provided, update the session state to reflect that an account has been created.
            # st.session_state['create_account'] is a persistent variable that holds the state of account creation.
            st.session_state['create_account'] = True

            # Display a success message in the sidebar using st.sidebar.success to inform the user that the account was created successfully.
            st.sidebar.success("Account created successfully!")
        else:
            # If no email is entered (email string is empty), display an error message prompting the user to enter an email address.
            # This uses st.sidebar.error to show the message in the sidebar.
            st.sidebar.error("Please enter an email address.")


# Initialize the 'create_account' flag in the session state if it's not already set.
# This flag will keep track of whether a user has created an account.
if 'create_account' not in st.session_state:
    st.session_state['create_account'] = False


account_type = st.sidebar.selectbox("Please choose how you wish to continue", options=["Continue as a Guest",
                                                                                       "Create an Account"])
st.sidebar.info("If you choose to continue as a Guest your information will not be saved")


if account_type == "Continue as a Guest":
    lease_type = st.sidebar.selectbox("Are we working on", options=["Current lease", "Future lease"])
    if lease_type == "Current lease":
        lease_end_date = st.date_input("Please select the lease end date")
        months_contracted = st.number_input("Enter the your lease's total contracted number of months", min_value=1)
        mileage_contracted = st.number_input("Enter the your lease's total contracted miles", min_value=1)
        current_mileage = st.number_input("Enter the current mileage of your car", min_value=0)
        excess_fee_known = st.selectbox("Do you know your miles excess charge fee, "
                                        "if no we will use the average $0.20/mile",
                                        options=["", "Yes", "No"])
        if excess_fee_known == "Yes":
            excess_fee = st.number_input("Enter the excess fee per mile", min_value=0.0, format="%.2f")

        elif excess_fee_known == "No":
            excess_fee = 0.20
            if current_mileage <= mileage_contracted:
                display_mileage_info_current()
            else:
                excess_fee_amount(excess_fee, current_mileage, mileage_contracted)

    else:
        lease_length = st.number_input("Please the desired lease's length in months (e.g 36 for 36 months)", min_value=1)
        lease_mileage = st.number_input("What is your desired yearly mileage. "
                                        "Please do not include any commas (e.g 10000 for 10,000/year)", min_value=1)
        display_mileage_info_future()

else:
    create_account_form()
    if st.session_state['create_account']:
        lease_type = st.sidebar.selectbox("Are we working on", options=["Current lease", "Future lease"])
        if lease_type == "Current lease":
            lease_end_date = st.date_input("Please select the lease end date")
            months_contracted = st.number_input("Enter the your lease's total contracted number of months", min_value=1)
            mileage_contracted = st.number_input("Enter the your lease's total contracted miles", min_value=1)
            current_mileage = st.number_input("Enter the current mileage of your car", min_value=0)
            excess_fee_known = st.selectbox("Do you know your miles excess charge fee, "
                                            "if no we will use the average $0.20/mile",
                                            options=["", "Yes", "No"])
            if excess_fee_known == "Yes":
                excess_fee = st.number_input("Enter the excess fee per mile", min_value=0.0, format="%.2f")

            elif excess_fee_known == "No":
                excess_fee = 0.20
                if current_mileage <= mileage_contracted:
                    display_mileage_info_current()
                    route_calculation = st.selectbox("Would you like to calculate how a future "
                                           "trip would affect the current mileage?",
                                           options=["Yes", "No"])
                    if route_calculation == "Yes":
                        start = st.text_input("Enter start location")
                        end = st.text_input("Enter destination location")
                        see_map = st.checkbox("Show on map.", value=True)
                        path, distance, duration, start_loc, end_loc = calculate_route(start, end, api_key)
                        if path:
                            st.write(f"Distance: {distance}, Duration: {duration}")
                            display_map(path, start_loc, end_loc)
                            clean_distance = distance.replace(' mi', '').replace(',', '')
                            current_mileage = current_mileage + int(clean_distance)
                            if current_mileage <= mileage_contracted:
                                display_mileage_info_current()
                            else:
                                excess_fee_amount(excess_fee, current_mileage, mileage_contracted)

                else:
                    excess_fee_amount(excess_fee, current_mileage, mileage_contracted)


        else:
            lease_length = st.number_input("Please the desired lease's length in months (e.g 36 for 36 months)",
                                           min_value=1)
            lease_mileage = st.number_input("What is your desired yearly mileage. "
                                            "Please do not include any commas (e.g 10000 for 10,000/year)", min_value=1)
            display_mileage_info_future()






