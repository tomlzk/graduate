package com.examservice.controller;

import com.examservice.common.Result;
import com.examservice.dto.AnswerDTO;
import com.examservice.service.AnswerService;
import com.examservice.vo.AnswerVO;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/answer")
public class AnswerController {

    @Autowired
    private AnswerService answerService;

    @GetMapping("/list")
    public Result<List<AnswerVO>> list(@RequestParam Long questionId) {
        return Result.success(answerService.listByQuestion(questionId));
    }

    @PostMapping
    public Result<?> create(HttpServletRequest request, @Valid @RequestBody AnswerDTO dto) {
        Long userId = (Long) request.getAttribute("userId");
        answerService.create(userId, dto);
        return Result.success("回答成功", null);
    }

    @DeleteMapping("/{id}")
    public Result<?> delete(HttpServletRequest request, @PathVariable Long id) {
        Long userId = (Long) request.getAttribute("userId");
        answerService.delete(userId, id);
        return Result.success("删除成功", null);
    }
}
