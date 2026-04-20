import request from '@/utils/request'

// 用户注册
export const register = (data) => request.post('/user/register', data)

// 用户登录
export const login = (data) => request.post('/user/login', data)

// 获取个人信息
export const getProfile = () => request.get('/user/profile')

// 修改个人信息
export const updateProfile = (data) => request.put('/user/profile', data)

// 修改密码
export const changePassword = (data) => request.put('/user/password', data)
