<template>
    <header class="py-2 fixed w-full top-0 bg-white z-10">
        <nav class="mx-auto flex max-w-7xl items-center justify-between p-2 px-4" aria-label="Global">
            <div class="flex flex-1 justify-start">
                <p class=" text-4xl font-bold" v-text="headinfo.title"></p>
            </div>
            <div class="flex flex-1 justify-end">
                <div class="flex items-center">
                    <button id="exclude1" class=" flex items-center w-full hover:bg-hover transition-colors py-1 px-2 rounded-lg ml-1"
                        type="button" aria-label="connector" @click="togoshow">
                        <span
                            class="inline-flex text-zinc-500 flex-shrink-0 items-center justify-center 
                                                                          font-medium uppercase overflow-hidden text-[0px] rounded-full align-middle"
                            style="width: 40px; height: 40px;">
                            <span class="inline-block w-full h-full overflow-hidden">
                                <span class="inline-flex justify-center relative w-full h-full">
                                    <img v-if="user?.avatar !== undefined" width="40" height="40"
                                        class="overflow-hidden object-cover rounded-full" :src="'./uploads/' + user.avatar">
                                    <img v-else width="40" height="40" class="overflow-hidden object-cover rounded-full"
                                        src="@/assets/user.svg">
                                </span>
                            </span>
                        </span>
                    </button>
                </div>
                <div id="exclude2" :class="{ 'hidden': !showplan }" class="text-gray-600 bg-white rounded-lg ring-1 ring-zinc-100 min-w-[140px] absolute top-14 
                                                        shadow-md py-2 text-base mt-1">
                    <button v-if="user?.avatar !== undefined"
                        class="pl-5 pr-6 h-11 flex items-center w-full whitespace-nowrap hover:bg-slate-100">
                        <img width="40" height="40" class="overflow-hidden object-cover rounded-full"
                            :src="'./uploads/' + user.avatar">
                        <span class="p-2">{{ user.username }}</span> </button>
                    <button v-if="user?.avatar === undefined" @click="showLoginForm = true; showRegisterForm = false"
                        class="pl-5 pr-6 h-11 flex items-center w-full whitespace-nowrap hover:bg-slate-100">
                        登录</button>
                    <button @click="logout"
                        class="pl-5 pr-6 h-11 flex items-center w-full whitespace-nowrap hover:bg-slate-100">
                        注销</button>
                </div>
            </div>
        </nav>
        <div :class="{ 'translate-y-0': showLoginForm, 'translate-y-[-200%]': !showLoginForm }"
            class="left-1/2 translate-x-[-50%] top-32  absolute transition duration-500 ease-in-out border border-cyan-700 rounded-md m-0">
            <login :show-form="showLoginForm" @closeform="() => { showLoginForm = false }" @goregister="() => {
                showLoginForm = false
                showRegisterForm = true
            }" />
        </div>
        <div :class="{ 'translate-y-0': showRegisterForm, 'translate-y-[-200%]': !showRegisterForm }"
            class="left-1/2 translate-x-[-50%] top-32 absolute transition duration-500 ease-in-out border border-cyan-700 rounded-md m-0">
            <register :show-form="showRegisterForm" @closeform="() => { showRegisterForm = false }" @gologin="() => {
                showLoginForm = true
                showRegisterForm = false
            }" />
        </div>
    </header>
</template>
<script setup lang="ts">
import { OpenAPI, Service, UserOut, ApiError } from '@/client'
import login from '@/components/login.vue';
import register from './register.vue';
import { ref, watch } from 'vue';
import cogoToast from 'cogo-toast';


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
        cogoToast.warn('未登录')
        return
    }
    localStorage.removeItem('token')
    location.reload()
}
document.addEventListener('click', (e) => {
    const exclude1 = document.getElementById('exclude1')
    const exclude2 = document.getElementById('exclude2')
    if (!exclude1?.contains(e.target as Node) && !exclude2?.contains(e.target as Node)){
        showplan.value=false
        
    }
    
});
</script>