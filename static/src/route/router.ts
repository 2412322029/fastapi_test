
import { createRouter, createWebHistory } from 'vue-router'
const routes = [
    {
        path: '/',
        name: 'home',
        component: () => import('@/route/home.vue')
    },
    {
        path: '/user/:username',
        name: 'user',
        component: () => import('@/route/userhome.vue')
    },
    {
        path: '/p/:id',
        name: 'post',
        component: () => import('@/route/post.vue')
    },
    {
        path: '/tag/:name',
        name: 'tag',
        component: () => import('@/route/tag.vue')
    },
    {
        path: '/websocket',
        name: 'websocket',
        component: () => import('@/route/websocket.vue')
    },
    {
        path: '/admin',
        name: 'admin',
        component: () => import('@/route/admin.vue')
    },
    {
        path: '/404',
        name: 'notfound',
        component: () => import('@/route/NotFound.vue')
    },
    {
        path: '/:pathMatch(.*)',
        redirect: (to: any) => {
            return { name: 'notfound' }
        },
    },

]

export const router = createRouter({
    history: createWebHistory(),
    routes,
})
