package com.examservice.controller.admin;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.examservice.common.Result;
import com.examservice.dto.PostDTO;
import com.examservice.entity.Post;
import com.examservice.exception.BusinessException;
import com.examservice.mapper.PostMapper;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/admin/post")
public class AdminPostController {

    @Autowired
    private PostMapper postMapper;

    @GetMapping("/list")
    public Result<Page<Post>> list(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) Long moduleId,
            @RequestParam(required = false) String keyword) {
        LambdaQueryWrapper<Post> wrapper = new LambdaQueryWrapper<>();
        if (moduleId != null) {
            wrapper.eq(Post::getModuleId, moduleId);
        }
        if (keyword != null && !keyword.isEmpty()) {
            wrapper.like(Post::getTitle, keyword);
        }
        wrapper.orderByDesc(Post::getCreateTime);
        return Result.success(postMapper.selectPage(new Page<>(page, size), wrapper));
    }

    @PostMapping
    public Result<?> create(HttpServletRequest request, @Valid @RequestBody PostDTO dto) {
        Long userId = (Long) request.getAttribute("userId");
        Post post = new Post();
        post.setUserId(userId);
        post.setModuleId(dto.getModuleId());
        post.setTitle(dto.getTitle());
        post.setContent(dto.getContent());
        post.setViewCount(0);
        postMapper.insert(post);
        return Result.success("发布成功", null);
    }

    @PutMapping("/{id}")
    public Result<?> update(@PathVariable Long id, @Valid @RequestBody PostDTO dto) {
        Post post = postMapper.selectById(id);
        if (post == null) {
            throw new BusinessException(404, "帖子不存在");
        }
        post.setTitle(dto.getTitle());
        post.setContent(dto.getContent());
        post.setModuleId(dto.getModuleId());
        postMapper.updateById(post);
        return Result.success("修改成功", null);
    }

    @DeleteMapping("/{id}")
    public Result<?> delete(@PathVariable Long id) {
        postMapper.deleteById(id);
        return Result.success("删除成功", null);
    }
}
