
# Import necessary libraries
import streamlit as st
import pandas as pd
import joblib

# Load data
data = pd.read_csv(r"C:/Users/durga prasad/Desktop/project/.venv/retail_sales/singapore.csv")

# Create dictionary to get the encoded values
town_dict = dict(zip(data['town'].unique(), data['town_code'].unique()))
model_dict = dict(zip(data['flat_model'].unique(), data['flat_modelcode'].unique()))
town_list = data['town'].unique()
model_list = data['flat_model'].unique()
room_category = {'1 ROOM': 1,
       '2 ROOM':2,
       '3 ROOM':3,
       '4 ROOM':4,
       '5 ROOM':5,
       'EXECUTIVE':6,
       'MULTI GENERATION':7}
type_list = list(room_category.keys())

# Set page config for the web app
st.set_page_config(page_title='Resale Price Prediction', layout='wide')
st.title('Singapore Flat Resale Price Prediction')

# Create columns in UI
col1,col2,col3,col4,col5 = st.columns(5)

with col1:
   # Create input field for year input
    selling_year = st.number_input('Selling Year',value=None, placeholder="yyyy") #number_input

with col2:
   # Create input field for month input
   selling_month = int(st.select_slider('Selling month',options=[1,2,3,4,5,6,7,8,9,10,11,12])) #select_slider

with col3:
   # Create input field for town
   town_key= st.selectbox('Town',options=town_list)

with col4:
    # Create input field for flat type
    flat_type_key = st.selectbox('Flat Type',options=type_list)

with col1:
   # Create input field for storey range
   storey_range = st.text_input('Storey range',value=None, placeholder="ex: 01 TO 03") #text_input

with col2:
   # Create input field for floor area
   floor_area_sqm = st.number_input('Floor Area (sqm)',value=None, placeholder="Type floor area...") #number_input

with col3:
   # Create input field for flat model
   flat_model = st.selectbox('Flat Model',options = model_list) #text_input

with col4:
   # Create input field for lease commence date
   lease_commence_date = st.number_input('Lease Commence Date',value=None, placeholder="yyyy") #number_input

with col5:
   # Create input field for lease commence date
   remaining_lease_years = st.number_input('Remaining Lease Years',value=None) #number_input

# Function to load pickled model
def model_data():
   with open("C:/Users/durga prasad/Desktop/project/.venv/retail_sales/rf_model.pkl", "rb") as file:
      model = joblib.load(file)
   return model

# Function to predict
def predict(model,a,b,c,d,e,f,g,h,i):
   pred_value = model.predict([[a,b,c,d,e,f,g,h,i]])
   return pred_value 

# Create predict button
if st.button('Predict Price'):
    town = town_dict[town_key]
    flat_type = room_category[flat_type_key]

    # Check if storey_range is not None
    if storey_range is not None:
        # Split storey_range and handle the case where it doesn't return two values
        storey_values = storey_range.split(" TO ")
        if len(storey_values) == 2:
            storey_min, storey_max = map(int, storey_values)
        else:
            # Handle the case where storey_range doesn't contain two values
            st.error("Invalid storey range. Please enter a valid range.")

        flat_modelcode = model_dict[flat_model]
        # Call predict function
        pred = predict(model_data(), selling_year, selling_month, town, storey_min, storey_max, floor_area_sqm, flat_modelcode, lease_commence_date,remaining_lease_years)

        # Display predicted price in dollar
        st.success(f'Predicted Price: ${pred[0]:,.2f}')

        # Display predicted price in INR
        st.success(f'Resale Price in INR: ₹{(pred[0] * 63.02):,.2f}')
    else:
        # Handle the case where storey_range is None
        st.error("Please enter a valid storey range.")

