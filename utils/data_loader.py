
import pandas as pd
import streamlit as st

@st.cache_data
def load_data(path=r"C:\Users\anush\OneDrive\Desktop\projects\home credit\data\application_train.csv"):
    df = pd.read_csv(filepath_or_buffer=path)
    return df
#from utils.data_loader import clean_data