# linux-arabic-lexicon

阿拉伯语词汇数据集与工具集。

## 简介

本项目提供阿拉伯语词汇、英文释义及用法的数据集，支持多语言检索与学习，助力自然语言处理研究与教育应用。

## 功能特性

- 提供结构化的阿拉伯语词汇与英文释义数据。
- 支持多语言检索与学习。
- 适用于自然语言处理（NLP）研究与教育应用。
- 包含命令行工具与桌面端入口。

## 目录结构

- `arabic_lexicon/`: 核心数据集与逻辑模块。
- `bin/`: 可执行脚本或二进制文件。
- `debian/`: Debian 打包相关文件。
- `LICENSE`: 开源协议文件（GPL-3.0）。
- `Makefile`: 项目构建与安装脚本。
- `araby.desktop`: 桌面快捷方式配置。
- `araby.svg`: 项目图标资源。

## 快速开始

### 克隆仓库

```
git clone https://gitee.com/lysator/linux-arabic-lexicon.git

cd linux-arabic-lexicon
```

### 构建与安装

项目包含 `Makefile`，可尝试使用以下命令进行构建或安装：

```
make

sudo make install
```
## 使用说明

安装完成后，可通过命令行工具或桌面快捷方式（`araby.desktop`）启动应用进行词汇检索与学习。

## 贡献指南

欢迎提交 Issue 和 Pull Request 来完善数据集或改进工具。

## 开源协议

本项目基于 [GPL-3.0](LICENSE) 协议开源。
