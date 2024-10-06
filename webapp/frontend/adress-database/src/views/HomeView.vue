<script setup lang="ts">
  import { useSourceCoordinator } from '@/composables/SourceCoordinator';
  import SourceSelector from "@/components/SourceSelector.vue"
  import AddressTable from "@/components/AddressTable.vue"
  import AddressEditor from '@/components/AddressEditor.vue';
</script>

<template>
  <main>
    <SourceSelector></SourceSelector>
    <AddressTable></AddressTable>
    <AddressEditor></AddressEditor>
  </main>
</template>
