import { createApp, ref, watch } from 'vue'
import "./style.css"
import App from './App.vue'
import { router } from '@/route/router'
import { OpenAPI } from './client/core/OpenAPI'
import { VMdPreview, VueMarkdownEditor } from './md'
import { host } from '@/host'
import { darkTheme } from 'naive-ui'

if (process.env.NODE_ENV == "development") {
  OpenAPI.BASE = host
  console.log('in development')
} else if (process.env.NODE_ENV == "production") {
  OpenAPI.BASE = location.origin
} else {
  OpenAPI.BASE = location.origin
}
export const imgbase: string = OpenAPI.BASE + '/uploads/'
export const usews: boolean = true
export const msgs = ref<[{ username: string, path: string }]>([{ username: '', path: '' }])
export const loading = ref(false)
export const theme = ref<typeof darkTheme | null>()
export const followos = ref(true)



const app = createApp(App)
app.use(router)
app.use(VueMarkdownEditor);
app.use(VMdPreview)
app.mount('#app')


