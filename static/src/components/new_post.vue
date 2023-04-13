<template>
    <div>
        title <input type="text" v-model="npost.title">
        <br>
        <textarea name="" id="" cols="30" rows="10" v-model="npost.content">
            </textarea>
        <br>
        tsg:
        <n-dynamic-tags v-model:value="npost.tag_names" />
        <br>
        <button @click="addpost">new</button>
    </div>
</template>
<script setup lang="ts">
import { ref, onMounted, reactive, toRaw } from 'vue'
import { OpenAPI, Service, UserOut, ApiError, PubUserInfo, PostIn } from '@/client'
import cogoToast from 'cogo-toast';
import { useRouter } from 'vue-router';
import { NDynamicTags } from 'naive-ui'

const router = useRouter()
const npost = reactive<PostIn>({
    'title': '',
    "content": '',
    "tag_names": []
})

const addpost = () => {
    Service.newPost(npost).then((p) => {
        cogoToast.success('发表成功')
        router.push({ name: 'post', params: { id: p.id } })
    }).catch((e: ApiError) => {
        cogoToast.error(e.message + e.body.detail)
    })
}

</script>