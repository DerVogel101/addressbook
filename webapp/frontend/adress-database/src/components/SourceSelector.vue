<script setup lang="ts">
   import { useSourceCoordinator } from '@/composables/SourceCoordinator';
</script>

<template>
   <div>
        <button @click="useSourceCoordinator().setSource('server')">Get Locale</button>
   </div>
</template>

<style scoped>
</style>