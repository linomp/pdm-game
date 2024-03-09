import type { MachineStateSnapshotDict } from "./types";
import { getFormattedTimeseriesForParameters } from "./utils";

describe('getFormattedTimeseriesForParameters', () => {
    it('should return an empty object if machineStateSnapshots is null or undefined', () => {
        const parameters = ['temperature', 'oil_age', 'mechanical_wear'];
        const machineStateSnapshots: MachineStateSnapshotDict | null | undefined = null;

        const result = getFormattedTimeseriesForParameters(parameters, machineStateSnapshots);

        expect(result).toEqual({});
    });

    it('should return formatted timeseries', () => {
        const parameters = ['temperature', 'oil_age', 'mechanical_wear'];
        const machineStateSnapshots: MachineStateSnapshotDict = {
            1: {
                operational_parameters: {
                    temperature: 20,
                    oil_age: 1,
                    mechanical_wear: 0.5
                },
                predicted_rul: null
            },
            2: {
                operational_parameters: {
                    temperature: 22,
                    oil_age: 1.5,
                    mechanical_wear: 0.6
                },
                predicted_rul: null
            }
        };

        const result = getFormattedTimeseriesForParameters(parameters, machineStateSnapshots);

        // Check if the result contains the expected keys
        expect(Object.keys(result)).toEqual(parameters);

        // Check if each parameter has the expected number of time series points
        parameters.forEach(parameter => {
            expect(result[parameter].length).toEqual(Object.keys(machineStateSnapshots).length);
        });

        // Check if each time series point has the expected structure
        parameters.forEach(parameter => {
            result[parameter].forEach(point => {
                expect(point).toHaveProperty('time');
                expect(point).toHaveProperty('value');
            });
        });
    });
});
