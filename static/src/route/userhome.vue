<template>
    <Headers :user="userinfo" :headinfo="{ title: '个人中心' }" />
    <div class="mx-auto flex max-w-7xl items-center justify-between px-4 top-20 relative">
        <table>
            <tr>
                <td>修改头像</td>
                <td>
                    <input ref="file" type="file" name="" @change="onChange()" />
                </td>
                <td>
                    <img :src="base64" width="100" alt="">
                </td>
                <td>
                    <button @click="upl()">提交</button>
                </td>
            </tr>
        </table>


    </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { OpenAPI, Service, UserOut, ApiError } from '@/client'
import cogoToast from 'cogo-toast';
import Headers from '@/components/header.vue';
const userinfo = ref<UserOut>()

const file = ref()
const fileblob = ref()
const base64 = ref()
onMounted(() => {
    OpenAPI.TOKEN = localStorage.getItem("token") as string
    Service.userinfo().then((u: UserOut) => {
        userinfo.value = u
    }).catch((e: ApiError) => {
        cogoToast.error(e.message)
    })

})

const upl = () => {
    Service.updateUsername1({'avatar_new': file.value.files[0]}).then((up) => {
        cogoToast.success(up.detail)
    }).catch((e: ApiError) => {
        cogoToast.error(e.message)
    })
}
const onChange = () => {

    let f = file.value.files[0]
    const type = f.type;
    const reader = new FileReader();
    reader.readAsDataURL(f)
    reader.onload = (e) => {
        try {
            //@ts-ignore
            fileblob.value = new Blob([e.target.result], { type });
            //@ts-ignore
            base64.value = e.target.result
        } catch (e) {
        }
    }
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