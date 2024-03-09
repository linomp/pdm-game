import type { UTCTimestamp } from "lightweight-charts";
import type { GameSessionWithStateSnapshots, MachineStateSnapshotDict, TimeSeriesPoint } from "./types";

export const isUndefinedOrNull = (value: any): boolean => {
    return value === undefined || value === null;
}

export const isNotUndefinedNorNull = (value: any): boolean => {
    return !isUndefinedOrNull(value);
}

export const formatNumber = (number: number | undefined | null) => {
    return number?.toFixed(2);
};


export const getFormattedTimeseriesForParameters = (parameters: string[], machineStateSnapshots: MachineStateSnapshotDict | null | undefined): { [key: string]: TimeSeriesPoint[] } => {
    if (isUndefinedOrNull(machineStateSnapshots)) {
        return {};
    }

    const formattedTimeseries: { [key: string]: TimeSeriesPoint[] } = {};

    parameters.forEach(parameter => {
        formattedTimeseries[parameter] = [];
    });

    for (let step in machineStateSnapshots) {
        const snapshot = machineStateSnapshots[step];
        parameters.forEach(parameter => {
            const value = snapshot.operational_parameters[parameter];
            if (value !== null && value !== undefined) {
                formattedTimeseries[parameter].push({
                    time: (Number(step) + (new Date()).getTime() / 1000) as UTCTimestamp,
                    value: value
                });
            }
        });
    }

    return formattedTimeseries;
};
