<template>
  <div>
    <el-card shadow="never">
      <template #header>
        <div style="display:flex;align-items:center;justify-content:space-between">
          <h3>公告管理</h3>
          <el-button type="primary" @click="openDialog()">
            <el-icon><Plus /></el-icon> 新增公告
          </el-button>
        </div>
      </template>
      <el-table :data="list" stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
        <el-table-column prop="createTime" label="发布时间" width="180">
          <template #default="{ row }">{{ formatDate(row.createTime) }}</template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="180">
          <template #default="{ row }">
            <el-button size="small" @click="openDialog(row)">编辑</el-button>
            <el-popconfirm title="确定删除此公告吗？" @confirm="handleDelete(row.id)">
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
        @current-change="loadList"
        style="margin-top:16px;justify-content:flex-end"
      />
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="editId ? '编辑公告' : '新增公告'" width="600px" destroy-on-close>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="公告标题" maxlength="100" clearable />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="form.content" type="textarea" :rows="8" placeholder="公告内容" maxlength="5000" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { adminGetAnnouncementList, createAnnouncement, updateAnnouncement, deleteAnnouncement } from '@/api/admin'
import { ElMessage } from 'element-plus'

const list = ref([])
const loading = ref(false)
const page = ref(1)
const pageSize = 15
const total = ref(0)

const dialogVisible = ref(false)
const editId = ref(null)
const formRef = ref()
const submitLoading = ref(false)
const form = reactive({ title: '', content: '' })
const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
}

const formatDate = (str) => str ? str.substring(0, 16).replace('T', ' ') : ''

const loadList = async () => {
  loading.value = true
  try {
    const res = await adminGetAnnouncementList({ page: page.value, size: pageSize })
    list.value = res.data?.records || res.data || []
    total.value = res.data?.total || 0
  } catch (e) {} finally {
    loading.value = false
  }
}

const openDialog = (row) => {
  if (row) {
    editId.value = row.id
    form.title = row.title
    form.content = row.content
  } else {
    editId.value = null
    form.title = ''
    form.content = ''
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  submitLoading.value = true
  try {
    if (editId.value) {
      await updateAnnouncement(editId.value, { title: form.title, content: form.content })
      ElMessage.success('修改成功')
    } else {
      await createAnnouncement({ title: form.title, content: form.content })
      ElMessage.success('发布成功')
    }
    dialogVisible.value = false
    loadList()
  } catch (e) {} finally {
    submitLoading.value = false
  }
}

const handleDelete = async (id) => {
  try {
    await deleteAnnouncement(id)
    ElMessage.success('已删除')
    loadList()
  } catch (e) {}
}

onMounted(loadList)
</script>
