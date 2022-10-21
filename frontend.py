#import packages
import streamlit as st
from PIL import Image

from backend import *
from startpage import *
from treemap import *


#load favicon
im = Image.open("./favicon.ico")

#configure page
st.set_page_config(
    page_title = "Securities",
    page_icon = im,
    layout = "wide"
    )
 

#list pages
pages = {
"Treemap": treemap,
"Earnings": startpage,
    }

#run app
selected_page = st.sidebar.selectbox("Menu:", options = pages.keys(), index = 0)
pages[selected_page]()