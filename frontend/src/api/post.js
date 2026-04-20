import request from '@/utils/request'

// 帖子列表
export const getPostList = (params) => request.get('/post/list', { params })

// 帖子详情
export const getPostDetail = (id) => request.get(`/post/detail/${id}`)

// 创建帖子
export const createPost = (data) => request.post('/post', data)

// 修改帖子
export const updatePost = (id, data) => request.put(`/post/${id}`, data)

// 删除帖子
export const deletePost = (id) => request.delete(`/post/${id}`)
