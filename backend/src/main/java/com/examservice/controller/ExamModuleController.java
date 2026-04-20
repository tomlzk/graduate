package com.examservice.controller;

import com.examservice.common.Result;
import com.examservice.entity.ExamModule;
import com.examservice.service.ExamModuleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/module")
public class ExamModuleController {

    @Autowired
    private ExamModuleService examModuleService;

    @GetMapping("/list")
    public Result<List<ExamModule>> list() {
        List<ExamModule> modules = examModuleService.listAll();
        return Result.success(modules);
    }
}
