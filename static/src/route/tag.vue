<template>
    <Headers :user="userinfo" :headinfo="{ title: 'Tag:' + $route.params.name }" />
    <section class="mx-auto flex max-w-7xl justify-between lg:px-4 mt-20" style="min-height: calc(100vh - 170px);">
        <div class="lg:w-2/3 max-lg:w-full">
            <n-layout v-if="posts !== undefined && posts.posts[0] !== undefined" style="background-color: transparent;">
                <n-layout-content content-style="padding:15px;background-color: transparent;">
                    <n-card v-for="post in posts.posts" class="mb-5" hoverable bordered>
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
                            <n-tag type="info" round v-for="t in post.tags" @click="" class=" cursor-pointer">
                                <span @click="$router.push({ name: 'tag', params: { name: t } })">{{ t }}</span>
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
            <n-empty v-else description="无相关内容"></n-empty>
        </div>
        <div class="lg:w-1/3 max-lg:hidden">

        </div>
    </section>
    <n-back-top :right="40" :bottom="60"/>
    <Footer />
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { OpenAPI, Service, UserOut, ApiError, PostOut, PostOutPage } from '@/client'
import Headers from '@/components/header.vue';
import Footer from '@/components/footer.vue';
import { NTag, NLayout, NLayoutContent, NCard, NPagination, NAvatar, NEllipsis, NEmpty, NBackTop } from 'naive-ui'
import { watchEffect } from 'vue';
import { imgbase, loading } from '@/main';
import { useMessage } from 'naive-ui'
import { useRoute, useRouter } from 'vue-router';
const message = useMessage()
const userinfo = ref<UserOut>()
const router = useRouter()
const route = useRoute()
const posts = ref<PostOutPage>()
const page = ref(1)
const pagesize = ref(5)
document.title = route.params.name.toString()
onMounted(() => {
    if (localStorage.getItem('onlogin') == 'true') {
        if (!localStorage.getItem('userinfo')) {
            Service.userinfo().then((u: UserOut) => {
                userinfo.value = u
                localStorage.setItem('userinfo', JSON.stringify(userinfo.value))
            }).catch((e: ApiError) => {
                message.error(e.message)
            })
        } else {
            userinfo.value = JSON.parse(localStorage.getItem('userinfo') || '')
        }
    }
    function getpost(page: number, pagesize: number) {
        Service.getPostsByTagPage(route.params.name.toString(), page, pagesize).then((po: PostOutPage) => {
            posts.value = po
            loading.value = false
        }).catch((e: ApiError) => {
            message.error(e.message)
        })
    }
    watchEffect(() => getpost(page.value, pagesize.value))

})
document.querySelector('#hua>.n-scrollbar-container')?.scrollTo(0, 0);

</script>
<style scoped>
.n-layout-content {
    background-color: transparent;
}
</style>