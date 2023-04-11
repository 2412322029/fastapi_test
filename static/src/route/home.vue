<template>
    <router-link :to="{ name: 'home' }">
        <Headers :user="userinfo" :headinfo="{ title: 'home' }" />
    </router-link>
    <div class="mx-auto flex max-w-7xl items-center justify-between px-4 top-20 relative">
        <n-tag type="error" round >
      手写的从前
    </n-tag>
    </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { OpenAPI, Service, UserOut, ApiError } from '@/client'
import cogoToast from 'cogo-toast';
import Headers from '@/components/header.vue';
import { NTag } from 'naive-ui'
const userinfo = ref<UserOut>()

onMounted(() => {
    OpenAPI.TOKEN = localStorage.getItem("token") as string
    Service.userinfo().then((u: UserOut) => {
        userinfo.value = u
    }).catch((e: ApiError) => {
        cogoToast.error(e.message)
    })

})

</script>