package com.examservice.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.examservice.dto.PostDTO;
import com.examservice.vo.PostVO;

public interface PostService {
    Page<PostVO> list(Long moduleId, String keyword, int page, int size);
    PostVO detail(Long id);
    void create(Long userId, PostDTO dto);
    void update(Long userId, Long postId, PostDTO dto);
    void delete(Long userId, Long postId);
}
