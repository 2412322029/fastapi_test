<template>
    <router-link :to="{ name: 'home' }">
        <Headers :user="userinfo" :headinfo="{ title: 'home' }" />
    </router-link>
    <div class="mx-auto flex max-w-7xl justify-between lg:px-4 top-20 relative">
        <div class="lg:w-2/3 max-lg:w-full">
            <n-layout>
                <n-layout-content content-style="padding:15px;">
                    <n-card :title="post.title" class=" rounded-xl mb-6" v-for="post in posts?.posts" hoverable bordered>
                        <div v-text="post.content" @click="" class=" cursor-pointer">
                        </div>
                        <template #header-extra>
                            <div class=" cursor-pointer flex justify-between items-center">
                                <n-avatar round size="small" :src="imgbase + post.author_img" />
                                <span v-text="post.author" class=" pl-2"></span>
                            </div>
                        </template>
                        <template #footer>
                            <n-tag type="info" round v-for="t in post.tags" v-text="t" @click="" class=" cursor-pointer">
                            </n-tag>
                        </template>
                        <template #action>
                            <div class=" float-right">
                                <n-ellipsis style="max-width: 220px">
                                    created at:{{ post.created_at.replace('T', ' ') }}
                                    | updated at:{{ post.updated_at.replace('T', ' ') }}
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
        <div class="lg:w-1/3 max-lg:hidden">
            <n-affix :trigger-top="100" :trigger-bottom="100" class=" absolute">
                <Tags :tags="tags" />
            </n-affix>
        </div>
    </div>
    <Footer />
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { OpenAPI, Service, UserOut, ApiError, PostOutPage, PostOut, TagInDB } from '@/client'
import cogoToast from 'cogo-toast';
import Headers from '@/components/header.vue';
import Footer from '@/components/footer.vue';
import Tags from '@/components/tags.vue';
import { NTag, NLayout, NLayoutContent, NCard, NPagination, NAvatar, NEllipsis, NAffix } from 'naive-ui'
import { watchEffect } from 'vue';
import { imgbase } from '@/main';
const userinfo = ref<UserOut>()

const posts = ref<PostOutPage>()
const page = ref(1)
const pagesize = ref(5)
const tags = ref<Array<TagInDB>>()
function getpost(page: number, pagesize: number) {
    Service.getAllPosts(page, pagesize).then((pop: PostOutPage) => {
        posts.value = pop
    }).catch((e: ApiError) => {
        cogoToast.error(e.message)
    })
    Service.getAllTags().then((t: Array<TagInDB>) => {
        tags.value = t
    })
}
watchEffect(() => getpost(page.value, pagesize.value))
onMounted(() => {
    OpenAPI.TOKEN = localStorage.getItem("token") as string
    Service.userinfo().then((u: UserOut) => {
        userinfo.value = u
    }).catch((e: ApiError) => {
        cogoToast.error(e.message)
    })

})


</script>