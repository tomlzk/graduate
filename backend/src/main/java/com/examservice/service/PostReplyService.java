package com.examservice.service;

import com.examservice.dto.PostReplyDTO;
import com.examservice.vo.PostReplyVO;
import java.util.List;

public interface PostReplyService {
    List<PostReplyVO> listByPost(Long postId);
    void create(Long userId, PostReplyDTO dto);
    void delete(Long userId, Long replyId);
}
