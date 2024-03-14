import type { UTCTimestamp } from "lightweight-charts";
import type { GameSessionWithTimeSeries, MachineStateSnapshotDict, TimeSeriesPoint } from "./types";
import type { GameSessionDTO } from "src/api/generated";

export const isUndefinedOrNull = (value: any): boolean => {
    return value === undefined || value === null;
}

export const isNotUndefinedNorNull = (value: any): boolean => {
    return !isUndefinedOrNull(value);
}

export const formatNumber = (number: number | undefined | null) => {
    return number?.toFixed(2);
};


export const getUpdatedTimeseries = (newGameSessionDto: GameSessionDTO, previousTimeSeries: { [key: string]: TimeSeriesPoint[] }): { [key: string]: TimeSeriesPoint[] } => {
    const newTimestamp = (Date.now() / 1000) as UTCTimestamp;

    for (const [parameterName, newValue] of Object.entries(newGameSessionDto.machine_state.operational_parameters)) {

        if (isUndefinedOrNull(previousTimeSeries[parameterName])) {
            previousTimeSeries[parameterName] = [];
            continue;
        }

        if (
            isUndefinedOrNull(newValue)
            ||
            (
                previousTimeSeries[parameterName].length > 0 &&
                previousTimeSeries[parameterName][previousTimeSeries[parameterName].length - 1].time === newTimestamp
            )
        ) {
            continue;
        }

        previousTimeSeries[parameterName].push({
            time: newTimestamp,
            value: newValue!,
        });
    }

    return previousTimeSeries;
}
