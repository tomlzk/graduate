package com.examservice.controller.admin;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.examservice.common.Result;
import com.examservice.entity.ExamInfo;
import com.examservice.entity.ExamModule;
import com.examservice.exception.BusinessException;
import com.examservice.mapper.ExamModuleMapper;
import com.examservice.service.ExamInfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/admin/module")
public class AdminModuleController {

    @Autowired
    private ExamModuleMapper examModuleMapper;
    @Autowired
    private ExamInfoService examInfoService;

    @GetMapping("/list")
    public Result<List<ExamModule>> list() {
        return Result.success(examModuleMapper.selectList(null));
    }

    @PostMapping
    public Result<?> createModule(@RequestBody ExamModule module) {
        examModuleMapper.insert(module);
        return Result.success("创建成功", null);
    }

    @PutMapping("/{id}")
    public Result<?> updateModule(@PathVariable Long id, @RequestBody ExamModule module) {
        ExamModule existing = examModuleMapper.selectById(id);
        if (existing == null) {
            throw new BusinessException(404, "模块不存在");
        }
        module.setId(id);
        examModuleMapper.updateById(module);
        return Result.success("修改成功", null);
    }

    @DeleteMapping("/{id}")
    public Result<?> deleteModule(@PathVariable Long id) {
        examModuleMapper.deleteById(id);
        return Result.success("删除成功", null);
    }

    @GetMapping("/exam-info/list")
    public Result<Page<ExamInfo>> examInfoList(
            @RequestParam(required = false) Long moduleId,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int size) {
        return Result.success(examInfoService.listByModule(moduleId, page, size));
    }

    @PostMapping("/exam-info")
    public Result<?> addExamInfo(@RequestBody ExamInfo examInfo) {
        examInfoService.add(examInfo);
        return Result.success("添加成功", null);
    }

    @PutMapping("/exam-info/{id}")
    public Result<?> updateExamInfo(@PathVariable Long id, @RequestBody ExamInfo examInfo) {
        examInfo.setId(id);
        examInfoService.update(examInfo);
        return Result.success("修改成功", null);
    }

    @DeleteMapping("/exam-info/{id}")
    public Result<?> deleteExamInfo(@PathVariable Long id) {
        examInfoService.delete(id);
        return Result.success("删除成功", null);
    }
}
