<template>
    <div class="flex min-h-full items-center justify-center px-4 py-6 lg:px-8 w-80 bg-white">
        <div class="w-full max-w-md space-y-8">
            <div>
                <h2 class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">注册
                </h2>
            </div>
            <form class="mt-8 space-y-6" action="#" method="POST">
                <div class="-space-y-px rounded-md shadow-sm">
                    <div>
                        <label for="name" class="sr-only">Username</label>
                        <input id="name" :class="{ 'focus:ring-red-600': !ck0(), 'focus:ring-green-600': ck0() }"
                            name="username" type="text" required v-model="user.username"
                            class="p-5 h-9 relative block w-full rounded-t-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:z-10 focus:ring-2 focus:ring-inset focus-visible:outline-none focus:ring-indigo-600 sm:text-sm sm:leading-6"
                            placeholder="Username.length>=5">
                    </div>
                    <div>
                        <label for="password1" class="sr-only">Password</label>
                        <input id="password1" :class="{ 'focus:ring-red-600': !ck1(), 'focus:ring-green-600': ck1() }"
                            name="password" type="password" autocomplete="current-password" v-model="user.password" required
                            class="p-5 h-9 relative block w-full border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:z-10 focus:ring-2 focus:ring-inset focus-visible:outline-none focus:ring-indigo-600 sm:text-sm sm:leading-6"
                            placeholder="Password.length>=8">
                    </div>
                    <div>
                        <label for="password2" class="sr-only">Password</label>
                        <input id="password2" :class="{ 'focus:ring-red-600': !ck2(), 'focus:ring-green-600': ck2() }"
                            name="password" type="password" autocomplete="current-password" v-model="password_agine"
                            required
                            class="p-5 h-9 relative block w-full rounded-b-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:z-10 focus:ring-2 focus:ring-inset focus-visible:outline-none sm:text-sm sm:leading-6"
                            placeholder="Enter password agine">
                    </div>
                </div>

                <div class="flex items-center justify-between">
                    <div class="text-sm cursor-pointer">
                        <a @click="$emit('gologin')" class="font-medium text-indigo-600 hover:text-indigo-500">返回登录</a>
                    </div>
                </div>

                <div>
                    <button type="button" @click="registerAction(user)"
                        :class="{ 'bg-indigo-600 hover:bg-indigo-500 focus-visible:outline-indigo-600 cursor-pointer': ck0() && ck1() && ck2() }"
                        class="group relative flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white  focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 cursor-not-allowed">
                        注册
                    </button>
                    <button type="button" @click="$emit('closeform')"
                        class="group mt-2 relative flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                        关闭
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script async setup lang="ts">
import { ref } from 'vue'
import { OpenAPI, Service, type RegisterSuccess, UserCreate, ApiError } from '../client'
import cogoToast from 'cogo-toast';
const emit = defineEmits(['gologin'])
defineProps<{
    showForm: boolean
}>()

const user = ref<UserCreate>({
    username: "",
    password: ""
})

const password_agine = ref()
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
const ck2 = () => {
    if (!ck1() || user.value.password !== password_agine.value) {
        return false
    } else {
        return true
    }
}

const registerAction = async (user: UserCreate) => {
    if (!ck0()) {
        cogoToast.error('用户名只包含大小写字母、数字、下划线、空格和短横线')
        return
    } else if (!ck1()) {
        cogoToast.error('密码太短')
        return
    } else if (!ck2()) {
        cogoToast.error('密码不一致')
        return
    }
    await Service.register(user).then((r: RegisterSuccess) => {
        cogoToast.success(r.detail)
        emit('gologin')
    }).catch((e: ApiError) => {
        cogoToast.error(e.message);
    })
}


</script>
