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
		if (!gameSession) {
			return;
		}

		if (gameSession?.machine_stats && gameSession.machine_stats.health_percentage <= 0) {
			gameOver = true;
			return;
		}

		try {
			gameSession = await SessionsService.getSessionSessionGet(gameSession?.id);
		} catch (error) {
			console.error('Error fetching session:', error);
		}
	};

	const advanceToNextDay = async () => {
		if (!gameSession || gameOver) {
			return;
		}

		try {
			// start fetching machine health every second while the day is advancing
			const intervalId = setInterval(fetchExistingSession, 700);

			advanceButtonDisabled = true;
			gameSession = await SessionsService.advanceSessionTurnSessionTurnsPut(gameSession?.id);
			advanceButtonDisabled = false;

			// stop fetching machine health until the player advances to next day again
			clearInterval(intervalId);

			// TODO: migrate this polling strategy to a websocket connection
		} catch (error) {
			console.error('Error advancing day:', error);
		}
	};
</script>

<div>
	<h2>The Predictive Maintenance Game</h2>

	{#if !gameSession}
		<button on:click={startSession}>Start Session</button>
	{/if}

	{#if gameSession}
		<img
			src={stopAnimation ? stoppedMachineSrc : runningMachineSrc}
			alt="Machine"
			width="369"
			height="276"
		/>
	{/if}

	{#if gameSession && !gameOver}
		<div>
			<h3>Game Session Details</h3>
			<pre>{JSON.stringify(gameSession, null, 2)}</pre>
		</div>
		<button on:click={advanceToNextDay} disabled={advanceButtonDisabled}>Advance to next day</button
		>
	{/if}

	<!-- TODO show section with available predictions / stats -->

	{#if gameOver}
		<h3>Game Over</h3>
		<pre>{JSON.stringify(gameSession, null, 2)}</pre>
		<p>Machine health has reached 0%.</p>
	{/if}
</div>
