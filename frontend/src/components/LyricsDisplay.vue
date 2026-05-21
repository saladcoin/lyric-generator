<template>
  <div class="lyrics-display" v-if="lyrics">
    <div class="lyrics-header">
      <div class="lyrics-title-row">
        <div class="title-decoration"></div>
        <h3 class="lyrics-title">生成结果</h3>
      </div>
      <div class="lyrics-actions">
        <button class="btn-action" @click="copyLyrics" title="复制">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="9" y="9" width="13" height="13" rx="2" /><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" />
          </svg>
          复制
        </button>
        <button class="btn-action" @click="downloadLyrics" title="下载">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 16V4m0 0L8 8m4-4l4 4" /><path d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2" />
          </svg>
          下载
        </button>
        <button class="btn-action btn-retry" @click="$emit('retry')" title="重新生成">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M23 4v6h-6" /><path d="M1 20v-6h6" />
            <path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15" />
          </svg>
          重新生成
        </button>
      </div>
    </div>
    <div class="lyrics-content">
      <div class="lyrics-scroll">
        <pre class="lyrics-text">{{ lyrics }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ lyrics: String })
const emit = defineEmits(['retry'])

async function copyLyrics() {
  try {
    await navigator.clipboard.writeText(props.lyrics)
    alert('✅ 已复制到剪贴板！')
  } catch {
    alert('复制失败，请手动复制')
  }
}

function downloadLyrics() {
  const blob = new Blob([props.lyrics], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = '歌词.txt'
  a.click()
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.lyrics-display {
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255,255,255,0.08);
  overflow: hidden;
  animation: fadeInUp 0.5s ease;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

.lyrics-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  flex-wrap: wrap; gap: 12px;
}
.lyrics-title-row { display: flex; align-items: center; gap: 10px; }
.title-decoration {
  width: 4px; height: 20px;
  background: linear-gradient(180deg, #667eea, #f093fb);
  border-radius: 2px;
}
.lyrics-title { font-size: 16px; font-weight: 600; color: rgba(255,255,255,0.8); margin: 0; }

.lyrics-actions { display: flex; gap: 6px; }
.btn-action {
  display: flex; align-items: center; gap: 5px;
  padding: 7px 13px;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  background: rgba(255,255,255,0.04);
  cursor: pointer;
  font-size: 13px;
  color: rgba(255,255,255,0.6);
  transition: all 0.2s;
}
.btn-action:hover {
  background: rgba(255,255,255,0.08);
  color: #e0e0e0;
  border-color: rgba(255,255,255,0.2);
}
.btn-action svg { flex-shrink: 0; }
.btn-retry { color: #f093fb; }
.btn-retry:hover { background: rgba(240,147,251,0.1); border-color: rgba(240,147,251,0.3); }

.lyrics-content { padding: 24px; }
.lyrics-scroll {
  max-height: 520px; overflow-y: auto;
  padding: 20px 24px;
  background: rgba(0,0,0,0.2);
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.05);
}
.lyrics-scroll::-webkit-scrollbar { width: 6px; }
.lyrics-scroll::-webkit-scrollbar-track { background: transparent; }
.lyrics-scroll::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }

.lyrics-text {
  white-space: pre-wrap; word-wrap: break-word;
  font-family: 'Georgia', 'KaiTi', 'Noto Sans SC', serif;
  font-size: 15px;
  line-height: 2;
  color: rgba(255,255,255,0.85);
  margin: 0;
}
</style>
