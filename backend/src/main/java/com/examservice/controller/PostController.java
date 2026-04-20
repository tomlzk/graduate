package com.examservice.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.examservice.common.Result;
import com.examservice.dto.PostDTO;
import com.examservice.service.PostService;
import com.examservice.vo.PostVO;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/post")
public class PostController {

    @Autowired
    private PostService postService;

    @GetMapping("/list")
    public Result<Page<PostVO>> list(
            @RequestParam(required = false) Long moduleId,
            @RequestParam(required = false) String keyword,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int size) {
        return Result.success(postService.list(moduleId, keyword, page, size));
    }

    @GetMapping("/detail/{id}")
    public Result<PostVO> detail(@PathVariable Long id) {
        return Result.success(postService.detail(id));
    }

    @PostMapping
    public Result<?> create(HttpServletRequest request, @Valid @RequestBody PostDTO dto) {
        Long userId = (Long) request.getAttribute("userId");
        postService.create(userId, dto);
        return Result.success("发帖成功", null);
    }

    @PutMapping("/{id}")
    public Result<?> update(HttpServletRequest request, @PathVariable Long id, @Valid @RequestBody PostDTO dto) {
        Long userId = (Long) request.getAttribute("userId");
        postService.update(userId, id, dto);
        return Result.success("修改成功", null);
    }

    @DeleteMapping("/{id}")
    public Result<?> delete(HttpServletRequest request, @PathVariable Long id) {
        Long userId = (Long) request.getAttribute("userId");
        postService.delete(userId, id);
        return Result.success("删除成功", null);
    }
}
