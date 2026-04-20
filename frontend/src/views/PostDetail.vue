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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getPostDetail, deletePost } from '@/api/post'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const post = ref(null)

const postId = route.params.id

const isAuthor = computed(() => {
  if (!post.value || !userStore.user) return false
  return post.value.userId === userStore.user.id
})

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

onMounted(loadPost)
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
</style>
