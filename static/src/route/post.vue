<template>
    <Headers :user="userinfo" :headinfo="{ title: 'home' }" />
    <hr>
    <article class="mx-auto flex max-w-7xl justify-between lg:px-4 mt-20 mb-20" style="min-height: calc(100vh - 170px);">
        <div class="lg:w-2/3 max-lg:w-full" v-if="post !== undefined">
            <p v-text="post?.title" class=" text-2xl flex justify-center m-5"></p>
            <div class=" flex items-center m-3 ml-6 flex-col justify-center">
                <div class=" flex items-center m-2">
                    <n-avatar round size="small" :src="imgbase + post?.author_img" object-fit="cover" />
                    <span v-text="post?.author" class=" pl-2 cursor-pointer"
                        @click="router.push({ name: 'user', params: { username: post?.author } })"></span>
                </div>
                <span class=" text-sm text-gray-500 ">&nbsp;&nbsp; 创建于:{{ post?.created_at.replace('T', ' ') }} |
                    更新于:{{ post?.updated_at.replace('T', ' ') }}</span>
            </div>
            <v-md-preview :text="post?.content"></v-md-preview>
            <p class=" text-xl m-5">评论</p>
            <hr>
            <div class="m-5">
                <n-space vertical>
                    <div v-for="c, index in comlist" class="shadow">
                        <n-card>
                            <span class=" float-right">{{ index + 1 }}楼</span>
                            <n-avatar round size="small" :src="imgbase + c.user_img" object-fit="cover" />
                            <span v-text="c.username" class=" pl-2 cursor-pointer"
                                @click="router.push({ name: 'user', params: { username: c.username } })"></span>
                            <p v-text="c.content" class="ml-5"></p>
                            <n-button @click="replyto = { id: c.id_, L: index + 1 };" class=" float-right"> 回复</n-button>
                            <p v-text="c.created_at.replace('T', ' ')" class=" float-right" style="padding: 7px;"></p>

                            <n-card v-if="c.reply !== null" v-for="r in c.reply">
                                <n-avatar round size="small" :src="imgbase + c.user_img" object-fit="cover" />
                                <span v-text="r.username" class=" pl-2 cursor-pointer"
                                    @click="router.push({ name: 'user', params: { username: r.username } })"></span>
                                <p v-text="r.content" class="ml-5"></p>
                                <p v-text="r.created_at.replace('T', ' ')" class=" float-right"></p>

                            </n-card>
                        </n-card>
                    </div>

                    <div v-show="userinfo !== undefined">
                        <div v-if="replyto.id !== 0">
                            <n-card>
                                <p>回复给:{{ replyto.L }}楼
                                    <n-button class=" float-right" @click="replyto.id = 0">清除</n-button>
                                </p>

                            </n-card>
                        </div>
                        <n-input v-model:value="cominp.content" type="textarea" placeholder="友善发言" class=" shadow" />
                        <n-button class="m-2 float-right" @click="sendcom(replyto.id)"> 发表</n-button>
                    </div>
                    <p v-show="userinfo === undefined">登录以发表评论</p>
                </n-space>
            </div>

        </div>
        <aside class="lg:w-1/3 max-lg:hidden">
            <n-tag type="info" round v-text="t" @click="$router.push({ name: 'tag', params: { name: t } })"
                class="m-2 cursor-pointer" v-for="t in post?.tags">
            </n-tag>
        </aside>
    </article>
    <n-back-top :right="40" />
    <Footer />
</template>
<script setup lang="ts">
import { imgbase, loading } from '@/main';
import Headers from '@/components/header.vue';
import Footer from '@/components/footer.vue';
import { useRoute, useRouter } from 'vue-router';
import { Service, ApiError, PostOut, OpenAPI, UserOut, CommentInput, CommentPostOut } from '@/client/index'
import { useMessage, NAvatar, NCard, NTag, NSpace, NInput, NButton, NBackTop } from 'naive-ui'
import { onMounted, ref } from 'vue';
const message = useMessage()
const route = useRoute()
const router = useRouter()
let pid = Number(route.params.id)
if (Number.isNaN(pid)) {
    location.href = '/'
}
const post = ref<PostOut>()

const userinfo = ref<UserOut>()
const comlist = ref<CommentPostOut[]>()
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
    Service.getPostById(pid).then((po: PostOut) => {
        post.value = po
        document.title = post.value.title
        loading.value = false
    }).catch((e: ApiError) => {
        message.error(e.message)
        if (e.status == 404) {
            router.push({ name: 'notfound' })
        }
    })
    Service.postComm(pid).then((c: CommentPostOut[]) => {
        comlist.value = c
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
})

const cominp = ref<CommentInput>({
    post_id: 0,
    parent_id: 0,
    content: ''
})
const replyto = ref({ id: 0, L: 0 })
function sendcom(pa: number) {
    cominp.value.parent_id = pa
    cominp.value.post_id = pid
    if (cominp.value.content.replaceAll(' ', '') === '') {
        message.warning('空内容')
        return
    }
    if (cominp.value.content.length > 1000) {
        message.warning('最多1000个字')
        return
    }
    Service.newComment(cominp.value).then(() => {
        message.success('发表成功,等待审核')
        cominp.value.content = ''
        Service.postComm(pid).then((c: CommentPostOut[]) => {
            comlist.value = c
        }).catch((e: ApiError) => {
            message.error(e.message)
        })
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
}
document.querySelector('#hua>.n-scrollbar-container')?.scrollTo(0, 0);
</script>