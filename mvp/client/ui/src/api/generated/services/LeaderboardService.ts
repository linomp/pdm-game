/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { HighScoreDTO } from '../models/HighScoreDTO';
import type { ScoreCreateRequest } from '../models/ScoreCreateRequest';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class LeaderboardService {

    /**
     * Get Leaderboard
     * @returns HighScoreDTO Successful Response
     * @throws ApiError
     */
    public static getLeaderboardLeaderboardGet(): CancelablePromise<Array<HighScoreDTO>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/leaderboard/',
            errors: {
                404: `Not found`,
            },
        });
    }

    /**
     * Post Score
     * @param sessionId 
     * @param requestBody 
     * @returns any Successful Response
     * @throws ApiError
     */
    public static postScoreLeaderboardScorePost(
sessionId: string,
requestBody: ScoreCreateRequest,
): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/leaderboard/score',
            query: {
                'session_id': sessionId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                404: `Not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Test Leaderboard Post
     * @returns any Successful Response
     * @throws ApiError
     */
    public static testLeaderboardPostLeaderboardTestPost(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/leaderboard/test',
            errors: {
                404: `Not found`,
            },
        });
    }

    /**
     * Test Leaderboard Delete
     * @returns any Successful Response
     * @throws ApiError
     */
    public static testLeaderboardDeleteLeaderboardTestDelete(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/leaderboard/test',
            errors: {
                404: `Not found`,
            },
        });
    }

}
