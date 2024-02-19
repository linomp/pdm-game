<script lang="ts">
  export let parameter: string;
  export let value: number | null;
  export let sensorPurchaseButtonDisabled: boolean;
  export let purchaseSensor: (parameter: string) => void;
  export let sensorCost: number;

  const formatParameterName = (parameter: string) => {
    return parameter
      .split("_")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };
</script>

<p>
  {formatParameterName(parameter)}: {value ?? "???"}
  <span hidden={value != null}>
    <button
      disabled={sensorPurchaseButtonDisabled}
      on:click={() => purchaseSensor(parameter)}
    >
      Buy (${sensorCost})
    </button>
  </span>
</p>
