from pydantic import BaseModel, constr


class ScoreCreateRequest(BaseModel):
    nickname: constr(strip_whitespace=True, min_length=1, max_length=10)
