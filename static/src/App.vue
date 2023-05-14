

<template>
    <n-config-provider :locale="zhCN" :date-locale="dateZhCN" preflight-style-disabled>
        <n-message-provider>
            <n-dialog-provider>
                <n-scrollbar id="hua" class="h-screen">
                    <online v-if="usews"></online>
                    <router-view />
                </n-scrollbar>
            </n-dialog-provider>
        </n-message-provider>
    </n-config-provider>
    <Transition>
        <div v-if="loading" class="loading">
            <n-spin size="large" />
        </div>
    </Transition>
    <canvas id="cbg" class="rib"
        style="opacity: 0.6; position: fixed; top: 0px; left: 0px; z-index: -2; width: 100%; height: 70%; pointer-events: none;"></canvas>
</template>

<script setup lang="ts">
import { NScrollbar, NConfigProvider, zhCN, dateZhCN, NMessageProvider, NDialogProvider, NSpin } from 'naive-ui'
import { ribbon } from './script/ribbon';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import online from '@/components/online.vue'
import { loading, usews } from '@/main'
const router = useRouter()
onMounted(() => {
    let t = localStorage.getItem('ribbon-times')
    if (t) {
        ribbon(Number(t))
    }
})

router.beforeEach((to, from) => {
    if (to.name == 'home' || to.name == 'post' ||to.name == 'tag') {
        loading.value = true
    }
    return true
})
// router.afterEach((to, from) => {
//     loading.value = false
//     return true
// })
</script>
<style>
#hua>.n-scrollbar-rail>.n-scrollbar-rail__scrollbar {
    z-index: 10;
    width: 9px;
}

.loading {
    width: 100%;
    height: 100%;
    z-index: 9;
    top: 0;
    position: fixed;
    display: flex;
    justify-content: center;
}
/* 下面我们会解释这些 class 是做什么的 */
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
  display: none;
}
</style>