/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { GameParametersDTO } from '../models/GameParametersDTO';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class GameParametersService {

    /**
     * Get Parameters
     * @returns GameParametersDTO Successful Response
     * @throws ApiError
     */
    public static getParametersGameParametersGet(): CancelablePromise<GameParametersDTO> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/game-parameters',
        });
    }

}
