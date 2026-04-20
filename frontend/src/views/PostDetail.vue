<template>
  <div class="page-container post-detail-page" v-if="post">
    <el-card shadow="never">
      <div class="post-header">
        <h1>{{ post.title }}</h1>
        <div class="post-meta">
          <span><el-icon><User /></el-icon> {{ post.authorName || '匿名' }}</span>
          <span><el-icon><Calendar /></el-icon> {{ formatDate(post.createTime) }}</span>
          <el-tag size="small">{{ post.moduleName || '帖子' }}</el-tag>
        </div>
      </div>
      <el-divider />
      <div class="post-content" v-html="renderContent(post.content)"></div>
      <el-divider />
      <div class="post-actions">
        <el-button v-if="isAuthor" type="primary" text @click="router.push(`/post/${post.id}/edit`)">
          <el-icon><Edit /></el-icon> 编辑
        </el-button>
        <el-button v-if="isAuthor" type="danger" text @click="handleDelete">
          <el-icon><Delete /></el-icon> 删除
        </el-button>
        <el-button text @click="router.back()">
          <el-icon><Back /></el-icon> 返回
        </el-button>
      </div>
    </el-card>

    <!-- 回复区 -->
    <div class="reply-section">
      <h3 class="section-title">
        <el-icon><ChatLineSquare /></el-icon>
        {{ replies.length }} 条回复
      </h3>

      <el-empty v-if="!replies.length" description="还没有回复，快来抢沙发吧" />

      <div v-for="reply in replies" :key="reply.id" class="reply-item">
        <div class="reply-floor-badge">#{{ reply.floor }}楼</div>
        <div class="reply-header">
          <el-avatar :size="32" :icon="UserFilled" />
          <div class="reply-meta">
            <span class="reply-author">{{ reply.nickname || reply.username || '匿名' }}</span>
            <span class="reply-time">{{ formatDate(reply.createTime) }}</span>
          </div>
          <el-button
            v-if="canDeleteReply(reply)"
            type="danger" text size="small"
            @click="handleDeleteReply(reply.id)"
          >删除</el-button>
        </div>
        <div class="reply-content" v-html="renderContent(reply.content)"></div>
      </div>
    </div>

    <!-- 回复框 -->
    <el-card v-if="userStore.isLoggedIn" shadow="never" class="reply-card">
      <h3>发表回复</h3>
      <el-input v-model="replyContent" type="textarea" :rows="4" placeholder="写下你的回复..." maxlength="3000" show-word-limit />
      <el-button type="primary" :loading="replyLoading" style="margin-top:12px" @click="handleReply">
        提交回复
      </el-button>
    </el-card>
    <el-card v-else shadow="never" class="reply-card">
      <el-button type="primary" @click="router.push('/login')">登录后参与回复</el-button>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getPostDetail, deletePost, getPostReplyList, createPostReply, deletePostReply } from '@/api/post'
import { UserFilled } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const post = ref(null)
const replies = ref([])
const replyContent = ref('')
const replyLoading = ref(false)

const postId = route.params.id

const isAuthor = computed(() => {
  if (!post.value || !userStore.user) return false
  return post.value.userId === userStore.user.id
})

const canDeleteReply = (reply) => {
  if (!userStore.user) return false
  return reply.userId === userStore.user.id || userStore.isAdmin
}

const formatDate = (str) => str ? str.substring(0, 16).replace('T', ' ') : ''
const renderContent = (text) => text ? text.replace(/\n/g, '<br/>') : ''

const loadPost = async () => {
  try {
    const res = await getPostDetail(postId)
    post.value = res.data
  } catch (e) {
    ElMessage.error('帖子不存在或已被删除')
    router.back()
  }
}

const loadReplies = async () => {
  try {
    const res = await getPostReplyList(postId)
    replies.value = res.data || []
  } catch (e) {}
}

const handleReply = async () => {
  if (!replyContent.value.trim()) {
    ElMessage.warning('请输入回复内容')
    return
  }
  replyLoading.value = true
  try {
    await createPostReply({ postId, content: replyContent.value })
    ElMessage.success('回复成功')
    replyContent.value = ''
    loadReplies()
  } catch (e) {} finally {
    replyLoading.value = false
  }
}

const handleDelete = () => {
  ElMessageBox.confirm('确定删除此帖子吗？此操作不可撤销', '警告', {
    confirmButtonText: '确定删除',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    await deletePost(postId)
    ElMessage.success('已删除')
    router.back()
  }).catch(() => {})
}

const handleDeleteReply = (id) => {
  ElMessageBox.confirm('确定删除此回复吗？', '提示', {
    confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning'
  }).then(async () => {
    await deletePostReply(id)
    ElMessage.success('已删除')
    loadReplies()
  }).catch(() => {})
}

onMounted(() => {
  loadPost()
  loadReplies()
})
</script>

<style scoped>
.post-detail-page { max-width: 800px; }
.post-header h1 { font-size: 22px; margin-bottom: 12px; }
.post-meta {
  display: flex; align-items: center; gap: 16px;
  font-size: 13px; color: var(--text-secondary);
}
.post-meta span { display: flex; align-items: center; gap: 4px; }
.post-content {
  font-size: 15px; line-height: 1.8; color: var(--text-regular);
  min-height: 200px;
}
.post-actions { display: flex; gap: 8px; }
.reply-section { margin-top: 24px; }
.section-title {
  display: flex; align-items: center; gap: 6px;
  font-size: 18px; margin-bottom: 16px;
}
.reply-item {
  background: #fff;
  border-radius: 10px;
  padding: 16px 20px;
  margin-bottom: 12px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  position: relative;
}
.reply-floor-badge {
  position: absolute;
  top: 12px;
  right: 16px;
  font-size: 13px;
  color: #409eff;
  font-weight: 500;
  background: #ecf5ff;
  padding: 2px 8px;
  border-radius: 4px;
}
.reply-header {
  display: flex; align-items: center; gap: 10px; margin-bottom: 10px;
}
.reply-meta { flex: 1; }
.reply-author { font-size: 14px; font-weight: 500; }
.reply-time { font-size: 12px; color: var(--text-secondary); margin-left: 8px; }
.reply-content { font-size: 14px; line-height: 1.7; color: var(--text-regular); }
.reply-card { margin-top: 20px; }
.reply-card h3 { margin-bottom: 12px; }
</style>
