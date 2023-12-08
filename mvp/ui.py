import base64
import sys
import time
from typing import Any

import requests
import streamlit as st

from mvp.constants import DEFAULT_SESSION_ID
from mvp.data_models import GameSessionDTO

api_base = "https://api.pdmgame.xmp.systems"

if '--dev' in sys.argv:
    api_base = "http://localhost:8000"


def show_gif(path) -> Any:
    file_ = open(path, "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    return st.markdown(
        f'<img src="data:image/gif;base64,{data_url}">',
        unsafe_allow_html=True,
    )


st.title("The Predictive Maintenance Game")

with st.container(border=False):
    gif = show_gif("media/healthy.gif")

previous_placeholder = None

while True:
    placeholder = st.empty()
    with placeholder.container(border=True):
        response = requests.get(f"{api_base}/session?session_id={DEFAULT_SESSION_ID}").json()
        session = GameSessionDTO.from_json(response)

        if previous_placeholder is not None:
            previous_placeholder.empty()

        st.info(f"Current step: {session.current_step}")
        st.info(f"Session id: {session.id}")

        if session.machine_stats.is_broken():
            gif.empty()
            st.warning(f"The machine health is {session.machine_stats.health_percentage:.2f}")
            st.warning(f"The machine broke after {session.current_step} cycles")
            break
        else:
            st.info(f"The machine health is {session.machine_stats.health_percentage:.2f}")
            if session.machine_stats.rul is None:
                st.warning("RUL prediction is not available")
            else:
                st.info(f"It will break down in {session.machine_stats.rul} cycles")

        time.sleep(1)
        previous_placeholder = placeholder
