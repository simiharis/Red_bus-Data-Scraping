
import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_option_menu import option_menu





# Load CSV files and convert route names to lists
state_routes = {
    "Andhra Pradesh": pd.read_csv("APSRTC_bus_details.csv")['Route_Name'].tolist(),
    "Telungana": pd.read_csv("TSRTC_bus_details.csv")['Route_Name'].tolist(),
    "Uttar Pradesh": pd.read_csv("UPSRTC_bus_details.csv")['Route_Name'].tolist(),
    "South Bengal": pd.read_csv("South_Bengal_bus_details.csv")['Route_Name'].tolist(),
    "Himachal Pradesh": pd.read_csv("HRTC_bus_details.csv")['Route_Name'].tolist(),
    "West Bengal": pd.read_csv("WBTC_bus_details.csv")['Route_Name'].tolist(),
    "Rajasthan": pd.read_csv("RSRTC_bus_details.csv")['Route_Name'].tolist(),
    "Kerala": pd.read_csv("KSRTC_bus_details.csv")['Route_Name'].tolist(),
    "Assam": pd.read_csv("ASTC_bus_detais.csv")['Route_Name'].tolist(),
    "Bihar": pd.read_csv("BSRTC_bus_detais.csv")['Route_Name'].tolist()
}

# Define the function to fetch and filter bus data
def type_and_fare(route_name, bus_type, fare_range):
    conn = mysql.connector.connect(host="localhost", user="root", password="simi", database="REDBUS")
    my_cursor = conn.cursor()

    # Define fare range
    fare_min, fare_max = {
        "50-1000": (50, 1000),
        "1000-2000": (1000, 2000),
        "2000 and above": (2000, 100000)
    }.get(fare_range, (0, 100000))

    # Define bus type condition
    bus_type_condition = {
        "sleeper": "Bus_type LIKE '%Sleeper%'",
        "semi-sleeper": "Bus_type LIKE '%A/c Semi Sleeper%'",
        "others": "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"
    }.get(bus_type, "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'")

    query = f'''
        SELECT * FROM redBusdata 
        WHERE Price BETWEEN {fare_min} AND {fare_max}
        AND Route_name = "{route_name}"
        AND {bus_type_condition} 
        ORDER BY Price DESC
    '''
    my_cursor.execute(query)
    out = my_cursor.fetchall()
    conn.close()

    # Convert the results to a DataFrame
    df = pd.DataFrame(out, columns=[
        "ID","Route_name", "Route_link", "Bus_name", "Bus_type", "Departing_Time",
        "Duration", "Reaching_time", "Star_Rating", "Price", "Seat_Availability"
    ])
    
    return df

# Streamlit App Layout
st.set_page_config(page_title="Red Bus", layout="wide")

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Find Buses", "About"],
        icons=["house", "bus", "info-circle"],
        default_index=0
    )

# Home Page
if selected == "Home":
    st.markdown("<h1 style='color:red;text-align:center;'>Welcome to Red Bus Travels</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:blue;text-align:center;'>Your one-stop destination for bus ticket booking services</h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:green;text-align:center;'>Book your bus tickets at the best prices!</h4>", unsafe_allow_html=True)
    st.image("https://4.imimg.com/data4/IT/NQ/MY-13785395/bus-ticket-booking-services-500x500.gif", use_column_width=True)
    st.markdown('''- **Easy Booking**: Book your bus tickets in just a few clicks.
- **Wide Range of Options**: Choose from a variety of bus routes and timings.
- **Best Prices**: Get the best deals on bus tickets.''')

# Find Buses Page
elif selected == "Find Buses":
    st.title("Bus Information")
    selected_route = st.selectbox("Select a state", list(state_routes.keys()))
    select_type = st.radio("Choose bus type", ("sleeper", "semi-sleeper", "others"))
    select_fare = st.radio("Choose fare range", ("50-1000", "1000-2000", "2000 and above"))
    #TIME = st.time_input("Select the time")

    # Display bus routes for the selected state
    route_name = st.selectbox("List of routes", state_routes[selected_route])

    # Fetch filtered bus data
    df_result = type_and_fare(route_name, select_type, select_fare)
    st.dataframe(df_result)

# About Us Page
elif selected == "About":
    
    st.markdown("<h2 style='color:red;'>Red bus data scraping using selenium and dynamic filtering using streamlit</h2>", unsafe_allow_html=True)
    st.write("This is a web scraping project that scrapes bus data from the redBus website and displays it using Streamlit.")
    st.write("The project uses the Selenium library to scrape the data and the Streamlit library to create the web app.")
    st.write("The user can filter the bus data based on the route, bus type, and fare range.")

    