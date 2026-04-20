<template>
  <div class="page-container post-edit-page">
    <el-card shadow="never">
      <template #header>
        <h2>{{ isEdit ? '编辑帖子' : '发表帖子' }}</h2>
      </template>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px" style="max-width:700px">
        <el-form-item label="所属模块">
          <el-tag>{{ moduleName }}</el-tag>
        </el-form-item>
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入帖子标题" maxlength="100" show-word-limit clearable />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="form.content" type="textarea" :rows="12" placeholder="请输入帖子内容" maxlength="5000" show-word-limit />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">
            {{ isEdit ? '保存修改' : '发表帖子' }}
          </el-button>
          <el-button @click="router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getPostDetail, createPost, updatePost } from '@/api/post'
import { getModuleList } from '@/api/module'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const formRef = ref()
const loading = ref(false)

const moduleId = ref(route.params.moduleId)
const postId = ref(route.params.id)
const isEdit = computed(() => !!postId.value)
const moduleName = ref('')

const form = reactive({
  title: '',
  content: ''
})
const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
}

const loadModuleName = async () => {
  try {
    const res = await getModuleList()
    const mod = (res.data || []).find(m => m.id == moduleId.value)
    moduleName.value = mod?.name || '未知模块'
  } catch (e) {}
}

const loadPost = async () => {
  if (!isEdit.value) return
  try {
    const res = await getPostDetail(postId.value)
    form.title = res.data.title
    form.content = res.data.content
    moduleId.value = res.data.moduleId
  } catch (e) {}
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    if (isEdit.value) {
      await updatePost(postId.value, { title: form.title, content: form.content })
      ElMessage.success('修改成功')
      router.push(`/post/${postId.value}`)
    } else {
      const res = await createPost({ moduleId: moduleId.value, title: form.title, content: form.content })
      ElMessage.success('发表成功')
      router.push(`/post/${res.data?.id || res.data}`)
    }
  } catch (e) {} finally {
    loading.value = false
  }
}

onMounted(() => {
  loadModuleName()
  loadPost()
})
</script>

<style scoped>
.post-edit-page { max-width: 800px; }
</style>
