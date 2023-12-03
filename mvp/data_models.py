from typing import Any

from pydantic import BaseModel


class MachineStats(BaseModel):
    rul: int | None = None

    @staticmethod
    def from_json(json: dict[str, Any]):
        return MachineStats(rul=json.get("rul", None))

    def is_broken(self) -> bool:
        # if no rul data is available, assume the machine is not broken
        if self.rul is None:
            return False
        return self.rul <= 0
