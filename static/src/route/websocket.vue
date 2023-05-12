<template>
    <Headers :user="userinfo" :headinfo="{ title: '聊天室' }" />
    <div class="mx-auto flex max-w-7xl items-center justify-between px-4 top-20 relative">
        <div class=" flex flex-col p-3 w-full border h-5/6">
            <div v-for='x in msgs' class="flex m-2">
                <div class=" flex">
                    <img :src="imgbase + x.a" alt="" width="40" height="40"
                        class="overflow-hidden object-cover rounded-full">
                    <p> {{ x.username }}</p>
                </div>
                <div class="">
                    <div class=" border-sky-700 border-x-2 border-y-2 p-2 rounded "> {{ x.path }}</div>
                </div>
            </div>

        </div>
        <div class=" border fixed bottom-10 w-5/6">
            <input type="text" v-model="msg"
                class=" float-left h-10 w-4/5 rounded text-lg border-sky-300 border-x-2 border-y-2 text-indigo-600 ">
            <button @click="send(msg)" class=" float-right left-0 pl-5 pr-6 h-11 bg-slate-100">send</button>
        </div>

    </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { OpenAPI, Service, UserOut, ApiError } from '@/client'
import Headers from '@/components/header.vue';
import { imgbase, usews } from '@/main';
import { useMessage } from 'naive-ui'

if (usews===false) {
    location.href='/'
}
const message = useMessage()
const userinfo = ref<UserOut>()


const msg = ref('')
const msgs = ref<Array<{ username: string, path: string, a: string }>>([])
let ws: WebSocket
onMounted(() => {
    OpenAPI.TOKEN = localStorage.getItem("token") as string
    Service.userinfo().then((u: UserOut) => {
        userinfo.value = u
    }).catch((e: ApiError) => {
        message.error(e.message)
        localStorage.removeItem('userinfo')
        localStorage.removeItem('token')
    })
    let url = `${OpenAPI.BASE.replace('http', 'ws')}/api/websocket/join?token=${OpenAPI.TOKEN}`

    ws = new WebSocket(url);
    ws.addEventListener("error", (ev) => {
        message.error('websocket connection error')
    })
    ws.addEventListener("open", (ev) => {
        message.success('websocket ready')
    })
    ws.addEventListener("close", (ev) => {
        message.error('websocket close')
    })
    ws.addEventListener("message", (ev) => {
        try {
            let da = JSON.parse(ev.data)
            msgs.value.forEach((el) => {
                if (el.username == da.username) {
                    da.a = el.a
                }
            })
            if (da.a == undefined) {
                Service.publishUserInfo(da.username).then((pu) => {
                    da.a = pu.avatar
                }).catch((e: ApiError) => {
                    message.error(`${e.message},${e.statusText}`)
                })
            }
            msgs.value.push(da as never)

        } catch (e) {
            message.error(`${e}`)
        }

    })

})

const send = (m: string) => {
    if (msg.value == '') {
        message.error('消息为空')
        return
    }
    ws.send(JSON.stringify({ 'username': userinfo.value?.username, "path": m }))
}



</script>