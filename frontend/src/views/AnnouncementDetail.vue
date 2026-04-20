<template>
  <div class="page-container announcement-detail" v-if="detail">
    <el-card shadow="never">
      <div class="ann-header">
        <el-tag type="danger">公告</el-tag>
        <h1>{{ detail.title }}</h1>
        <div class="ann-meta">
          <span><el-icon><Calendar /></el-icon> {{ formatDate(detail.createTime) }}</span>
        </div>
      </div>
      <el-divider />
      <div class="ann-content" v-html="renderContent(detail.content)"></div>
      <el-divider />
      <el-button text @click="router.back()">
        <el-icon><Back /></el-icon> 返回
      </el-button>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getAnnouncementDetail } from '@/api/announcement'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const detail = ref(null)

const formatDate = (str) => str ? str.substring(0, 16).replace('T', ' ') : ''
const renderContent = (text) => text ? text.replace(/\n/g, '<br/>') : ''

onMounted(async () => {
  try {
    const res = await getAnnouncementDetail(route.params.id)
    detail.value = res.data
  } catch (e) {
    ElMessage.error('公告不存在')
    router.back()
  }
})
</script>

<style scoped>
.announcement-detail { max-width: 800px; }
.ann-header h1 { font-size: 22px; margin: 12px 0 8px; }
.ann-meta { font-size: 13px; color: var(--text-secondary); display: flex; align-items: center; gap: 4px; }
.ann-content { font-size: 15px; line-height: 1.8; color: var(--text-regular); min-height: 200px; }
</style>
