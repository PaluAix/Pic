# 作品概述

这是一个图片分类器，可以将压缩包内的文件按照尺寸进行分类

本作品采用 Python 和 HTML 编写，专注于解决实际问题

在技术上，本作品可以归为“信息管理系统”

仓库地址：https://github.com/PaluAix/Pic

## 环境

### 开发环境
- 操作系统: Ubuntu 22.04.4 LTS
- Python 版本: 3.11

### 运行环境

- Python 版本需在 3.9 以上
- 需要通畅的网络连接

## 本地部署

1. 首先，确保已安装以下两个依赖：
   ```
   pip install Flask
   pip install pillow
   ```

2. 运行 app.py。

3. 在本地打开浏览器，并访问 `http://127.0.0.1:8888/`，即可进入服务页面。

4. 上传需要处理的图包，每个尺寸都提供了压缩包下载

## 云服务器测试服务

按照要求，同样部署了云上的测试服务，可以直接使用

http://207.148.94.213:8888/

## 测试数据

文件夹下附有部分测试数据（Data.zip）