from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from mvp.analysis import get_rul_prediction
from mvp.constants import MACHINE_STATS_ENDPOINT
from mvp.data_models import MachineStats

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get(MACHINE_STATS_ENDPOINT, tags=["Machine stats"], response_model=MachineStats)
async def get_machine_stats() -> MachineStats:
    return MachineStats(rul=get_rul_prediction())
