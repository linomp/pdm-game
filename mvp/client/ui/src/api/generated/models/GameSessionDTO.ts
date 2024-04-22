/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { MachineStateDTO } from './MachineStateDTO';

export type GameSessionDTO = {
    id: string;
    current_step: number;
    machine_state: MachineStateDTO;
    available_funds: number;
    is_game_over: boolean;
    game_over_reason?: (string | null);
    final_score?: (number | null);
};
