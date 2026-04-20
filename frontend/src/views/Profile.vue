<template>
  <div class="page-container profile-page">
    <el-row :gutter="24">
      <!-- 左侧基本信息 -->
      <el-col :span="8">
        <el-card shadow="never">
          <div class="profile-avatar">
            <el-avatar :size="80" :icon="UserFilled" />
            <h3>{{ userStore.nickname }}</h3>
            <el-tag v-if="userStore.isAdmin" type="danger" size="small">管理员</el-tag>
            <el-tag v-else size="small">普通用户</el-tag>
          </div>
          <el-descriptions :column="1" border size="small" style="margin-top:20px">
            <el-descriptions-item label="用户名">{{ profile.username }}</el-descriptions-item>
            <el-descriptions-item label="注册时间">{{ formatDate(profile.createTime) }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>

      <!-- 右侧信息管理 -->
      <el-col :span="16">
        <el-card shadow="never">
          <el-tabs v-model="activeTab">
            <!-- 修改资料 -->
            <el-tab-pane label="修改资料" name="info">
              <el-form ref="infoRef" :model="infoForm" :rules="infoRules" label-width="80px" style="max-width:450px">
                <el-form-item label="昵称" prop="nickname">
                  <el-input v-model="infoForm.nickname" placeholder="输入新昵称" clearable />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" :loading="infoLoading" @click="handleUpdateInfo">保存修改</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>

            <!-- 修改密码 -->
            <el-tab-pane label="修改密码" name="password">
              <el-form ref="pwdRef" :model="pwdForm" :rules="pwdRules" label-width="100px" style="max-width:450px">
                <el-form-item label="原密码" prop="oldPassword">
                  <el-input v-model="pwdForm.oldPassword" type="password" show-password clearable />
                </el-form-item>
                <el-form-item label="新密码" prop="newPassword">
                  <el-input v-model="pwdForm.newPassword" type="password" show-password clearable />
                </el-form-item>
                <el-form-item label="确认新密码" prop="confirmPassword">
                  <el-input v-model="pwdForm.confirmPassword" type="password" show-password clearable />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" :loading="pwdLoading" @click="handleChangePwd">修改密码</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { getProfile, updateProfile, changePassword } from '@/api/user'
import { UserFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const activeTab = ref('info')
const profile = ref({})

const infoRef = ref()
const infoForm = reactive({ nickname: '' })
const infoLoading = ref(false)
const infoRules = {
  nickname: [{ required: true, message: '请输入昵称', trigger: 'blur' }]
}

const pwdRef = ref()
const pwdForm = reactive({ oldPassword: '', newPassword: '', confirmPassword: '' })
const pwdLoading = ref(false)
const pwdRules = {
  oldPassword: [{ required: true, message: '请输入原密码', trigger: 'blur' }],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (r, v, cb) => v !== pwdForm.newPassword ? cb(new Error('两次密码不一致')) : cb(),
      trigger: 'blur'
    }
  ]
}

const formatDate = (str) => str ? str.substring(0, 10) : ''

const loadProfile = async () => {
  try {
    const res = await getProfile()
    profile.value = res.data
    infoForm.nickname = res.data.nickname || ''
  } catch (e) {}
}

const handleUpdateInfo = async () => {
  const valid = await infoRef.value.validate().catch(() => false)
  if (!valid) return
  infoLoading.value = true
  try {
    await updateProfile({ nickname: infoForm.nickname })
    userStore.updateUser({ nickname: infoForm.nickname })
    ElMessage.success('资料已更新')
    loadProfile()
  } catch (e) {} finally {
    infoLoading.value = false
  }
}

const handleChangePwd = async () => {
  const valid = await pwdRef.value.validate().catch(() => false)
  if (!valid) return
  pwdLoading.value = true
  try {
    await changePassword({
      oldPassword: pwdForm.oldPassword,
      newPassword: pwdForm.newPassword
    })
    ElMessage.success('密码已修改，请重新登录')
    userStore.logout()
    setTimeout(() => window.location.href = '/login', 1000)
  } catch (e) {} finally {
    pwdLoading.value = false
  }
}

onMounted(loadProfile)
</script>

<style scoped>
.profile-page {
  max-width: 960px;
}
.profile-avatar {
  text-align: center;
  padding: 20px 0;
}
.profile-avatar h3 {
  margin: 12px 0 8px;
}
</style>
