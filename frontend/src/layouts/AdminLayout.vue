<template>
  <div class="admin-layout">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside :width="isCollapse ? '64px' : '220px'" class="sidebar">
        <div class="sidebar-header">
          <el-icon :size="24" color="#fff"><Setting /></el-icon>
          <span v-show="!isCollapse" class="sidebar-title">管理后台</span>
        </div>
        <el-menu
          :default-active="route.path"
          router
          :collapse="isCollapse"
          background-color="#1d1e1f"
          text-color="#bbb"
          active-text-color="#409eff"
          class="sidebar-menu"
        >
          <el-menu-item index="/admin/user">
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/post">
            <el-icon><Document /></el-icon>
            <span>帖子管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/question">
            <el-icon><ChatDotSquare /></el-icon>
            <span>问答管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/announcement">
            <el-icon><Bell /></el-icon>
            <span>公告管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/module">
            <el-icon><Grid /></el-icon>
            <span>模块管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 右侧内容 -->
      <el-container>
        <el-header class="admin-header">
          <div class="header-left">
            <el-button text @click="isCollapse = !isCollapse">
              <el-icon :size="20"><Fold v-if="!isCollapse" /><Expand v-else /></el-icon>
            </el-button>
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item>{{ currentTitle }}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          <div class="header-right">
            <el-button text @click="router.push('/')">
              <el-icon><HomeFilled /></el-icon> 返回前台
            </el-button>
            <el-dropdown trigger="click" @command="handleCommand">
              <span class="admin-user">
                <el-avatar :size="28" :icon="UserFilled" />
                <span>{{ userStore.nickname }}</span>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="logout">
                    <el-icon><SwitchButton /></el-icon> 退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        <el-main class="admin-main">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { UserFilled } from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const isCollapse = ref(false)

const titleMap = {
  '/admin/user': '用户管理',
  '/admin/post': '帖子管理',
  '/admin/question': '问答管理',
  '/admin/announcement': '公告管理',
  '/admin/module': '模块管理',
}
const currentTitle = computed(() => titleMap[route.path] || '管理后台')

const handleCommand = (cmd) => {
  if (cmd === 'logout') {
    ElMessageBox.confirm('确定退出登录吗？', '提示', {
      confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning'
    }).then(() => {
      userStore.logout()
      router.push('/login')
    }).catch(() => {})
  }
}
</script>

<style scoped>
.admin-layout {
  height: 100vh;
}
.admin-layout > .el-container {
  height: 100%;
}
.sidebar {
  background: #1d1e1f;
  transition: width 0.3s;
  overflow: hidden;
}
.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  border-bottom: 1px solid #333;
}
.sidebar-title {
  color: #fff;
  font-size: 16px;
  font-weight: 600;
}
.sidebar-menu {
  border-right: none;
}
.admin-header {
  background: #fff;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  padding: 0 20px;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.admin-user {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
}
.admin-main {
  background: #f0f2f5;
  padding: 20px;
}
</style>
