## 后端
1. 安装依赖

2. 最好使用虚拟环境
```bash
pip install -r requirements.txt
```

2. 配置

修改`config.yaml`
> 修改数据库用户名密码，创建数据库,数据库名填入dbname


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

3. api url 和 img url

在main.ts中，修改后端api的url, 图片baseurl


