import type { SeriesDataItemTypeMap } from "lightweight-charts";
import type { GameSessionDTO, MachineStateDTO } from "src/api/generated";

export const SAMPLE_INTERVAL_MS = 100;

export type MachineStateSnapshotDict = { [key: number]: MachineStateDTO }

export interface GameSessionWithTimeSeries extends GameSessionDTO {
    formattedTimeSeries: { [key: string]: TimeSeriesPoint[] }
}

export type TimeSeriesPoint = SeriesDataItemTypeMap["Line"]
