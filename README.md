# Vendor Magisk

这是一个用于Android系统集成的Magisk模块项目，专门为Redroid容器环境设计，提供系统级的root权限管理功能。

## 项目概述

本项目将Magisk集成到Android vendor分区中，通过init.rc脚本在系统启动时自动初始化和配置Magisk环境。主要功能包括：

- 系统级Magisk集成
- 自动权限管理
- Redroid容器兼容性
- 模块化安装支持

## 项目结构

```
vendor_magisk/
├── Android.mk              # Android构建配置
├── device.mk               # 设备特定配置
├── extract.py              # APK提取脚本
├── magisk.apk              # Magisk APK文件
├── magisk.rc               # Init脚本配置
└── rootfs/                 # 根文件系统覆盖
    └── vendor/
        └── etc/
            └── init/
                └── magisk/
                    ├── busybox      # BusyBox工具集
                    ├── magisk32     # 32位Magisk二进制
                    ├── magisk64     # 64位Magisk二进制
                    ├── magiskboot   # Magisk启动工具
                    ├── magiskinit   # Magisk初始化工具
                    └── magiskpolicy # SELinux策略工具
```

## 核心组件

### 1. Magisk二进制文件
- **magisk64**: 64位架构的Magisk主程序
- **magisk32**: 32位架构的Magisk主程序
- **magiskinit**: Magisk初始化程序
- **magiskboot**: 启动镜像处理工具
- **magiskpolicy**: SELinux策略管理工具
- **busybox**: 系统工具集

### 2. 配置文件
- **magisk.rc**: Init脚本，定义Magisk的启动流程和服务
- **Android.mk**: Android构建系统配置
- **device.mk**: 设备特定的包和文件配置

### 3. 工具脚本
- **extract.py**: 从Magisk APK中提取必要文件的Python脚本

## 功能特性

### 系统集成
- 在系统启动时自动初始化Magisk环境
- 创建必要的目录结构（/sbin/.magisk）
- 设置适当的文件权限和SELinux上下文

### 权限管理
- 自动配置SELinux策略
- 提供root权限访问控制
- 支持模块化权限管理

### Redroid兼容性
- 专门为Redroid容器环境优化
- 通过`ro.boot.redroid_magisk=1`属性控制启用
- 适配容器环境的文件系统结构

### 自动安装
- 系统启动完成后自动安装Magisk APK
- 智能检测避免重复安装
- 支持Zygote重启时的重新初始化

## 使用方法

### 1. 构建集成

将本项目添加到Android构建系统中：

```bash
# 在device.mk中添加
PRODUCT_PACKAGES += magisk

PRODUCT_COPY_FILES += \
    vendor/magisk/magisk.rc:$(TARGET_COPY_OUT_VENDOR)/etc/init/magisk.rc \
    $(call find-copy-subdir-files,*,vendor/magisk/rootfs/vendor/etc/init,$(TARGET_COPY_OUT_VENDOR)/etc/init)
```

### 2. 启用Magisk

在启动参数中添加：

```bash
ro.boot.redroid_magisk=1
```

### 3. 提取文件

运行提取脚本以更新二进制文件：

```bash
python3 extract.py
```

## 启动流程

1. **post-fs-data阶段**: 初始化Magisk环境，设置权限和目录
2. **boot-complete阶段**: 安装Magisk APK，完成启动配置
3. **zygote重启**: 重新初始化Magisk服务

## 依赖要求

- Android系统（支持vendor分区）
- Python 3（用于extract.py脚本）
- 支持SELinux的Android内核
- Redroid容器环境（推荐）

## 注意事项

- 仅在`ro.boot.redroid_magisk=1`属性设置时启用
- 需要适当的SELinux权限配置
- 建议在测试环境中验证功能
- 确保系统有足够的存储空间

## 许可证

本项目遵循Magisk项目的许可证条款。

## 贡献

欢迎提交Issue和Pull Request来改进项目功能。

## 相关链接

- [Magisk项目](https://github.com/topjohnwu/Magisk)
- [Redroid项目](https://github.com/remote-android/redroid) 