<template>
    <div>
        <n-collapse>
            <n-collapse-item title="标题和标签" :expanded-names="[1]" name="1">
                <n-input type="text" v-model:value="title" placeholder="标题" class=" mb-1" />
                <n-h4>已有标签(点击添加)<n-button @click="tag_names.length = 0">清除所有</n-button></n-h4>
                <n-tag type="info" v-for="t in tags" round v-text="t.name" @click="selecttag(t.name)"
                    class="m-2 cursor-pointer">
                </n-tag>
                <n-dynamic-tags type="success" v-model:value.trim="tag_names" @create="handleCreate" :max="5" />
                <n-divider />
            </n-collapse-item>
        </n-collapse>
        <v-md-editor v-model="content" height="600px" class=" m-1" @save="addpost"></v-md-editor>

    </div>
</template>
<script setup lang="ts">
import { ref, onMounted, reactive, toRaw, watch } from 'vue'
import { OpenAPI, Service, UserOut, ApiError, PubUserInfo, PostIn, TagInDB } from '@/client'
import { useRouter } from 'vue-router';
import { NDynamicTags, NInput, NButton, NDivider, NH4, NTag, NCollapse,NCollapseItem } from 'naive-ui'
import { useMessage } from 'naive-ui'
import { watchEffect } from 'vue';
const message = useMessage()

const router = useRouter()

const title = ref('')
const content = ref('')
const tag_names = ref<Array<string>>([])
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
        router.push({ name: 'post', params: { id: p.id } })
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
    if (tag_names.value.length>5) {
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