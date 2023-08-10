<script>
  import BeadPreview from "./BeadPreview.svelte";
  import TipPreview from "./TipPreview.svelte";
</script>

<svelte:head>
  <title>Bead Generation</title>
  <meta name="description" content="Automatic Wire-Jamming Bead Generation" />
</svelte:head>

<section
  class="flex flex-row min-w-screen flex-1 divide-x divide-dashed divide-slate-500"
>
  <TipPreview />
  <BeadPreview />
</section>

<style>
</style>
