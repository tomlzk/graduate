package com.examservice.service;

import com.examservice.dto.ChangePasswordDTO;
import com.examservice.dto.LoginDTO;
import com.examservice.dto.RegisterDTO;
import com.examservice.dto.UserProfileDTO;
import com.examservice.vo.LoginVO;
import com.examservice.vo.UserVO;

public interface UserService {
    void register(RegisterDTO dto);
    LoginVO login(LoginDTO dto);
    UserVO getProfile(Long userId);
    void updateProfile(Long userId, UserProfileDTO dto);
    void changePassword(Long userId, ChangePasswordDTO dto);
}
