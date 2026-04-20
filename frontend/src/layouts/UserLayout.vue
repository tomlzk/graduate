<template>
  <div class="user-layout">
    <!-- 顶部导航 -->
    <el-header class="navbar">
      <div class="navbar-inner">
        <div class="navbar-left" @click="router.push('/')">
          <el-icon :size="28" color="#409eff"><Reading /></el-icon>
          <span class="logo-text">考证服务平台</span>
        </div>
        <div class="navbar-right">
          <el-button text @click="router.push('/')">
            <el-icon><HomeFilled /></el-icon> 首页
          </el-button>
          <template v-if="userStore.isLoggedIn">
            <el-dropdown trigger="click" @command="handleCommand">
              <span class="user-info">
                <el-avatar :size="32" :icon="UserFilled" />
                <span class="username">{{ userStore.nickname }}</span>
                <el-icon><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">
                    <el-icon><User /></el-icon> 个人中心
                  </el-dropdown-item>
                  <el-dropdown-item v-if="userStore.isAdmin" command="admin" divided>
                    <el-icon><Setting /></el-icon> 管理后台
                  </el-dropdown-item>
                  <el-dropdown-item command="logout" divided>
                    <el-icon><SwitchButton /></el-icon> 退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <el-button type="primary" @click="router.push('/login')">登录</el-button>
            <el-button @click="router.push('/register')">注册</el-button>
          </template>
        </div>
      </div>
    </el-header>

    <!-- 主内容 -->
    <el-main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>

    <!-- 底部 -->
    <el-footer class="footer">
      <span>© 2026 高校学生考证服务系统 · 毕业设计</span>
    </el-footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { UserFilled } from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const handleCommand = (cmd) => {
  if (cmd === 'profile') router.push('/profile')
  else if (cmd === 'admin') router.push('/admin')
  else if (cmd === 'logout') {
    ElMessageBox.confirm('确定退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      userStore.logout()
      router.push('/')
    }).catch(() => {})
  }
}
</script>

<style scoped>
.user-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.navbar {
  background: #fff;
  box-shadow: 0 1px 8px rgba(0,0,0,0.08);
  position: sticky;
  top: 0;
  z-index: 100;
  height: 60px;
  padding: 0;
}
.navbar-inner {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}
.navbar-left {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
}
.logo-text {
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #409eff, #67c23a);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.navbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 8px;
  transition: background 0.2s;
}
.user-info:hover {
  background: #f5f7fa;
}
.username {
  font-size: 14px;
  color: var(--text-regular);
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.main-content {
  flex: 1;
  padding: 0;
}
.footer {
  text-align: center;
  color: var(--text-secondary);
  font-size: 13px;
  padding: 20px;
  height: auto;
}
</style>
