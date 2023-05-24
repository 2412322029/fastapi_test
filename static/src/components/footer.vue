<template>
    <div style="height: 300px;"></div>
    <footer class="w-full text-gray-500 border" style="border-color: var(--bg-bo);">
        <div class=" flex justify-center h-20 items-center">
            <p class=" text-sm p-6"> Made by <a href="https://github.com/2412322029" target="_blank">Lolik</a></p>
            <a href="https://github.com/2412322029/fastapi_test" target="_blank">
                <img src="../assets/github.svg" 
                    class="inline-flex hover:scale-110 transition-transform ease align-middle mr-2 sm:mr-5 cursor-pointer w-5"
                    alt=""></a>
            <n-checkbox v-model:checked="followos">
                跟随系统
            </n-checkbox>
            <n-switch v-model:value="kai" :disabled="followos">
                <template #checked-icon>
                    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                        viewBox="0 0 512 512">
                        <path
                            d="M152.62 126.77c0-33 4.85-66.35 17.23-94.77C87.54 67.83 32 151.89 32 247.38C32 375.85 136.15 480 264.62 480c95.49 0 179.55-55.54 215.38-137.85c-28.42 12.38-61.8 17.23-94.77 17.23c-128.47 0-232.61-104.14-232.61-232.61z"
                            fill="currentColor"></path>
                    </svg>
                </template>
                <template #unchecked-icon>
                    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 24 24">
                        <g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                            stroke-linejoin="round">
                            <circle cx="12" cy="12" r="4"></circle>
                            <path d="M3 12h1m8-9v1m8 8h1m-9 8v1M5.6 5.6l.7.7m12.1-.7l-.7.7m0 11.4l.7.7m-12.1-.7l-.7.7">
                            </path>
                        </g>
                    </svg>
                </template>
            </n-switch>
        </div>

    </footer>
</template>
<script lang="ts" setup>
import { darkTheme, NSwitch, NCheckbox } from 'naive-ui'
import { followos, theme } from '@/main';
import { ref } from 'vue';
import { watch } from 'vue';

let f = (a: string, b: string) => {
    document.documentElement.style.setProperty(a, b)
}
let kai = ref(theme.value?.name == 'dark')
watch(kai, () => {
    if (kai.value) {
        theme.value = darkTheme;
        localStorage.setItem('theme-dark', 'true')
    } else {
        theme.value = null
        localStorage.setItem('theme-dark', 'false')
    }
    cg()
})
let _kai = localStorage.getItem('theme-dark')
if (_kai == 'true') {
    kai.value = true
} else {
    kai.value = false
}
watch(followos, () => {
    if (followos.value) {
        kai.value = theme.value?.name == 'dark'
        localStorage.setItem('follow-os', 'true')
    } else {
        localStorage.setItem('follow-os', 'false')
    }
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
</script>
<style scoped>
.n-divider .n-divider__line {
    background-color: transparent !important;
    ;
}
</style>
