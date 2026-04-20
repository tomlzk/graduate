package com.examservice.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("post_reply")
public class PostReply {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long postId;
    private Long userId;
    private String content;
    private Integer floor;
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;
}
