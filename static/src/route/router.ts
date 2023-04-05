
import { createRouter, createWebHistory } from 'vue-router'
const routes = [
    {
        path: '/',
        component: () => import('@/route/home.vue')
    },
    {
        path: '/login',
        component: () => import('@/route/login.vue')
    },
    {
        path: '/register',
        component: () => import('@/route/register.vue')
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
