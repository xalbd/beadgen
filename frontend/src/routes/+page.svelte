<script>
  import PreviewStl from "./PreviewSTL.svelte";
  import Square from "./Square.svelte";
</script>

<svelte:head>
  <title>Bead Generation</title>
  <meta name="description" content="Automatic Wire-Jamming Bead Generation" />
</svelte:head>

<section class="flex flex-row flex-nowrap">
  <Square />
  <PreviewStl />
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
