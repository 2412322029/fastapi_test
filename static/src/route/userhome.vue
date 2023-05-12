<template>
    <Headers :user="userinfo" :headinfo="isme ? { title: '个人中心' } : { title: '用户:' + route.params.username.toString() }"
        @me="isme = true" />
    <div class="mx-auto flex max-w-7xl justify-between px-4 relative mb-20"
        style="top:56px;min-height: calc(100vh - 100px);">
        <n-tabs ref="tabsInstRef" type="line" animated size="large" justify-content="center" v-model:value="tabnow"
            class="mt-3">
            <n-tab-pane name="self" :tab="isme ? '我的' : '用户:' + route.params.username.toString()"
                display-directive="show:lazy" @vnode-mounted="getcom()">
                <div v-if="isme">{{ userinfo }}</div>
                <div v-else>{{ pubuserinfo }}</div>
            </n-tab-pane>
            <n-tab-pane name="post" tab="文章" display-directive="show:lazy">
                <n-layout v-if="posts?.total !== 0 && posts !== undefined" style="background-color: transparent;">
                    <n-layout-content content-style="padding:15px;background-color: transparent;">
                        <n-card :title="post.title || '无标题'" class=" rounded-xl mb-6 shadow" v-for="post in posts?.posts"
                            hoverable bordered>
                            <template #header>
                                <p v-text="post.title || '无标题'" class=" rounded-xl mb-6 cursor-pointer hover:opacity-70"
                                    @click="router.push({ name: 'post', params: { id: post.id_ } })"></p>
                            </template>
                            <div v-text="post.content || '无内容'" @click="">
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
                                <n-tag type="info" round v-for="t in post.tags" @click=""
                                    class=" cursor-pointer hover:shadow">
                                    <span @click="$router.push('tag/' + t)">{{ t }}</span>
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
            <n-tab-pane name="tags" tab="标签" display-directive="show:lazy">
                <Tags v-if="tags?.length !== 0" :tags="tags" />
                <n-empty v-else description="没有tag"></n-empty>
            </n-tab-pane>
            <n-tab-pane v-if="isme" name="new" tab="写文章" display-directive="show:lazy">
                <newpost />
            </n-tab-pane>
            <n-tab-pane v-if="isme" name="comm" tab="评论审核" display-directive="show:lazy" @vnode-mounted="getcom()">
                <n-button strong secondary circle type="primary" @click="getcom()">
                    更新
                </n-button>
                <n-space vertical>
                    <div v-for="c in comlist">
                        <n-card>
                            <p>{{ c.id_ }}</p>
                            <n-avatar round size="small" :src="imgbase + c.user_img" object-fit="cover" />
                            <span v-text="c.username" class=" pl-2 cursor-pointer"
                                @click="router.push({ name: 'user', params: { username: c.username } })"></span>
                            <p v-text="c.content" class="ml-5"></p>
                            <p @click="router.push('/p/' + c.post_id)" class="ml-5 float-right cursor-pointer">详情</p>
                            <p v-text="c.created_at.replace('T', ' ')" class=" float-right"></p>
                        </n-card>
                    </div>
                </n-space>
            </n-tab-pane>
            <n-tab-pane name="mycomm" :tab="isme ? '我的评论' : 'TA的评论'" display-directive="show:lazy"
                @vnode-mounted="getcom()">
                xx
            </n-tab-pane>
            <n-tab-pane v-if="isme" name="setting" tab="设置" display-directive="show:lazy">
                <n-table :striped="true" :single-line="false">
                    <tr>
                        <td>修改头像</td>
                        <td>
                            <input ref="file" type="file" name="" @change="onChange()"
                                accept="image/jpeg,image/png,image/gif" />
                        </td>
                        <td>
                            <n-image :src="base64" width="100" alt="" />
                        </td>
                        <td>
                            <button @click="delimg()">取消</button>
                        </td>
                        <td>
                            <button @click="upl()">提交</button>
                        </td>
                    </tr>
                    <tr>
                        <td>背景点击次数</td>
                        <td>(点击多少次切换)</td>
                        <td>
                            <n-input-number v-model:value="times" :min="1" :max="10">
                                <template #suffix>
                                    次
                                </template>
                            </n-input-number>
                        </td>
                        <td>
                            <button @click="times = 5">恢复默认</button>
                        </td>
                        <td>
                            <button @click="rib()">提交</button>
                        </td>
                    </tr>
                </n-table>
            </n-tab-pane>

        </n-tabs>

    </div>
    <Footer />
</template>
<script setup lang="ts">
import { ref, onMounted, watchEffect, watch } from 'vue'
import Tags from '@/components/tags.vue';
import Footer from '@/components/footer.vue';
import { useRouter, useRoute } from 'vue-router'
import { NDivider, NInputNumber, NTag, NLayout, NLayoutContent, NCard, NPagination, NEmpty, NTabs, NTabPane, NEllipsis, NAvatar, NSpace, NButton, NImage, NTable, TabsInst } from 'naive-ui'
import { OpenAPI, Service, UserOut, ApiError, PubUserInfo, PostOut, PostOutPage, TagInDB, CommentUserOut } from '@/client'
import Headers from '@/components/header.vue';
import newpost from '@/components/new_post.vue';
import { imgbase } from '@/main'
import { useMessage } from 'naive-ui'
const message = useMessage()
const router = useRouter()
const route = useRoute()
const userinfo = ref<UserOut>()
const pubuserinfo = ref<PubUserInfo>()
const isme = ref(false)
const tags = ref<Array<TagInDB>>()

const file = ref()
const base64 = ref()

const page = ref(1)
const pagesize = ref(5)
const posts = ref<PostOutPage>()
function getpost(page: number, pagesize: number) {
    Service.getUsersPosts(route.params.username as string, page, pagesize).then((po: PostOutPage) => {
        posts.value = po
    }).catch((e: ApiError) => {
        message.error(e.message + e.body.detail)
    })
}

watchEffect(() => getpost(page.value, pagesize.value))
onMounted(() => {
    OpenAPI.TOKEN = localStorage.getItem("token") as string
    if (localStorage.getItem("userinfo") !== null) {
        OpenAPI.USERNAME = JSON.parse(localStorage.getItem("userinfo") || '').username
    }
    if (OpenAPI.USERNAME == route.params.username) {
        isme.value = true
    } else {
        Service.publishUserInfo(route.params.username as string).then((up: PubUserInfo) => {
            pubuserinfo.value = up
            gettags(pubuserinfo.value.username)
        }).catch((e: ApiError) => {
            message.error(e.message + e.body.detail)
            router.push({ name: 'notfound' })
        })
    }
    if (localStorage.getItem("token")) {
        Service.userinfo().then((u: UserOut) => {
            userinfo.value = u
            gettags(userinfo.value.username)

        }).catch((e: ApiError) => {
            message.error(e.message)
            localStorage.removeItem('userinfo')
            localStorage.removeItem('token')
        })
    }
})
function gettags(name: string) {
    Service.getUserAllTags(name).then((t: Array<TagInDB>) => {
        tags.value = t
    })
}
const comlist = ref<CommentUserOut[]>()
function getcom() {
    if (userinfo.value !== undefined) {
        Service.commToUser(userinfo.value.username).then((c: CommentUserOut[]) => {
            comlist.value = c
        })
    }
}

const upl = () => {
    if (file.value.value) {
        Service.updateAvatar({ 'avatar_new': file.value.files[0] }).then((up) => {
            message.success(up.detail)
        }).catch((e: ApiError) => {
            message.error(e.message + e.body.detail)
        })
    } else {
        message.warning('请选择文件')
    }

}
const onChange = () => {
    if (file.value.value !== '') {
        let f = file.value.files[0]
        const type = f.type
        if (type === "image/jpeg" || type === "image/png" || type === 'image/gif') {
            const reader = new FileReader();
            reader.readAsDataURL(f)
            reader.onload = (e) => {
                try {
                    //@ts-ignore
                    base64.value = e.target.result
                } catch (e) {
                }
            }
        } else {
            message.warning('仅支持jpg/png/gif')
            delimg()
        }

    } else {
        message.warning('取消选择')
    }
}
const delimg = () => {
    file.value.value = ''
    base64.value = ''
}
let times = ref(5)
{
    let t = localStorage.getItem('ribbon-times')
    if (t && Number.isInteger(Number(t))) {
        times.value = Number(t)
    } else {
        times.value = 5
    }
}


const rib = () => {
    localStorage.setItem('ribbon-times', times.value.toString())
    router.push({ name: 'home' })
}
const tabsInstRef = ref<TabsInst>()
const tabnow = ref('')
setTimeout(() => {
    let prx = location.hash.toString().replace("#", "")
    if (prx == 'self' || prx == 'post' || prx == 'tags' || prx == 'new' || prx == 'comm' || prx == 'mycomm' || prx == 'setting') {
        tabnow.value = prx
    } else {
        tabnow.value = 'self'
    }
}, 500);
watch(tabnow, (newv) => {
    location.hash = newv
    document.querySelector('#hua>.n-scrollbar-container')?.scrollTo(0, 0);
})

</script>

<style scoped>
.n-layout-content {
    background-color: transparent;
}
</style>
<style>
.n-tabs-nav--line-type.n-tabs-nav--top.n-tabs-nav {
    position: sticky;
    top: 56px;
    z-index: 9;
    background-color: white;
}
</style>