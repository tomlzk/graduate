package com.examservice.controller;

import com.examservice.common.Result;
import com.examservice.dto.PostReplyDTO;
import com.examservice.service.PostReplyService;
import com.examservice.vo.PostReplyVO;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/post-reply")
public class PostReplyController {

    @Autowired
    private PostReplyService postReplyService;

    @GetMapping("/list")
    public Result<List<PostReplyVO>> list(@RequestParam Long postId) {
        return Result.success(postReplyService.listByPost(postId));
    }

    @PostMapping
    public Result<?> create(HttpServletRequest request, @Valid @RequestBody PostReplyDTO dto) {
        Long userId = (Long) request.getAttribute("userId");
        postReplyService.create(userId, dto);
        return Result.success("回复成功", null);
    }

    @DeleteMapping("/{id}")
    public Result<?> delete(HttpServletRequest request, @PathVariable Long id) {
        Long userId = (Long) request.getAttribute("userId");
        postReplyService.delete(userId, id);
        return Result.success("删除成功", null);
    }
}
