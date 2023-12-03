# create streamlit app with a button to do a request to the api
import base64
from typing import Any

import requests
import streamlit as st

from mvp.constants import MACHINE_STATS_ENDPOINT
from mvp.data_models import MachineStats

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
button = st.button("Check Remaining Useful Life (RUL)")
gif = show_gif("media/healthy.gif")

if button:
    machine = MachineStats.from_json(
        requests.get(f"{api_base}{MACHINE_STATS_ENDPOINT}").json())
    if machine.is_broken():
        gif.empty()
        st.warning("The machine broke down")
    else:
        st.success(f"The machine will break down in {machine.rul} cycles")
