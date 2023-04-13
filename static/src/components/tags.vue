<template>
    <n-card>
        <n-tag type="info" round v-for="t in tags" v-text="t.name + ' ' + t.reference_count" @click=""
            class="m-2 cursor-pointer">
        </n-tag>
    </n-card>
</template>
<script setup lang="ts">
import { TagInDB } from '@/client';
import { NTag, NCard } from 'naive-ui'
defineProps<{
    tags?: Array<TagInDB>
}>()
</script>