<template>
    <Headers :user="userinfo" :headinfo="{ title: '管理' }" />
    <section v-if="userinfo" class="mx-auto flex max-w-7xl items-center flex-col px-4 top-20 relative">
        <n-tabs ref="tabsInstRef" type="line" animated size="large" justify-content="center" v-model:value="tabnow">
            <n-tab-pane name="setting" tab="设置" display-directive="show:lazy">
                <n-table striped>
                    <tbody>
                        <tr>
                            <td>用户注册 </td>
                            <td><n-switch v-model:value="isr"></n-switch> </td>
                            <td> <button @click="tj1">提交</button></td>
                        </tr>
                        <tr>
                            <td> 接口限制 </td>
                            <td><n-switch v-model:value="isl"></n-switch> </td>
                            <td> <button @click="tj2">提交</button></td>
                        </tr>
                        <tr>
                            <td> 下载excel </td>
                            <td> <button @click="download()">download</button></td>
                        </tr>
                    </tbody>
                </n-table>
            </n-tab-pane>
            <n-tab-pane name="user" tab="用户管理" display-directive="show:lazy">
                <n-table striped>
                    <thead>
                        <th>id</th>
                        <th>username</th>
                        <th>avatar</th>
                        <th>state</th>
                        <th>group_id</th>
                        <th>created_at</th>
                        <th>updated_at</th>
                    </thead>
                    <tbody>
                        <tr v-for="u in alluserinfo">
                            <td v-text="u.id_"></td>
                            <td v-text="u.username"></td>
                            <td>
                                <img class="overflow-hidden object-cover rounded-full" style="width: 40px;height: 40px;"
                                    :src="imgbase + u.avatar">
                            </td>
                            <td v-text="u.state"></td>
                            <td v-text="u.group_id"></td>
                            <td v-text="u.created_at"></td>
                            <td v-text="u.updated_at"></td>
                            <td><button
                                    @click="$router.push({ name: 'user', params: { username: u.username } })">查看</button>
                            </td>
                        </tr>
                    </tbody>
                </n-table>
            </n-tab-pane>
            <n-tab-pane name="api" tab="api访问统计" display-directive="show:lazy">
                <n-table striped>
                    <thead>
                        <th>path <button @click="show_api_count()">刷新</button></th>
                        <th>count</th>
                    </thead>
                    <tbody>
                        <tr v-for="a in api_path_count" :key="a[0]">
                            <td v-text="a[0]"></td>
                            <td v-text="a[1]"></td>
                        </tr>
                    </tbody>
                </n-table>
            </n-tab-pane>
            <n-tab-pane name="ua" tab="UA访问统计" display-directive="show:lazy">
                <n-table striped>
                    <thead>
                        <th>UA <button @click="show_us_count()">刷新</button></th>
                        <th>count</th>
                    </thead>
                    <tbody>
                        <tr v-for="a in ua_count" :key="a[0]">
                            <td v-text="a[0]"></td>
                            <td v-text="a[1]"></td>
                        </tr>
                    </tbody>
                </n-table>
            </n-tab-pane>

        </n-tabs>

        <div style="width: 100%;height: 30vh;"></div>

    </section>
    <!-- <Footer /> -->
</template>
<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { OpenAPI, Service, UserOut, ApiError } from '@/client'
import Headers from '@/components/header.vue';
import CPU from '@/components/cpu.vue';
import { useMessage, NTable, NSwitch, NTabs, NTabPane, TabsInst } from 'naive-ui'
import { imgbase } from '@/main';
import axios from 'axios';
document.title = '管理'
const message = useMessage()
const userinfo = ref<UserOut>()
const api_path_count = ref()
const ua_count = ref()
const show_api_count = () => {
    Service.apiCount().then((res) => {
        api_path_count.value = Object.keys(res).map(function (e) { return [e, res[e]] });
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
}
const show_us_count = () => {
    Service.count().then((res) => {
        ua_count.value = Object.keys(res).map(function (e) { return [e, res[e]] });
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
}

const isr = ref()
const isl = ref()
const alluserinfo = ref<Array<UserOut>>()
const showalluser = () => {
    Service.alluserinfo().then((us: Array<UserOut>) => {
        alluserinfo.value = us
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
}

onMounted(() => {
    OpenAPI.TOKEN = localStorage.getItem("token") as string
    Service.admininfo().then((u: UserOut) => {
        userinfo.value = u
        showalluser()
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
    Service.isAllowRegister().then((b: boolean) => {
        isr.value = b
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
    Service.isLimiter().then((b: boolean) => {
        isl.value = b
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
})

const tj1 = () => {
    Service.allowRegister(isr.value).then((b: boolean) => {
        message.success(b + '允许注册=' + isr.value)
        location.reload()
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
}
const tj2 = () => {
    Service.setLimiter(isl.value).then((b: boolean) => {
        message.success(b + '限制=' + isl.value)
        location.reload()
    }).catch((e: ApiError) => {
        message.error(e.message)
    })
}

const tabsInstRef = ref<TabsInst>()
const tabnow = ref('')
setTimeout(() => {
    let prx = location.hash.toString().replace("#", "")
    if (prx == 'setting' || prx == 'user' || prx == 'api') {
        tabnow.value = prx
    } else {
        tabnow.value = 'setting'
    }
}, 500);
watch(tabnow, (newv) => {
    location.hash = newv
    if (newv === 'api' && !api_path_count.value) {
        show_api_count()
    }
    if (newv === 'ua' && !ua_count.value) {
        show_us_count()
    }
    document.querySelector('#hua>.n-scrollbar-container')?.scrollTo(0, 0);
})
function download() {
    axios({
        url: OpenAPI.BASE + '/api/other/download_excel',
        method: 'get',
        responseType: 'blob',
        headers: { 'Authorization': `Bearer ${OpenAPI.TOKEN}` }
    }).then((res) => { 
        const fileName = res.headers["content-disposition"]?.split(';')[1]?.split('filename=')[1];
        const filestream = res.data;
        const blob = new Blob([filestream], { type:  res.headers['content-type']?.toString()});
        const a = document.createElement('a');
        const href = window.URL.createObjectURL(blob);
        a.href = href;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(href);
    })
}
</script>

<style>
.n-tabs-nav--line-type.n-tabs-nav--top.n-tabs-nav {
    position: sticky;
    top: 56px;
    z-index: 9;
    background-color: var(--bg-a);
}
</style>