import os
import requests
import json
import re
import streamlit as st
import streamlit_authenticator as stauth
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

from helper import *

load_dotenv(".env")
KEY = os.getenv("KEY")

st.set_page_config(layout="wide",initial_sidebar_state="collapsed")
user_list="{\"usernames\":{"
res = requests.get(url = "http://127.0.0.1:8000/users").json()
for user in res:
    user_list +="\"" + user['user_name'] + "\":{\"email\":\"" + user['email'] + "\", \"name\":\"Ime\", \"password\":\"" + user['hashed_password'] + "\"},"
user_list = user_list[:-1]
user_list+="}}"
json_object = json.loads(user_list)

authenticator = stauth.Authenticate(json_object,"random_cookie_name",KEY,30)

name, authentication_status, username = authenticator.login()

if authentication_status:
    with st.sidebar:
        selected_team = sidebar_form(username)
    authenticator.logout('Logout', 'sidebar')
    if selected_team == "Home":
        main_tabs = st.tabs(["Event calendar","Create new team","Create new Event","Friends"])    
        with main_tabs[0]:
            #calendar_form(username,"Home")
            ev=(get_user_events(username))
            if not ev:
                ev = []
            calendar_form(username,ev)
        with main_tabs[1]:
            create_new_team_form(username)
        with main_tabs[2]:
            create_new_event_form(username)
        with main_tabs[3]:
            friends_tab(username) 
    else:
        team_site(selected_team)
        calendar_events = get_team_events(selected_team)
        calendar_form(username,calendar_events)
          
    
else:
    if authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')
    with st.expander("Don't have an account, Sign Up here:"):
        sign_up_form()

