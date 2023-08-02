<script>
  import BeadPreview from "./BeadPreview.svelte";
  import PathPreview from "./PathPreview.svelte";
  import TipPreview from "./TipPreview.svelte";
</script>

<svelte:head>
  <title>Bead Generation</title>
  <meta name="description" content="Automatic Wire-Jamming Bead Generation" />
</svelte:head>

<section class="flex flex-row">
  <TipPreview />
  <BeadPreview />
</section>

<style>
</style>
