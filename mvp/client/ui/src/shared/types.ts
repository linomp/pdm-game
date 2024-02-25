import type { GameSessionDTO, MachineStateDTO } from "src/api/generated";

export type MachineStateSnapshotDict = { [key: number]: MachineStateDTO }

export interface GameSessionWithStateSnapshots extends GameSessionDTO {
    machineStateSnapshots: MachineStateSnapshotDict
}