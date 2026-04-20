package com.examservice.controller.admin;

import com.examservice.common.Result;
import com.examservice.entity.Announcement;
import com.examservice.service.AnnouncementService;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/admin/announcement")
public class AdminAnnouncementController {

    @Autowired
    private AnnouncementService announcementService;

    @PostMapping
    public Result<?> create(HttpServletRequest request, @RequestBody Announcement announcement) {
        Long adminId = (Long) request.getAttribute("userId");
        announcementService.create(adminId, announcement);
        return Result.success("发布成功", null);
    }

    @PutMapping("/{id}")
    public Result<?> update(HttpServletRequest request, @PathVariable Long id, @RequestBody Announcement announcement) {
        Long adminId = (Long) request.getAttribute("userId");
        announcement.setId(id);
        announcementService.update(adminId, announcement);
        return Result.success("修改成功", null);
    }

    @DeleteMapping("/{id}")
    public Result<?> delete(@PathVariable Long id) {
        announcementService.delete(id);
        return Result.success("删除成功", null);
    }
}
