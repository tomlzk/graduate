import request from '@/utils/request'

// 公告列表
export const getAnnouncementList = (params) => request.get('/announcement/list', { params })

// 公告详情
export const getAnnouncementDetail = (id) => request.get(`/announcement/detail/${id}`)
