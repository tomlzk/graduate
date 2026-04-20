package com.examservice.service;

import com.examservice.dto.AnswerDTO;
import com.examservice.vo.AnswerVO;

import java.util.List;

public interface AnswerService {
    List<AnswerVO> listByQuestion(Long questionId);
    void create(Long userId, AnswerDTO dto);
    void delete(Long userId, Long answerId);
}
