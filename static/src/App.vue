

<template>
    <n-config-provider :locale="zhCN" :date-locale="dateZhCN" preflight-style-disabled>
        <n-message-provider>
            <n-scrollbar id="hua" class="h-screen">
                <router-view />
            </n-scrollbar>
        </n-message-provider>
    </n-config-provider>
    <canvas id="cbg" class="rib"
        style="opacity: 0.6; position: fixed; top: 0px; left: 0px; z-index: -2; width: 100%; height: 70%; pointer-events: none;"></canvas>
</template>

<script setup lang="ts">
import { NScrollbar, NConfigProvider, zhCN, dateZhCN, NMessageProvider } from 'naive-ui'
import { ribbon } from './script/ribbon';
import { onMounted } from 'vue';

onMounted(() => {
    let t = localStorage.getItem('ribbon-times')
    if (t) {
        ribbon(Number(t))
    }
})

</script>
<style>
#hua>.n-scrollbar-rail>.n-scrollbar-rail__scrollbar {
    z-index: 10;
    width: 9px;
}
</style>