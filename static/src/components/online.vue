<template></template>
<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { OpenAPI } from '@/client'
import { useMessage } from 'naive-ui'
import { router } from '@/route/router'
import { msgs } from '@/main'
const message = useMessage()



const path = ref('')

let ws: WebSocket
onMounted(() => {
    OpenAPI.TOKEN = localStorage.getItem("token") as string
    if (localStorage.getItem("userinfo") !== null) {
        OpenAPI.USERNAME = JSON.parse(localStorage.getItem("userinfo") || '').username
    }
    let url = `${OpenAPI.BASE.replace('http', 'ws')}/api/websocket/join?token=${OpenAPI.TOKEN}`

    ws = new WebSocket(url);
    ws.addEventListener("error", (ev) => {
        message.error('websocket connection error')
    })
    ws.addEventListener("open", (ev) => {
        send(path.value)
        message.success('websocket ready')
    })
    ws.addEventListener("close", (ev) => {
        message.error('websocket close')
    })
    ws.addEventListener("message", (ev) => {
        try {
            let da = JSON.parse(ev.data)
            var userlist: string[] = []
            msgs.value.forEach((v, index) => {
                if (v.username !== '') {
                    userlist.push(v.username)
                }
            })
            if (da.username == 'server') {
                msgs.value.forEach((v, index) => {
                    if (da.left == v.username) {
                        msgs.value.splice(index, 1)
                    }
                })
            } else if (userlist.includes(da.username)) {
                msgs.value.forEach((v, index) => {
                    if (da.username == v.username) {
                        msgs.value[index].path = da.path
                    }
                })
            } else {
                msgs.value.push({ username: da.username, path: da.path })
            }
            console.log(msgs.value);

        } catch (e) {
            message.error(`${e}`)
        }

    })
    const send = (m: string) => {
        console.log(ws.readyState, m);
        if (ws.readyState == 1) {
            ws.send(JSON.stringify({ 'username': OpenAPI.USERNAME, "path": m }))

        }
    }

    path.value = location.href.toString()
    router.beforeEach((to, from, next) => {
        path.value = to.path+to.hash
        next()
    })
    watch(path, () => {
        send(path.value)
    })


})





</script>