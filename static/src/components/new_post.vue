<template>
    <div style="top:56px;min-height: calc(100vh - 100px);">
        <n-collapse :default-expanded-names="['1']" class="m-3">
            <n-collapse-item title="标题和标签" name="1">
                <template #header-extra v-if="!Number.isNaN(route.query.pid) && uppost">
                    作者:{{ uppost?.author }}|{{ uppost?.created_at.replace('T', ' ') }}->{{
                        uppost?.updated_at.replace('T', ' ') }}
                </template>
                <n-input type="text" v-model:value="title" placeholder="标题" class=" mb-1" />
                <div v-if="!Number.isNaN(route.query.pid) && uppost == undefined">
                    <n-h4>已有标签(点击添加)<n-button @click="tag_names.length = 0">清除所有</n-button></n-h4>
                    <n-tag type="info" v-for="t in tags" round v-text="t.name" @click="selecttag(t.name)"
                        class="m-2 cursor-pointer">
                    </n-tag>
                    <n-dynamic-tags type="success" v-model:value.trim="tag_names" @create="handleCreate" :max="5" />
                </div>

                <n-divider />
            </n-collapse-item>
        </n-collapse>
        <v-md-editor v-model="content" height="600px" class=" m-1" @save="saveaction()"></v-md-editor>

    </div>
</template>
<script setup lang="ts">
import { ref, onMounted, watch, watchEffect } from 'vue'
import { OpenAPI, Service, UserOut, ApiError, PostIn, TagInDB, PostOut } from '@/client'
import { useRouter, useRoute } from 'vue-router';
import { NDynamicTags, NInput, NButton, NDivider, NH4, NTag, NCollapse, NCollapseItem } from 'naive-ui'
import { useMessage } from 'naive-ui'
import { onUpdated } from 'vue';
const message = useMessage()
const router = useRouter()
const route = useRoute()

const title = ref('')
const content = ref('')
const tag_names = ref<Array<string>>([])
const uppost = ref<PostOut>()
const getpost = (pi:number) => {
    if (!Number.isNaN(pi)) {
        Service.getPostById(pi).then((p: PostOut) => {
            message.success('文章获取成功')
            uppost.value = p
            title.value = p.title
            content.value = p.content
            tag_names.value = p.tags
        }).catch((e: ApiError) => {
            message.error(e.message + e.body.detail)
        })
    }
}

watch(
    () => router.currentRoute.value.query,
    () => {
        if (route.hash == '#new') {
            getpost(Number(route.query.pid))
        }
    },
    { immediate: true }
)

const updatapost = () => {
    if (title.value == '') {
        message.error('标题是必须的')
        return
    }
    if (content.value == '') {
        message.error('内容是必须的')
        return
    }
    Service.updatePost({ pid: Number(route.query.pid), title: title.value, content: content.value }).then((p) => {
        message.success('更新成功')
        router.push({ name: 'post', params: { id: p.id_ } })
    }).catch((e: ApiError) => {
        message.error(e.message + e.body.detail)
    })
}
const saveaction = () => {
    if (Number.isNaN(route.query.pid) && uppost) {
        // console.log('up');
        updatapost()
    } else {
        // console.log('add');
        addpost()
    }
}
const addpost = () => {
    if (title.value == '') {
        message.error('标题是必须的')
        return
    }
    if (content.value == '') {
        message.error('内容是必须的')
        return
    }
    Service.newPost({ title: title.value, content: content.value, tag_names: tag_names.value }).then((p) => {
        message.success('发表成功')
        router.push({ name: 'post', params: { id: p.id_ } })
    }).catch((e: ApiError) => {
        message.error(e.message + e.body.detail)
    })
}
const tags = ref<Array<TagInDB>>()
Service.getAllTags().then((t: Array<TagInDB>) => {
    tags.value = t
})
const selecttag = (t: string) => {
    if (tag_names.value.includes(t)) {
        message.error('重复添加')
        setTimeout(() => {
            tag_names.value.pop()
        }, 100);
    }
    tag_names.value.push(t)
    if (tag_names.value.length > 5) {
        message.error('最多五个')
        tag_names.value.pop()
    }

}
const handleCreate = (label: string) => {
    if (tag_names.value.includes(label)) {
        message.error('重复添加')
        setTimeout(() => {
            tag_names.value.pop()
        }, 100);
    }
    if (label.replaceAll(' ', '') == '') {
        message.error('只有空格!')
        setTimeout(() => {
            tag_names.value.pop()
        }, 100);
    }
    return label

}
</script>