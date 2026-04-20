package com.examservice.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.examservice.dto.QuestionDTO;
import com.examservice.vo.QuestionVO;

public interface QuestionService {
    Page<QuestionVO> list(Long moduleId, String keyword, int page, int size);
    QuestionVO detail(Long id);
    void create(Long userId, QuestionDTO dto);
    void delete(Long userId, Long questionId);
}
