<script lang="ts">
	import { SessionsService, type GameSessionDTO, OpenAPI } from '../generated';
	import runningMachineSrc from '$lib/assets/healthy.gif';

	const stoppedMachineSrc = new URL('../lib/assets/stopped.PNG', import.meta.url).href;

	let gameSession: GameSessionDTO | null;
	let gameOver = false;
	let advanceButtonDisabled = false;

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

		try {
			gameSession = await SessionsService.advanceSessionTurnsPut(gameSession?.id);
		} catch (error) {
			console.error('Error advancing day:', error);
		} finally {
			await fetchExistingSession();
			// stop fetching machine health until the player advances to next day again
			clearInterval(intervalId);
			advanceButtonDisabled = false;
		}
	};

	const checkForGameOver = () => {
		if (!gameSession) {
			return;
		}

		if (gameSession?.machine_stats && gameSession.machine_stats.health_percentage <= 0) {
			gameOver = true;
		}
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
			<p>Machine health has reached 0%.</p>
		{:else}
			<div>
				<h3>Game Session Details</h3>
				<pre>{JSON.stringify(gameSession, null, 2)}</pre>
			</div>
			<button on:click={advanceToNextDay} disabled={advanceButtonDisabled}
				>Advance to next day</button
			>
		{/if}
	{:else}
		<button on:click={startSession}>Start Session</button>
	{/if}
</div>
