package com.examservice.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.examservice.common.Result;
import com.examservice.entity.ExamInfo;
import com.examservice.service.ExamInfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/exam-info")
public class ExamInfoController {

    @Autowired
    private ExamInfoService examInfoService;

    @GetMapping("/list")
    public Result<Page<ExamInfo>> list(
            @RequestParam(required = false) Long moduleId,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int size) {
        Page<ExamInfo> result = examInfoService.listByModule(moduleId, page, size);
        return Result.success(result);
    }
}
