import type {UTCTimestamp} from "lightweight-charts";
import type {TimeSeriesPoint} from "./types";
import type {GameSessionDTO} from "src/shared/api";

export const isUndefinedOrNull = (value: any): boolean => {
    return value === undefined || value === null;
}

export const isNotUndefinedNorNull = (value: any): boolean => {
    return !isUndefinedOrNull(value);
}

export const formatNumber = (number: number | undefined | null) => {
    return number?.toFixed(2);
};

export const getUpdatedTimeseries = (newGameSessionDto: GameSessionDTO, previousTimeSeries: {
    [key: string]: TimeSeriesPoint[]
}): { [key: string]: TimeSeriesPoint[] } => {
    const newTimestamp = (Date.now() / 1000) as UTCTimestamp;

    for (const [parameterName, newValue] of Object.entries(newGameSessionDto.machine_state)) {

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

export const formatDatetime = (datetimeStr: string): string => {
    const datetime = new Date(datetimeStr);
    const formattedDate = `${datetime.getDate().toString().padStart(2, '0')}.${(datetime.getMonth() + 1).toString().padStart(2, '0')}.${datetime.getFullYear()}`
    const formattedTime = `${datetime.getHours().toString().padStart(2, '0')}:${datetime.getMinutes().toString().padStart(2, '0')}`;

    return `${formattedDate} @ ${formattedTime}`;
}
