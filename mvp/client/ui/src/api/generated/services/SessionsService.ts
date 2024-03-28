/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { GameMetrics } from '../models/GameMetrics';
import type { GameSessionDTO } from '../models/GameSessionDTO';
import type { MqttFrontendConnectionDetails } from '../models/MqttFrontendConnectionDetails';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class SessionsService {

    /**
     * Get Mqtt Connection Details
     * @param sessionId 
     * @returns MqttFrontendConnectionDetails Successful Response
     * @throws ApiError
     */
    public static getMqttConnectionDetailsSessionsMqttConnectionDetailsGet(
sessionId: string,
): CancelablePromise<MqttFrontendConnectionDetails> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sessions/mqtt-connection-details',
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
     * Create Session
     * @returns GameSessionDTO Successful Response
     * @throws ApiError
     */
    public static createSessionSessionsPost(): CancelablePromise<GameSessionDTO> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/sessions/',
            errors: {
                404: `Not found`,
            },
        });
    }

    /**
     * Get Session
     * @param sessionId 
     * @returns GameSessionDTO Successful Response
     * @throws ApiError
     */
    public static getSessionSessionsGet(
sessionId: string,
): CancelablePromise<GameSessionDTO> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sessions/',
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
     * Get Metrics
     * @returns GameMetrics Successful Response
     * @throws ApiError
     */
    public static getMetricsSessionsMetricsGet(): CancelablePromise<GameMetrics> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sessions/metrics',
            errors: {
                404: `Not found`,
            },
        });
    }

    /**
     * Advance
     * @param sessionId 
     * @returns GameSessionDTO Successful Response
     * @throws ApiError
     */
    public static advanceSessionsTurnsPut(
sessionId: string,
): CancelablePromise<GameSessionDTO> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/sessions/turns',
            query: {
                'session_id': sessionId,
            },
            errors: {
                404: `Not found`,
                422: `Validation Error`,
            },
        });
    }

}
