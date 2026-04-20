import request from '@/utils/request'

// ===== 用户管理 =====
export const getUserList = (params) => request.get('/admin/user/list', { params })
export const deleteUser = (id) => request.delete(`/admin/user/${id}`)
export const resetUserPassword = (id) => request.put(`/admin/user/${id}/reset-password`)
export const adminUpdateUser = (id, data) => request.put(`/admin/user/${id}`, data)
export const adminToggleUserStatus = (id) => request.put(`/admin/user/${id}/toggle-status`)

// ===== 帖子管理 =====
export const adminGetPostList = (params) => request.get('/admin/post/list', { params })
export const adminCreatePost = (data) => request.post('/admin/post', data)
export const adminUpdatePost = (id, data) => request.put(`/admin/post/${id}`, data)
export const adminDeletePost = (id) => request.delete(`/admin/post/${id}`)

// ===== 问答管理 =====
export const adminGetQuestionList = (params) => request.get('/admin/question/list', { params })
export const adminDeleteQuestion = (id) => request.delete(`/admin/question/${id}`)
export const adminGetAnswerList = (params) => request.get('/admin/answer/list', { params })
export const adminDeleteAnswer = (id) => request.delete(`/admin/answer/${id}`)

// ===== 公告管理 =====
export const adminGetAnnouncementList = (params) => request.get('/admin/announcement/list', { params })
export const createAnnouncement = (data) => request.post('/admin/announcement', data)
export const updateAnnouncement = (id, data) => request.put(`/admin/announcement/${id}`, data)
export const deleteAnnouncement = (id) => request.delete(`/admin/announcement/${id}`)

// ===== 模块管理 =====
export const adminGetModuleList = () => request.get('/admin/module/list')
export const createModule = (data) => request.post('/admin/module', data)
export const updateModule = (id, data) => request.put(`/admin/module/${id}`, data)
export const deleteModule = (id) => request.delete(`/admin/module/${id}`)
export const adminGetExamInfoList = (params) => request.get('/admin/module/exam-info/list', { params })
export const adminAddExamInfo = (data) => request.post('/admin/module/exam-info', data)
export const adminUpdateExamInfo = (id, data) => request.put(`/admin/module/exam-info/${id}`, data)
export const adminDeleteExamInfo = (id) => request.delete(`/admin/module/exam-info/${id}`)
