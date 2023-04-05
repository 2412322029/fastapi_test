<template>
    <div class="container overflow-hidden">
        <div class="flex items-center min-w-max absolute left-1/2 top-1/3 translate-x-[-50%] translate-y-[-50%]">
            <div class="flex min-h-full items-center justify-center px-4 py-12 sm:px-6 lg:px-8 w-full">
                <div class="w-full max-w-md space-y-8">
                    <div>
                        <h2 class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">Sign in to your account
                        </h2>
                    </div>
                    <form class="mt-8 space-y-6" action="#" method="POST">
                        <div class="-space-y-px rounded-md shadow-sm">
                            <div>
                                <label for="name" class="sr-only" >Username</label>
                                <input id="name" :class="{ 'focus:ring-red-600': !ck0(),'focus:ring-green-600': ck0()}" name="username" type="text" required v-model="user.username"
                                    class="p-5 h-9 relative block w-full rounded-t-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:z-10 focus:ring-2 focus:ring-inset focus-visible:outline-none focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                    placeholder="Username">
                            </div>
                            <div>
                                <label for="password" class="sr-only">Password</label>
                                <input id="password" :class="{ 'focus:ring-red-600': !ck1(),'focus:ring-green-600': ck1()}" name="password" type="password" autocomplete="current-password" v-model="user.password"
                                    required
                                    class="p-5 h-9 relative block w-full rounded-b-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:z-10 focus:ring-2 focus:ring-inset focus-visible:outline-none focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                    placeholder="Password">
                            </div>
                        </div>

                        <div class="flex items-center justify-between">
                            <div class="flex items-center">
                                <input id="remember-me" name="remember-me" type="checkbox" v-model="remember"
                                    class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600">
                                <label for="remember-me" class="ml-2 block text-sm text-gray-900 select-none">Remember
                                    me</label>
                            </div>
                            <div class="text-sm">
                                <a href="./register" class="font-medium text-indigo-600 hover:text-indigo-500">No account?
                                    register</a>
                            </div>

                        </div>

                        <div>
                            <button type="button" @click="loginAction(user)"
                                class="group relative flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                                Sign in
                            </button>
                        </div>
                    </form>
                </div>
            </div>

        </div>
    </div>
</template>

<script async setup lang="ts">
import { ref, onMounted } from 'vue'
import { OpenAPI, Service, type Token, UserCreate, ApiError } from '../client'
import cogoToast from 'cogo-toast';

const user = ref<UserCreate>({
    username: "",
    password: ""
})
const remember=ref(false)
const ck0=()=>{
    const regex = /^[a-zA-Z0-9_ -]+$/;
    if (user.value.username.length>=5 && regex.test(user.value.username)) {
        return true
    }else{
        return false
    }
}
const ck1=()=>{
    if (user.value.password.length>=8) {
        return true
    }else{
        return false
    }
}
const token = ref<Token>()
const loginAction = async (user: UserCreate) => {
    await Service.loginForAccessToken(user).then((token: Token) => {
        OpenAPI.TOKEN = token.access_token
        console.log(OpenAPI.TOKEN);
        localStorage.setItem('token',OpenAPI.TOKEN)
        if (remember.value) {
            localStorage.setItem('user',JSON.stringify(user))
        }else{
            localStorage.removeItem('user')
        }
        location.href='/'
    }).catch((e: ApiError) => {
        cogoToast.error(e.message)
    })
}
onMounted(() => {
  var a = localStorage.getItem("user")
  if (a){
    user.value = JSON.parse( a as string)
  }
})

OpenAPI.TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlkIjo0MSwiZ2lkIjoxLCJleHAiOjE2ODA2ODIxNTB9.dYA1gRweLOa-7TuHkXi8EsNY--ON3lrVC7vJ4U9RBKI'
async function alluser() { return console.log(await Service.alluserinfo()) }
async function info() { return console.log(await Service.userinfo()) }



</script>
