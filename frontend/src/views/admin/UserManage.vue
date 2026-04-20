<template>
  <div>
    <el-card shadow="never">
      <template #header>
        <div style="display:flex;align-items:center;justify-content:space-between">
          <h3>用户管理</h3>
          <el-input v-model="keyword" placeholder="搜索用户名/昵称" clearable style="width:240px" @clear="loadUsers" @keyup.enter="loadUsers">
            <template #append>
              <el-button @click="loadUsers"><el-icon><Search /></el-icon></el-button>
            </template>
          </el-input>
        </div>
      </template>
      <el-table :data="users" stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="username" label="用户名" width="140" />
        <el-table-column prop="nickname" label="昵称" width="140" />
        <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="row.role === 'ADMIN' ? 'danger' : ''">{{ row.role === 'ADMIN' ? '管理员' : '用户' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="注册时间" width="180">
          <template #default="{ row }">{{ formatDate(row.createTime) }}</template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="handleResetPwd(row)">重置密码</el-button>
            <el-popconfirm title="确定删除该用户吗？" @confirm="handleDelete(row.id)">
              <template #reference>
                <el-button size="small" type="danger" :disabled="row.role === 'ADMIN'">删除</el-button>
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
        @current-change="loadUsers"
        style="margin-top:16px;justify-content:flex-end"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUserList, deleteUser, resetUserPassword } from '@/api/admin'
import { ElMessage } from 'element-plus'

const users = ref([])
const loading = ref(false)
const keyword = ref('')
const page = ref(1)
const pageSize = 15
const total = ref(0)

const formatDate = (str) => str ? str.substring(0, 16).replace('T', ' ') : ''

const loadUsers = async () => {
  loading.value = true
  try {
    const res = await getUserList({ keyword: keyword.value, page: page.value, size: pageSize })
    users.value = res.data?.records || res.data || []
    total.value = res.data?.total || 0
  } catch (e) {} finally {
    loading.value = false
  }
}

const handleResetPwd = async (row) => {
  try {
    await resetUserPassword(row.id)
    ElMessage.success(`已重置 ${row.username} 的密码为 123456`)
  } catch (e) {}
}

const handleDelete = async (id) => {
  try {
    await deleteUser(id)
    ElMessage.success('已删除')
    loadUsers()
  } catch (e) {}
}

onMounted(loadUsers)
</script>
