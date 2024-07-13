<script lang="ts">
  export let messages: Record<string, { type: string; content: string }>;
</script>

<div class="user-messages">
  {#each Object.entries(messages) as [key, message]}
    <div class="message-card {message.type}">
      <span>{message.content}</span>
    </div>
  {/each}
</div>

<style>
  .user-messages {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    align-items: center;
    width: 80%;
  }

  .message-card {
    border-radius: 8px;
    padding: 1em;
    width: 100%;
    text-align: center;
    border: 1px solid #ccc;
    transition: opacity 0.3s;
    font-size: smaller;
  }

  .message-card.WARNING {
    background-color: #ffffe0;
    color: #000000;
  }

  .message-card.INFO {
    background-color: rgba(129, 248, 94, 0.86);
    color: #000000;
  }
</style>
