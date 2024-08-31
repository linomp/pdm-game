/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { MachineDTO } from './MachineDTO';
import type { UserMessage } from './UserMessage';

export type GameSessionDTO = {
    id: string;
    current_step: number;
    machine_state: MachineDTO;
    available_funds: number;
    is_game_over: boolean;
    game_over_reason?: (string | null);
    final_score?: (number | null);
    user_messages?: Record<string, UserMessage>;
    cash_multiplier?: number;
};
