<template>
    <Headers :user="userinfo" :headinfo="{ title: '管理' }" />
    <div v-if="userinfo" class="mx-auto flex max-w-7xl items-center flex-col px-4 top-20 relative">
        <n-tabs type="line" animated size="large">
            <n-tab-pane name="setting" tab="设置" display-directive="show:lazy">
                <n-table striped>
                    <tbody>
                        <tr>
                            <td>用户注册 </td>
                            <td><n-switch v-model:value="isr"></n-switch> </td>
                            <td> <button @click="tj1">提交</button></td>
                        </tr>
                        <tr>
                            <td> 接口限制 </td>
                            <td><n-switch v-model:value="isl"></n-switch> </td>
                            <td> <button @click="tj2">提交</button></td>
                        </tr>
                    </tbody>
                </n-table>
            </n-tab-pane>
            <n-tab-pane name="user" tab="用户管理" display-directive="show:lazy">
                <n-table striped>
                    <thead>
                        <th>id</th>
                        <th>username</th>
                        <th>avatar</th>
                        <th>state</th>
                        <th>group_id</th>
                        <th>created_at</th>
                        <th>updated_at</th>
                    </thead>
                    <tbody>
                        <tr v-for="u in alluserinfo">
                            <td v-text="u.id_"></td>
                            <td v-text="u.username"></td>
                            <td>
                                <img class="overflow-hidden object-cover rounded-full" style="width: 40px;height: 40px;"
                                    :src="imgbase + u.avatar">
                            </td>
                            <td v-text="u.state"></td>
                            <td v-text="u.group_id"></td>
                            <td v-text="u.created_at"></td>
                            <td v-text="u.updated_at"></td>
                            <td><button @click="$router.push({name:'user',params:{username:u.username}})">查看</button></td>
                        </tr>
                    </tbody>
                </n-table>
            </n-tab-pane>

        </n-tabs>




    </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { OpenAPI, Service, UserOut, ApiError } from '@/client'
import Headers from '@/components/header.vue';
import CPU from '@/components/cpu.vue';
import { useMessage, NTable, NSwitch, NTabs, NTabPane } from 'naive-ui'
import { imgbase } from '@/main';

const message = useMessage()
const userinfo = ref<UserOut>()


const isr = ref()
const isl = ref()
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
    Service.isAllowRegister().then((b: boolean) => {
        isr.value = b
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
    Service.isLimiter().then((b: boolean) => {
        isl.value = b
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
})

const tj1 = () => {
    Service.allowRegister(isr.value).then((b: boolean) => {
        message.success(b + '允许注册=' + isr.value)
        location.reload()
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
}
const tj2 = () => {
    Service.setLimiter(isl.value).then((b: boolean) => {
        message.success(b + '限制=' + isl.value)
        location.reload()
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
}

</script>

<style scoped></style>