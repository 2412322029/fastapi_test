<template>
    <div class="flex min-h-full items-center justify-center px-4 py-6 lg:px-8 w-80 bg-white">
        <div class="w-full max-w-md space-y-8">
            <div>
                <h2 class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">登录
                </h2>
            </div>
            <n-form ref="formRef" :model="user" :rules="rules">
                <n-form-item path="username" label="用户名">
                    <n-input v-model:value="user.username" @keydown.enter.prevent />
                </n-form-item>
                <n-form-item path="password" label="密码">
                    <n-input v-model:value="user.password" type="password" @keydown.enter.prevent />
                </n-form-item>
                <n-row :gutter="[0, 24]">
                    <div class="text-sm cursor-pointer">
                        <a @click="$emit('goregister')" class="font-medium" style="color: #18a058;">注册</a>
                    </div>
                    <n-col :span="24">

                        <div class=" flex justify-between">
                            <n-button class="text-black" round type="primary" @click="$emit('closeform')">
                                关闭
                            </n-button>
                            <n-button :disabled="user.username === ''" round type="primary" @click="loginAction(user)"
                                class="text-black">
                                登录
                            </n-button>
                        </div>
                    </n-col>
                </n-row>
            </n-form>
        </div>
    </div>
</template>

<script async setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { OpenAPI, Service, type Token, UserCreate, ApiError, UserOut } from '../client'
import cogoToast from 'cogo-toast';
import { NButton, NForm, NFormItem, NRow, NCol, NInput, FormItemRule, FormRules } from 'naive-ui'

defineProps<{
    showForm: boolean
}>()

const user = reactive<UserCreate>({
    username: "",
    password: ""
})
const remember = ref(true)
const rules: FormRules = {
    username: [
        {
            required: true,
            validator(rule: FormItemRule, value: string) {
                if (!value) {
                    return new Error('需要用户名')
                } else if (!/^[a-zA-Z0-9_ -]+$/.test(value)) {
                    return new Error('用户名只包含英文 _-')
                } else if (value.length <= 4) {
                    return new Error('用户名应大于4位')
                }
                return true
            },
            trigger: ['input', 'blur']
        }
    ],
    password: [
        {
            required: true,
            validator(rule: FormItemRule, value: string) {
                if (!value) {
                    return new Error('密码')
                } else if (value.length >= 8) {
                    return new Error('密码应大于8位')
                }
                return true
            },
            message: '请输入密码'
        }
    ],
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
            localStorage.setItem('username', user.username)
        } else {
            localStorage.removeItem('username')
        }
        location.reload()
    }).catch((e: ApiError) => {
        cogoToast.error(e.message)
    })
}
onMounted(() => {
    var a = localStorage.getItem("username")
    if (a) {
        user.username = a as string
    }
})



</script>
