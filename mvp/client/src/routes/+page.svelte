<script lang="ts">
	import { onDestroy } from 'svelte';
	import { SessionsService, type GameSessionDTO } from '../generated';

	let gameSession: GameSessionDTO | null;
	let validationError: any;
	let intervalId: number | undefined;

	const startSession = async () => {
		const response = await SessionsService.startSessionSessionPost();
		if (response?.id) {
			gameSession = response;
			validationError = null;
			intervalId = setInterval(fetchSession, 2000);
		} else {
			validationError = response;
		}
	};

	const fetchSession = async () => {
		if (!gameSession) {
			return;
		}

		if (gameSession?.machine_stats && gameSession.machine_stats.health_percentage <= 0) {
			clearInterval(intervalId);
			return;
		}

		try {
			gameSession = await SessionsService.getSessionSessionGet(gameSession?.id);
		} catch (error) {
			console.error('Error fetching session:', error);
			validationError = error;
		}
	};

	onDestroy(() => {
		if (intervalId) {
			clearInterval(intervalId);
		}
	});
</script>

<div>
	<h2>The Predictive Maintenance Game</h2>

	<button on:click={startSession}>Start Session</button>

	<!-- TODO show healthy machine gif, and stop the animation on machine breakdown -->

	{#if gameSession}
		<div>
			<h3>Game Session Details</h3>
			<pre>{JSON.stringify(gameSession, null, 2)}</pre>
		</div>
	{/if}

	{#if validationError}
		<div>
			<h3>Error Details</h3>
			<pre>{JSON.stringify(validationError, null, 2)}</pre>
		</div>
	{/if}
</div>
