package com.examservice.vo;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class AnswerVO {
    private Long id;
    private Long questionId;
    private Long userId;
    private String username;
    private String nickname;
    private String content;
    private LocalDateTime createTime;
}
