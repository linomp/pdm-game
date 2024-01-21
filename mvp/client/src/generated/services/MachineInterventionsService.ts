/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { GameSessionDTO } from '../models/GameSessionDTO';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class MachineInterventionsService {

    /**
     * Do Maintenance
     * @param sessionId 
     * @returns GameSessionDTO Successful Response
     * @throws ApiError
     */
    public static doMaintenanceSessionMachineInterventionsMaintenancePost(
sessionId: string,
): CancelablePromise<GameSessionDTO> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/session/machine/interventions/maintenance',
            query: {
                'session_id': sessionId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
