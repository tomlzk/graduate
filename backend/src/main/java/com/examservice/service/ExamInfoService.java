package com.examservice.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.examservice.entity.ExamInfo;

public interface ExamInfoService {
    Page<ExamInfo> listByModule(Long moduleId, int page, int size);
    void add(ExamInfo examInfo);
    void update(ExamInfo examInfo);
    void delete(Long id);
}
