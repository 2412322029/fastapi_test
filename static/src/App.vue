<script setup lang="ts">
import login from './components/login.vue'
</script>

<template>
  <div>

  </div>
  <Suspense>
    <template #default>
      <login />
    </template>

    <template #fallback>
      Loading...
    </template>
    
  </Suspense>
</template>

<style scoped></style>
