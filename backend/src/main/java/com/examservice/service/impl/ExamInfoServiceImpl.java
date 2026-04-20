package com.examservice.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.examservice.entity.ExamInfo;
import com.examservice.mapper.ExamInfoMapper;
import com.examservice.service.ExamInfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ExamInfoServiceImpl implements ExamInfoService {

    @Autowired
    private ExamInfoMapper examInfoMapper;

    @Override
    public Page<ExamInfo> listByModule(Long moduleId, int page, int size) {
        LambdaQueryWrapper<ExamInfo> wrapper = new LambdaQueryWrapper<>();
        if (moduleId != null) {
            wrapper.eq(ExamInfo::getModuleId, moduleId);
        }
        wrapper.orderByDesc(ExamInfo::getCreateTime);
        return examInfoMapper.selectPage(new Page<>(page, size), wrapper);
    }

    @Override
    public void add(ExamInfo examInfo) {
        examInfoMapper.insert(examInfo);
    }

    @Override
    public void update(ExamInfo examInfo) {
        examInfoMapper.updateById(examInfo);
    }

    @Override
    public void delete(Long id) {
        examInfoMapper.deleteById(id);
    }
}
