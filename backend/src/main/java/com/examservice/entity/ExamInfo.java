package com.examservice.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("exam_info")
public class ExamInfo {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long moduleId;
    private String title;
    private String content;
    private String examTime;
    private String registerUrl;
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;
}
