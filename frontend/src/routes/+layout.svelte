<script>
  import "../app.css";
</script>

<nav>
  <a href="/">standard</a>
  <a href="/double">double-sided</a>
  <a href="/spherical">spheres</a>
  <a href="/structures">structures</a>
</nav>
<slot />

<style>
  a {
    @apply m-2;
  }
</style>
