package com.examservice.vo;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class PostVO {
    private Long id;
    private Long userId;
    private String username;
    private String nickname;
    private Long moduleId;
    private String moduleName;
    private String title;
    private String content;
    private Integer viewCount;
    private LocalDateTime createTime;
    private LocalDateTime updateTime;
}
