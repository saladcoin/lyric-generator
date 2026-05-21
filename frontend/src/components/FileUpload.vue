<template>
  <div class="file-upload"
    @dragover.prevent="dragOver = true"
    @dragleave.prevent="dragOver = false"
    @drop.prevent="onDrop">
    <div class="drop-zone" @click="onClickSelect">
      <div class="upload-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M12 16V4m0 0L8 8m4-4l4 4" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <p class="upload-text">
        拖拽文件到此处，或 <span class="upload-link">浏览选择</span>
      </p>
      <p class="upload-hint">支持 TXT · PDF · DOCX · PNG · JPG（最大 10MB，可多选）</p>
      <input ref="inputRef" type="file" :accept="acceptStr" multiple @change="onSelect" hidden />
    </div>

    <div class="file-list" v-if="files.length > 0">
      <div v-for="(f, idx) in files" :key="f.name + f.size" class="file-card">
        <span class="file-icon">{{ isImage(f) ? '🖼️' : '📄' }}</span>
        <div class="file-details">
          <span class="file-name">{{ f.name }}</span>
          <span class="file-size">{{ formatSize(f.size) }}</span>
        </div>
        <button class="btn-remove" @click="removeFile(idx)" title="移除文件">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 6L6 18M6 6l12 12" stroke-linecap="round"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['files-change'])

const ALLOWED = ['.txt', '.pdf', '.docx', '.png', '.jpg', '.jpeg']
const IMG_EXT = ['.png', '.jpg', '.jpeg']
const acceptStr = ALLOWED.join(',')

const files = ref([])
const dragOver = ref(false)
const inputRef = ref(null)

function isImage(f) {
  const ext = '.' + f.name.split('.').pop().toLowerCase()
  return IMG_EXT.includes(ext)
}

function formatSize(bytes) {
  if (bytes < 1024) return bytes + 'B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + 'KB'
  return (bytes / 1024 / 1024).toFixed(1) + 'MB'
}

function validate(f) {
  const ext = '.' + f.name.split('.').pop().toLowerCase()
  if (!ALLOWED.includes(ext)) {
    alert('不支持的文件类型：' + ext)
    return false
  }
  if (f.size > 10 * 1024 * 1024) {
    alert('文件大小不能超过 10MB')
    return false
  }
  return true
}

function addFiles(newFiles) {
  for (const f of newFiles) {
    if (validate(f)) {
      files.value.push(f)
    }
  }
  emit('files-change', [...files.value])
}

function onClickSelect() {
  inputRef.value?.click()
}

function onDrop(e) {
  dragOver.value = false
  addFiles([...e.dataTransfer.files])
}

function onSelect(e) {
  addFiles([...e.target.files])
  if (inputRef.value) inputRef.value.value = ''
}

function removeFile(idx) {
  files.value.splice(idx, 1)
  emit('files-change', [...files.value])
}
</script>

<style scoped>
.file-upload { margin-bottom: 20px; }
.drop-zone {
  border: 2px dashed rgba(255,255,255,0.15);
  border-radius: 16px;
  padding: 44px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(255,255,255,0.03);
}
.drop-zone:hover {
  border-color: #667eea;
  background: rgba(102,126,234,0.08);
  transform: scale(1.01);
}
.upload-icon {
  color: rgba(255,255,255,0.3);
  margin-bottom: 12px;
  transition: color 0.3s;
}
.drop-zone:hover .upload-icon { color: #667eea; }
.upload-text { font-size: 16px; color: rgba(255,255,255,0.7); margin: 0 0 8px; }
.upload-link { color: #667eea; font-weight: 600; }
.upload-hint { font-size: 13px; color: rgba(255,255,255,0.35); margin: 0; }

.file-list { margin-top: 12px; display: flex; flex-direction: column; gap: 8px; }
.file-card {
  display: flex; align-items: center; gap: 14px;
  padding: 12px 16px;
  background: rgba(102,126,234,0.1);
  border: 1px solid rgba(102,126,234,0.2);
  border-radius: 12px;
  animation: slideIn 0.25s ease;
}
@keyframes slideIn { from { opacity: 0; transform: translateY(-8px); } to { opacity: 1; transform: translateY(0); } }
.file-icon { font-size: 24px; }
.file-details { flex: 1; min-width: 0; }
.file-name {
  display: block; font-weight: 600; color: #e0e0e0;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.file-size { font-size: 12px; color: rgba(255,255,255,0.4); }
.btn-remove {
  background: none; border: none; cursor: pointer;
  color: rgba(255,255,255,0.3); padding: 4px; border-radius: 6px;
  transition: all 0.2s; display: flex;
}
.btn-remove:hover { background: rgba(231,76,60,0.15); color: #e74c3c; }
</style>
