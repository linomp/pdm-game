/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { MachineState } from './MachineState';

export type GameSessionDTO = {
    id: string;
    current_step: number;
    machine_state?: (MachineState | null);
    available_funds?: number;
    is_game_over?: boolean;
    game_over_reason?: (string | null);
};
