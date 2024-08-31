import type {SeriesDataItemTypeMap} from "lightweight-charts";
import type {GameSessionDTO, MachineDTO} from "src/shared/api";

export type MachineStateSnapshotDict = { [key: number]: MachineDTO }

export interface GameSessionWithTimeSeries extends GameSessionDTO {
    formattedTimeSeries: { [key: string]: TimeSeriesPoint[] }
}

export type TimeSeriesPoint = SeriesDataItemTypeMap["Line"]
