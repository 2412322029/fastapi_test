<template>
    <div class="flex min-h-full items-center justify-center px-4 py-6 lg:px-8 w-80 bg-white">
        <div class="w-full max-w-md space-y-8">
            <div>
                <h2 class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">登录
                </h2>
            </div>
            <form class="mt-8 space-y-6">
                <div class="-space-y-px rounded-md shadow-sm">
                    <div>
                        <label for="name1" class="sr-only">Username</label>
                        <input id="name1" :class="{ 'focus:ring-red-600': !ck0(), 'focus:ring-green-600': ck0() }"
                            name="username" type="text" required v-model="user.username"
                            class="p-5 h-9 relative block w-full rounded-t-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:z-10 focus:ring-2 focus:ring-inset focus-visible:outline-none focus:ring-indigo-600 sm:text-sm sm:leading-6"
                            placeholder="Username">
                    </div>
                    <div>
                        <label for="password" class="sr-only">Password</label>
                        <input id="password" :class="{ 'focus:ring-red-600': !ck1(), 'focus:ring-green-600': ck1() }"
                            name="password" type="password" autocomplete="current-password" v-model="user.password" required
                            class="p-5 h-9 relative block w-full rounded-b-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:z-10 focus:ring-2 focus:ring-inset focus-visible:outline-none focus:ring-indigo-600 sm:text-sm sm:leading-6"
                            placeholder="Password">
                    </div>

                </div>

                <div class="flex items-center justify-between">
                    <div class="flex items-center">
                        <input id="remember-me" name="remember-me" type="checkbox" v-model="remember"
                            class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600">
                        <label for="remember-me" class="ml-2 block text-sm text-gray-900 select-none">记住我</label>
                    </div>
                    <div class="text-sm cursor-pointer">
                        <a @click="$emit('goregister')" class="font-medium text-indigo-600 hover:text-indigo-500">注册</a>
                    </div>

                </div>

                <div>
                    <button type="button" @click="loginAction(user)"
                        class="relative flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                        登录
                    </button>
                    <button type="button" @click="$emit('closeform')"
                        class="mt-2 relative flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                        关闭
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script async setup lang="ts">
import { ref, onMounted } from 'vue'
import { OpenAPI, Service, type Token, UserCreate, ApiError } from '../client'
import cogoToast from 'cogo-toast';

defineProps<{
    showForm: boolean
}>()

const user = ref<UserCreate>({
    username: "",
    password: ""
})
const remember = ref(false)
const ck0 = () => {
    const regex = /^[a-zA-Z0-9_ -]+$/;
    if (user.value.username.length >= 5 && regex.test(user.value.username)) {
        return true
    } else {
        return false
    }
}
const ck1 = () => {
    if (user.value.password.length >= 8) {
        return true
    } else {
        return false
    }
}
const loginAction = async (user: UserCreate) => {
    if (user.username == '' || user.password == '') {
        cogoToast.error('请输入账号密码')
        return
    }
    await Service.loginForAccessToken(user).then((token: Token) => {
        OpenAPI.TOKEN = token.access_token
        cogoToast.success('登录成功')
        localStorage.setItem('token', OpenAPI.TOKEN)
        if (remember.value) {
            localStorage.setItem('user', JSON.stringify(user))
        } else {
            localStorage.removeItem('user')
        }
        location.reload()
    }).catch((e: ApiError) => {
        cogoToast.error(e.message)
    })
}
onMounted(() => {
    var a = localStorage.getItem("user")
    if (a) {
        user.value = JSON.parse(a as string)
    }
})

async function alluser() { return console.log(await Service.alluserinfo()) }
async function info() { return console.log(await Service.userinfo()) }



</script>
