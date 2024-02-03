<script lang="ts">
	import {
		SessionsService,
		type GameSessionDTO,
		OpenAPI,
		PlayerActionsService,
		type GameParameters,
		GameParametersService
	} from '../generated';
	import runningMachineSrc from '$lib/assets/healthy.gif';
	import { onMount } from 'svelte';

	const stoppedMachineSrc = new URL('../lib/assets/stopped.PNG', import.meta.url).href;

	// TODO remove this from here, find out where to put it (fucking sveltekit...)
	OpenAPI.BASE = import.meta.env.VITE_API_BASE;

	let gameSession: GameSessionDTO | null;
	let gameOver = false;
	let gameOverReason: string | null = null;
	let maintenanceButtonDisabled = false;
	let dayInProgress = false;
	let stopAnimation = false;
	let globalSettings: GameParameters;

	$: {
		stopAnimation = gameOver || !dayInProgress;
		maintenanceButtonDisabled =
			(gameSession?.available_funds ?? 0) < (globalSettings?.maintenance_cost ?? Infinity);
	}

	onMount(async () => {
		try {
			globalSettings = await GameParametersService.getParametersGameParametersGet();
		} catch (error) {
			console.error('Error fetching global settings:', error);
		}
	});

	const startSession = async () => {
		try {
			gameSession = await SessionsService.createSessionSessionsPost();
		} catch (error) {
			console.error('Error fetching session:', error);
		}
	};

	const fetchExistingSession = async () => {
		if (!gameSession || gameOver) {
			return;
		}

		try {
			gameSession = await SessionsService.getSessionSessionsGet(gameSession?.id);
			checkForGameOver();
		} catch (error) {
			console.error('Error fetching session:', error);
		}
	};

	const advanceToNextDay = async () => {
		if (!gameSession || gameOver) {
			return;
		}

		// TODO: migrate this polling strategy to a websocket connection
		// start fetching machine health every second while the day is advancing
		const intervalId = setInterval(fetchExistingSession, 500);
		dayInProgress = true;

		try {
			gameSession = await SessionsService.advanceSessionsTurnsPut(gameSession?.id);
		} catch (error) {
			console.error('Error advancing day:', error);
		} finally {
			await fetchExistingSession();
			// stop fetching machine health until the player advances to next day again
			clearInterval(intervalId);
			dayInProgress = false;
		}
	};

	const doMaintenance = async () => {
		if (!gameSession || gameOver) {
			return;
		}

		try {
			gameSession =
				await PlayerActionsService.doMaintenancePlayerActionsMaintenanceInterventionsPost(
					gameSession?.id
				);
			await advanceToNextDay();
		} catch (error: any) {
			if (error.status === 400) {
				alert('Not enough funds to perform maintenance!');
			} else {
				console.error('Error performing maintenance:', error);
			}
		}
	};

	const checkForGameOver = () => {
		if (!gameSession) {
			return;
		}

		gameOver = gameSession.is_game_over ?? false;
		gameOverReason = gameSession.game_over_reason ?? null;
	};
</script>

<div>
	<h2>The Predictive Maintenance Game</h2>

	{#if gameSession}
		<img
			src={stopAnimation ? stoppedMachineSrc : runningMachineSrc}
			alt="Machine"
			width="369"
			height="276"
		/>

		{#if gameOver}
			<h3>Game Over</h3>
			<pre>{JSON.stringify(gameSession, null, 2)}</pre>
			<p>{gameOverReason}</p>
		{:else}
			<div>
				<h3>Game Session Details</h3>
				<pre>{JSON.stringify(gameSession, null, 2)}</pre>
			</div>
			<button on:click={advanceToNextDay} disabled={dayInProgress}> Advance to next day </button>
			<button on:click={doMaintenance} disabled={dayInProgress || maintenanceButtonDisabled}>
				Perform Maintenance (${globalSettings?.maintenance_cost ?? 0})
			</button>
		{/if}
	{:else}
		<button on:click={startSession}>Start Session</button>
	{/if}
</div>
