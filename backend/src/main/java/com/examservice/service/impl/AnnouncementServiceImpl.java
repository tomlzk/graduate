package com.examservice.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.examservice.entity.Announcement;
import com.examservice.exception.BusinessException;
import com.examservice.mapper.AnnouncementMapper;
import com.examservice.service.AnnouncementService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class AnnouncementServiceImpl implements AnnouncementService {

    @Autowired
    private AnnouncementMapper announcementMapper;

    @Override
    public Page<Announcement> list(int page, int size) {
        LambdaQueryWrapper<Announcement> wrapper = new LambdaQueryWrapper<>();
        wrapper.orderByDesc(Announcement::getIsTop).orderByDesc(Announcement::getCreateTime);
        return announcementMapper.selectPage(new Page<>(page, size), wrapper);
    }

    @Override
    public Announcement detail(Long id) {
        Announcement announcement = announcementMapper.selectById(id);
        if (announcement == null) {
            throw new BusinessException(404, "公告不存在");
        }
        return announcement;
    }

    @Override
    public void create(Long adminId, Announcement announcement) {
        announcement.setAdminId(adminId);
        announcementMapper.insert(announcement);
    }

    @Override
    public void update(Long adminId, Announcement announcement) {
        Announcement existing = announcementMapper.selectById(announcement.getId());
        if (existing == null) {
            throw new BusinessException(404, "公告不存在");
        }
        announcementMapper.updateById(announcement);
    }

    @Override
    public void delete(Long id) {
        announcementMapper.deleteById(id);
    }
}
