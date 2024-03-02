import type { GameSessionWithStateSnapshots, TimeSeriesPoint } from "./types";

export const isUndefinedOrNull = (value: any): boolean => {
    return value === undefined || value === null;
}

export const isNotUndefinedNorNull = (value: any): boolean => {
    return !isUndefinedOrNull(value);
}

export const formatNumber = (number: number | undefined | null) => {
    return number?.toFixed(2);
};

// TODO add test
export const getFormattedTimeseriesForParameters = (parameters: string[], gameSession: GameSessionWithStateSnapshots): { [key: string]: TimeSeriesPoint[] } => {
    const formattedTimeseries: { [key: string]: TimeSeriesPoint[] } = {};

    parameters.forEach(parameter => {
        formattedTimeseries[parameter] = [];
    });

    for (let step in gameSession.machineStateSnapshots) {
        const snapshot = gameSession.machineStateSnapshots[step];
        parameters.forEach(parameter => {
            const value = snapshot.operational_parameters[parameter];
            if (value !== null && value !== undefined) {
                formattedTimeseries[parameter].push({
                    time: `${2000 + parseInt(step)}-01-11`,
                    value: value
                });
            }
        });
    }

    return formattedTimeseries;
};