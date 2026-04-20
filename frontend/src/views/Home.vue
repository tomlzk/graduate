<template>
  <div class="page-container home-page">
    <!-- 顶部横幅 -->
    <div class="hero-banner">
      <div class="hero-content">
        <h1>🎓 高校学生考证服务平台</h1>
        <p>覆盖考公、考研、四六级、雅思、托福、计算机等级等热门考试，提供备考交流、经验分享、信息查询一站式服务</p>
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-num">{{ modules.length }}</span>
            <span class="stat-label">考证模块</span>
          </div>
          <div class="stat-item">
            <span class="stat-num">{{ announcements.length }}</span>
            <span class="stat-label">最新公告</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 公告区域 -->
    <div class="section" v-if="announcements.length">
      <div class="section-header">
        <h2><el-icon><Bell /></el-icon> 系统公告</h2>
      </div>
      <el-carousel height="60px" direction="vertical" :autoplay="true" :interval="4000" indicator-position="none">
        <el-carousel-item v-for="item in announcements" :key="item.id">
          <div class="announcement-item" @click="router.push(`/announcement/${item.id}`)">
            <el-tag type="danger" size="small">公告</el-tag>
            <span class="announcement-title">{{ item.title }}</span>
            <span class="announcement-time">{{ formatDate(item.createTime) }}</span>
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>

    <!-- 考证模块入口 -->
    <div class="section">
      <div class="section-header">
        <h2><el-icon><Grid /></el-icon> 考证模块</h2>
        <span class="section-desc">选择你感兴趣的考试模块，开始备考之旅</span>
      </div>
      <el-row :gutter="20">
        <el-col :xs="12" :sm="8" :md="6" v-for="mod in modules" :key="mod.id">
          <div class="module-card" @click="router.push(`/module/${mod.id}`)">
            <div class="module-icon" :style="{ background: iconColors[mod.id % iconColors.length] }">
              {{ iconEmojis[mod.id - 1] || '📚' }}
            </div>
            <h3>{{ mod.name }}</h3>
            <p>{{ mod.description?.substring(0, 30) }}...</p>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getModuleList } from '@/api/module'
import { getAnnouncementList } from '@/api/announcement'

const router = useRouter()
const modules = ref([])
const announcements = ref([])

const iconEmojis = ['🏛️', '🎓', '🅰️', '🅱️', '✈️', '🌐', '💻']
const iconColors = [
  'linear-gradient(135deg, #ff9a9e, #fad0c4)',
  'linear-gradient(135deg, #a18cd1, #fbc2eb)',
  'linear-gradient(135deg, #fbc2eb, #a6c1ee)',
  'linear-gradient(135deg, #84fab0, #8fd3f4)',
  'linear-gradient(135deg, #f6d365, #fda085)',
  'linear-gradient(135deg, #fccb90, #d57eeb)',
  'linear-gradient(135deg, #667eea, #764ba2)',
]

const formatDate = (str) => {
  if (!str) return ''
  return str.substring(0, 10)
}

onMounted(async () => {
  try {
    const [modRes, annRes] = await Promise.all([
      getModuleList(),
      getAnnouncementList({ page: 1, size: 5 })
    ])
    modules.value = modRes.data || []
    announcements.value = annRes.data?.records || annRes.data || []
  } catch (e) {
    // ignore
  }
})
</script>

<style scoped>
.home-page {
  max-width: 1100px;
}
.hero-banner {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 48px 40px;
  color: #fff;
  margin-bottom: 28px;
}
.hero-content h1 {
  font-size: 28px;
  margin-bottom: 12px;
}
.hero-content p {
  font-size: 15px;
  opacity: 0.9;
  line-height: 1.6;
  max-width: 600px;
}
.hero-stats {
  display: flex;
  gap: 40px;
  margin-top: 24px;
}
.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.stat-num {
  font-size: 28px;
  font-weight: 700;
}
.stat-label {
  font-size: 13px;
  opacity: 0.8;
}
.section {
  margin-bottom: 28px;
}
.section-header {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 16px;
}
.section-header h2 {
  font-size: 20px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.section-desc {
  font-size: 14px;
  color: var(--text-secondary);
}
.announcement-item {
  display: flex;
  align-items: center;
  gap: 12px;
  height: 60px;
  padding: 0 16px;
  background: #fff;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}
.announcement-item:hover {
  background: #f5f7fa;
}
.announcement-title {
  flex: 1;
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.announcement-time {
  font-size: 13px;
  color: var(--text-secondary);
  flex-shrink: 0;
}
.module-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.module-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}
.module-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  margin: 0 auto 12px;
}
.module-card h3 {
  font-size: 16px;
  margin-bottom: 6px;
}
.module-card p {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.4;
}
</style>
