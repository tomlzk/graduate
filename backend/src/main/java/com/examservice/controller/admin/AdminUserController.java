package com.examservice.controller.admin;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.examservice.common.Result;
import com.examservice.entity.User;
import com.examservice.exception.BusinessException;
import com.examservice.mapper.UserMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/admin/user")
public class AdminUserController {

    @Autowired
    private UserMapper userMapper;

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    @GetMapping("/list")
    public Result<Page<User>> list(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) String keyword) {
        LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
        if (keyword != null && !keyword.isEmpty()) {
            wrapper.like(User::getUsername, keyword).or().like(User::getNickname, keyword);
        }
        wrapper.orderByDesc(User::getCreateTime);
        Page<User> userPage = userMapper.selectPage(new Page<>(page, size), wrapper);
        // 清除密码字段
        userPage.getRecords().forEach(u -> u.setPassword(null));
        return Result.success(userPage);
    }

    @PutMapping("/update/{id}")
    public Result<?> updateUsername(@PathVariable Long id, @RequestBody Map<String, String> body) {
        User user = userMapper.selectById(id);
        if (user == null) {
            throw new BusinessException(404, "用户不存在");
        }
        String newUsername = body.get("username");
        if (newUsername != null && !newUsername.isEmpty()) {
            // 检查用户名是否重复
            LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
            wrapper.eq(User::getUsername, newUsername).ne(User::getId, id);
            if (userMapper.selectCount(wrapper) > 0) {
                throw new BusinessException(400, "用户名已存在");
            }
            user.setUsername(newUsername);
        }
        String nickname = body.get("nickname");
        if (nickname != null) {
            user.setNickname(nickname);
        }
        userMapper.updateById(user);
        return Result.success("修改成功", null);
    }

    @PutMapping("/reset-password/{id}")
    public Result<?> resetPassword(@PathVariable Long id) {
        User user = userMapper.selectById(id);
        if (user == null) {
            throw new BusinessException(404, "用户不存在");
        }
        user.setPassword(passwordEncoder.encode("123456"));
        userMapper.updateById(user);
        return Result.success("密码已重置为123456", null);
    }

    @PutMapping("/status/{id}")
    public Result<?> toggleStatus(@PathVariable Long id) {
        User user = userMapper.selectById(id);
        if (user == null) {
            throw new BusinessException(404, "用户不存在");
        }
        user.setStatus(user.getStatus() == 1 ? 0 : 1);
        userMapper.updateById(user);
        return Result.success(user.getStatus() == 1 ? "已启用" : "已禁用", null);
    }
}
