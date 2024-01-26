import datetime
import json
import random
import re
import time

import requests
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_calendar import calendar
from streamlit_option_menu import option_menu


def get_user_friends(username):
    user_info = requests.get(url="http://127.0.0.1:8000/account/" + username).json()
    return user_info["friends"]


def get_user_teams(username):
    user_info = requests.get(url="http://127.0.0.1:8000/account/" + username).json()
    user_teams_list = []
    for x in user_info["teams"]:
        user_teams_list.append(x["team_name"])
    user_teams_list.sort()
    return user_teams_list


def format_list_to_string(list_input):
    string_list = [str(element) for element in list_input]
    delimiter = '","'
    return '["' + delimiter.join(string_list) + '"]'


def create_new_event_form(username):
    user_friends = get_user_friends(username)
    user_teams = get_user_teams(username)
    if not user_friends:
        user_friends = []
    if not user_teams:
        user_teams = []
    with st.form(key="Create Event"):
        st.header("Create Event")
        event_name = st.text_input("Name", max_chars=30, key="event_name")
        date_start_end = st.date_input(
            "Select event start date and event end date",
            (datetime.datetime.now(), datetime.datetime.now()),
            format="MM.DD.YYYY",
        )
        time_color_columns = st.columns(3, gap="large")
        with time_color_columns[0]:
            event_start_time = st.time_input("Starts at")
        with time_color_columns[1]:
            event_end_time = st.time_input("Ends at")
        with time_color_columns[2]:
            event_color = st.color_picker("Color", "#0FFF00")
        teams_friends_columns = st.columns(2, gap="large")
        with teams_friends_columns[0]:
            teams_attending = st.multiselect("Invite Teams", user_teams)
        with teams_friends_columns[1]:
            friends_attending = st.multiselect("Invite Friends", user_friends)
        create_event_button = st.form_submit_button("Create event")
        if create_event_button:
            if not event_name:
                st.error("Event name can't be empty.")
            elif (
                date_start_end[0] == date_start_end[1]
                and event_start_time == event_end_time
            ):
                st.error("Event can't have a druation of 0.")
            else:
                post_string = (
                    '{"event_name": "'
                    + event_name
                    + " "
                    + event_color
                    + '", "starts_at": "'
                    + date_start_end[0].strftime("%Y-%m-%d")
                    + "T"
                    + event_start_time.strftime("%H:%M:%S")
                    + '", "ends_at": "'
                    + date_start_end[1].strftime("%Y-%m-%d")
                    + "T"
                    + event_end_time.strftime("%H:%M:%S")
                    + '", "attendees": '
                    + format_list_to_string(friends_attending)
                    + ', "teams": '
                    + format_list_to_string(teams_attending)
                    + "}"
                )
                post_string = post_string.replace('[""]', "[]")
                requests.post(
                    url="http://127.0.0.1:8000/create_event?user_name=" + username,
                    data=post_string,
                )
                st.success("You have created a new event.")


def create_new_team_form(username):
    user_friends = get_user_friends(username)
    if not user_friends:
        st.warning("You need friends to create a team.")
    else:
        with st.form(key="Create Team"):
            st.header("Create Team")
            team_name = st.text_input("Name", max_chars=30, key="team_name")
            team_description = st.text_input(
                "Description", max_chars=100, key="team_description"
            )
            team_members = st.multiselect("Team members", user_friends)
            team_button = st.form_submit_button("Create team")
            if team_button:
                if not team_name:
                    st.error("Team name can't be empty.")
                elif not team_description:
                    st.error("Team description can't be empty.")
                elif not team_members:
                    st.error("A team must have members.")
                elif nisam_script_kunem_se(team_name, "Team name"):
                    st.write()
                else:  # jos treba provjerit kako radi i osigurat po potrebi
                    requests.post(
                        url="http://127.0.0.1:8000/create_team?user_name=" + username,
                        data='{"team_name": "'
                        + team_name
                        + '", "description": "'
                        + team_description
                        + '", "members": '
                        + format_list_to_string(team_members)
                        + "}",
                    )
                    st.success("You have created a new team.")


def get_user_events(username):
    user_events = requests.get(url="http://127.0.0.1:8000/account/" + username).json()
    existing_events = []
    all_events = "["
    for event in user_events["events"]:
        existing_events.append(event["event_id"])
        all_events += (
            '{ "title": "'
            + event["event_name"][:-7]
            + '", "color": "'
            + event["event_name"][-7:]
            + '", "start": "'
            + event["starts_at"]
            + '", "end": "'
            + event["ends_at"]
            + '", "event_id": "'
            + str(event["event_id"])
            + '"},'
        )
    for team in user_events["teams"]:
        team_events = requests.get(
            url="http://127.0.0.1:8000/team/" + team["team_name"]
        ).json()
        if team_events["events"]:
            for team_event in team_events["events"]:
                if team_event["event_id"] not in existing_events:
                    existing_events.append(team_event["event_id"])
                    all_events += (
                        '{ "title": "'
                        + team_event["event_name"][:-7]
                        + '", "color": "'
                        + team_event["event_name"][-7:]
                        + '", "start": "'
                        + team_event["starts_at"]
                        + '", "end": "'
                        + team_event["ends_at"]
                        + '", "event_id": "'
                        + str(team_event["event_id"])
                        + '"},'
                    )
    all_events = all_events[:-1]
    all_events += "]"

    if all_events != "]":
        json_object = json.loads(all_events)
        return json_object
    else:
        return {}


def get_team_events(team_name):
    all_events = "["
    team_events = requests.get(url="http://127.0.0.1:8000/team/" + team_name).json()
    if team_events["events"]:
        for team_event in team_events["events"]:
            all_events += (
                '{ "title": "'
                + team_event["event_name"][:-7]
                + '", "color": "'
                + team_event["event_name"][-7:]
                + '", "start": "'
                + team_event["starts_at"]
                + '", "end": "'
                + team_event["ends_at"]
                + '", "event_id": "'
                + str(team_event["event_id"])
                + '"},'
            )
        all_events = all_events[:-1]
        all_events += "]"
        json_object = json.loads(all_events)
        return json_object
    return ""


def team_site(selected_team):
    st.title(selected_team)
    res = requests.get(url="http://127.0.0.1:8000/team/" + selected_team).json()
    team_columns = st.columns(2, gap="large")
    with team_columns[0]:
        st.subheader("Team description: ")
        st.write(res["description"])
    with team_columns[1]:
        st.subheader("Team members: ")
        memb = ""
        for member in res["members"]:
            memb += member["user_name"] + ", "
        memb = memb[:-2]
        st.code(memb)
    st.container(height=50, border=False)


def sidebar_form(username):
    st.markdown("UA NEOPLANTA PROJEKT")
    my_teams = ["Home"] + get_user_teams(username)
    ikone = ["house"]
    for x in range(len(my_teams)):
        ikone.append("s")
    selected_team = option_menu(
        None,
        my_teams,
        icons=ikone,
        styles={"container": {"background-color": "#f0f2f6"}},
    )
    return selected_team


def sign_up_form():
    with st.form(key="SignUp", clear_on_submit=True, border=False):
        st.subheader("Sign Up")
        email = st.text_input("Email", placeholder="Enter Your Email")
        username = st.text_input("Username", placeholder="Enter Your Username")
        password1 = st.text_input(
            "Password", placeholder="Enter Your Password", type="password"
        )
        password2 = st.text_input(
            "Confirm Password", placeholder="Confirm Your Password", type="password"
        )
        button = st.form_submit_button("Sign up")
        if button:
            sign_up_mail_password_check(username, email, password1, password2)


def sign_up_mail_password_check(username, mail, p1, p2):
    upper_letter = False
    for x in username:
        if x.isupper():
            upper_letter = True
    if (
        re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", mail)
        == None
    ):
        st.error("Email address not valid")
    elif p1 != p2:
        st.error("Passwords don't match")
    elif upper_letter:
        st.warning("Username must have only non capital letters")
    elif nisam_script_kunem_se(username, "User name"):
        st.write()
    else:
        res = requests.get(url="http://127.0.0.1:8000/account/" + username).text
        if res != '{"detail":"User with username: ' + username + " doesn't exist.\"}":
            st.warning("Username " + username + " is already taken.")
        elif len(p1) < 10:
            st.warning("Password must be at least 10 character long")
        elif (
            any(char.isupper() for char in p1) == False
            or any(char.islower() for char in p1) == False
        ):
            st.warning(
                "Password must contain at least one upper case letter and one lower case letter"
            )
        elif any(char.isdigit() for char in p1) == False:
            st.warning("Password must contain at least one number")
        else:
            p_list = [p1]
            hashed_password = stauth.Hasher(p_list).generate()
            requests.post(
                url="http://127.0.0.1:8000/register",
                data='{"user_name": "'
                + username
                + '","email": "'
                + mail
                + '","hashed_password": "'
                + hashed_password[0]
                + '"}',
            )
            st.success("You have created a new account.")


def friends_tab(username):
    friends_column, add_friends_column = st.columns([1, 1], gap="large")
    user_friends = get_user_friends(username)
    if not user_friends:
        user_friends = []
    else:
        user_friends.sort()
    st.write(user_friends)
    with friends_column:
        with st.container(height=700, border=False):
            st.subheader("My friends")
            for x in user_friends:
                st.code(x)
    with add_friends_column:
        with st.form(key="Add_new_friends"):
            st.subheader("Add new friends")
            add_friend = st.text_input("Insert username")
            add_friend_button = st.form_submit_button("Add Friend")
            if add_friend_button:
                friend_response = requests.get(
                    url="http://127.0.0.1:8000/account/" + add_friend
                ).text
                if friend_response.find("user_name") == -1:
                    st.error("User doesn't exist")
                else:
                    friend_user_name = friend_response[
                        friend_response.find(":") + 2 : friend_response.find(",") - 1
                    ]
                    if friend_user_name in user_friends:
                        st.warning(
                            "User " + friend_user_name + " is already your friend."
                        )
                    elif friend_user_name == username:
                        st.warning("You can't add yourself as a friend.")
                    else:
                        user_friends.append(friend_user_name)
                        requests.post(
                            url="http://127.0.0.1:8000/user/" + username + "/friends",
                            data=format_list_to_string(user_friends),
                        )
                        user2_friends = get_user_friends(friend_user_name)
                        if not user2_friends:
                            user2_friends = []
                        user2_friends.append(username)
                        requests.post(
                            url="http://127.0.0.1:8000/user/"
                            + friend_user_name
                            + "/friends",
                            data=format_list_to_string(user2_friends),
                        )
                        st.success("Added a new friend.")
                        time.sleep(0.5)
                        st.rerun()


def nisam_script_kunem_se(input_string, input_form):
    if "$" in input_string:
        st.warning(input_form + " can't have $ as a character.")
    elif '"' in input_string:
        st.warning(input_form + " can't have \" as a character.")
    elif "'" in input_string:
        st.warning(input_form + " can't have ' as a character.")
    elif "<" in input_string:
        st.warning(input_form + " can't have < as a character.")
    elif ">" in input_string:
        st.warning(input_form + " can't have > as a character.")
    elif " " in input_string:
        st.warning(input_form + " must be one word.")
    else:
        return False
    return True


def calendar_form(username, selected_events):
    year = datetime.datetime.now().strftime("%Y")
    month = datetime.datetime.now().strftime("%m")
    day = datetime.datetime.now().strftime("%d")
    this_day = year + "-" + month + "-" + day
    this_month = year + "-" + month + "-01"
    calendar_column, event_column = st.columns([1.3, 1], gap="medium")

    with calendar_column:
        mode = st.selectbox(
            "Calendar Mode:", ("daygrid", "timegrid", "timeline", "list", "multimonth")
        )

    # st.write(selected_events)
    # if selected_events == 'Home':
    #     calendar_events = get_user_events(username)
    #    st.write("1")
    #     st.write(calendar_events)
    # else:
    #    calendar_events = get_team_events(selected_events)
    #   st.write("2")
    #   st.write(calendar_events)

    calendar_resources = []

    calendar_options = {
        "year": "numeric",
        "month": "numeric",
        "day": "numeric",
        "hour": "numeric",
        "minute": "numeric",
        "second": "numeric",
        "hour12": "false",
        "firstDay": 1,
        "editable": "true",
        "navLinks": "true",
        "resources": calendar_resources,
        "selectable": "true",
    }

    if "resource" in mode:
        print("ok")
    else:
        if mode == "daygrid":
            calendar_options = {
                **calendar_options,
                "headerToolbar": {
                    "left": "today prev,next",
                    "center": "title",
                    "right": "dayGridDay,dayGridWeek,dayGridMonth",
                },
                "initialView": "dayGridMonth",
            }
        elif mode == "timegrid":
            calendar_options = {**calendar_options, "initialView": "timeGridWeek"}
        elif mode == "timeline":
            calendar_options = {
                **calendar_options,
                "headerToolbar": {
                    "left": "today prev,next",
                    "center": "title",
                    "right": "timelineDay,timelineWeek,timelineMonth",
                },
                "initialView": "timelineDay",
            }
        elif mode == "list":
            calendar_options = {
                **calendar_options,
                "initialView": "listMonth",
            }
        elif mode == "multimonth":
            calendar_options = {
                **calendar_options,
                "initialView": "multiMonthYear",
            }

    calendar_css = """
            .fc-scrollgrid{
                height:80%
                }
            .fc-event-main{
                margin: 0 0 0 0
                }
            .fc-event-time {
                font family:Gill Sans;
                font-weight: 600;
            }
            .fc-event-title {
                font family:Gill Sans;
                font-weight: 600;
            }
            .fc-toolbar-title {
                font-size: 1.9rem;
            }
            .fc-button-primary{
                font-size: 14px;
            }

           .fc-daygrid-body-natural{
               height:0px
           }
            """

    with calendar_column:
        state = calendar(
            events=selected_events,  # st.session_state.get("events", events),
            options=calendar_options,
            custom_css=calendar_css,
            key=mode,
        )

    with event_column:
        if state.get("eventsSet") is not None:
            st.session_state["events"] = state["eventsSet"]
        if state["callback"] == "eventClick":
            event_pop_up(state)


def event_pop_up(state):
    res = requests.get(
        url="http://127.0.0.1:8000/event/"
        + state["eventClick"]["event"]["extendedProps"]["event_id"]
    ).json()
    teams_attending = ""
    users_attending = ""
    if res["teams"]:
        for team in res["teams"]:
            teams_attending += team["team_name"] + ", "
        teams_attending = teams_attending[:-2]
    if res["attendees"]:
        for user in res["attendees"]:
            users_attending += user["user_name"] + ", "
        users_attending = users_attending[:-2]
    st.divider()
    event_container = st.container()
    st.markdown("""<div id = 'chat_outer'></div>""", unsafe_allow_html=True)
    with event_container:
        st.markdown("""<div id = 'chat_inner'></div>""", unsafe_allow_html=True)
        event_columns = st.columns([0.5, 1, 0.5], gap="small")
        with event_columns[1]:
            st.header(state["eventClick"]["event"]["title"])
    start_date = state["eventClick"]["event"]["start"][0:10]
    end_date = state["eventClick"]["event"]["end"][0:10]

    if start_date == end_date:
        with event_columns[1]:
            st.markdown(start_date)
    else:
        with event_columns[1]:
            st.markdown(
                "From "
                + state["eventClick"]["event"]["start"][0:10].replace("T", " ")
                + " to "
                + state["eventClick"]["event"]["end"][0:10].replace("T", " ")
            )
    st.write("Event starts at: " + state["eventClick"]["event"]["start"][11:16])
    st.write("Event ends at: " + state["eventClick"]["event"]["end"][11:16])
    st.markdown("Teams attending: " + teams_attending)
    st.markdown("People attending: " + users_attending)
    st.write("Created by: " + res["created_by"])

    st.markdown(
        """<style>
    div[data-testid='stVerticalBlock']:has(div#chat_inner):not(:has(div#chat_outer))
    {
        border:7px double """
        + state["eventClick"]["event"]["backgroundColor"]
        + """;
        border-radius:5px;
        };
    </style>""",
        unsafe_allow_html=True,
    )
