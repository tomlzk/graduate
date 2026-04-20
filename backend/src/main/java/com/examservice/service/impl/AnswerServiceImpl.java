package com.examservice.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.examservice.dto.AnswerDTO;
import com.examservice.entity.Answer;
import com.examservice.entity.User;
import com.examservice.exception.BusinessException;
import com.examservice.mapper.AnswerMapper;
import com.examservice.mapper.UserMapper;
import com.examservice.service.AnswerService;
import com.examservice.vo.AnswerVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class AnswerServiceImpl implements AnswerService {

    @Autowired
    private AnswerMapper answerMapper;
    @Autowired
    private UserMapper userMapper;

    @Override
    public List<AnswerVO> listByQuestion(Long questionId) {
        LambdaQueryWrapper<Answer> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Answer::getQuestionId, questionId);
        wrapper.orderByAsc(Answer::getCreateTime);
        List<Answer> answers = answerMapper.selectList(wrapper);
        return answers.stream().map(this::toAnswerVO).collect(Collectors.toList());
    }

    @Override
    public void create(Long userId, AnswerDTO dto) {
        Answer answer = new Answer();
        answer.setQuestionId(dto.getQuestionId());
        answer.setUserId(userId);
        answer.setContent(dto.getContent());
        answerMapper.insert(answer);
    }

    @Override
    public void delete(Long userId, Long answerId) {
        Answer answer = answerMapper.selectById(answerId);
        if (answer == null) {
            throw new BusinessException(404, "回答不存在");
        }
        if (!answer.getUserId().equals(userId)) {
            throw new BusinessException(403, "只能删除自己的回答");
        }
        answerMapper.deleteById(answerId);
    }

    private AnswerVO toAnswerVO(Answer answer) {
        AnswerVO vo = new AnswerVO();
        vo.setId(answer.getId());
        vo.setQuestionId(answer.getQuestionId());
        vo.setUserId(answer.getUserId());
        vo.setContent(answer.getContent());
        vo.setCreateTime(answer.getCreateTime());

        User user = userMapper.selectById(answer.getUserId());
        if (user != null) {
            vo.setUsername(user.getUsername());
            vo.setNickname(user.getNickname());
        }
        return vo;
    }
}
