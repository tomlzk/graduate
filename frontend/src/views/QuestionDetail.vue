<template>
  <div class="page-container question-detail-page" v-if="question">
    <!-- 问题 -->
    <el-card shadow="never" class="question-card">
      <div class="question-header">
        <h1>{{ question.title }}</h1>
        <div class="post-meta">
          <span><el-icon><User /></el-icon> {{ question.authorName || '匿名' }}</span>
          <span><el-icon><Calendar /></el-icon> {{ formatDate(question.createTime) }}</span>
        </div>
      </div>
      <el-divider />
      <div class="post-content" v-html="renderContent(question.content)"></div>
      <div class="post-actions" v-if="isAuthor">
        <el-button type="danger" text @click="handleDeleteQuestion">
          <el-icon><Delete /></el-icon> 删除问题
        </el-button>
      </div>
    </el-card>

    <!-- 回答区 -->
    <div class="answer-section">
      <h3 class="section-title">
        <el-icon><ChatLineSquare /></el-icon>
        {{ answers.length }} 个回答
      </h3>

      <el-empty v-if="!answers.length" description="还没有回答，快来抢答吧" />

      <div v-for="ans in answers" :key="ans.id" class="answer-item">
        <div class="answer-header">
          <el-avatar :size="32" :icon="UserFilled" />
          <div class="answer-meta">
            <span class="answer-author">{{ ans.authorName || '匿名' }}</span>
            <span class="answer-time">{{ formatDate(ans.createTime) }}</span>
          </div>
          <el-button
            v-if="canDeleteAnswer(ans)"
            type="danger" text size="small"
            @click="handleDeleteAnswer(ans.id)"
          >删除</el-button>
        </div>
        <div class="answer-content" v-html="renderContent(ans.content)"></div>
      </div>
    </div>

    <!-- 回答框 -->
    <el-card v-if="userStore.isLoggedIn" shadow="never" class="reply-card">
      <h3>我来回答</h3>
      <el-input v-model="replyContent" type="textarea" :rows="4" placeholder="写下你的回答..." maxlength="3000" show-word-limit />
      <el-button type="primary" :loading="replyLoading" style="margin-top:12px" @click="handleReply">
        提交回答
      </el-button>
    </el-card>
    <el-card v-else shadow="never" class="reply-card">
      <el-button type="primary" @click="router.push('/login')">登录后参与回答</el-button>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getQuestionDetail, deleteQuestion, getAnswerList, createAnswer, deleteAnswer } from '@/api/question'
import { UserFilled } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const questionId = route.params.id
const question = ref(null)
const answers = ref([])
const replyContent = ref('')
const replyLoading = ref(false)

const isAuthor = computed(() => {
  if (!question.value || !userStore.user) return false
  return question.value.userId === userStore.user.id
})

const canDeleteAnswer = (ans) => {
  if (!userStore.user) return false
  return ans.userId === userStore.user.id || userStore.isAdmin
}

const formatDate = (str) => str ? str.substring(0, 16).replace('T', ' ') : ''
const renderContent = (text) => text ? text.replace(/\n/g, '<br/>') : ''

const loadQuestion = async () => {
  try {
    const res = await getQuestionDetail(questionId)
    question.value = res.data
  } catch (e) {
    ElMessage.error('问题不存在或已被删除')
    router.back()
  }
}

const loadAnswers = async () => {
  try {
    const res = await getAnswerList({ questionId })
    answers.value = res.data || []
  } catch (e) {}
}

const handleReply = async () => {
  if (!replyContent.value.trim()) {
    ElMessage.warning('请输入回答内容')
    return
  }
  replyLoading.value = true
  try {
    await createAnswer({ questionId, content: replyContent.value })
    ElMessage.success('回答成功')
    replyContent.value = ''
    loadAnswers()
  } catch (e) {} finally {
    replyLoading.value = false
  }
}

const handleDeleteQuestion = () => {
  ElMessageBox.confirm('确定删除此问题吗？所有回答也会被删除', '警告', {
    confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning'
  }).then(async () => {
    await deleteQuestion(questionId)
    ElMessage.success('已删除')
    router.back()
  }).catch(() => {})
}

const handleDeleteAnswer = (id) => {
  ElMessageBox.confirm('确定删除此回答吗？', '提示', {
    confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning'
  }).then(async () => {
    await deleteAnswer(id)
    ElMessage.success('已删除')
    loadAnswers()
  }).catch(() => {})
}

onMounted(() => {
  loadQuestion()
  loadAnswers()
})
</script>

<style scoped>
.question-detail-page { max-width: 800px; }
.question-header h1 { font-size: 22px; margin-bottom: 12px; }
.post-meta {
  display: flex; align-items: center; gap: 16px;
  font-size: 13px; color: var(--text-secondary);
}
.post-meta span { display: flex; align-items: center; gap: 4px; }
.post-content {
  font-size: 15px; line-height: 1.8; color: var(--text-regular);
  min-height: 100px;
}
.post-actions { margin-top: 12px; }
.answer-section {
  margin-top: 24px;
}
.section-title {
  display: flex; align-items: center; gap: 6px;
  font-size: 18px; margin-bottom: 16px;
}
.answer-item {
  background: #fff;
  border-radius: 10px;
  padding: 16px 20px;
  margin-bottom: 12px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.answer-header {
  display: flex; align-items: center; gap: 10px; margin-bottom: 10px;
}
.answer-meta { flex: 1; }
.answer-author { font-size: 14px; font-weight: 500; }
.answer-time { font-size: 12px; color: var(--text-secondary); margin-left: 8px; }
.answer-content { font-size: 14px; line-height: 1.7; color: var(--text-regular); }
.reply-card { margin-top: 20px; }
.reply-card h3 { margin-bottom: 12px; }
</style>
