import request from '@/utils/request'

// 获取考试模块列表
export const getModuleList = () => request.get('/module/list')

// 获取考试信息列表
export const getExamInfoList = (moduleId) => request.get('/exam-info/list', { params: { moduleId } })
