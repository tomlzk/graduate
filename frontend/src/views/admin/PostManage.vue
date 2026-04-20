<template>
  <div>
    <el-card shadow="never">
      <template #header>
        <div style="display:flex;align-items:center;justify-content:space-between">
          <h3>帖子管理</h3>
          <el-input v-model="keyword" placeholder="搜索帖子标题" clearable style="width:240px" @clear="loadPosts" @keyup.enter="loadPosts">
            <template #append>
              <el-button @click="loadPosts"><el-icon><Search /></el-icon></el-button>
            </template>
          </el-input>
        </div>
      </template>
      <el-table :data="posts" stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
        <el-table-column prop="authorName" label="作者" width="120" />
        <el-table-column prop="moduleName" label="模块" width="120" />
        <el-table-column prop="viewCount" label="浏览量" width="90" />
        <el-table-column prop="createTime" label="发布时间" width="180">
          <template #default="{ row }">{{ formatDate(row.createTime) }}</template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="160">
          <template #default="{ row }">
            <el-button size="small" @click="openEdit(row)">编辑</el-button>
            <el-popconfirm title="确定删除该帖子吗？" @confirm="handleDelete(row.id)">
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
        @current-change="loadPosts"
        style="margin-top:16px;justify-content:flex-end"
      />
    </el-card>

    <!-- 编辑帖子弹窗 -->
    <el-dialog v-model="editVisible" title="编辑帖子" width="650px" destroy-on-close>
      <el-form ref="editFormRef" :model="editForm" :rules="editRules" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="editForm.title" placeholder="帖子标题" maxlength="200" clearable />
        </el-form-item>
        <el-form-item label="模块" prop="moduleId">
          <el-select v-model="editForm.moduleId" placeholder="选择模块">
            <el-option v-for="m in modules" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="editForm.content" type="textarea" :rows="10" placeholder="帖子内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" :loading="editLoading" @click="handleEditSubmit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { adminGetPostList, adminUpdatePost, adminDeletePost } from '@/api/admin'
import { getModuleList } from '@/api/module'
import { ElMessage } from 'element-plus'

const posts = ref([])
const loading = ref(false)
const keyword = ref('')
const page = ref(1)
const pageSize = 15
const total = ref(0)
const modules = ref([])

const editVisible = ref(false)
const editLoading = ref(false)
const editFormRef = ref()
const editId = ref(null)
const editForm = reactive({ title: '', content: '', moduleId: null })
const editRules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  moduleId: [{ required: true, message: '请选择模块', trigger: 'change' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
}

const formatDate = (str) => str ? str.substring(0, 16).replace('T', ' ') : ''

const loadPosts = async () => {
  loading.value = true
  try {
    const res = await adminGetPostList({ keyword: keyword.value, page: page.value, size: pageSize })
    posts.value = res.data?.records || res.data || []
    total.value = res.data?.total || 0
  } catch (e) {} finally {
    loading.value = false
  }
}

const loadModules = async () => {
  try {
    const res = await getModuleList()
    modules.value = res.data || []
  } catch (e) {}
}

const openEdit = (row) => {
  editId.value = row.id
  editForm.title = row.title
  editForm.content = row.content
  editForm.moduleId = row.moduleId
  editVisible.value = true
}

const handleEditSubmit = async () => {
  const valid = await editFormRef.value.validate().catch(() => false)
  if (!valid) return
  editLoading.value = true
  try {
    await adminUpdatePost(editId.value, {
      title: editForm.title,
      content: editForm.content,
      moduleId: editForm.moduleId
    })
    ElMessage.success('修改成功')
    editVisible.value = false
    loadPosts()
  } catch (e) {} finally {
    editLoading.value = false
  }
}

const handleDelete = async (id) => {
  try {
    await adminDeletePost(id)
    ElMessage.success('已删除')
    loadPosts()
  } catch (e) {}
}

onMounted(() => {
  loadPosts()
  loadModules()
})
</script>
