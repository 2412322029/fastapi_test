<template>
    <div>
        title <input type="text" v-model="npost.title">
        <br>
        <textarea name="" id="" cols="30" rows="10" v-model="npost.content">
            </textarea>
        <br>
        tsg:
        <p v-for="t, index in npost.tag_names">{{ t }}<button @click="deltag(index)">----x</button><br></p>
        <br>
        <input type="text" v-model="tagnaw"><button type="button" @click="addtag()">添加tag</button>
        <button @click="addpost">new</button>
    </div>
</template>
<script setup lang="ts">
import { ref, onMounted, reactive, toRaw } from 'vue'
import { OpenAPI, Service, UserOut, ApiError, PubUserInfo, PostIn } from '@/client'
import cogoToast from 'cogo-toast';
import { useRouter } from 'vue-router';
const router = useRouter()
const npost = reactive<PostIn>({
    'title': '',
    "content": '',
    "tag_names": []
})
const tagnaw = ref('')
const addtag = () => {
    if (tagnaw.value == ''||toRaw(npost.tag_names).includes(tagnaw.value)) { return }
    npost.tag_names.push(tagnaw.value)
    tagnaw.value = ''
}
const deltag = (index: number) => {
    npost.tag_names.splice(index, 1)
}
const addpost = () => {
    Service.newPost(npost).then((p) => {
        cogoToast.success('发表成功')
        router.push({ name: 'post', params: { id: p.id } })
    }).catch((e: ApiError) => {
        cogoToast.error(e.message + e.body.detail)
    })
}

</script>