<script lang="ts">
  export let current_angle_input: number;
  export let angles: number[];
</script>

<label for="angle-input"> Angle Editor </label>
<div class="flex flex-row space-x-1">
  <input
    name="angle-input"
    class="flex-1 h-10 min-w-0 appearance-none bg-gray-200 border border-gray-200 rounded-lg py-3 px-4 focus:outline-none focus:bg-white"
    type="number"
    bind:value={current_angle_input}
  />
  <button
    class="h-10 rounded-lg w-1/4 bg-green-400 hover:bg-green-500 active:bg-green-600 flex flex-row items-center justify-center"
    on:click={() => {
      if (!angles.includes(current_angle_input)) {
        angles.push(current_angle_input);
        angles = angles;
      }
    }}
  >
    <svg
      class="fill-current w-4 h-4 mr-1"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      ><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
    </svg>Add</button
  >
  <button
    class="h-10 rounded-lg w-1/4 bg-red-300 hover:bg-red-400 active:bg-red-500 flex flex-row items-center justify-center"
    on:click={() => {
      angles = [0];
    }}
  >
    <svg
      class="fill-current w-4 h-4 mr-1"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      ><path
        d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
      />
    </svg>Reset
  </button>
</div>
<p>
  Current Angles: {angles}
</p>
