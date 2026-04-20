package com.examservice.controller.admin;

import com.examservice.common.Result;
import com.examservice.entity.ExamInfo;
import com.examservice.entity.ExamModule;
import com.examservice.exception.BusinessException;
import com.examservice.mapper.ExamModuleMapper;
import com.examservice.service.ExamInfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/admin/module")
public class AdminModuleController {

    @Autowired
    private ExamModuleMapper examModuleMapper;
    @Autowired
    private ExamInfoService examInfoService;

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
