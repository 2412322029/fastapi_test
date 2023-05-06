

<template>
    <n-config-provider :locale="zhCN" :date-locale="dateZhCN" preflight-style-disabled>
        <n-message-provider>
            <n-scrollbar id="hua" class="h-screen">
                <router-view />
            </n-scrollbar>
        </n-message-provider>
    </n-config-provider>
</template>

<script setup lang="ts">
import { NScrollbar, NConfigProvider, zhCN, dateZhCN, NMessageProvider } from 'naive-ui'

</script>
<style>
#hua>.n-scrollbar-rail>.n-scrollbar-rail__scrollbar {
    z-index: 10;
    width: 9px;
}
</style>