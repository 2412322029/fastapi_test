<template>
    <main class="grid min-h-full place-items-center px-6 py-24 sm:py-32 lg:px-8">
        <div class="text-center">
            <p class="text-base font-semibold ">404</p>
            <h1 class="mt-4 text-3xl font-bold tracking-tight sm:text-5xl">path not found</h1>
            <p class="mt-6 text-base leading-7 text-gray-600">Sorry, we couldn’t find the page you’re looking for.</p>
            <div class="mt-10 flex items-center justify-center gap-x-6">
                <a @click="$router.push({name:'home'})"
                    class=" cursor-pointer rounded-md px-3.5 py-2.5 text-sm 
                    font-semibold shadow-sm focus-visible:outline 
                    focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                    Go back home</a>
            </div>
        </div>
    </main>
</template>
<script setup lang="ts">
document.title = '404'
</script>
