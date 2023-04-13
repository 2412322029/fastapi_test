<template>
    <Headers v-if="!isme" :user="myself" :headinfo="{ title: '用户:' + route.params.username.toString() }" />
    <Headers v-if="isme" :user="userinfo" :headinfo="{ title: '个人中心' }" />
    <div class="mx-auto flex max-w-7xl items-center justify-between px-4 relative" style="top:56px">
        <n-tabs type="line" animated size="large">
            <n-tab-pane name="post" tab="文章">
                <n-layout v-if="posts?.total != 0">
                    <n-layout-content content-style="padding:15px;">
                        <n-card :title="post.title" class=" rounded-xl mb-6" v-for="post in posts?.posts" hoverable
                            bordered>
                            <div v-text="post.content" @click="" class=" cursor-pointer">
                            </div>
                            <template #header-extra>
                                <div class=" cursor-pointer w-6 opacity-70" v-if="isme">
                                    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                                        viewBox="0 0 32 32">
                                        <path d="M2 26h28v2H2z" fill="currentColor"></path>
                                        <path
                                            d="M25.4 9c.8-.8.8-2 0-2.8l-3.6-3.6c-.8-.8-2-.8-2.8 0l-15 15V24h6.4l15-15zm-5-5L24 7.6l-3 3L17.4 7l3-3zM6 22v-3.6l10-10l3.6 3.6l-10 10H6z"
                                            fill="currentColor"></path>
                                    </svg>
                                </div>
                                <div v-else class=" cursor-pointer flex justify-between items-center">
                                    <n-avatar round size="small" :src="imgbase + post.author_img" />
                                    <span v-text="post.author" class=" pl-2"></span>
                                </div>
                            </template>
                            <template #footer>
                                <n-tag type="info" round v-for="t in post.tags" v-text="t" @click=""
                                    class=" cursor-pointer">
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
                    <n-pagination v-model:page="page" :page-count="Math.ceil(posts?.total as number / pagesize)"
                        :page-slot="5" size="large" :page-sizes="[5, 10]" v-model:page-size="pagesize" show-size-picker
                        class=" flex justify-center" />
                </n-layout>
                <n-empty v-else description="没有文章"></n-empty>
            </n-tab-pane>
            <n-tab-pane name="tags" tab="tags" display-directive="show:lazy">
                <Tags v-if="tags?.length !== 0" :tags="tags" />
                <n-empty v-else description="没有tag"></n-empty>
            </n-tab-pane>
            <n-tab-pane v-if="isme" name="new" tab="写文章" display-directive="show:lazy">
                <newpost />
            </n-tab-pane>
            <n-tab-pane v-if="isme" name="setting" tab="设置" display-directive="show:lazy">
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
            </n-tab-pane>

        </n-tabs>

    </div>
    <Footer />
</template>
<script setup lang="ts">
import { ref, onMounted, watchEffect } from 'vue'
import Tags from '@/components/tags.vue';
import Footer from '@/components/footer.vue';
import { useRouter, useRoute } from 'vue-router'
import { NTag, NLayout, NLayoutContent, NCard, NPagination, NEmpty, NTabs, NTabPane, NEllipsis, NAvatar } from 'naive-ui'
import { OpenAPI, Service, UserOut, ApiError, PubUserInfo, PostOut, PostOutPage, TagInDB } from '@/client'
import cogoToast from 'cogo-toast';
import Headers from '@/components/header.vue';
import newpost from '@/components/new_post.vue';
import { imgbase } from '@/main'
const router = useRouter()
const route = useRoute()
const userinfo = ref<UserOut>()
const myself = ref<UserOut>()
const pubuserinfo = ref<PubUserInfo>()
const isme = ref(false)
const tags = ref<Array<TagInDB>>()
const file = ref()
const fileblob = ref()
const base64 = ref()
const page = ref(1)
const pagesize = ref(5)
const posts = ref<PostOutPage>()
function getpost(page: number, pagesize: number) {
    Service.getUsersPosts(route.params.username as string, page, pagesize).then((po: PostOutPage) => {
        posts.value = po
    }).catch((e: ApiError) => {
        cogoToast.error(e.message + e.body.detail)
    })
}
watchEffect(() => getpost(page.value, pagesize.value))
onMounted(() => {
    OpenAPI.TOKEN = localStorage.getItem("token") as string
    OpenAPI.USERNAME = localStorage.getItem("username") as string
    if (OpenAPI.USERNAME == route.params.username) {
        Service.userinfo().then((u: UserOut) => {
            userinfo.value = u
            isme.value = true
            gettags(userinfo.value.username)
        })
    } else {
        Service.publishUserInfo(route.params.username as string).then((up: PubUserInfo) => {
            pubuserinfo.value = up
            gettags(pubuserinfo.value.username)
        }).catch((e: ApiError) => {
            cogoToast.error(e.message + e.body.detail)
            router.push({ name: 'notfound' })
        })
        if (localStorage.getItem("token")) {
            OpenAPI.TOKEN = localStorage.getItem("token") as string
            Service.userinfo().then((u: UserOut) => {
                myself.value = u
            }).catch((e: ApiError) => {
                cogoToast.error(e.message)
            })
        }

    }
})
function gettags(name: string) {
    Service.getUserAllTags(name).then((t: Array<TagInDB>) => {
        tags.value = t
    })
}

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
<style>
.n-tabs-nav--line-type.n-tabs-nav--top.n-tabs-nav {
    position: sticky;
    top: 56px;
    z-index: 1;
    background-color: white;
}
</style>