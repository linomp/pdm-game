import base64
import time
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

start_time = 0

if button:
    start_time = time.time()
    machine = MachineStats.from_json(
        requests.get(f"{api_base}{MACHINE_STATS_ENDPOINT}").json())
    if machine.is_broken():
        gif.empty()
        elapsed_time = time.time() - start_time
        st.warning(f"The machine broke down after lasting {elapsed_time:.2f} seconds")
    else:
        st.success(f"The machine will break down in {machine.rul} cycles")
