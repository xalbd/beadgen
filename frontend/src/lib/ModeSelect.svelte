<script lang="ts">
  export let label: string;
  export let binding: string;
  export let values: { [value: string]: string };
</script>

<div class="block">
  <label for="selection" class="pr-2"> {label} </label>
  <select
    name="selection"
    class=" bg-gray-200 border border-gray-200 px-2 rounded focus:outline-none focus:bg-white focus:border-gray-500"
    bind:value={binding}
  >
    {#each Object.entries(values) as [value, name]}
      <option {value}>{name}</option>
    {/each}
  </select>
</div>
