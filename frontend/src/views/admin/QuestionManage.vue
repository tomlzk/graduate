<template>
  <div>
    <el-card shadow="never">
      <template #header>
        <div style="display:flex;align-items:center;justify-content:space-between">
          <h3>问答管理</h3>
          <el-input v-model="keyword" placeholder="搜索问题标题" clearable style="width:240px" @clear="loadQuestions" @keyup.enter="loadQuestions">
            <template #append>
              <el-button @click="loadQuestions"><el-icon><Search /></el-icon></el-button>
            </template>
          </el-input>
        </div>
      </template>
      <el-table :data="questions" stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
        <el-table-column prop="authorName" label="提问人" width="120" />
        <el-table-column prop="moduleName" label="模块" width="120" />
        <el-table-column prop="createTime" label="提问时间" width="180">
          <template #default="{ row }">{{ formatDate(row.createTime) }}</template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="100">
          <template #default="{ row }">
            <el-popconfirm title="确定删除该问题及所有回答吗？" @confirm="handleDelete(row.id)">
              <template #reference>
                <el-button size="small" type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        v-if="total > pageSize"
        layout="total, prev, pager, next"
        :total="total" :page-size="pageSize"
        v-model:current-page="page"
        @current-change="loadQuestions"
        style="margin-top:16px;justify-content:flex-end"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminGetQuestionList, adminDeleteQuestion } from '@/api/admin'
import { ElMessage } from 'element-plus'

const questions = ref([])
const loading = ref(false)
const keyword = ref('')
const page = ref(1)
const pageSize = 15
const total = ref(0)

const formatDate = (str) => str ? str.substring(0, 16).replace('T', ' ') : ''

const loadQuestions = async () => {
  loading.value = true
  try {
    const res = await adminGetQuestionList({ keyword: keyword.value, page: page.value, size: pageSize })
    questions.value = res.data?.records || res.data || []
    total.value = res.data?.total || 0
  } catch (e) {} finally {
    loading.value = false
  }
}

const handleDelete = async (id) => {
  try {
    await adminDeleteQuestion(id)
    ElMessage.success('已删除')
    loadQuestions()
  } catch (e) {}
}

onMounted(loadQuestions)
</script>
