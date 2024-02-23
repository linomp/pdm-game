import { writable } from 'svelte/store';
import type { GameParametersDTO, GameSessionDTO } from 'src/api/generated';

export const globalSettings = writable<GameParametersDTO | null>(null);
export const gameSession = writable<GameSessionDTO | null>(null);
export const gameOver = writable(false);
export const gameOverReason = writable<string | null>(null);
export const maintenanceButtonDisabled = writable(false);
export const sensorPurchaseButtonDisabled = writable(false);
export const predictionPurchaseButtonDisabled = writable(false);
export const dayInProgress = writable(false);
export const performedMaintenanceInThisTurn = writable(false);