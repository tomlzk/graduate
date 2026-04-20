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

// ===== 帖子回复 =====
// 回复列表
export const getPostReplyList = (postId) => request.get('/post-reply/list', { params: { postId } })

// 创建回复
export const createPostReply = (data) => request.post('/post-reply', data)

// 删除回复
export const deletePostReply = (id) => request.delete(`/post-reply/${id}`)
