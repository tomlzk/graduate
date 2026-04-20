<template>
  <div class="register-page">
    <div class="login-bg"></div>
    <div class="register-card">
      <div class="login-header">
        <el-icon :size="40" color="#409eff"><Reading /></el-icon>
        <h2>创建新账号</h2>
        <p>加入考证服务平台，开启你的备考之旅</p>
      </div>
      <el-form ref="formRef" :model="form" :rules="rules" size="large" label-position="top">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="4-20位字母或数字" :prefix-icon="User" clearable />
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="form.nickname" placeholder="给自己取个昵称吧（选填，默认为用户名）" :prefix-icon="UserFilled" clearable />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="至少6位密码" :prefix-icon="Lock" show-password clearable />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="form.confirmPassword" type="password" placeholder="再次输入密码" :prefix-icon="Lock" show-password clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" style="width:100%" @click="handleRegister">
            注 册
          </el-button>
        </el-form-item>
      </el-form>
      <div class="login-footer">
        已有账号？
        <el-link type="primary" @click="router.push('/login')">去登录</el-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api/user'
import { User, UserFilled, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const formRef = ref()
const loading = ref(false)

const form = reactive({
  username: '',
  nickname: '',
  password: '',
  confirmPassword: ''
})

const validateConfirm = (rule, value, callback) => {
  if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 4, max: 20, message: '用户名长度4-20位', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_]+$/, message: '用户名只能包含字母、数字和下划线', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirm, trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await register({
      username: form.username,
      password: form.password,
      nickname: form.nickname || form.username
    })
    ElMessage.success('注册成功，即将跳转登录页')
    setTimeout(() => router.push('/login'), 1000)
  } catch (e) {
    // 错误已在拦截器处理
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}
.login-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  z-index: 0;
}
.login-bg::after {
  content: '';
  position: absolute;
  inset: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}
.register-card {
  position: relative;
  z-index: 1;
  width: 440px;
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 40px 40px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}
.login-header {
  text-align: center;
  margin-bottom: 24px;
}
.login-header h2 {
  margin: 12px 0 8px;
  font-size: 24px;
  color: var(--text-primary);
}
.login-header p {
  color: var(--text-secondary);
  font-size: 14px;
}
.login-footer {
  text-align: center;
  font-size: 14px;
  color: var(--text-regular);
}
</style>
