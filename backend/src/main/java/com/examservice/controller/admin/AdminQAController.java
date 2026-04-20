package com.examservice.controller.admin;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.examservice.common.Result;
import com.examservice.entity.Answer;
import com.examservice.entity.Question;
import com.examservice.mapper.AnswerMapper;
import com.examservice.mapper.QuestionMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/admin")
public class AdminQAController {

    @Autowired
    private QuestionMapper questionMapper;
    @Autowired
    private AnswerMapper answerMapper;

    @GetMapping("/question/list")
    public Result<Page<Question>> questionList(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) Long moduleId) {
        LambdaQueryWrapper<Question> wrapper = new LambdaQueryWrapper<>();
        if (moduleId != null) {
            wrapper.eq(Question::getModuleId, moduleId);
        }
        wrapper.orderByDesc(Question::getCreateTime);
        return Result.success(questionMapper.selectPage(new Page<>(page, size), wrapper));
    }

    @DeleteMapping("/question/{id}")
    public Result<?> deleteQuestion(@PathVariable Long id) {
        // 先删除该问题下的所有回答
        LambdaQueryWrapper<Answer> answerWrapper = new LambdaQueryWrapper<>();
        answerWrapper.eq(Answer::getQuestionId, id);
        answerMapper.delete(answerWrapper);
        questionMapper.deleteById(id);
        return Result.success("删除成功", null);
    }

    @GetMapping("/answer/list")
    public Result<Page<Answer>> answerList(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) Long questionId) {
        LambdaQueryWrapper<Answer> wrapper = new LambdaQueryWrapper<>();
        if (questionId != null) {
            wrapper.eq(Answer::getQuestionId, questionId);
        }
        wrapper.orderByDesc(Answer::getCreateTime);
        return Result.success(answerMapper.selectPage(new Page<>(page, size), wrapper));
    }

    @DeleteMapping("/answer/{id}")
    public Result<?> deleteAnswer(@PathVariable Long id) {
        answerMapper.deleteById(id);
        return Result.success("删除成功", null);
    }
}
