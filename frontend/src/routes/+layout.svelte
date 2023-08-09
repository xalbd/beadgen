<script>
  import "../app.css";
</script>

<div class="divide-y divide-solid divide-stone-600">
  <div class="flex flex-row items-center justify-between">
    <p class="text-xl font-semibold pl-2">Bead Generation</p>
    <nav class="py-1 px-2 font-sans">
      <a href="/" id="" class="hover:text-blue-800 px-2">Standard</a>
      <a href="/double" class="hover:text-blue-800 px-2">Complex</a>
      <a href="/spherical" class="hover:text-blue-800 px-2">Spheres</a>
      <a href="/structures" class="hover:text-blue-800 px-2">Structures</a>
    </nav>
  </div>

  <slot />
</div>

<style>
</style>
