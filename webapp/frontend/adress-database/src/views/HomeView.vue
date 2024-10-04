<script setup lang="ts">
  import { useSourceCoordinator } from '@/composables/SourceCoordinator';
  import SourceSelector from "@/components/SourceSelector.vue"
</script>

<template>
  <main>
    <div class="text-red-500">Hello World</div>
    <SourceSelector></SourceSelector>
  </main>
</template>
