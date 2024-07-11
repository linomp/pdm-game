/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type UserMessage = {
    type: UserMessage.type;
    content: string;
    seen?: boolean;
};

export namespace UserMessage {

    export enum type {
        WARNING = 'WARNING',
        INFO = 'INFO',
    }


}
