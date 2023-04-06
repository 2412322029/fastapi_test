<template>
    <Headers :user="userinfo" :headinfo="{title:'title'}" />
    <div class="mx-auto flex max-w-7xl items-center justify-between px-4 top-20 relative">
        <div class=" bg-slate-300 w-full h-96">s</div>

    </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { OpenAPI, Service, UserOut, ApiError } from '@/client'
import cogoToast from 'cogo-toast';
import Headers from '@/components/header.vue';
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