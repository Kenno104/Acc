import streamlit as st
import pandas as pd
from PIL import Image

# url: 'https://forms.gle/uSaFmv8ZNv33yyd78'

#Page Configuration
st.set_page_config(page_title='Acclimatise Demo',
                   page_icon='i',
                   layout='wide')

col1, col2, col3 = st.columns(3)
with col2:

  st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>Welcome to the Acclimatise Demo</h1>", unsafe_allow_html=True)
  
  st.markdown("<h4 style = 'text-align: center;'>This page will host the latest developments in the production of the Acclimatise MVP. <br> We hope to update it regularly as more functionality and interactivity is incorporated. <br> <br> Currently, the purpose of this demo is to convey a familiar and intuitive use case for the Acclimatise platform by exhibiting how users can choose the right utility bill for their energy usage habits.</h4>", unsafe_allow_html=True)

# divider
st.markdown("<hr style='background-color:black;'>", unsafe_allow_html=True)

############## DEMO INTRO
col1, col2 = st.columns(2)
with col1:
  st.markdown("<h3 style='color: #F39A68;'>What is the Purpose of this Demo?</h3>", unsafe_allow_html=True)
  
  st.markdown("<h5> Acclimatise aims to give customers specific enery solutions that cater for their circumstances. <br> It will take time to build out this functionality, and different customers will benefit from some features and products more than others. Therefore, the purpose of this demo is to introduce the general concept behind Acclimatise and convey the intended user experience with a simple but familiar use case.</h5>", unsafe_allow_html=True)
      
with col2:
  image2 = Image.open('esb.jpg')
  st.image(image2, caption='ESB Smart Meter Account')

st.markdown("<h3 style='color: #F39A68;'><center><b>Example Use Case:</b> Choosing the Optimum Electricity Supplier for your Energy Circumstances</center></h3>", unsafe_allow_html=True)
  
st.markdown("<h5> With the roll-out of smart meters and night-saver tariffs in Ireland the task of choosing the best value electricity rate is no longer as simple as it once was. Choosing the optimum rate now requires an understanding of your daily energy usage habits and a more detailed cost-comparison process. </a> <br><br> For the purpose of this demo, we'll take approximately 2 months of a household's electricity data over the December-January period, shown below, and use this to obtain the optimum energy tariff for this specific house. <br> If you would like to view the electricity consumption of your own home, you can access the smater meter readings for your house <a href='https://myaccount.esbnetworks.ie/''>here.</h5>", unsafe_allow_html=True)
       
######## Data Manipulation ############

#Initialise df
df = pd.read_csv('sample_data.csv')
df = df.drop(['MPRN','Meter Serial Number','Read Type'], axis = 1)
df = df.rename(columns={"Read Value": "Power", "Read Date & Time": "Time"})

df['Time'] = df['Time'].astype('string')
df['Time'] = pd.to_datetime(df['Time'], format = '%d-%m-%Y %H:%M')

df['Energy (kWh)'] = df['Power'] * 0.5
df['Current_Cost(€)'] = df['Energy (kWh)'] * 0.4089
df['Night_Energy'] = 0
df['Night_Rate(€)'] = 0
df['Peak_Energy'] = 0
df['Peak_Rate(€)'] = 0

#Night Data
for i in range(len(df)):
  x = str(df['Time'].iloc[i])
  x = x[-8:-6]
  x = int(x)
  if x >= 22 or x <= 8:
    df['Night_Energy'].iloc[i] = df['Energy (kWh)'].iloc[i]
    df['Night_Rate(€)'].iloc[i] = df['Energy (kWh)'].iloc[i] * 0.2339

#Get Peak Data
for i in range(len(df)):
  x = str(df['Time'].iloc[i])
  x = x[-8:-6]
  x = int(x)
  if x >= 17 and x <= 19:
    df['Peak_Energy'].iloc[i] = df['Energy (kWh)'].iloc[i]
    df['Peak_Rate(€)'].iloc[i] = df['Energy (kWh)'].iloc[i] * 0.4746

#Values to Calculate:
#Total Consumption:
#Final Values
total_energy = int(df['Energy (kWh)'].sum())
total_night_energy = int(df['Night_Energy'].sum())
total_current_cost = int(df['Current_Cost(€)'].sum())
total_night_cost = int(df['Night_Rate(€)'].sum())
total_peak_energy = int(df['Peak_Energy'].sum())
total_peak_cost = int(df['Peak_Rate(€)'].sum())

night_percentage = int((total_night_energy / total_energy)*100)
peak_percentage = int((total_peak_energy / total_energy)*100)

##GRAPH############################################################
# # Setting the first column as index, important
df.set_index('Time', inplace=True)

with st.container():
  st.line_chart(df['Energy (kWh)'])

#Data Analysis Explanation
st.markdown("<h3 style='color: #F39A68;'>Analysing your Home Energy Consumption</h3>", unsafe_allow_html=True)

st.markdown("<h5> By leveraging the data provided by smart meters, a number of customer-specific insights can be inferred to inform users of their energy usage habits. This information can then be used to evaluate what energy solutions may be feasible for the specific customer. <br> In this case, we are identifying the optimal electricity tariff for a particular customer. <br><br> Shown below is a typical customer dashboard that can be created from a simple analysis of the given data. As this demo develops in the coming months, we aim to incorporate more detailed analytics and allow users to analyse their own energy data as well. </h5>", unsafe_allow_html=True)

# divider
st.markdown("<hr style='background-color:black;'>", unsafe_allow_html=True)

##################################        DASHBOARD

# Introduce Customer Dashboard
st.markdown("<h2 style='text-align: center; color: #FFFFFF;'>Customer Dashboard<br><br></h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:#Show total electricity consumption to date (kWh) - compare with national average
  col1.metric(label="Total Energy Consumption", value= f'{total_energy} kWh')

with col2: #Show night-time energy consumption - compare with national average
  col2.metric(label="Total Night-Time Consumption (23:00 - 8:00)", value= f'{total_night_energy} kWh')

with col3: #Total Peak Time Consumption(17:00 - 19:00)
  col3.metric(label="Total Peak Time Consumption(17:00 - 19:00)", value= f'{total_peak_energy} kWh')

st.markdown("<h2 style='text-align: center; color: #FFFFFF;'><br></h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1: #Show estimated cost under current plan - compare with cost of ideal plan for customer profile
  col1.metric(label="Estimated Cost to Date", value= f'€{total_current_cost}')
  
with col2: #Percentage Night-Time Energy
  col2.metric(label="Percentage Night-Time Energy", value= f'{night_percentage}%')
  
with col3: #Percentage Peak-Time Energy
  col3.metric(label="Percentage Peak-Time Energy", value= f'{peak_percentage}%')

# divider
st.markdown("<hr style='background-color:black;'>", unsafe_allow_html=True)

###############Customer Actions################

st.markdown("<h2 style='text-align: center; color: #FFFFFF;'>Recommended Actions<br><br></h2>", unsafe_allow_html=True)

st.markdown("<h4 style= 'color: #FFFFFF;'>Under your current plan: <span style= 'color: #0075B0;'> Electric Ireland - Home Electric+</span>, we estimate your next bi-monthly bill to be approx. <span style= 'color: #AF4F41;' > €430.</span><br></h4>", unsafe_allow_html=True)

st.markdown("<h4 style= color: #FFFFFF;'>Your Energy Usage Analysis indicates that you may be a good candidate for the <span style= 'color: #0075B0;'> Electric Ireland Night Saver </span> plan, and potentially save up to <span style= 'color: #799B3E;'> €63 </span> on your next bill. <br><br> Here are a few suggestions: <br><br></h4>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
  st.markdown("<h3 style= 'text-align: center; color: #FFFFFF;'> Electric Ireland <br> Home Electric+ Night Boost</h3>", unsafe_allow_html=True)
  st.markdown("<h6 style= 'text-align: center; color: #FFFFFF;'>Estimated Bill</h6>", unsafe_allow_html=True)
  st.markdown("<h1 style= 'text-align: center; color: #FFFFFF;'> €367 <br></h1>", unsafe_allow_html=True)
  st.markdown("<h6 style= 'text-align: center; color: #F39A68;'>Best Value<br><br></h6>", unsafe_allow_html=True)
  col4, col5, col6, col7, col8 = st.columns(5)
  with col6:
    st.button('Switch Now', key = 1)
  


with col2:
  st.markdown("<h3 style= 'text-align: center; color: #FFFFFF;'> Electric Ireland <br>Green Electricity NightSaver</h3>", unsafe_allow_html=True)
  st.markdown("<h6 style= 'text-align: center; color: #FFFFFF;'>Estimated Bill</h6>", unsafe_allow_html=True)
  st.markdown("<h1 style= 'text-align: center; color: #FFFFFF;'> €392 <br></h1>", unsafe_allow_html=True)
  st.markdown("<h6 style= 'text-align: center; color: #799B3E;'>Green Option<br><br></h6>", unsafe_allow_html=True)
  col9, col10, col11, col12, col13 = st.columns(5)
  with col11:
    st.button('Switch Now', key = 2)

with col3:
  st.markdown("<h3 style= 'text-align: center; color: #FFFFFF;'> SSE Airtricity <br>Green Night Boost</h3>", unsafe_allow_html=True)
  st.markdown("<h6 style= 'text-align: center; color: #FFFFFF;'>Estimated Bill</h6>", unsafe_allow_html=True)
  st.markdown("<h1 style= 'text-align: center; color: #FFFFFF;'> €380 <br></h1>", unsafe_allow_html=True)
  st.markdown("<h6 style= 'text-align: center; color: #F39A68;'>Best New Customer Discount <br><br> </h6>", unsafe_allow_html=True)
  col14, col15, col16, col17, col18 = st.columns(5)
  with col16:
    st.button('Switch Now', key = 3)
    