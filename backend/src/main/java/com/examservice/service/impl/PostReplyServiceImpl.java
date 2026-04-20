package com.examservice.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.examservice.dto.PostReplyDTO;
import com.examservice.entity.PostReply;
import com.examservice.entity.User;
import com.examservice.exception.BusinessException;
import com.examservice.mapper.PostReplyMapper;
import com.examservice.mapper.UserMapper;
import com.examservice.service.PostReplyService;
import com.examservice.vo.PostReplyVO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class PostReplyServiceImpl implements PostReplyService {

    @Autowired
    private PostReplyMapper postReplyMapper;
    @Autowired
    private UserMapper userMapper;

    @Override
    public List<PostReplyVO> listByPost(Long postId) {
        LambdaQueryWrapper<PostReply> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(PostReply::getPostId, postId);
        wrapper.orderByAsc(PostReply::getFloor);
        List<PostReply> replies = postReplyMapper.selectList(wrapper);
        return replies.stream().map(this::toVO).collect(Collectors.toList());
    }

    @Override
    public void create(Long userId, PostReplyDTO dto) {
        // 计算楼层号：当前帖子最大楼层 + 1
        LambdaQueryWrapper<PostReply> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(PostReply::getPostId, dto.getPostId());
        wrapper.orderByDesc(PostReply::getFloor);
        wrapper.last("LIMIT 1");
        PostReply lastReply = postReplyMapper.selectOne(wrapper);
        int nextFloor = (lastReply != null) ? lastReply.getFloor() + 1 : 1;

        PostReply reply = new PostReply();
        reply.setPostId(dto.getPostId());
        reply.setUserId(userId);
        reply.setContent(dto.getContent());
        reply.setFloor(nextFloor);
        postReplyMapper.insert(reply);
    }

    @Override
    public void delete(Long userId, Long replyId) {
        PostReply reply = postReplyMapper.selectById(replyId);
        if (reply == null) {
            throw new BusinessException(404, "回复不存在");
        }
        if (!reply.getUserId().equals(userId)) {
            throw new BusinessException(403, "只能删除自己的回复");
        }
        postReplyMapper.deleteById(replyId);
    }

    private PostReplyVO toVO(PostReply reply) {
        PostReplyVO vo = new PostReplyVO();
        vo.setId(reply.getId());
        vo.setPostId(reply.getPostId());
        vo.setUserId(reply.getUserId());
        vo.setContent(reply.getContent());
        vo.setFloor(reply.getFloor());
        vo.setCreateTime(reply.getCreateTime());

        User user = userMapper.selectById(reply.getUserId());
        if (user != null) {
            vo.setUsername(user.getUsername());
            vo.setNickname(user.getNickname());
        }
        return vo;
    }
}
