# 智能歌词生成系统

## 📖 项目概述

基于大模型（智谱 BigModel GLM-4V）的智能歌词生成系统。用户可上传多个文件（文本/图片/PDF/Word）或直接选择风格，AI 理解素材内容后创作符合要求的歌词。

## 🛠 技术栈

| 层次 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite + Axios |
| 后端 | Python FastAPI + Uvicorn |
| 大模型 | 智谱 BigModel GLM-4V-Plus（支持图片理解） |
| 部署 | 虚拟机直跑 / Docker 容器 |

## 📁 项目结构

```
lyric-generator/
├── backend/                     # 后端服务
│   ├── app/
│   │   ├── main.py              # FastAPI 入口 + CORS
│   │   ├── config.py            # 配置文件
│   │   ├── routers/
│   │   │   └── generate.py      # POST /api/generate 路由（支持多文件）
│   │   ├── services/
│   │   │   ├── llm_client.py       # 智谱 API 客户端
│   │   │   ├── file_parser.py      # 文件解析（txt/pdf/docx/image）
│   │   │   └── lyric_generator.py  # Prompt 构建 + 歌词生成
│   │   └── schemas/
│   │       └── request.py       # 数据模型
│   ├── uploads/                 # 临时文件目录
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                    # 前端页面
│   ├── src/
│   │   ├── App.vue              # 根组件
│   │   ├── main.js              # 入口
│   │   ├── api/index.js         # Axios 封装
│   │   ├── components/
│   │   │   ├── FileUpload.vue   # 多文件拖拽上传
│   │   │   ├── StyleConfig.vue  # 风格配置
│   │   │   ├── LyricsDisplay.vue # 歌词展示
│   │   │   └── LoadingSpinner.vue # 加载动画
│   │   └── styles/main.css      # 全局样式
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml           # 容器编排
└── .env.example                 # 环境变量示例
```

## 🚀 本地运行方式

### 1. 配置 API Key

```bash
cd backend
# 编辑 .env 填入你的智谱 API Key
nano .env
```

`.env` 内容：
```
ZHIPU_API_KEY=你的智谱APIKey
LLM_API_BASE=https://open.bigmodel.cn/api/paas/v4
LLM_MODEL=glm-4v-plus-0111
```

> 注册智谱 BigModel 获取免费额度：https://open.bigmodel.cn/

### 2. 虚拟机直接运行

**后端：**
```bash
cd backend
pip install -r requirements.txt
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**前端：**
```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

浏览器访问 http://localhost:5173

### 3. Docker 容器运行

```bash
export ZHIPU_API_KEY=你的智谱APIKey
docker-compose up --build
```

浏览器访问 http://localhost

## 📸 功能截图

（实验报告时补充完整操作流程截图）

## 💡 功能说明

- **多文件上传**：支持同时上传多个文件（TXT / PDF / DOCX / PNG / JPG）
- **曲风选择**：流行 / 摇滚 / 古风 / R&B / 民谣 / 说唱
- **情感基调**：欢快 / 伤感 / 激昂 / 温柔 / 浪漫 / 深情
- **歌词展示**：支持复制、下载为 .txt 文件
- **图片理解**：利用智谱 GLM-4V 视觉模型直接理解图片内容生成歌词
