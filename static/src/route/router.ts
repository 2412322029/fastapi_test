
import { createRouter, createWebHashHistory } from 'vue-router'
const routes = [
    {
        path: '/',
        component: () => import('@/route/home.vue')
    },
    {
        path: '/user/:username',
        name: 'user',
        component: () => import('@/route/userhome.vue')
    },
    {
        path: '/post/:id',
        name: 'post',
        component: () => import('@/route/post.vue')
    },
    {
        path: '/websocket',
        component: () => import('@/route/websocket.vue')
    },
    {
        path: '/admin',
        component: () => import('@/route/admin.vue')
    },
    {
        path: '/:pathMatch(.*)',
        component: () => import('@/route/NotFound.vue')
    }
]

export const router = createRouter({
    history: createWebHashHistory(),
    routes,
})
