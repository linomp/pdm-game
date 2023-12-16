<script lang="ts">
	import { onDestroy } from 'svelte';

	let sessionId: string | undefined;
	// TODO import game session type from generated openapi client
	let gameSession: any = null;
	let validationError: any;
	let intervalId: number | undefined;

	// TODO move this to .env file
	const api = 'http://localhost:8000';

	// TODO replace this with generated openapi client
	const startSession = async () => {
		try {
			const response = await fetch(`${api}/session`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({})
			});
			if (response.ok) {
				const data = await response.json();
				sessionId = data.id;
				validationError = null;
				await fetchSession();
				intervalId = setInterval(fetchSession, 2000);
			} else {
				validationError = await response.json();
			}
		} catch (error) {
			console.error('Error starting session:', error);
		}
	};

	// TODO replace this with generated openapi client
	const fetchSession = async () => {
		if (gameSession && gameSession.machine_stats.health_percentage <= 0) {
			clearInterval(intervalId);
			return;
		}
		try {
			const response = await fetch(`${api}/session?session_id=${sessionId}`);
			if (response.ok) {
				gameSession = await response.json();
				validationError = null;
			} else {
				validationError = await response.json();
				gameSession = null;
			}
		} catch (error) {
			console.error('Error fetching session:', error);
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
