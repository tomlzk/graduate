package com.examservice.config;

import com.examservice.interceptor.AdminInterceptor;
import com.examservice.interceptor.JwtInterceptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebMvcConfig implements WebMvcConfigurer {

    @Autowired
    private JwtInterceptor jwtInterceptor;

    @Autowired
    private AdminInterceptor adminInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // JWT拦截器 - 拦截需要登录的接口
        registry.addInterceptor(jwtInterceptor)
                .addPathPatterns("/api/**")
                .excludePathPatterns(
                        "/api/user/login",
                        "/api/user/register",
                        "/api/module/list",
                        "/api/exam-info/list",
                        "/api/post/list",
                        "/api/post/detail/**",
                        "/api/post-reply/list",
                        "/api/question/list",
                        "/api/question/detail/**",
                        "/api/answer/list",
                        "/api/announcement/list"
                );

        // 管理员拦截器 - 拦截管理接口
        registry.addInterceptor(adminInterceptor)
                .addPathPatterns("/api/admin/**");
    }
}
