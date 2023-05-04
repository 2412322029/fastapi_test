import { createApp } from 'vue'
import "./style.css"
import App from './App.vue'
import { router } from '@/route/router'
import { OpenAPI } from './client/core/OpenAPI'
import VueMarkdownEditor from '@kangc/v-md-editor';
import '@kangc/v-md-editor/lib/style/base-editor.css';
import vuepressTheme from '@kangc/v-md-editor/lib/theme/vuepress.js';
import '@kangc/v-md-editor/lib/theme/style/vuepress.css';
//@ts-ignore
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
//@ts-ignore
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';

// highlightjs
import hljs from 'highlight.js';
VMdPreview.use(githubTheme, {
  Hljs: hljs,
});

import Prism from 'prismjs';// 引入所有语言包
VueMarkdownEditor.use(vuepressTheme, {
  Prism,
});


// OpenAPI.BASE = 'https://lolik.azurewebsites.net'
OpenAPI.BASE ='http://127.0.0.1:8000'
export const imgbase:string = OpenAPI.BASE+'/uploads/'

const app = createApp(App)
app.use(router)
app.use(VueMarkdownEditor);
app.use(VMdPreview)
app.mount('#app')


