# 智能歌词生成系统

## 📖 项目概述

基于大模型（DeepSeek API）的智能歌词生成系统。用户上传文件（文本/图片/PDF/Word）或直接选择风格，AI 理解素材内容后创作符合要求的歌词。

## 🛠 技术栈

| 层次 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite + Axios |
| 后端 | Python FastAPI + Uvicorn |
| 大模型 | DeepSeek API（OpenAI 兼容接口） |
| 部署 | 虚拟机直跑 / Docker 容器 |

## 📁 项目结构

```
lyric-generator/
├── backend/                     # 后端服务
│   ├── app/
│   │   ├── main.py              # FastAPI 入口 + CORS
│   │   ├── config.py            # 配置文件
│   │   ├── routers/
│   │   │   └── generate.py      # POST /api/generate 路由
│   │   ├── services/
│   │   │   ├── deepseek_client.py  # DeepSeek API 客户端
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
│   │   │   ├── FileUpload.vue   # 文件拖拽上传
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

复制 `.env.example` 为 `.env`，填入你的 DeepSeek API Key：

```bash
cd backend
cp ../.env.example .env
# 编辑 .env 填入你的 Key
```

> 注册 DeepSeek 开放平台获取免费额度：https://platform.deepseek.com/

### 2. 虚拟机直接运行

**后端：**
```bash
cd backend
pip install -r requirements.txt
# 或设置环境变量 set DEEPSEEK_API_KEY=sk-xxx
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**前端：**
```bash
cd frontend
npm install
npm run dev
```

浏览器访问 http://localhost:5173

### 3. Docker 容器运行

```bash
# 在项目根目录
export DEEPSEEK_API_KEY=sk-xxx
docker-compose up -d --build
```

浏览器访问 http://localhost

## 📸 功能截图

（实验报告时补充完整操作流程截图）

## 💡 功能说明

- **文件上传**：支持 TXT、PDF、DOCX、PNG、JPG 格式
- **曲风选择**：流行 / 摇滚 / 古风 / R&B / 民谣 / 说唱
- **情感基调**：欢快 / 伤感 / 激昂 / 温柔 / 浪漫 / 深情
- **歌词展示**：支持复制、下载为 .txt 文件
- **图片理解**：利用 DeepSeek 视觉能力理解图片内容生成歌词
