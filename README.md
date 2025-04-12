# Multi-Disk Extraction Tool

<img src="icon.png" alt="Multi-Disk Extractor Icon" width="120" align="right" />

A brand new, intelligent extraction tool that supports multi-disk auto-switching, ensuring a smooth and efficient extraction process. This tool supports extracting various file formats such as `.zip`, `.tar.gz`, `.7z`, `.rar`, and more, while managing disk space intelligently. It can be used in both graphical interface mode (GUI) and command-line interface (CLI) mode.

---

## Features

- **Multi-disk support**: Automatically switches between available disks based on free space.
- **Intelligent file classification**: Automatically categorizes extracted files (e.g., images, documents, videos).
- **Partial extraction**: Allows you to extract specific folders or files within a compressed archive.
- **Backup support**: Moves extracted files to external storage or backup disks when needed to free up space.
- **Cross-platform**: Works on both Windows and POSIX-based systems (Linux/macOS).
- **User-friendly GUI**: Easily select files or folders to extract, choose output directories, and monitor progress.
- **Automatic disk space management**: Ensures that extraction will continue without errors due to insufficient space.
- **Clear temporary directories**: Removes temporary files from the disk after extraction.

---

## Installation

### Requirements

- Python >= 3.8
- Libraries: `tqdm`, `patoolib`, `matplotlib`

```bash
pip install tqdm patoolib matplotlib
```

For extracting `.7z` and `.rar` files, you will need to have [7-Zip](https://www.7-zip.org/) or [WinRAR](https://www.rarlab.com/) installed and added to your system path.

---

## Usage

### 1. GUI Mode (Recommended)

To use the graphical interface, simply run:

```bash
python main.py
```

The GUI will allow you to:
- Select compressed files
- Scan a folder for archives
- Choose output directory
- View disk usage bar
- Clean temporary folders

### 2. CLI Mode (Batch Processing)

For command-line usage, set the archive path at the top of `main.py`:

```python
ARCHIVE_PATH = 'D://Project_CodeNet.tar.gz'
```

Then run:

```bash
python main.py
```

If this variable is set, the program automatically enters CLI mode and performs extraction.

### 3. Partial Extraction

When extracting `.tar.gz` or `.zip` files, the program allows you to enter a **keyword** to only extract specific subfolders or files matching that keyword. Just enter it when prompted by the dialog box. Leave it blank to extract all.

---

## File Classification

Extracted files are automatically sorted by file type into structured folders:

```
_unpacked/
├── _分类/
│   ├── 图片/        # .jpg, .png, .bmp, etc.
│   ├── 文档/        # .pdf, .docx, .txt, .xlsx, etc.
│   ├── 音视频/      # .mp3, .mp4, .avi, .mkv, etc.
│   ├── 安装包/      # .exe, .msi, .apk, etc.
│   └── 其他/        # uncategorized files
```

---

## License

This project is licensed under the Apache-2.0 License. See the [LICENSE](LICENSE) file for more details.

---

## Contributing

We welcome contributions! You can:
- Fork this repository
- Submit bug reports or feature requests via [Issues](https://github.com/tiger652814/your-repo/issues)
- Create pull requests to improve the code or documentation

Please make sure to follow the coding standards and write clear commit messages.

---

## 🛠 Usage Demo

![Extraction Process Demo](extract-process.gif)

This demo shows the full workflow: selecting archive(s), switching disks, extracting files, and sorting them into classified folders.

---

## 📝 Authors

- **tiger** ([@tiger652814]((https://github.com/tiger652814)))

---

## 🌍 Acknowledgments

- This tool was inspired by real-world extraction needs involving large archive files across multiple disks.
- Special thanks to the open-source Python ecosystem and the `tqdm`, `patoolib`, and `matplotlib` libraries.
- Shoutout to users for feedback and feature suggestions!

