import type {GameSessionDTO} from 'src/shared/api';
import type {TimeSeriesPoint} from './types';
import {getUpdatedTimeseries} from './utils';
import type {UTCTimestamp} from 'lightweight-charts';

const previousTimeSeries: { [key: string]: TimeSeriesPoint[] } = {
    temperature: [
        {time: 1 as UTCTimestamp, value: 20},
        {time: 2 as UTCTimestamp, value: 30}
    ],
    oil_age: [
        {time: 1 as UTCTimestamp, value: 2.5},
        {time: 2 as UTCTimestamp, value: 3.0}
    ],
    mechanical_wear: []
};

const newGameSessionDTO: GameSessionDTO = {
    id: "1",
    current_step: 1,
    machine_state: {
        operational_parameters: {
            temperature: 40,
            oil_age: 3.5,
            mechanical_wear: null
        },
        predicted_rul: null
    },
    available_funds: 1000,
    is_game_over: false
};

describe('getUpdatedTimeseries', () => {
    it('updates the time series correctly', () => {
        const updatedTimeseries = getUpdatedTimeseries(newGameSessionDTO, previousTimeSeries);

        expect(updatedTimeseries.temperature).toEqual([
            {time: expect.any(Number), value: 20},
            {time: expect.any(Number), value: 30},
            {time: expect.any(Number), value: 40}
        ]);

        expect(updatedTimeseries.oil_age).toEqual([
            {time: expect.any(Number), value: 2.5},
            {time: expect.any(Number), value: 3.0},
            {time: expect.any(Number), value: 3.5}
        ]);

        expect(updatedTimeseries.mechanical_wear).toEqual([]);
    });

    it('does not update the time series when values are undefined or null', () => {
        const updatedTimeseries = getUpdatedTimeseries({
            ...newGameSessionDTO, machine_state: {
                operational_parameters: {
                    temperature: null,
                    oil_age: null,
                    mechanical_wear: null
                },
                predicted_rul: null
            }
        }, previousTimeSeries);

        expect(updatedTimeseries.temperature).toEqual(previousTimeSeries.temperature);
        expect(updatedTimeseries.oil_age).toEqual(previousTimeSeries.oil_age);
        expect(updatedTimeseries.mechanical_wear).toEqual(previousTimeSeries.mechanical_wear);
    });
});
