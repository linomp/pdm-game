<script lang="ts">
	import {
		SessionsService,
		type GameSessionDTO,
		OpenAPI,
		MachineInterventionsService
	} from '../generated';
	import runningMachineSrc from '$lib/assets/healthy.gif';

	const stoppedMachineSrc = new URL('../lib/assets/stopped.PNG', import.meta.url).href;

	let gameSession: GameSessionDTO | null;
	let gameOver = false;
	let gameOverReason: string | null = null;
	let advanceButtonDisabled = false;
	let maintenanceButtonDisabled = false;

	// TODO: add logic to disable maintenance button when player can't afford it
	// TODO: show cost of maintenance in the button

	let stopAnimation = false;

	$: {
		stopAnimation = gameOver || !advanceButtonDisabled;
	}

	// TODO remove this from here, find out where to put it (fucking sveltekit...)
	OpenAPI.BASE = import.meta.env.VITE_API_BASE;

	const startSession = async () => {
		try {
			gameSession = await SessionsService.createSessionSessionPost();
		} catch (error) {
			console.error('Error fetching session:', error);
		}
	};

	const fetchExistingSession = async () => {
		if (!gameSession || gameOver) {
			return;
		}

		try {
			gameSession = await SessionsService.getSessionSessionGet(gameSession?.id);
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
		advanceButtonDisabled = true;
		maintenanceButtonDisabled = true;

		try {
			gameSession = await SessionsService.advanceSessionTurnsPut(gameSession?.id);
		} catch (error) {
			console.error('Error advancing day:', error);
		} finally {
			await fetchExistingSession();
			// stop fetching machine health until the player advances to next day again
			clearInterval(intervalId);
			advanceButtonDisabled = false;
			maintenanceButtonDisabled = false;
		}
	};

	const doMaintenance = async () => {
		if (!gameSession || gameOver) {
			return;
		}

		try {
			maintenanceButtonDisabled = true;
			gameSession =
				await MachineInterventionsService.doMaintenanceSessionMachineInterventionsMaintenancePost(
					gameSession?.id
				);
		} catch (error) {
			console.error('Error performing maintenance:', error);
			maintenanceButtonDisabled = false;
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
			<button on:click={advanceToNextDay} disabled={advanceButtonDisabled}
				>Advance to next day</button
			>
			<button on:click={doMaintenance} disabled={maintenanceButtonDisabled}
				>Perform Maintenance</button
			>
		{/if}
	{:else}
		<button on:click={startSession}>Start Session</button>
	{/if}
</div>
