<template>
    <Headers :user="myself" :headinfo="isme ? { title: '个人中心' } : { title: '用户:' + route.params.username.toString() }"
        @me="isme = true; needshow = myself" />
    <section class="mx-auto flex max-w-7xl justify-between lg:px-4 relative mb-20"
        style="top:56px;min-height: calc(100vh - 100px);">
        <n-tabs ref="tabsInstRef" type="line" animated size="large" justify-content="center" v-model:value="tabnow"
            class="mt-3">
            <n-tab-pane name="self" :tab="isme ? '我的' : '用户:' + route.params.username.toString()"
                display-directive="show:lazy" class=" flex justify-center">
                <div class=" w-96">
                    <n-card hoverable :title="needshow?.username">
                        <template #cover>
                            <n-image :src="imgbase + needshow?.avatar" object-fit="cover" class="w-full"
                                style="max-height: 200px;" />
                        </template>
                        <p>uid: {{ needshow?.id_ }}</p>
                        <template #footer>
                            <p>创建于: {{ needshow?.created_at.replace('T', ' ') }}</p>
                            <p>最后更新于: {{ needshow?.updated_at.replace('T', ' ') }}</p>
                        </template>
                        <template #action>
                            <n-alert v-if="needshow?.group_id == 0" title="账号状态" type="success">普通用户
                            </n-alert>
                            <n-alert v-if="needshow?.group_id == 1" title="账号状态" type="info">管理员
                            </n-alert>
                            <n-alert v-if="needshow?.group_id == 2" title="账号状态" type="warning">审核中
                            </n-alert>
                            <n-alert v-if="needshow?.group_id == 3" title="账号状态" type="error">封禁
                            </n-alert>
                        </template>


                    </n-card>
                </div>
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

                                <div class=" cursor-pointer w-6 opacity-70 mx-2 hover:text-green-600" v-if="isme"
                                    @click="gotoedit(post.id_)">
                                    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                                        viewBox="0 0 32 32">
                                        <path d="M2 26h28v2H2z" fill="currentColor"></path>
                                        <path
                                            d="M25.4 9c.8-.8.8-2 0-2.8l-3.6-3.6c-.8-.8-2-.8-2.8 0l-15 15V24h6.4l15-15zm-5-5L24 7.6l-3 3L17.4 7l3-3zM6 22v-3.6l10-10l3.6 3.6l-10 10H6z"
                                            fill="currentColor"></path>
                                    </svg>
                                </div>
                                <div class=" cursor-pointer w-6 opacity-70 mx-2 hover:text-red-600" v-if="isme"
                                    @click="delpost(post.id_, getpost)">
                                    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                                        viewBox="0 0 28 28">
                                        <g fill="none">
                                            <path
                                                d="M14 2.25a3.75 3.75 0 0 1 3.745 3.55l.005.2h5.5a.75.75 0 0 1 .102 1.493l-.102.007h-1.059l-1.22 15.053A3.75 3.75 0 0 1 17.233 26h-6.466a3.75 3.75 0 0 1-3.738-3.447L5.808 7.5H4.75a.75.75 0 0 1-.743-.648L4 6.75a.75.75 0 0 1 .648-.743L4.75 6h5.5A3.75 3.75 0 0 1 14 2.25zm6.687 5.25H7.313l1.211 14.932a2.25 2.25 0 0 0 2.243 2.068h6.466a2.25 2.25 0 0 0 2.243-2.068L20.686 7.5zm-8.937 3.75a.75.75 0 0 1 .743.648L12.5 12v8a.75.75 0 0 1-1.493.102L11 20v-8a.75.75 0 0 1 .75-.75zm4.5 0a.75.75 0 0 1 .743.648L17 12v8a.75.75 0 0 1-1.493.102L15.5 20v-8a.75.75 0 0 1 .75-.75zM14 3.75a2.25 2.25 0 0 0-2.245 2.096L11.75 6h4.5l-.005-.154A2.25 2.25 0 0 0 14 3.75z"
                                                fill="currentColor"></path>
                                        </g>
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
                            <p class=" text-green-500">{{ c.state == 0 ? '审核中' : '' }}</p>
                            <n-button class=" float-right" v-if="isme" tertiary type="error"
                                @click="delcomm(c.id_, getcom)">删除</n-button>
                            <n-button class=" float-right" v-if="c.state == 0" tertiary type="primary"
                                @click="setcomm(c.id_, true)">通过</n-button>
                            <n-button class=" float-right" v-if="c.state == 1" tertiary type="error"
                                @click="setcomm(c.id_, false)">标记为未审核</n-button>
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
            <n-tab-pane name="mycomm" :tab="isme ? '我的评论' : 'TA的评论'" display-directive="show:lazy">
                <n-button strong secondary circle type="primary" @click="getmycom()">
                    更新
                </n-button>
                <n-space vertical>
                    <div v-for="c in mycomlist">
                        <n-card>
                            <p>{{ c.id_ }}</p>
                            <p class=" text-green-500">{{ c.state == 0 ? '审核中' : '' }}</p>
                            <n-button class=" float-right" v-if="isme" tertiary type="error"
                                @click="delcomm(c.id_, getmycom)">删除</n-button>
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
            <n-tab-pane v-if="isme" name="setting" tab="设置" display-directive="show:lazy" class=" overflow-auto">
                <n-table :striped="true" :single-line="false" class=" min-w-max">
                    <tr>
                        <td>修改密码</td>
                        <td>
                            <n-button @click="showModal = true">
                                go
                            </n-button>
                        </td>
                        <td>
                            <n-modal v-model:show="showModal" :closable="true">
                                <n-card style="width: 600px" title="密码修改" :bordered="false" size="huge" role="dialog"
                                    aria-modal="true">
                                    <n-space vertical>
                                        <p>最少8位!</p>
                                        <n-input placeholder="原密码" v-model:value="changpeass.oldp"></n-input>
                                        <n-input placeholder="新密码" v-model:value="changpeass.newp" minlength="8"></n-input>
                                        <n-input placeholder="重复密码" v-model:value="changpeass.newp2" minlength="8"></n-input>
                                    </n-space>
                                    <template #footer>
                                        <n-button @click="changepasswd()" class=" float-right">
                                            提交
                                        </n-button>
                                    </template>
                                </n-card>
                            </n-modal>
                        </td>
                    </tr>
                    <tr>
                        <td>修改头像</td>
                        <td>
                            <input ref="file" type="file" name="" @change="onChange()" accept="image/jpeg,image/png" />
                        </td>
                        <td>

                            <n-image :src="crbo" style="max-width: 200px;" alt=""
                                @load="message.success('图片处理完成,压缩' + Math.floor((1 - bfaf[1] / bfaf[0]) * 10000) / 100 + '%')" /><br>
                            <div v-if="bfaf[0]">
                                原图: {{ bfaf[0] }}kb <br>
                                压缩后:{{ bfaf[1] }}kb<br>
                                质量:{{ bfaf[2] }}
                            </div>
                            <p v-else>压缩大于100kb的图片,尽量是正方形</p>

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

    </section>
    <Footer />
</template>
<script setup lang="ts">
import { ref, onMounted, watchEffect, watch } from 'vue'
import Tags from '@/components/tags.vue';
import Footer from '@/components/footer.vue';
import { useRouter, useRoute } from 'vue-router'
import {
    NAlert, NInputNumber, NTag, NLayout, NLayoutContent, useDialog, NModal, NInput,
    NCard, NPagination, NEmpty, NTabs, NTabPane, NEllipsis, NAvatar, NSpace, NButton, NImage, NTable, TabsInst
} from 'naive-ui'
import { OpenAPI, Service, UserOut, ApiError, PostOut, PostOutPage, TagInDB, CommentUserOut, UpdateSuccess } from '@/client'
import Headers from '@/components/header.vue';
import newpost from '@/components/new_post.vue';
import { imgbase } from '@/main'
import { useMessage } from 'naive-ui'

const message = useMessage()
const router = useRouter()
const route = useRoute()
const userinfo = ref<UserOut>()
const myself = ref<UserOut>()
const needshow = ref<UserOut>()

const isme = ref(false)
const tags = ref<Array<TagInDB>>()

const file = ref()
const resbin = ref()
const crbo = ref()
const bfaf = ref([NaN, NaN, 1])

const page = ref(1)
const pagesize = ref(5)
const posts = ref<PostOutPage>()

const showModal = ref(false)
const changpeass = ref({
    oldp: '',
    newp: '',
    newp2: '',
})
function changepasswd() {
    if (changpeass.value.oldp && changpeass.value.newp && changpeass.value.newp2) {
        if (changpeass.value.newp !== changpeass.value.newp2) {
            message.error('密码不一致')
            return
        }
        if (changpeass.value.newp.length<8) {
            message.error('8位以上')
            return
        }
        Service.updatePassword(changpeass.value.oldp, changpeass.value.newp).then((v: UpdateSuccess) => {
            message.success(v.data.username + ', ' + v.detail)
            showModal.value = false
            changpeass.value.oldp = changpeass.value.newp = changpeass.value.newp2 = ''
            localStorage.removeItem('token')
            localStorage.removeItem('userinfo')
            localStorage.removeItem('onlogin')
            location.reload()
        }).catch((e: ApiError) => {
            message.error(e.message + JSON.stringify(e.body.detail),{duration:8000})
        })
    } else {
        message.warning('空')
    }
}
function getpost(page: number, pagesize: number) {
    Service.getUsersPosts(route.params.username as string, page, pagesize).then((po: PostOutPage) => {
        posts.value = po
    }).catch((e: ApiError) => {
        message.error(e.message + e.body.detail)
    })
}
const gotoedit = (id: number) => {
    router.replace({ hash: "#new", query: { 'pid': id } });
    setTimeout(() => {
        tabnow.value = 'new'
    }, 100);
}
watch(page, () => getpost(page.value, pagesize.value))
watch(pagesize, () => getpost(page.value, pagesize.value))

OpenAPI.TOKEN = localStorage.getItem("token") as string
if (localStorage.getItem("userinfo") !== null && OpenAPI.TOKEN !== undefined) {
    myself.value = JSON.parse(localStorage.getItem("userinfo") || '')
}
// else {
//     message.warning('未登录')
// }

if (myself.value?.username == route.params.username) {
    isme.value = true
    needshow.value = myself.value
    getpost(page.value, pagesize.value)
    gettags()
    getmycom()
} else {
    Service.publishUserInfo(route.params.username as string).then((up: UserOut) => {
        userinfo.value = up
        needshow.value = userinfo.value
        getpost(page.value, pagesize.value)
        gettags()
        getmycom()
    }).catch((e: ApiError) => {
        message.error(e.message + e.body.detail)
        router.push({ name: 'notfound' })
    })
}

document.title = needshow.value?.username || '用户'

function gettags() {
    Service.getUserAllTags((needshow.value as UserOut).username).then((t: Array<TagInDB>) => {
        tags.value = t
    })
}
const comlist = ref<CommentUserOut[]>()
function getcom() {
    if (needshow.value !== undefined) {
        Service.commToUser(needshow.value.username).then((c: CommentUserOut[]) => {
            comlist.value = c
        })
    }
}

const mycomlist = ref<CommentUserOut[]>()
function getmycom() {
    if (needshow.value !== undefined) {
        Service.userComm(needshow.value.username).then((c: CommentUserOut[]) => {
            mycomlist.value = c
        })
    }
}

const setcomm = (cid: number, passed: boolean) => {
    Service.reviewCcomm(cid, passed).then(() => {
        message.success(passed ? '修改为通过' : '修改为未审核')
        getcom()
    }).catch((e: ApiError) => {
        message.error('修改失败--' + e.message + e.body.detail)
    })
}
const dialog = useDialog()
const delcomm = (cid: number, success: Function) => {
    dialog.warning({
        title: '确认删除',
        content: '删除后无法恢复',
        negativeText: '确定',
        onNegativeClick: () => {
            Service.delComments(cid).then(() => {
                message.success('删除成功')
                success()
            }).catch((e: ApiError) => {
                message.error('删除失败--' + e.message + e.body.detail)
            })
        },
        onMaskClick: () => {
            message.info('取消删除')
        }
    })
}
const delpost = (pid: number, success: Function) => {
    dialog.warning({
        title: '确认删除',
        content: '删除后无法恢复',
        negativeText: '确定',
        onNegativeClick: () => {
            Service.deletePost(pid).then(() => {
                message.success('删除成功')
                success()
            }).catch((e: ApiError) => {
                message.error('删除失败--' + e.message + e.body.detail)
            })
        },
        onMaskClick: () => {
            message.info('取消删除')
        }
    })
}

const upl = () => {
    if (file.value.value && resbin.value) {
        Service.updateAvatar({ 'avatar_new': resbin.value }).then((up) => {
            message.success(up.detail)
            Service.userinfo().then((u: UserOut) => {
                localStorage.setItem('userinfo', JSON.stringify(u))
                location.reload()
            })
        }).catch((e: ApiError) => {
            message.error(e.message + e.body.detail)
        })
    } else {
        message.warning('请选择文件')
    }

}
const onChange = () => {
    bfaf.value = []
    if (file.value.value !== '') {
        message.info('图片处理中')
        let f = file.value.files[0]
        const type = f.type
        if (type === "image/jpeg" || type === "image/png") {
            const reader = new FileReader();
            reader.readAsDataURL(f)
            reader.onload = (e) => {
                try {
                    var img = new Image()
                    //@ts-ignore
                    img.src = e.target?.result
                    var canvas = document.createElement('canvas')
                    var ctx = canvas.getContext('2d') as CanvasRenderingContext2D;
                    img.onload = () => {
                        var width = img.width;
                        var height = img.height;
                        canvas.width = width;
                        canvas.height = height;
                        ctx.drawImage(img, 0, 0, width, height);
                        var quality = 1
                        if (f.size > 1024 * 1024 * 20) {
                            delimg()
                            message.warning('图片大于20mb!!!,')
                            return
                        }
                        if (f.size > 102400) {
                            quality = Math.floor(102400 / f.size * 10000) / 10000
                        }
                        if (f.size <= 102400) {
                            crbo.value = img.src
                            resbin.value = f
                            bfaf.value.push(Math.floor(f.size / 1024), Math.floor(f.size / 1024), quality)
                            return
                        }
                        if (quality <= 0.1) { quality = 0.1 }
                        let resultBlob: Blob = new Blob();
                        canvas.toBlob(function (blob) {
                            resultBlob = blob as Blob;
                            bfaf.value.push(Math.floor(f.size / 1024), Math.floor(resultBlob.size / 1024), quality)
                            const blobUrl = URL.createObjectURL(resultBlob)
                            crbo.value = blobUrl
                            resbin.value = new window.File([resultBlob], f.name)

                        }, 'image/jpeg', quality);
                    }
                } catch (e) {
                    console.error(e)
                }
            }
        } else {
            message.warning('仅支持jpg/png')
            delimg()
        }

    } else {
        message.warning('取消选择')
    }
}
const delimg = () => {
    bfaf.value = []
    resbin.value = ''
    file.value.value = ''
    crbo.value = ''
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
    location.reload()
}
const tabsInstRef = ref<TabsInst>()
const tabnow = ref('')
setTimeout(() => {
    let prx = location.hash.replace("#", "")
    if (prx == 'self' || prx == 'post' || prx == 'tags' || prx == 'new' || prx == 'comm' || prx == 'mycomm' || prx == 'setting') {
        tabnow.value = prx
    } else {
        tabnow.value = 'self'
    }
    if (!isme.value || localStorage.getItem('onlogin') == 'false') {
        tabnow.value = 'self'
    }
}, 500);
watch(tabnow, (newv) => {
    router.push({ hash: '#' + newv, query: route.query })
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
    background-color: var(--bg-a);
}
</style>