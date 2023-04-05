<template>
   <Headers :url="userinfo?.avatar"/>
    <router-link to='/login'>login</router-link>
    <router-link to='/register'>register</router-link>
    <br>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { OpenAPI, Service, UserOut, ApiError } from '../client'
import cogoToast from 'cogo-toast';
import Headers from '@/components/header.vue';
const userinfo = ref<UserOut>()

onMounted(() => {
    OpenAPI.TOKEN = localStorage.getItem("token") as string
    Service.userinfo().then((u: UserOut) => {
        userinfo.value = u
    }).catch((e: ApiError) => {
        cogoToast.error(e.message)
        setTimeout(() => {
            location.href='./login'
        }, 1000);
    })

})

</script>