#!/usr/bin/env python3
# 导入所需的标准库
import atexit
import os.path
import re
import shutil
import subprocess
import zipfile


def main():
    # 获取当前脚本所在目录
    current_path = os.path.dirname(os.path.abspath(__file__))
    # 拼接 magisk.apk 的路径
    apk_path = os.path.join(current_path, "magisk.apk")
    # 解压临时目录
    unzip_path = os.path.join(current_path, "temp")
    # overlay 根目录
    overlay_path = os.path.join(current_path, "rootfs")
    # overlay 下 magisk 目录
    overlay_magisk_path = os.path.join(overlay_path, "vendor", "etc", "init", "magisk")
    # overlay 下 magisk.rc 路径
    overlay_init_path = os.path.join(overlay_path, "vendor", "etc", "init", "magisk.rc")

    # 清理临时解压目录
    shutil.rmtree(unzip_path, ignore_errors=True)
    # 创建临时解压目录
    os.makedirs(unzip_path, exist_ok=True)
    # 程序退出时自动清理临时目录
    atexit.register(shutil.rmtree, unzip_path, ignore_errors=True)

    print("==> Extracting archive...")
    # 解压 magisk.apk 到临时目录
    with zipfile.ZipFile(apk_path) as z:
        z.extractall(unzip_path)

    # 清理 overlay 目录
    shutil.rmtree(overlay_path, ignore_errors=True)
    # 创建 overlay/magisk 目录
    os.makedirs(overlay_magisk_path, exist_ok=True)

    print("==> Installing magisk now ...")
    # 处理 64 位 so 文件
    lib64_path = os.path.join(unzip_path, "lib", "arm64-v8a")
    for parent, dirnames, filenames in os.walk(lib64_path):
        for filename in filenames:
            so_path = os.path.join(lib64_path, filename)  # so 文件路径
            so_name = re.search(r"lib(.*)\.so", filename)  # 提取 so 名称
            target_path = os.path.join(overlay_magisk_path, so_name.group(1))  # 目标路径
            shutil.copyfile(so_path, target_path)  # 拷贝 so 文件
            subprocess.check_call(["chmod", "+x", target_path])  # 赋予可执行权限

    # 处理 32 位 so 文件，只拷贝 libmagisk32.so
    lib32_path = os.path.join(unzip_path, "lib", "armeabi-v7a")
    shutil.copyfile(os.path.join(lib32_path, "libmagisk32.so"), os.path.join(overlay_magisk_path, "magisk32"))


if __name__ == '__main__':
    main()
