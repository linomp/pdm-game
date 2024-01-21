/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { MachineState } from './MachineState';

export type GameSessionDTO = {
    id: string;
    current_step: number;
    machine_state?: (MachineState | null);
};
