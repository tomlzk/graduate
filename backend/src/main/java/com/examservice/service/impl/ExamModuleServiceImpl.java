package com.examservice.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.examservice.entity.ExamModule;
import com.examservice.mapper.ExamModuleMapper;
import com.examservice.service.ExamModuleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ExamModuleServiceImpl implements ExamModuleService {

    @Autowired
    private ExamModuleMapper examModuleMapper;

    @Override
    public List<ExamModule> listAll() {
        LambdaQueryWrapper<ExamModule> wrapper = new LambdaQueryWrapper<>();
        wrapper.orderByAsc(ExamModule::getSortOrder);
        return examModuleMapper.selectList(wrapper);
    }
}
