package com.examservice.vo;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class PostReplyVO {
    private Long id;
    private Long postId;
    private Long userId;
    private String username;
    private String nickname;
    private String content;
    private Integer floor;
    private LocalDateTime createTime;
}
