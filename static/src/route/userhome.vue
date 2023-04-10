<template>
    <Headers :user="userinfo" :headinfo="{ title: '个人中心' }" />
    <div class="mx-auto flex max-w-7xl items-center justify-between px-4 top-20 relative">
        <div v-if="isme">
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
        <div v-if="!isme">
            <div>
                <img v-if="pubuserinfo != undefined" :src="imgbase + pubuserinfo.avatar" alt="" class=" w-20">
                <p v-text="pubuserinfo?.id"></p>
                <p v-text="pubuserinfo?.username"></p>
            </div>
            <div v-for="post in posts">
                <div class=" border">
                    <div>
                        <a :href="'#' + post.id">
                            <h3 v-text="post.title"></h3>
                        </a>
                        <p v-text="post.content"></p>
                    </div>
                    <div>
                        <p v-text="post.created_at"></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { OpenAPI, Service, UserOut, ApiError, PubUserInfo, PostOut } from '@/client'
import cogoToast from 'cogo-toast';
import Headers from '@/components/header.vue';
import { imgbase } from '@/main'
const router = useRouter()
const route = useRoute()
const userinfo = ref<UserOut>()
const pubuserinfo = ref<PubUserInfo>()
const isme = ref(false)

const file = ref()
const fileblob = ref()
const base64 = ref()
const page = ref(1)
const pagesize = ref(5)
const posts = ref<Array<PostOut>>()
onMounted(() => {
    OpenAPI.TOKEN = localStorage.getItem("token") as string
    OpenAPI.USERNAME = localStorage.getItem("username") as string
    if (OpenAPI.USERNAME == route.params.username) {
        Service.userinfo().then((u: UserOut) => {
            userinfo.value = u
            isme.value = true
        })
    } else {
        Service.publishUserInfo(route.params.username as string).then((up: PubUserInfo) => {
            pubuserinfo.value = up
        }).catch((e: ApiError) => {
            cogoToast.error(e.message + e.body.detail)
        })
        Service.getUsersPosts(route.params.username as string, page.value, pagesize.value).then((po: Array<PostOut>) => {
            posts.value = po
        }).catch((e: ApiError) => {
            cogoToast.error(e.message + e.body.detail)
        })
    }
})

const upl = () => {
    Service.updateAvatar({ 'avatar_new': file.value.files[0] }).then((up) => {
        cogoToast.success(up.detail)
    }).catch((e: ApiError) => {
        cogoToast.error(e.message + e.body.detail)
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