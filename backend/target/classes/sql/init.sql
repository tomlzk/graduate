-- ============================================
-- 高校学生考证服务系统 数据库初始化脚本
-- ============================================

CREATE DATABASE IF NOT EXISTS exam_service
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE exam_service;

-- -------------------------------------------
-- 1. 用户表
-- -------------------------------------------
DROP TABLE IF EXISTS `answer`;
DROP TABLE IF EXISTS `question`;
DROP TABLE IF EXISTS `post`;
DROP TABLE IF EXISTS `exam_info`;
DROP TABLE IF EXISTS `announcement`;
DROP TABLE IF EXISTS `exam_module`;
DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '用户ID',
    `username` VARCHAR(50) NOT NULL COMMENT '用户名',
    `password` VARCHAR(255) NOT NULL COMMENT '密码(BCrypt加密)',
    `email` VARCHAR(100) DEFAULT NULL COMMENT '邮箱',
    `nickname` VARCHAR(50) DEFAULT NULL COMMENT '昵称',
    `avatar` VARCHAR(255) DEFAULT NULL COMMENT '头像URL',
    `role` TINYINT NOT NULL DEFAULT 0 COMMENT '角色: 0-普通用户, 1-管理员',
    `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态: 0-禁用, 1-正常',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- -------------------------------------------
-- 2. 考试模块表
-- -------------------------------------------
CREATE TABLE `exam_module` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '模块ID',
    `name` VARCHAR(50) NOT NULL COMMENT '模块名称',
    `description` VARCHAR(500) DEFAULT NULL COMMENT '模块描述',
    `icon` VARCHAR(100) DEFAULT NULL COMMENT '图标',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '排序',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考试模块表';

-- -------------------------------------------
-- 3. 帖子表
-- -------------------------------------------
CREATE TABLE `post` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '帖子ID',
    `user_id` BIGINT NOT NULL COMMENT '发帖用户ID',
    `module_id` BIGINT NOT NULL COMMENT '所属模块ID',
    `title` VARCHAR(200) NOT NULL COMMENT '帖子标题',
    `content` TEXT NOT NULL COMMENT '帖子内容',
    `view_count` INT NOT NULL DEFAULT 0 COMMENT '浏览量',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_module_id` (`module_id`),
    CONSTRAINT `fk_post_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
    CONSTRAINT `fk_post_module` FOREIGN KEY (`module_id`) REFERENCES `exam_module` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='帖子表';

-- -------------------------------------------
-- 4. 问题表
-- -------------------------------------------
CREATE TABLE `question` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '问题ID',
    `user_id` BIGINT NOT NULL COMMENT '提问用户ID',
    `module_id` BIGINT NOT NULL COMMENT '所属模块ID',
    `title` VARCHAR(200) NOT NULL COMMENT '问题标题',
    `content` TEXT NOT NULL COMMENT '问题内容',
    `status` TINYINT NOT NULL DEFAULT 0 COMMENT '状态: 0-未解决, 1-已解决',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `idx_user_id` (`user_id`),
    KEY `idx_module_id` (`module_id`),
    CONSTRAINT `fk_question_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
    CONSTRAINT `fk_question_module` FOREIGN KEY (`module_id`) REFERENCES `exam_module` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='问题表';

-- -------------------------------------------
-- 5. 回答表
-- -------------------------------------------
CREATE TABLE `answer` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '回答ID',
    `question_id` BIGINT NOT NULL COMMENT '所属问题ID',
    `user_id` BIGINT NOT NULL COMMENT '回答用户ID',
    `content` TEXT NOT NULL COMMENT '回答内容',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `idx_question_id` (`question_id`),
    KEY `idx_user_id` (`user_id`),
    CONSTRAINT `fk_answer_question` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`),
    CONSTRAINT `fk_answer_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='回答表';

-- -------------------------------------------
-- 6. 公告表
-- -------------------------------------------
CREATE TABLE `announcement` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '公告ID',
    `admin_id` BIGINT NOT NULL COMMENT '发布管理员ID',
    `title` VARCHAR(200) NOT NULL COMMENT '公告标题',
    `content` TEXT NOT NULL COMMENT '公告内容',
    `is_top` TINYINT NOT NULL DEFAULT 0 COMMENT '是否置顶: 0-否, 1-是',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_admin_id` (`admin_id`),
    CONSTRAINT `fk_announcement_admin` FOREIGN KEY (`admin_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='公告表';

-- -------------------------------------------
-- 7. 考试信息表
-- -------------------------------------------
CREATE TABLE `exam_info` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '考试信息ID',
    `module_id` BIGINT NOT NULL COMMENT '所属模块ID',
    `title` VARCHAR(200) NOT NULL COMMENT '考试信息标题',
    `content` TEXT NOT NULL COMMENT '考试信息内容',
    `exam_time` VARCHAR(100) DEFAULT NULL COMMENT '考试时间',
    `register_url` VARCHAR(500) DEFAULT NULL COMMENT '报名链接',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `idx_module_id` (`module_id`),
    CONSTRAINT `fk_exam_info_module` FOREIGN KEY (`module_id`) REFERENCES `exam_module` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考试信息表';

-- ============================================
-- 初始数据
-- ============================================

-- 插入管理员账号 (密码为 admin123 的BCrypt加密值)
INSERT INTO `user` (`username`, `password`, `email`, `nickname`, `role`, `status`) VALUES
('admin', '$2a$10$//DQUsOCaF8SSNZw.spyIumUj3GPHfR4T/QK5r3jrBhbZP/xUfRAK', 'admin@exam.com', '系统管理员', 1, 1);

-- 插入七大考证模块
INSERT INTO `exam_module` (`name`, `description`, `icon`, `sort_order`) VALUES
('考公', '国家公务员考试、省考等公务员考试相关信息，包含行测、申论备考经验，岗位选择指南等', 'icon-gov', 1),
('考研', '全国硕士研究生考试相关信息，包含初试/复试经验、院校选择、专业课备考资料等', 'icon-graduate', 2),
('四级考试', '大学英语四级考试（CET-4）相关信息，包含听力、阅读、写作、翻译备考技巧等', 'icon-cet4', 3),
('六级考试', '大学英语六级考试（CET-6）相关信息，包含备考策略、真题解析、高分经验等', 'icon-cet6', 4),
('雅思考试', '雅思（IELTS）考试相关信息，包含听说读写各科备考方法、考试报名流程等', 'icon-ielts', 5),
('托福考试', '托福（TOEFL）考试相关信息，包含备考资源、考试技巧、成绩要求等', 'icon-toefl', 6),
('计算机等级考试', '全国计算机等级考试（NCRE）相关信息，包含一级至四级各科目备考资料等', 'icon-ncre', 7);
