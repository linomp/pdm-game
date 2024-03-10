from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from mvp.server.core.game.GameSession import GameSession
from mvp.server.core.game.GameSessionDTO import GameSessionDTO
from mvp.server.routers.sessions import get_session_dependency

router = APIRouter(
    prefix="/player-actions",
    tags=["Player actions"],
    responses={404: {"description": "Not found"}},
)


@router.post("/maintenance-interventions", response_model=GameSessionDTO)
async def do_maintenance(session: GameSession = Depends(get_session_dependency)) -> GameSessionDTO | JSONResponse:
    success = session.do_maintenance()

    if not success:
        return JSONResponse(status_code=400, content={"message": "Not enough funds to do maintenance"})

    return GameSessionDTO.from_session(session)


@router.post("/purchases/sensors", response_model=GameSessionDTO)
async def purchase_sensor(sensor: str,
                          session: GameSession = Depends(get_session_dependency)) -> GameSessionDTO | JSONResponse:
    if sensor not in session.available_sensors:
        return JSONResponse(status_code=404, content={"message": "Unknown sensor"})
    elif session.available_sensors[sensor]:
        return JSONResponse(status_code=204, content={"message": "Sensor already purchased"})

    success = session.purchase_sensor(sensor)
    if not success:
        return JSONResponse(status_code=400, content={"message": "Not enough funds to purchase sensor"})

    return GameSessionDTO.from_session(session)


@router.post("/purchases/prediction-models", response_model=GameSessionDTO)
async def purchase_prediction(prediction: str,
                              session: GameSession = Depends(get_session_dependency)) -> GameSessionDTO | JSONResponse:
    if prediction not in session.available_predictions:
        return JSONResponse(status_code=404, content={"message": "Unknown prediction model"})
    elif session.available_predictions[prediction]:
        return JSONResponse(status_code=400, content={"message": "Prediction model already purchased"})

    success = session.purchase_prediction(prediction)

    if not success:
        return JSONResponse(status_code=400, content={"message": "Not enough funds to purchase prediction model"})

    return GameSessionDTO.from_session(session)
