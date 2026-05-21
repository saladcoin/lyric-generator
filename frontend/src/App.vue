<template>
  <div class="app-container">
    <header class="app-header">
      <div class="logo">
        <span class="logo-icon">🎵</span>
      </div>
      <h1 class="app-title">智能歌词生成系统</h1>
      <p class="app-subtitle">上传你的素材，选择喜欢的风格，让 AI 为你谱写专属歌词</p>
      <p v-if="error" class="error-msg">{{ error }}</p>
    </header>

    <main class="app-main">
      <div class="card">
        <FileUpload @files-change="onFilesChange" />
        <StyleConfig @update="onConfigUpdate" />
      </div>

      <button class="btn-generate" :disabled="loading" @click="onGenerate">
        <span class="btn-icon" v-if="!loading">✨</span>
        <span class="btn-icon loading-icon" v-else>⏳</span>
        <span>{{ loading ? 'AI 正在创作中...' : '开始生成歌词' }}</span>
      </button>

      <LoadingSpinner :visible="loading" />

      <LyricsDisplay
        v-if="lyrics"
        :lyrics="lyrics"
        @retry="onGenerate" />
    </main>

    <footer class="app-footer">
      <p>Powered by DeepSeek &amp; Claude Code</p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import FileUpload from './components/FileUpload.vue'
import StyleConfig from './components/StyleConfig.vue'
import LyricsDisplay from './components/LyricsDisplay.vue'
import LoadingSpinner from './components/LoadingSpinner.vue'
import { generateLyrics } from './api/index.js'

const files = ref([])
const config = ref({ style: 'pop', emotion: '欢快', theme: '', extra: '' })
const lyrics = ref('')
const loading = ref(false)
const error = ref('')

function onFilesChange(fs) {
  files.value = fs
  error.value = ''
}

function onConfigUpdate(cfg) {
  config.value = cfg
}

async function onGenerate() {
  error.value = ''
  lyrics.value = ''
  loading.value = true
  try {
    const res = await generateLyrics(
      files.value,
      config.value.style,
      config.value.emotion,
      config.value.theme || undefined,
      config.value.extra || undefined,
    )
    if (res.success) {
      lyrics.value = res.data.lyrics
    } else {
      error.value = res.error || '生成失败，请重试'
    }
  } catch (e) {
    error.value = '请求失败：' + (e.response?.data?.detail || e.message)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.app-container {
  animation: fadeIn 0.6s ease;
}
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

.app-header {
  text-align: center;
  margin-bottom: 36px;
}
.logo {
  width: 72px;
  height: 72px;
  margin: 0 auto 16px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(102,126,234,0.3);
  animation: float 3s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}
.logo-icon { font-size: 32px; }
.app-title {
  font-size: 30px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea, #f093fb);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
}
.app-subtitle { font-size: 15px; color: rgba(255,255,255,0.6); margin-bottom: 8px; }

.card {
  background: rgba(255,255,255,0.06);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 28px;
  border: 1px solid rgba(255,255,255,0.08);
  margin-bottom: 20px;
  transition: border-color 0.3s;
}
.card:hover { border-color: rgba(255,255,255,0.15); }

.error-msg {
  margin-top: 12px;
  padding: 12px 18px;
  background: rgba(231,76,60,0.15);
  border: 1px solid rgba(231,76,60,0.3);
  border-radius: 10px;
  color: #e74c3c;
  font-size: 14px;
  backdrop-filter: blur(10px);
}

.btn-generate {
  width: 100%;
  padding: 16px;
  border: none;
  border-radius: 14px;
  font-size: 17px;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  position: relative;
  overflow: hidden;
}
.btn-generate::before {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 100%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
  transition: left 0.6s;
}
.btn-generate:hover::before { left: 100%; }
.btn-generate:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(102,126,234,0.4);
}
.btn-generate:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-icon { font-size: 20px; }
.loading-icon { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.app-footer {
  text-align: center;
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid rgba(255,255,255,0.06);
  font-size: 13px;
  color: rgba(255,255,255,0.3);
}
</style>
