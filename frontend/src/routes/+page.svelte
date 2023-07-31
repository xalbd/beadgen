<script>
  import TipPreview from "./TipPreview.svelte";
</script>

<svelte:head>
  <title>Bead Generation</title>
  <meta name="description" content="Automatic Wire-Jamming Bead Generation" />
</svelte:head>

<section class="flex flex-col">
  <TipPreview />
</section>

<style>
  section {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    flex: 0.6;
  }
</style>
