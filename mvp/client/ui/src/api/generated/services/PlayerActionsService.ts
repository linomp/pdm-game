/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { GameSessionDTO } from '../models/GameSessionDTO';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class PlayerActionsService {

    /**
     * Do Maintenance
     * @param sessionId 
     * @returns GameSessionDTO Successful Response
     * @throws ApiError
     */
    public static doMaintenancePlayerActionsMaintenanceInterventionsPost(
sessionId: string,
): CancelablePromise<GameSessionDTO> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/player-actions/maintenance-interventions',
            query: {
                'session_id': sessionId,
            },
            errors: {
                404: `Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Purchase Sensor
     * @param sensor 
     * @param sessionId 
     * @returns GameSessionDTO Successful Response
     * @throws ApiError
     */
    public static purchaseSensorPlayerActionsPurchasesSensorsPost(
sensor: string,
sessionId: string,
): CancelablePromise<GameSessionDTO> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/player-actions/purchases/sensors',
            query: {
                'sensor': sensor,
                'session_id': sessionId,
            },
            errors: {
                404: `Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Purchase Prediction
     * @param prediction 
     * @param sessionId 
     * @returns GameSessionDTO Successful Response
     * @throws ApiError
     */
    public static purchasePredictionPlayerActionsPurchasesPredictionModelsPost(
prediction: string,
sessionId: string,
): CancelablePromise<GameSessionDTO> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/player-actions/purchases/prediction-models',
            query: {
                'prediction': prediction,
                'session_id': sessionId,
            },
            errors: {
                404: `Not found`,
                422: `Validation Error`,
            },
        });
    }

}
