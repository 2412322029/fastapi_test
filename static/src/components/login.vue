<template>
    用户名 <input type="text" v-model="user.username"><br>
    密码 <input type="password" v-model="user.password">
    <br><button @click="loginAction(user)">login</button>

    <button @click="alluser()">alluser</button>
    <button @click="info()">info</button>
</template>

<script async setup lang="ts">
import { ref } from 'vue'
import { OpenAPI, Service, type Token, UserCreate, ApiError } from '../client'

const user = ref<UserCreate>({
    username: "",
    password: ""
})
const token = ref<Token>()
const loginAction = async (user: UserCreate) => {
    await Service.loginForAccessToken(user).then((token: Token) => {
        OpenAPI.TOKEN = token.access_token
        console.log(OpenAPI.TOKEN);
    }).catch((e: ApiError) => {
        console.log(e.message);
    })



}

OpenAPI.TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlkIjo0MSwiZ2lkIjoxLCJleHAiOjE2ODA2ODIxNTB9.dYA1gRweLOa-7TuHkXi8EsNY--ON3lrVC7vJ4U9RBKI'
async function alluser() { return console.log(await Service.alluserinfo()) }
async function info() { return console.log(await Service.userinfo()) }



</script>
