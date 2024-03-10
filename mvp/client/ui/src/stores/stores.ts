import { writable } from 'svelte/store';
import type { GameParametersDTO } from 'src/api/generated';
import type { GameSessionWithTimeSeries } from 'src/shared/types';

export const globalSettings = writable<GameParametersDTO>();
export const gameSession = writable<GameSessionWithTimeSeries | null>(null);
export const gameOver = writable(false);
export const gameOverReason = writable<string | null>(null);
export const maintenanceButtonDisabled = writable(false);
export const sensorPurchaseButtonDisabled = writable(false);
export const predictionPurchaseButtonDisabled = writable(false);
export const dayInProgress = writable(false);
export const performedMaintenanceInThisTurn = writable(false);