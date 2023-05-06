![image-20230506225558239](README.assets/image-20230506225558239.png)

![image-20230506225922997](README.assets/image-20230506225922997.png)

![image-20230506225902139](README.assets/image-20230506225902139.png)



![image-20230506225716959](README.assets/image-20230506225716959.png)

![image-20230506225751893](README.assets/image-20230506225751893.png)

 + server

  + fastapi+sqlalchemy 实现 RESTful API与api文档自动生成，pydantic数据校验
  + 前后端鉴权使用[OAuth2 实现 Bearer JWT 令牌](https://fastapi.tiangolo.com/zh/tutorial/security/oauth2-jwt/)
  + slowapi限制api速率
  + 简单websockets与api监控(python库 psutil)
  + Pillow库生成简单验证码(扒的代码),文本文件缓存验证码
  + 意义不大的异步aiomysql,aiofiles(异步的session导致写起来很麻烦)

+ client

  + vite+ts+vue3+vue-router+navie-ui
  + openapi-generate-typescript自动生成axios请求代码
  + tailwindcss，css in html
  + markdown解析和高亮使用highlight.js,编辑器[v-md-editor](https://code-farmer-i.github.io/vue-markdown-editor/zh/)

  

docker部署nginx,mysql,python3.10,nginx反向代理/api路径(api都以/api开头)单独代理/docs,/openapi.json路径的api文档，/uploads路径挂载文件上传的目录其他路径匹配[回退路由](https://router.vuejs.org/zh/guide/essentials/history-mode.html#nginx)

## 目录结构

```
├─static // vite构建目录
|   ├─dist //nginx静态文件挂载
├─nginx //nginx配置和日志文件
├─data/mysql //mysql数据，docker挂载目录
├─uploads //文件上传目录
├─utill //验证码生成/校验,cpu监控
├─api //fastapi子路由，数据校验模型
├─sql //数据库连接，crud代码，orm模型
├─config //读取配置文件，环境变量
├─app.py //fastapi主文件
├─config.yaml //主要是mysql信息，fasapi配置
├─...如其名

```



## 后端

1. 安装依赖

2. 最好使用虚拟环境
```bash
pip install -r requirements.txt
```

2. 配置

修改`config.yaml`
> 修改数据库用户名密码，创建数据库,数据库名填入dbname
> 
> 修改默认用户名密码

3. 启动

```bash
python app.py
```

---
## 前端
在 static 目录

1. 安装依赖
```bash
npm install
```

2. openapi生成代码
```bash
npm run generate-client
```

3. api url 和 img baseurl

## docker部署

nginx反向代理fastapi和静态文件目录
```bash
docker-compose up -d
```

## 前后端分离部署

后端填写mysql数据库信息到配置文件，或通过环境变量(覆盖前者),配置跨域，pip安装依赖，启动app.py

在main.ts中，修改后端api的url, 图片baseurl

前端代码静态部署（处理回退路由）

## 其他

修改config.yaml中的密钥，compose.yaml的mysql密码，保持mysql容器和python容器密码一致



最大文件上传限制：config.yaml中的是python代码中写的限制，还取决于nginx配置文件中client_max_body_size（10m）

...未完待续
