# 多磁盘智能解压工具（Multi-Disk Extraction Tool）

<img src="icon.png" alt="项目图标" width="120" align="right" />

这是一款全新开发的智能解压缩工具，支持多磁盘自动切换、空间不足自动搬运，并兼容 `.zip`、`.tar.gz`、`.7z`、`.rar` 等多种压缩格式。支持图形界面（GUI）与命令行（CLI）两种运行模式。

---

## 功能特点

- **多磁盘支持**：自动检测并切换剩余空间充足的磁盘解压
- **自动搬运机制**：空间不足时，将已解压数据搬运至移动硬盘继续解压
- **文件自动分类**：根据文件类型自动归类（文档、图片、音视频、安装包等）
- **部分内容提取**：可输入关键词，选择性解压压缩包中的部分文件夹/文件
- **图形界面友好**：支持文件选择、磁盘查看、临时清理等完整交互
- **跨平台兼容**：支持 Windows 和类 Unix 系统（Linux/macOS）
- **自动清理临时文件夹**：避免磁盘空间浪费

---

## 安装指南

### 依赖环境
- Python >= 3.8
- 所需依赖：

```bash
pip install tqdm patoolib matplotlib
```

> 若需支持 `.rar` 或 `.7z` 文件，请确保安装并配置好 7-Zip 或 WinRAR。

---

## 使用方式

### 1. 图形界面模式（推荐）

直接运行：

```bash
python main.py
```

支持操作：
- 选择单个或多个压缩包
- 扫描文件夹内所有压缩包
- 自定义解压输出目录
- 查看磁盘空间柱状图
- 一键清理临时目录

### 2. 命令行模式（批处理）

修改脚本中：

```python
ARCHIVE_PATH = 'D://Project_CodeNet.tar.gz'
```

然后运行：

```bash
python main.py
```

程序会自动识别 CLI 模式并执行解压任务。

### 3. 关键词部分提取

当解压 `.zip` 或 `.tar.gz` 文件时，弹出输入框，可填写关键子路径，如 `images/` 或 `README`，仅解压包含该关键词的文件。

留空则表示解压全部内容。

---

## 解压后分类目录结构

程序会自动将解压内容分类存入以下路径：

```
_unpacked/
├── _分类/
│   ├── 图片/       (.jpg, .png, .gif, .bmp)
│   ├── 文档/       (.pdf, .docx, .txt, .xlsx)
│   ├── 音视频/     (.mp3, .mp4, .avi, .mkv)
│   ├── 安装包/     (.exe, .msi, .apk)
│   └── 其他/
```

---

## 许可证（License）

本项目采用 **Apache License 2.0** 开源协议，允许用于商业和非商业项目，支持修改、再发布并提供专利权利保护。详情见 [LICENSE](LICENSE) 文件。

---

## 贡献方式（Contributing）

欢迎任何形式的贡献：
- Fork 本仓库并提交 PR
- 提交 bug 或功能建议 [Issues](https://github.com/tiger652814/your-repo/issues)
- 增加文档或优化界面交互

请使用清晰的提交信息，并遵循 PEP8 编码规范。

---

## 🛠 使用演示（GIF）

![解压演示](extract-process.gif)

此动画展示了：压缩包选择 → 解压 → 自动搬运 → 分类归档 → 清理临时目录 的完整过程。

---

## 📝 作者（Author）

- **tiger**（[@tiger652814](https://github.com/tiger652814)）

---

## 🌍 致谢（Acknowledgments）

- 致谢 Python 开源社区与 `tqdm`、`patoolib`、`matplotlib` 等优秀库
- 感谢测试者与反馈用户的建议与灵感
- 若本工具对你有所帮助，欢迎 Star 🌟、Fork、交流！
