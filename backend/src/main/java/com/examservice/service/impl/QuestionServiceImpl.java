package com.examservice.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.examservice.dto.QuestionDTO;
import com.examservice.entity.Answer;
import com.examservice.entity.ExamModule;
import com.examservice.entity.Question;
import com.examservice.entity.User;
import com.examservice.exception.BusinessException;
import com.examservice.mapper.AnswerMapper;
import com.examservice.mapper.ExamModuleMapper;
import com.examservice.mapper.QuestionMapper;
import com.examservice.mapper.UserMapper;
import com.examservice.service.QuestionService;
import com.examservice.vo.QuestionVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class QuestionServiceImpl implements QuestionService {

    @Autowired
    private QuestionMapper questionMapper;
    @Autowired
    private UserMapper userMapper;
    @Autowired
    private ExamModuleMapper examModuleMapper;
    @Autowired
    private AnswerMapper answerMapper;

    @Override
    public Page<QuestionVO> list(Long moduleId, String keyword, int page, int size) {
        LambdaQueryWrapper<Question> wrapper = new LambdaQueryWrapper<>();
        if (moduleId != null) {
            wrapper.eq(Question::getModuleId, moduleId);
        }
        if (keyword != null && !keyword.trim().isEmpty()) {
            wrapper.like(Question::getTitle, keyword.trim());
        }
        wrapper.orderByDesc(Question::getCreateTime);

        Page<Question> questionPage = questionMapper.selectPage(new Page<>(page, size), wrapper);
        Page<QuestionVO> voPage = new Page<>(questionPage.getCurrent(), questionPage.getSize(), questionPage.getTotal());
        List<QuestionVO> voList = questionPage.getRecords().stream().map(this::toQuestionVO).collect(Collectors.toList());
        voPage.setRecords(voList);
        return voPage;
    }

    @Override
    public QuestionVO detail(Long id) {
        Question question = questionMapper.selectById(id);
        if (question == null) {
            throw new BusinessException(404, "问题不存在");
        }
        return toQuestionVO(question);
    }

    @Override
    public void create(Long userId, QuestionDTO dto) {
        Question question = new Question();
        question.setUserId(userId);
        question.setModuleId(dto.getModuleId());
        question.setTitle(dto.getTitle());
        question.setContent(dto.getContent());
        question.setStatus(0);
        questionMapper.insert(question);
    }

    @Override
    public void delete(Long userId, Long questionId) {
        Question question = questionMapper.selectById(questionId);
        if (question == null) {
            throw new BusinessException(404, "问题不存在");
        }
        if (!question.getUserId().equals(userId)) {
            throw new BusinessException(403, "只能删除自己的问题");
        }
        // 先删除该问题下的所有回答
        LambdaQueryWrapper<Answer> answerWrapper = new LambdaQueryWrapper<>();
        answerWrapper.eq(Answer::getQuestionId, questionId);
        answerMapper.delete(answerWrapper);
        questionMapper.deleteById(questionId);
    }

    private QuestionVO toQuestionVO(Question question) {
        QuestionVO vo = new QuestionVO();
        vo.setId(question.getId());
        vo.setUserId(question.getUserId());
        vo.setModuleId(question.getModuleId());
        vo.setTitle(question.getTitle());
        vo.setContent(question.getContent());
        vo.setStatus(question.getStatus());
        vo.setCreateTime(question.getCreateTime());

        User user = userMapper.selectById(question.getUserId());
        if (user != null) {
            vo.setUsername(user.getUsername());
            vo.setNickname(user.getNickname());
            vo.setAuthorName(user.getNickname() != null ? user.getNickname() : user.getUsername());
        }
        ExamModule module = examModuleMapper.selectById(question.getModuleId());
        if (module != null) {
            vo.setModuleName(module.getName());
        }

        LambdaQueryWrapper<Answer> answerWrapper = new LambdaQueryWrapper<>();
        answerWrapper.eq(Answer::getQuestionId, question.getId());
        vo.setAnswerCount(Math.toIntExact(answerMapper.selectCount(answerWrapper)));

        return vo;
    }
}
