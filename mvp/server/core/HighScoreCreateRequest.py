from pydantic import BaseModel, constr


class HighScoreCreateRequest(BaseModel):
    nickname: constr(strip_whitespace=True, min_length=1, max_length=20)
