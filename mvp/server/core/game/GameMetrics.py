from pydantic import BaseModel


class GameMetrics(BaseModel):
    active_sessions: int
    total_started_games: int
    total_ended_games: int
    total_abandoned_games: int
    total_seconds_played: float
    avg_game_duration: float
    min_game_duration: float = 0
    max_game_duration: float = 0

    def __init__(self):
        super().__init__(
            active_sessions=0,
            total_started_games=0,
            total_ended_games=0,
            total_abandoned_games=0,
            total_seconds_played=0,
            avg_game_duration=0,
            min_game_duration=0,
            max_game_duration=0
        )

    def update_on_game_started(self, new_active_sessions_count: int) -> None:
        self.total_started_games += 1
        self.active_sessions = new_active_sessions_count

    def update_on_game_ended(self, game_duration: float) -> None:
        self.total_ended_games += 1
        self.active_sessions -= 1

        self.total_seconds_played = self.total_seconds_played + game_duration

        if self.total_ended_games == 0:
            self.avg_game_duration = game_duration
        else:
            self.avg_game_duration = self.total_seconds_played / self.total_ended_games

        if self.min_game_duration == 0 or game_duration < self.min_game_duration:
            self.min_game_duration = game_duration

        if self.max_game_duration == 0 or game_duration > self.max_game_duration:
            self.max_game_duration = game_duration

    def update_on_game_abandoned(self, new_active_sessions_count: int) -> None:
        self.total_abandoned_games += 1
        self.active_sessions = new_active_sessions_count
