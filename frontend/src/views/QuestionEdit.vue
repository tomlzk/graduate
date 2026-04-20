<template>
  <div class="page-container question-edit-page">
    <el-card shadow="never">
      <template #header>
        <h2>发起提问</h2>
      </template>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px" style="max-width:700px">
        <el-form-item label="所属模块">
          <el-tag>{{ moduleName }}</el-tag>
        </el-form-item>
        <el-form-item label="问题标题" prop="title">
          <el-input v-model="form.title" placeholder="简明概括你的问题" maxlength="100" show-word-limit clearable />
        </el-form-item>
        <el-form-item label="问题描述" prop="content">
          <el-input v-model="form.content" type="textarea" :rows="10" placeholder="详细描述你的问题，方便他人回答" maxlength="5000" show-word-limit />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">提交问题</el-button>
          <el-button @click="router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { createQuestion } from '@/api/question'
import { getModuleList } from '@/api/module'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const formRef = ref()
const loading = ref(false)
const moduleId = ref(route.params.moduleId)
const moduleName = ref('')

const form = reactive({ title: '', content: '' })
const rules = {
  title: [{ required: true, message: '请输入问题标题', trigger: 'blur' }],
  content: [{ required: true, message: '请描述你的问题', trigger: 'blur' }]
}

onMounted(async () => {
  try {
    const res = await getModuleList()
    const mod = (res.data || []).find(m => m.id == moduleId.value)
    moduleName.value = mod?.name || '未知模块'
  } catch (e) {}
})

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    const res = await createQuestion({ moduleId: moduleId.value, title: form.title, content: form.content })
    ElMessage.success('提问成功')
    router.push(`/question/${res.data?.id || res.data}`)
  } catch (e) {} finally {
    loading.value = false
  }
}
</script>

<style scoped>
.question-edit-page { max-width: 800px; }
</style>
