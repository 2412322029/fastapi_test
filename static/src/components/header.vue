<template>
    <header class="bg-white">
        <nav class="mx-auto flex max-w-7xl items-center justify-between p-2 border-b-2" aria-label="Global">
            <div class="flex flex-1 justify-end">
                <a href="#" class="-m-1.5 p-1">
                    <span class="sr-only">Your Company</span>
                    <img class="h-10 w-auto rounded-full " :src="'./uploads/' + url" alt="" />
                </a>
            </div>
        </nav>
    </header>
</template>
<script setup lang="ts">

defineProps<{
    url?: string
}>()
</script>