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


// export const getUpdatedTimeseries = (newGameSessionDto: GameSessionDTO, previousTimeSeries: { [key: string]: TimeSeriesPoint[] }): { [key: string]: TimeSeriesPoint[] } => {
//     const operationalParametersKeys = Object.keys(
//         newGameSessionDto.machine_state.operational_parameters,
//     );

//     for (const key of operationalParametersKeys) {
//         const newTimestamp = new Date().getTime() as UTCTimestamp;
//         const newValue =
//             newGameSessionDto.machine_state.operational_parameters[key];

//         if (isUndefinedOrNull(previousTimeSeries[key])) {
//             previousTimeSeries[key] = [];
//             continue;
//         }

//         if (
//             (previousTimeSeries[key].length > 0 &&
//                 previousTimeSeries[key][previousTimeSeries[key].length - 1].time ===
//                 newTimestamp) ||
//             isUndefinedOrNull(newValue)
//         ) {
//             continue;
//         }

//         previousTimeSeries[key].push({
//             time: newTimestamp,
//             value: newValue,
//         });
//     }

//     return previousTimeSeries;
// }

export const getUpdatedTimeseries = (newGameSessionDto: GameSessionDTO, previousTimeSeries: { [key: string]: TimeSeriesPoint[] }): { [key: string]: TimeSeriesPoint[] } => {
    const machineState = newGameSessionDto.machine_state;
    const operationalParameters = machineState.operational_parameters;

    // Iterate over the keys of operational parameters directly
    for (const key in operationalParameters) {
        if (Object.prototype.hasOwnProperty.call(operationalParameters, key)) {
            const newValue = operationalParameters[key];
            const newTimestamp = new Date().getTime() as UTCTimestamp;

            // Skip if newValue is undefined or null
            if (isUndefinedOrNull(newValue)) {
                continue;
            }

            // Initialize the time series array if it's not present
            if (!previousTimeSeries[key]) {
                previousTimeSeries[key] = [];
            }

            const previousSeries = previousTimeSeries[key];
            const lastItem = previousSeries[previousSeries.length - 1];

            // Check if the last item's time matches the current time
            if (lastItem && lastItem.time === newTimestamp) {
                continue;
            }

            // Push the new value to the time series
            previousSeries.push({
                time: newTimestamp,
                value: newValue
            });
        }
    }

    return previousTimeSeries;
}
