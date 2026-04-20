package com.examservice.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.examservice.dto.PostDTO;
import com.examservice.entity.ExamModule;
import com.examservice.entity.Post;
import com.examservice.entity.User;
import com.examservice.exception.BusinessException;
import com.examservice.mapper.ExamModuleMapper;
import com.examservice.mapper.PostMapper;
import com.examservice.mapper.UserMapper;
import com.examservice.service.PostService;
import com.examservice.vo.PostVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class PostServiceImpl implements PostService {

    @Autowired
    private PostMapper postMapper;
    @Autowired
    private UserMapper userMapper;
    @Autowired
    private ExamModuleMapper examModuleMapper;

    @Override
    public Page<PostVO> list(Long moduleId, String keyword, int page, int size) {
        LambdaQueryWrapper<Post> wrapper = new LambdaQueryWrapper<>();
        if (moduleId != null) {
            wrapper.eq(Post::getModuleId, moduleId);
        }
        if (keyword != null && !keyword.trim().isEmpty()) {
            wrapper.like(Post::getTitle, keyword.trim());
        }
        wrapper.orderByDesc(Post::getCreateTime);

        Page<Post> postPage = postMapper.selectPage(new Page<>(page, size), wrapper);

        // 转换为 VO
        Page<PostVO> voPage = new Page<>(postPage.getCurrent(), postPage.getSize(), postPage.getTotal());
        List<PostVO> voList = postPage.getRecords().stream().map(this::toPostVO).collect(Collectors.toList());
        voPage.setRecords(voList);
        return voPage;
    }

    @Override
    public PostVO detail(Long id) {
        Post post = postMapper.selectById(id);
        if (post == null) {
            throw new BusinessException(404, "帖子不存在");
        }
        // 浏览量+1
        post.setViewCount(post.getViewCount() + 1);
        postMapper.updateById(post);
        return toPostVO(post);
    }

    @Override
    public void create(Long userId, PostDTO dto) {
        Post post = new Post();
        post.setUserId(userId);
        post.setModuleId(dto.getModuleId());
        post.setTitle(dto.getTitle());
        post.setContent(dto.getContent());
        post.setViewCount(0);
        postMapper.insert(post);
    }

    @Override
    public void update(Long userId, Long postId, PostDTO dto) {
        Post post = postMapper.selectById(postId);
        if (post == null) {
            throw new BusinessException(404, "帖子不存在");
        }
        if (!post.getUserId().equals(userId)) {
            throw new BusinessException(403, "只能修改自己的帖子");
        }
        post.setTitle(dto.getTitle());
        post.setContent(dto.getContent());
        post.setModuleId(dto.getModuleId());
        postMapper.updateById(post);
    }

    @Override
    public void delete(Long userId, Long postId) {
        Post post = postMapper.selectById(postId);
        if (post == null) {
            throw new BusinessException(404, "帖子不存在");
        }
        if (!post.getUserId().equals(userId)) {
            throw new BusinessException(403, "只能删除自己的帖子");
        }
        postMapper.deleteById(postId);
    }

    private PostVO toPostVO(Post post) {
        PostVO vo = new PostVO();
        vo.setId(post.getId());
        vo.setUserId(post.getUserId());
        vo.setModuleId(post.getModuleId());
        vo.setTitle(post.getTitle());
        vo.setContent(post.getContent());
        vo.setViewCount(post.getViewCount());
        vo.setCreateTime(post.getCreateTime());
        vo.setUpdateTime(post.getUpdateTime());

        User user = userMapper.selectById(post.getUserId());
        if (user != null) {
            vo.setUsername(user.getUsername());
            vo.setNickname(user.getNickname());
            vo.setAuthorName(user.getNickname() != null ? user.getNickname() : user.getUsername());
        }
        ExamModule module = examModuleMapper.selectById(post.getModuleId());
        if (module != null) {
            vo.setModuleName(module.getName());
        }
        return vo;
    }
}
