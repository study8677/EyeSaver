# 护眼提醒项目 (Eye Saver)

这是一个简单的 Windows 桌面应用程序，旨在帮助用户每隔 50 分钟休息一下眼睛，以保护视力。

## 功能

- **定时提醒**: 每工作 50 分钟，弹出系统通知提醒休息。
- **系统托盘**: 在系统托盘显示图标，右键可退出程序。
- **轻量级**: 占用资源极少。

## 安装与运行

本项目使用 `uv` 进行依赖管理。

1.  克隆仓库:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  安装依赖并运行:
    ```bash
    uv run src/main.py
    ```

## 开发

- 依赖管理: `uv add <package>`
- 运行: `uv run src/main.py`

## 许可证

MIT
