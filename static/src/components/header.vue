<template>
    <header id="header" class="py-1 fixed w-full top-0 z-10 shadow-md" headinfo="">
        <nav class="mx-auto flex max-w-7xl items-center justify-between px-4" aria-label="Global">
            <div class="flex flex-1 justify-start">
                <router-link :to="{ name: 'home' }">
                    <p class=" text-4xl font-bold" v-text="headinfo.title"></p>
                </router-link>

            </div>

            <div class="flex flex-1 justify-end">
                <div class="flex items-center">
                    <button id="exclude1"
                        class="z-10 flex items-center w-full hover:opacity-50 transition-colors py-1 px-2 rounded-lg ml-1"
                        type="button" aria-label="connector" @click="togoshow">
                        <span
                            class="inline-flex text-zinc-500 flex-shrink-0 items-center justify-center 
                                                                                              font-medium uppercase overflow-hidden text-[0px] rounded-full align-middle"
                            style="width: 40px; height: 40px;">
                            <span class="inline-block w-full h-full overflow-hidden">
                                <span class="inline-flex justify-center relative w-full h-full">
                                    <img v-if="user?.avatar !== undefined" width="40" height="40"
                                        class="overflow-hidden object-cover rounded-full" :src="imgbase + user.avatar">
                                    <img v-else width="40" height="40" class="overflow-hidden object-cover rounded-full"
                                        src="@/assets/user.svg">
                                </span>
                            </span>
                        </span>
                    </button>
                </div>
                <div id="exclude2" :class="{ 'hidden': !showplan }" class="z-100 rounded-lg ring-zinc-100 min-w-[140px] absolute top-14 
                                                                            shadow-md py-2 text-base mt-1"
                    style="background-color: var(--bg-a); color: var(--bg-t);">
                    <!-- <a v-if="user?.avatar !== undefined" :href="'/user/'+user.username" target="_blank" -->

                    <button v-if="user?.avatar !== undefined"
                        @click="$router.push({ name: 'user', params: { username: user?.username }, hash: '#self' }); $emit('me'); showplan = false"
                        class="pl-5 pr-6 h-11 flex items-center w-full whitespace-nowrap hover:opacity-50">
                        <img class="overflow-hidden object-cover rounded-full" style="width: 40px;height: 40px;"
                            :alt="user.username + '的个人中心'" :src="imgbase + user.avatar">
                        <span class="p-2">{{ user.username }}</span> </button>
                    <button v-if="user?.avatar !== undefined"
                        @click="$router.push({ name: 'user', params: { username: user?.username }, hash: '#new' })"
                        class="pl-5 pr-6 h-11 flex items-center w-full whitespace-nowrap hover:opacity-50">
                        新文章</button>
                    <button v-if="user?.avatar === undefined"
                        @click="showLoginForm = true; showRegisterForm = false; showplan = false"
                        class="pl-5 pr-6 h-11 flex items-center w-full whitespace-nowrap hover:opacity-50">
                        登录</button>
                    <button @click="router.push({ name: 'home' }); showplan = false"
                        class="pl-5 pr-6 h-11 flex items-center w-full whitespace-nowrap hover:opacity-50">
                        主页</button>
                    <button @click="logout(); showplan = false"
                        class="pl-5 pr-6 h-11 flex items-center w-full whitespace-nowrap hover:opacity-50">
                        注销</button>
                </div>
            </div>
        </nav>
        <div v-if="showLoginForm || showRegisterForm"
        style="position: absolute;inset: 0;height: 100vh;background-color: rgba(0, 0, 0, .4);z-index: 19;"></div>
        <div :class="{ 'translate-y-0': showLoginForm, 'translate-y-[-200%]': !showLoginForm }"
            class="left-1/2 translate-x-[-50%] top-32 sm:top-16 absolute transition duration-500 ease-in-out z-20">
            <login :show-form="showLoginForm" @closeform="() => { showLoginForm = false }" @goregister="() => {
                showLoginForm = false
                showRegisterForm = true
            }" />
        </div>
        <div :class="{ 'translate-y-0': showRegisterForm, 'translate-y-[-200%]': !showRegisterForm }"
            class="left-1/2 translate-x-[-50%] top-32 sm:top-16 absolute transition duration-500 ease-in-out z-20">
            <register :show-form="showRegisterForm" @closeform="() => { showRegisterForm = false }" @gologin="() => {
                showLoginForm = true
                showRegisterForm = false
            }" />
        </div>
    </header>

</template>
<script setup lang="ts">
import { OpenAPI, Service, UserOut, ApiError, } from '@/client'
import login from '@/components/login.vue';
import register from './register.vue';
import { onMounted, ref, watch } from 'vue';
import { imgbase } from '@/main';
import { useMessage, NDropdown } from 'naive-ui'
import { router } from '@/route/router';
const message = useMessage()

defineProps<{
    user?: UserOut,
    headinfo: {
        title: string
    }
}>()

const showLoginForm = ref(false)
const showRegisterForm = ref(false)
const showplan = ref(false)

const togoshow = () => {
    showplan.value = !showplan.value
}

const logout = () => {
    if (localStorage.getItem('token') == null) {
        message.warning('未登录')
        localStorage.setItem('onlogin', 'false')
        return
    }
    localStorage.removeItem('token')
    localStorage.removeItem('userinfo')
    location.reload()
}
document.addEventListener('click', (e) => {
    const exclude1 = document.getElementById('exclude1')
    const exclude2 = document.getElementById('exclude2')
    if (!exclude1?.contains(e.target as Node) && !exclude2?.contains(e.target as Node)) {
        showplan.value = false

    }

});
</script>