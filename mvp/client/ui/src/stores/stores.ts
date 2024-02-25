import { writable } from 'svelte/store';
import type { GameParametersDTO, GameSessionDTO, MachineStateDTO } from 'src/api/generated';
import type { MachineStateSnapshotDict } from 'src/shared/types';

export const globalSettings = writable<GameParametersDTO | null>(null);
export const gameSession = writable<GameSessionDTO | null>(null);
export const machineStateSnapshots = writable<MachineStateSnapshotDict>({});
export const gameOver = writable(false);
export const gameOverReason = writable<string | null>(null);
export const maintenanceButtonDisabled = writable(false);
export const sensorPurchaseButtonDisabled = writable(false);
export const predictionPurchaseButtonDisabled = writable(false);
export const dayInProgress = writable(false);
export const performedMaintenanceInThisTurn = writable(false);