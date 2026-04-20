-- ============================================
-- 高校学生考证服务系统 测试数据脚本
-- 在已有 init.sql 基础数据之上填充真实感的测试数据
-- ============================================

USE exam_service;

-- -------------------------------------------
-- 清理旧的测试数据（保留admin和模块）
-- -------------------------------------------
DELETE FROM answer;
DELETE FROM question;
DELETE FROM post;
DELETE FROM exam_info;
DELETE FROM announcement;
DELETE FROM user WHERE id > 1;

-- 重置自增ID
ALTER TABLE user AUTO_INCREMENT = 2;

-- -------------------------------------------
-- 1. 插入测试用户（密码均为 123456）
-- BCrypt hash of "123456": $2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi
-- -------------------------------------------
INSERT INTO `user` (`username`, `password`, `nickname`, `role`, `status`) VALUES
('zhangsan',  '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', '张三', 0, 1),
('lisi',      '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', '李四', 0, 1),
('wangwu',    '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', '王五', 0, 1),
('zhaoliu',   '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', '赵六', 0, 1),
('chenqi',    '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', '陈七', 0, 1),
('xiaoming',  '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', '小明', 0, 1),
('xiaohong',  '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', '小红', 0, 1),
('liuyang',   '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', '刘洋', 0, 1),
('huanghe',   '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', '黄河', 0, 1),
('sunwei',    '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', '孙伟', 0, 1);
