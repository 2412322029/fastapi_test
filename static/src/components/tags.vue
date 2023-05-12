<template>
    <n-card>
        <n-badge v-for="t in tags" :value="t.reference_count" :show-zero="true" type="success" :offset="[-10, 10]">
        <n-tag type="info" round v-text="t.name" @click="$router.push({name:'tag',params:{name:t.name}})"
            class="m-2 cursor-pointer hover:shadow">
        </n-tag>
    </n-badge>
    </n-card>
</template>
<script setup lang="ts">
import { TagInDB } from '@/client';
import { NTag, NCard, NBadge } from 'naive-ui'
defineProps<{
    tags?: Array<TagInDB>
}>()
</script>