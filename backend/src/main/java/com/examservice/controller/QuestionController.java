package com.examservice.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.examservice.common.Result;
import com.examservice.dto.QuestionDTO;
import com.examservice.service.QuestionService;
import com.examservice.vo.QuestionVO;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/question")
public class QuestionController {

    @Autowired
    private QuestionService questionService;

    @GetMapping("/list")
    public Result<Page<QuestionVO>> list(
            @RequestParam(required = false) Long moduleId,
            @RequestParam(required = false) String keyword,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int size) {
        return Result.success(questionService.list(moduleId, keyword, page, size));
    }

    @GetMapping("/detail/{id}")
    public Result<QuestionVO> detail(@PathVariable Long id) {
        return Result.success(questionService.detail(id));
    }

    @PostMapping
    public Result<?> create(HttpServletRequest request, @Valid @RequestBody QuestionDTO dto) {
        Long userId = (Long) request.getAttribute("userId");
        questionService.create(userId, dto);
        return Result.success("提问成功", null);
    }

    @DeleteMapping("/{id}")
    public Result<?> delete(HttpServletRequest request, @PathVariable Long id) {
        Long userId = (Long) request.getAttribute("userId");
        questionService.delete(userId, id);
        return Result.success("删除成功", null);
    }
}
