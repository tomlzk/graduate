import request from '@/utils/request'

// 问题列表
export const getQuestionList = (params) => request.get('/question/list', { params })

// 问题详情
export const getQuestionDetail = (id) => request.get(`/question/detail/${id}`)

// 创建问题
export const createQuestion = (data) => request.post('/question', data)

// 删除问题
export const deleteQuestion = (id) => request.delete(`/question/${id}`)

// 回答列表
export const getAnswerList = (params) => request.get('/answer/list', { params })

// 创建回答
export const createAnswer = (data) => request.post('/answer', data)

// 删除回答
export const deleteAnswer = (id) => request.delete(`/answer/${id}`)
