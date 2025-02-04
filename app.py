# app.py (main file)
import streamlit as st
st.set_page_config(layout="wide") 

from streamlit_option_menu import option_menu
import importlib.util
from pathlib import Path

EXAMPLE_NO = 1
def streamlit_menu(example=1):
   if example == 1:
       with st.sidebar:
           return option_menu(
               menu_title="Main Menu",
               options=["Home","Medical Diagnosis Agent"],
            #    options=["Home","Deepseek","Chatgpt"],
               icons=["house", "book", "envelope"],
               menu_icon="cast",
               default_index=0
           )
   
   if example == 2:
       return option_menu(
           menu_title=None,
           options=["Home", "Projects", "Contact"],
           icons=["house", "book", "envelope"],
           menu_icon="cast",
           default_index=0,
           orientation="horizontal"
       )
   
   if example == 3:
       return option_menu(
           menu_title=None,
           options=["Home", "Projects", "Contact"],
           icons=["house", "book", "envelope"],
           menu_icon="cast",
           default_index=0,
           orientation="horizontal",
           styles={
               "container": {"padding": "0", "background-color": "#fafafa"},
               "icon": {"color": "orange", "font-size": "25px"},
               "nav-link": {
                   "font-size": "25px",
                   "text-align": "left",
                   "margin": "0px",
                   "--hover-color": "#eee",
               },
               "nav-link-selected": {"background-color": "green"},
           }
       )

# EXAMPLE_NO = st.selectbox('Select Menu Style:', [1, 2, 3])
selected = streamlit_menu(example=EXAMPLE_NO)

if selected:
   page = Path(__file__).parent / f"{selected}/{selected.lower()}.py"
   spec = importlib.util.spec_from_file_location(selected, page)
   module = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(module)

