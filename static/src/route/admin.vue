<template>
    <Headers :user="userinfo" :headinfo="{ title: '管理' }" />
    <div v-if="userinfo" class="mx-auto flex max-w-7xl items-center justify-between px-4 top-20 relative">
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
                    <td v-text="u.id"></td>
                    <td v-text="u.username"></td>
                    <td v-text="u.avatar"></td>
                    <td v-text="u.state"></td>
                    <td v-text="u.group_id"></td>
                    <td v-text="u.created_at"></td>
                    <td v-text="u.updated_at"></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { OpenAPI, Service, UserOut, ApiError } from '@/client'
import cogoToast from 'cogo-toast';
import Headers from '@/components/header.vue';
const userinfo = ref<UserOut>()

const alluserinfo = ref<Array<UserOut>>()
const showalluser = () => {
    Service.alluserinfo().then((us: Array<UserOut>) => {
        alluserinfo.value = us
    }).catch((e: ApiError) => {
        cogoToast.error(e.message)
    })
}
onMounted(() => {
    OpenAPI.TOKEN = localStorage.getItem("token") as string
    Service.admininfo().then((u: UserOut) => {
        userinfo.value = u
        showalluser()
    }).catch((e: ApiError) => {
        cogoToast.error(e.message)
    })
})

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