
import { createRouter, createWebHistory } from 'vue-router'
const routes = [
    {
        path: '/',
        component: () => import('@/route/home.vue')
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
    history: createWebHistory(),
    routes,
})
