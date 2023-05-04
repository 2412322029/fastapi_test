<template>
    <router-link :to="{ name: 'home' }">
        <Headers :user="userinfo" :headinfo="{ title: 'home' }" />
    </router-link>
    <hr>
    <div class="mx-auto flex max-w-7xl justify-between lg:px-4 top-20 relative">
        <div class="lg:w-2/3 max-lg:w-full">
            <p v-text="post?.title" class=" text-2xl flex justify-center m-5"></p>
            <div class=" flex items-center m-3 ml-6">
                <n-avatar round size="small" :src="imgbase + post?.author_img" />
                <span v-text="post?.author" class=" pl-2 cursor-pointer" @click="router.push({ name: 'user', params: { username: post?.author } })"></span>
                <span class=" text-sm text-gray-500 ">&nbsp;&nbsp; 创建于:{{ post?.created_at.replace('T', ' ') }} |
                    更新于:{{ post?.updated_at.replace('T', ' ') }}</span>
            </div>

            <v-md-preview :text="post?.content"></v-md-preview>
        </div>
        <div class="lg:w-1/3 max-lg:hidden">
            
        </div>
    </div>
    <Footer />
</template>
<script setup lang="ts">
import { imgbase } from '@/main';

import Headers from '@/components/header.vue';
import Footer from '@/components/footer.vue';
import { useRoute, useRouter } from 'vue-router';
import { Service, ApiError, PostOut, OpenAPI, UserOut } from '@/client/index'
import { useMessage, NAvatar } from 'naive-ui'
import { onMounted, ref } from 'vue';
const message = useMessage()
const route = useRoute()
const router = useRouter()
let pid = Number(route.params.id)
if (Number.isNaN(pid)) {
    location.href = '/'
}
const post = ref<PostOut>()
Service.getPostById(pid).then((po: PostOut) => {
    post.value = po
}).catch((e: ApiError) => {
    message.error(e.message)
    if (e.status == 404) {
        router.push({ name: 'notfound' })
    }
})
const userinfo = ref<UserOut>()
onMounted(() => {
    OpenAPI.TOKEN = localStorage.getItem("token") as string
    Service.userinfo().then((u: UserOut) => {
        userinfo.value = u
    }).catch((e: ApiError) => {
        message.error(e.message)
    })

})

</script>