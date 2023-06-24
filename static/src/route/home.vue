<template>
    <Headers :user="userinfo" :headinfo="{ title: 'home' }" />
    <section class="mx-auto flex max-w-7xl justify-between lg:px-4 mb-20 relative" style="min-height: calc(100vh - 100px);">
        <div class="lg:w-2/3 max-lg:w-full mt-20">
            <n-layout style="background-color: transparent;">
                <n-layout-content content-style="padding:15px;background-color: transparent;">
                    <n-card v-for="post in posts?.posts" class="mb-5" hoverable bordered :class="'shadow'">
                        <template #header>
                            <p v-text="post.title || '无标题'" class=" rounded-xl mb-6 cursor-pointer hover:opacity-70"
                                @click="router.push({ name: 'post', params: { id: post.id_ } })"></p>
                        </template>
                        <div v-text="post.content || '无内容'" @click="">
                        </div>
                        <template #header-extra>
                            <div class=" cursor-pointer flex justify-between items-center"
                                @click="router.push({ name: 'user', params: { username: post.author } })">
                                <n-avatar round size="small" :src="imgbase + post.author_img" object-fit="cover" />
                                <span v-text="post.author" class=" pl-2"></span>
                            </div>
                        </template>
                        <template #footer>
                            <n-tag type="info" round v-for="t in post.tags" @click=""
                                class=" cursor-pointer mx-1 hover:shadow">
                                <span @click="$router.push('tag/' + t)">{{ t }}</span>
                            </n-tag>
                        </template>
                        <template #action>
                            <div class=" float-right">
                                <n-ellipsis style="max-width: 220px">
                                    <p v-text="post.updated_at.replace('T', ' ')"></p>
                                </n-ellipsis>
                            </div>
                        </template>
                    </n-card>
                </n-layout-content>
                <n-pagination v-model:page="page" :page-count="Math.ceil(posts?.total as number / pagesize)" :page-slot="5"
                    size="large" :page-sizes="[5, 10]" v-model:page-size="pagesize" show-size-picker
                    class=" flex justify-center" />
            </n-layout>
        </div>
        <aside class="lg:w-1/3 max-lg:hidden m-2">
            <n-affix :trigger-top="95" class="absolute w-1/3 shadow-md ">
                <n-card v-if="usews">
                    <div v-for="m in msgs">
                        <span v-if="m.username !== ''">
                            <span v-text="m.username"
                                @click="router.push({ name: 'user', params: { username: m.username } })"
                                class=" cursor-pointer text-green-700"></span>
                            ->
                            <span v-text="m.path" @click="router.push(m.path)"
                                class=" cursor-pointer text-green-700"></span>
                        </span>
                    </div>
                </n-card>

                <Tags :tags="tags" />
            </n-affix>
        </aside>
    </section>
    <n-back-top :right="40" :bottom="60"/>
    <Footer />
    <!-- <CPU/> -->
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { OpenAPI, Service, UserOut, ApiError, PostOutPage, PostOut, TagInDB } from '@/client'
import Headers from '@/components/header.vue';
import Footer from '@/components/footer.vue';
import Tags from '@/components/tags.vue';
import CPU from '@/components/cpu.vue'
import { NTag, NLayout, NLayoutContent, NCard, NPagination, NAvatar, NEllipsis, NAffix, NBackTop } from 'naive-ui'
import { watchEffect } from 'vue';
import { imgbase, loading } from '@/main';
import { useMessage } from 'naive-ui'
import { useRouter } from 'vue-router';
import { msgs, usews } from '@/main'

document.title = 'undefined'
const message = useMessage()
const userinfo = ref<UserOut>()
const router = useRouter()
const posts = ref<PostOutPage>()
const page = ref(1)
const pagesize = ref(5)
const tags = ref<Array<TagInDB>>()
function getpost(page: number, pagesize: number) {
    Service.getAllPosts(page, pagesize).then((pop: PostOutPage) => {
        posts.value = pop
        loading.value = false
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
    Service.getAllTags().then((t: Array<TagInDB>) => {
        tags.value = t
    })
}
function checkinfo() {
    OpenAPI.TOKEN = localStorage.getItem("token") as string
    let outtime = Math.floor(Date.now() / 1000) - Number(localStorage.getItem('userinfo-time'))
    let localuser = localStorage.getItem('userinfo')
    localStorage.setItem('onlogin', 'false') 
    if (!OpenAPI.TOKEN) {
        message.warning('未登录')
    } else if (outtime > 24 * 60 * 60) {
        localStorage.removeItem('userinfo')
        localStorage.removeItem('token')
        message.error('登录信息过期')
    } else {
        // console.log(outtime);
    }

    if (!localuser && OpenAPI.TOKEN && outtime < 24 * 60 * 60) {
        Service.userinfo().then((u: UserOut) => {
            userinfo.value = u
            localStorage.setItem('userinfo', JSON.stringify(userinfo.value))
            localStorage.setItem('onlogin', 'true')
        }).catch((e: ApiError) => {
            message.error(e.message)
        })
    }
    if (localuser && OpenAPI.TOKEN && outtime < 24 * 60 * 60) {
        userinfo.value = JSON.parse(localuser)
        localStorage.setItem('onlogin', 'true')
    }
}
checkinfo()
// getpost(page.value, pagesize.value)
watchEffect(() => getpost(page.value, pagesize.value))
document.querySelector('#hua>.n-scrollbar-container')?.scrollTo(0, 0);

</script>
<style scoped>
.n-layout-content {
    background-color: transparent;
}
</style>