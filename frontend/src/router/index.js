import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/UserLayout.vue'),
    children: [
      { path: '', name: 'Home', component: () => import('@/views/Home.vue') },
      { path: 'module/:id', name: 'ModuleDetail', component: () => import('@/views/ModuleDetail.vue') },
      { path: 'module/:moduleId/post/create', name: 'PostCreate', component: () => import('@/views/PostEdit.vue'), meta: { requireAuth: true } },
      { path: 'post/:id/edit', name: 'PostEdit', component: () => import('@/views/PostEdit.vue'), meta: { requireAuth: true } },
      { path: 'post/:id', name: 'PostDetail', component: () => import('@/views/PostDetail.vue') },
      { path: 'module/:moduleId/question/create', name: 'QuestionCreate', component: () => import('@/views/QuestionEdit.vue'), meta: { requireAuth: true } },
      { path: 'question/:id', name: 'QuestionDetail', component: () => import('@/views/QuestionDetail.vue') },
      { path: 'profile', name: 'Profile', component: () => import('@/views/Profile.vue'), meta: { requireAuth: true } },
      { path: 'announcement/:id', name: 'AnnouncementDetail', component: () => import('@/views/AnnouncementDetail.vue') },
    ]
  },
  { path: '/login', name: 'Login', component: () => import('@/views/Login.vue') },
  { path: '/register', name: 'Register', component: () => import('@/views/Register.vue') },
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { requireAuth: true, requireAdmin: true },
    children: [
      { path: '', redirect: '/admin/user' },
      { path: 'user', name: 'AdminUser', component: () => import('@/views/admin/UserManage.vue') },
      { path: 'post', name: 'AdminPost', component: () => import('@/views/admin/PostManage.vue') },
      { path: 'question', name: 'AdminQuestion', component: () => import('@/views/admin/QuestionManage.vue') },
      { path: 'announcement', name: 'AdminAnnouncement', component: () => import('@/views/admin/AnnouncementManage.vue') },
      { path: 'module', name: 'AdminModule', component: () => import('@/views/admin/ModuleManage.vue') },
    ]
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  if (to.meta.requireAuth && !userStore.isLoggedIn) {
    next({ path: '/login', query: { redirect: to.fullPath } })
  } else if (to.meta.requireAdmin && !userStore.isAdmin) {
    next('/')
  } else {
    next()
  }
})

export default router
