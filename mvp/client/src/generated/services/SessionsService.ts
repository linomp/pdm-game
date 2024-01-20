/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { GameSessionDTO } from '../models/GameSessionDTO';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class SessionsService {

    /**
     * Create Session
     * @returns GameSessionDTO Successful Response
     * @throws ApiError
     */
    public static createSessionSessionPost(): CancelablePromise<GameSessionDTO> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/session',
        });
    }

    /**
     * Get Session
     * @param sessionId 
     * @returns GameSessionDTO Successful Response
     * @throws ApiError
     */
    public static getSessionSessionGet(
sessionId: string,
): CancelablePromise<GameSessionDTO> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/session',
            query: {
                'session_id': sessionId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Advance
     * @param sessionId 
     * @returns GameSessionDTO Successful Response
     * @throws ApiError
     */
    public static advanceSessionTurnsPut(
sessionId: string,
): CancelablePromise<GameSessionDTO> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/session/turns',
            query: {
                'session_id': sessionId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
