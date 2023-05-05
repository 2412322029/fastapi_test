import { createApp } from 'vue'
import "./style.css"
import App from './App.vue'
import { router } from '@/route/router'
import { OpenAPI } from './client/core/OpenAPI'
import { VMdPreview, VueMarkdownEditor } from './md'


if (process.env.NODE_ENV == "development") {
  OpenAPI.BASE = 'http://127.0.0.1:8000'
} else if (process.env.NODE_ENV == "production") {
  OpenAPI.BASE = location.origin
  console.log(OpenAPI)
} else {
  OpenAPI.BASE = location.origin
}
export const imgbase: string = OpenAPI.BASE + '/uploads/'



const app = createApp(App)
app.use(router)
app.use(VueMarkdownEditor);
app.use(VMdPreview)
app.mount('#app')


