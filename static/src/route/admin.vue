<template>
    <Headers :user="userinfo" :headinfo="{ title: '管理' }" />
    <div v-if="userinfo" class="mx-auto flex max-w-7xl items-center flex-col px-4 top-20 relative">
        <table>
            <tr>
                <th>id</th>
                <th>username</th>
                <th>avatar</th>
                <th>state</th>
                <th>group_id</th>
                <th>created_at</th>
                <th>updated_at</th>
            </tr>
            <tbody>
                <tr v-for="u in alluserinfo">
                    <td v-text="u.id_"></td>
                    <td v-text="u.username"></td>
                    <td v-text="u.avatar"></td>
                    <td v-text="u.state"></td>
                    <td v-text="u.group_id"></td>
                    <td v-text="u.created_at"></td>
                    <td v-text="u.updated_at"></td>
                </tr>
            </tbody>
        </table>
        <div>
            用户注册 <input v-model="isr" type="checkbox">  <button @click="tj1">提交</button>
            <br>
            接口限制 <input v-model="isl" type="checkbox">  <button @click="tj2">提交</button>
        </div>

    </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { OpenAPI, Service, UserOut, ApiError } from '@/client'
import Headers from '@/components/header.vue';
import { useMessage } from 'naive-ui'
const message = useMessage()
const userinfo = ref<UserOut>()

const isr =ref()
const isl =ref()
const alluserinfo = ref<Array<UserOut>>()
const showalluser = () => {
    Service.alluserinfo().then((us: Array<UserOut>) => {
        alluserinfo.value = us
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
}
onMounted(() => {
    OpenAPI.TOKEN = localStorage.getItem("token") as string
    Service.admininfo().then((u: UserOut) => {
        userinfo.value = u
        showalluser()
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
    Service.isAllowRegister().then((b:boolean) => {
        isr.value=b
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
    Service.isLimiter().then((b:boolean) => {
        isl.value=b
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
})

const tj1=()=>{
    Service.allowRegister(isr.value).then((b:boolean) => {
        message.error(b+'允许注册='+isr.value)
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
}
const tj2=()=>{
    Service.setLimiter(isl.value).then((b:boolean) => {
        message.error(b+'限制='+isl.value)
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
}

</script>

<style scoped>
table {
    border-collapse: collapse;
}

table th {
    font-weight: bold;
}

table th,
table td {
    border: 1px solid #ccc;
    padding: 6px 13px;
}

table tr {
    border-top: 1px solid #ccc;
    background-color: #fff;
}

table tr:nth-child(2n) {
    background-color: #f8f8f8;
}
</style>