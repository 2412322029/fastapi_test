

<template>
    <n-config-provider :locale="zhCN" :date-locale="dateZhCN" preflight-style-disabled :theme="theme">
        <n-global-style />
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
import { NScrollbar, NConfigProvider, zhCN, dateZhCN, NMessageProvider, NDialogProvider, NSpin, drawerDark } from 'naive-ui'
import { darkTheme, NGlobalStyle, useOsTheme } from 'naive-ui'
import { ribbon } from './script/ribbon';
import { onMounted, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import online from '@/components/online.vue'
import { loading, usews, theme, followos } from '@/main'
import { watchEffect } from 'vue';
import { OpenAPI } from './client';
const router = useRouter()

onMounted(() => {
    OpenAPI.TOKEN = localStorage.getItem("token") as string
    let t = localStorage.getItem('ribbon-times')
    let _followos = localStorage.getItem('follow-os')
    if (_followos == 'true') {
        followos.value = true
    }else{
        followos.value = false
    }
    if (t) {
        ribbon(Number(t))
    }
    let f = (a: string, b: string) => {
        document.documentElement.style.setProperty(a, b)
    }
    watchEffect(() => {
        if (followos.value) {
            if (useOsTheme().value == 'dark') {
                theme.value = darkTheme
            } else {
                theme.value = null
            }
        }
        cg()
    })
    function cg() {
        if (theme.value?.name == 'dark') {
            f('--bg-a', '#18181c');
            f('--bg-t', '#ffffffe6');
            f('--bg-bo', '#424242');
            f('--bg-app', '#00000085');

        } else {
            f('--bg-a', '#fff');
            f('--bg-t', '#333639');
            f('--bg-bo', '#efeff5');
            f('--bg-app', '#d3e8fb85');

        }
    }
})

router.beforeEach((to, from) => {
    if (to.name == 'home' || to.name == 'post' || to.name == 'tag') {
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