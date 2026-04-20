package com.examservice.vo;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class QuestionVO {
    private Long id;
    private Long userId;
    private String username;
    private String nickname;
    private String authorName;
    private Long moduleId;
    private String moduleName;
    private String title;
    private String content;
    private Integer status;
    private Integer answerCount;
    private LocalDateTime createTime;
}
