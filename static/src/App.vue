

<template>
    <n-scrollbar id="mmm" class="h-screen">
        <router-view />
    </n-scrollbar>
</template>

<script setup lang="ts">
import { NScrollbar } from 'naive-ui'
</script>
<style>
#mmm>.n-scrollbar-rail>.n-scrollbar-rail__scrollbar {
    z-index: 10;
}
</style>