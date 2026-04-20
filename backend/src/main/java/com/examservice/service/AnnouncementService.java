package com.examservice.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.examservice.entity.Announcement;

public interface AnnouncementService {
    Page<Announcement> list(int page, int size);
    Announcement detail(Long id);
    void create(Long adminId, Announcement announcement);
    void update(Long adminId, Announcement announcement);
    void delete(Long id);
}
