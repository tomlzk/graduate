<template>
  <div class="page-container module-detail">
    <!-- 模块头部 -->
    <div class="module-header" v-if="module">
      <div class="module-header-content">
        <div class="module-emoji">{{ emojiMap[module.id] || '📚' }}</div>
        <div>
          <h1>{{ module.name }}</h1>
          <p>{{ module.description }}</p>
        </div>
      </div>
    </div>

    <!-- 内容标签页 -->
    <el-tabs v-model="activeTab" class="module-tabs">
      <!-- 考试信息 -->
      <el-tab-pane label="📋 考试信息" name="info">
        <el-empty v-if="!examInfoList.length" description="暂无考试信息" />
        <div v-else class="info-list">
          <el-card v-for="info in examInfoList" :key="info.id" shadow="hover" class="info-card">
            <h3>{{ info.title }}</h3>
            <div class="info-content" v-html="renderContent(info.content)"></div>
            <div class="info-meta">
              <span><el-icon><Calendar /></el-icon> {{ formatDate(info.createTime) }}</span>
            </div>
          </el-card>
        </div>
      </el-tab-pane>

      <!-- 帖子讨论 -->
      <el-tab-pane label="💬 帖子讨论" name="post">
        <div class="tab-toolbar">
          <el-button v-if="userStore.isLoggedIn" type="primary" @click="router.push(`/module/${moduleId}/post/create`)">
            <el-icon><EditPen /></el-icon> 发帖
          </el-button>
        </div>
        <el-empty v-if="!postList.length" description="还没有帖子，快来发表第一个吧" />
        <div v-else class="post-list">
          <div v-for="post in postList" :key="post.id" class="post-item" @click="router.push(`/post/${post.id}`)">
            <div class="post-title">{{ post.title }}</div>
            <div class="post-meta">
              <span><el-icon><User /></el-icon> {{ post.authorName || '匿名' }}</span>
              <span><el-icon><Calendar /></el-icon> {{ formatDate(post.createTime) }}</span>
            </div>
          </div>
        </div>
        <el-pagination
          v-if="postTotal > postPageSize"
          layout="prev, pager, next"
          :total="postTotal"
          :page-size="postPageSize"
          v-model:current-page="postPage"
          @current-change="loadPosts"
          style="margin-top:16px;justify-content:center"
        />
      </el-tab-pane>

      <!-- 问答区 -->
      <el-tab-pane label="❓ 问答区" name="question">
        <div class="tab-toolbar">
          <el-button v-if="userStore.isLoggedIn" type="primary" @click="router.push(`/module/${moduleId}/question/create`)">
            <el-icon><EditPen /></el-icon> 提问
          </el-button>
        </div>
        <el-empty v-if="!questionList.length" description="还没有问题，快来提第一个吧" />
        <div v-else class="post-list">
          <div v-for="q in questionList" :key="q.id" class="post-item" @click="router.push(`/question/${q.id}`)">
            <div class="post-title">{{ q.title }}</div>
            <div class="post-meta">
              <span><el-icon><User /></el-icon> {{ q.authorName || '匿名' }}</span>
              <span><el-icon><Calendar /></el-icon> {{ formatDate(q.createTime) }}</span>
            </div>
          </div>
        </div>
        <el-pagination
          v-if="questionTotal > questionPageSize"
          layout="prev, pager, next"
          :total="questionTotal"
          :page-size="questionPageSize"
          v-model:current-page="questionPage"
          @current-change="loadQuestions"
          style="margin-top:16px;justify-content:center"
        />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getModuleList, getExamInfoList } from '@/api/module'
import { getPostList } from '@/api/post'
import { getQuestionList } from '@/api/question'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const moduleId = ref(route.params.id)
const module = ref(null)
const activeTab = ref('info')

const examInfoList = ref([])
const postList = ref([])
const postPage = ref(1)
const postPageSize = 10
const postTotal = ref(0)
const questionList = ref([])
const questionPage = ref(1)
const questionPageSize = 10
const questionTotal = ref(0)

const emojiMap = { 1: '🏛️', 2: '🎓', 3: '🅰️', 4: '🅱️', 5: '✈️', 6: '🌐', 7: '💻' }

const formatDate = (str) => str ? str.substring(0, 10) : ''
const renderContent = (text) => {
  if (!text) return ''
  return text.replace(/\n/g, '<br/>')
}

const loadModule = async () => {
  try {
    const res = await getModuleList()
    const list = res.data || []
    module.value = list.find(m => m.id == moduleId.value)
  } catch (e) {}
}
const loadExamInfo = async () => {
  try {
    const res = await getExamInfoList(moduleId.value)
    examInfoList.value = res.data || []
  } catch (e) {}
}
const loadPosts = async () => {
  try {
    const res = await getPostList({ moduleId: moduleId.value, page: postPage.value, size: postPageSize })
    postList.value = res.data?.records || res.data || []
    postTotal.value = res.data?.total || 0
  } catch (e) {}
}
const loadQuestions = async () => {
  try {
    const res = await getQuestionList({ moduleId: moduleId.value, page: questionPage.value, size: questionPageSize })
    questionList.value = res.data?.records || res.data || []
    questionTotal.value = res.data?.total || 0
  } catch (e) {}
}

watch(() => route.params.id, (newId) => {
  moduleId.value = newId
  loadModule()
  loadExamInfo()
  postPage.value = 1
  questionPage.value = 1
  loadPosts()
  loadQuestions()
})

onMounted(() => {
  loadModule()
  loadExamInfo()
  loadPosts()
  loadQuestions()
})
</script>

<style scoped>
.module-detail { max-width: 960px; }
.module-header {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 16px;
  padding: 32px;
  color: #fff;
  margin-bottom: 24px;
}
.module-header-content {
  display: flex;
  align-items: center;
  gap: 20px;
}
.module-emoji { font-size: 48px; }
.module-header h1 { font-size: 24px; margin-bottom: 6px; }
.module-header p { opacity: 0.85; font-size: 14px; }
.module-tabs { background: #fff; border-radius: 12px; padding: 20px; }
.tab-toolbar { margin-bottom: 16px; }
.info-card { margin-bottom: 16px; }
.info-card h3 { font-size: 16px; margin-bottom: 8px; }
.info-content { font-size: 14px; color: var(--text-regular); line-height: 1.8; }
.info-meta { margin-top: 12px; font-size: 13px; color: var(--text-secondary); }
.post-list { display: flex; flex-direction: column; gap: 8px; }
.post-item {
  padding: 14px 18px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  border: 1px solid #eee;
}
.post-item:hover { background: #f5f7fa; border-color: #409eff40; }
.post-title { font-size: 15px; font-weight: 500; margin-bottom: 8px; }
.post-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: var(--text-secondary);
}
.post-meta span { display: flex; align-items: center; gap: 4px; }
</style>
