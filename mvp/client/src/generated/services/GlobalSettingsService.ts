/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { GlobalSettings } from '../models/GlobalSettings';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class GlobalSettingsService {

    /**
     * Get Settings
     * @returns GlobalSettings Successful Response
     * @throws ApiError
     */
    public static getSettingsGlobalSettingsGet(): CancelablePromise<GlobalSettings> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/global-settings',
        });
    }

}
