import { createApp } from 'vue'
import "./style.css"
import App from './App.vue'
import { router } from '@/route/router'
import { OpenAPI } from './client/core/OpenAPI'

// OpenAPI.BASE = 'http://lolik.azurewebsites.net'
OpenAPI.BASE ='http://127.0.0.1:80'
export const imgbase:string = OpenAPI.BASE+'/uploads/'

const app = createApp(App)
app.use(router)
app.mount('#app')


