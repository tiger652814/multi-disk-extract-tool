import os
import shutil
import tarfile
import threading
from time import sleep
from tqdm import tqdm
import logging
import zipfile
import patoolib
import string
import platform
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from collections import defaultdict
from tkinter import simpledialog

REQUIRED_SPACE_GB = 10
SWITCH_THRESHOLD_GB = 2
BACKUP_DISK = 'G'
ARCHIVE_PATH = 'D://Project_CodeNet.tar.gz'

logging.basicConfig(filename='unpack_log.txt', level=logging.INFO, format='%(asctime)s %(message)s')

def get_free_gb(drive):
    return shutil.disk_usage(drive + ':\\')[2] / (1024 ** 3)

def get_candidate_disks():
    system_drive = os.environ.get("SystemDrive", "C:").replace(':\\', '').replace(':', '')
    available = []
    for letter in string.ascii_uppercase:
        path = f"{letter}:\\"
        if os.path.exists(path) and letter != system_drive:
            available.append(letter)
    logging.info(f'🧭 可用数据磁盘（排除系统盘 {system_drive}:）：{available}')
    return available

CANDIDATE_DISKS = get_candidate_disks()

def find_disk():
    global CANDIDATE_DISKS
    CANDIDATE_DISKS = get_candidate_disks()
    for d in CANDIDATE_DISKS:
        if get_free_gb(d) >= REQUIRED_SPACE_GB:
            return d
    return None

def detect_backup_disk(possible_letters=['G', 'H', 'I', 'J']):
    if platform.system() == 'Windows':
        logging.info('🔍 正在检测 Windows 移动硬盘...')
        for letter in possible_letters:
            path = f'{letter}:\\'
            if os.path.exists(path):
                try:
                    output = os.popen(f'fsutil fsinfo drivetype {letter}:').read().lower()
                    if 'removable' in output:
                        logging.info(f'🔌 检测到移动硬盘（Windows）：{letter}:')
                        print(f'🔌 检测到移动硬盘（Windows）：{letter}:')
                        return letter
                except Exception:
                    continue
    else:
        for mount_root in ['/media', '/mnt', '/Volumes']:
            if os.path.exists(mount_root):
                for entry in os.listdir(mount_root):
                    full_path = os.path.join(mount_root, entry)
                    if os.path.ismount(full_path):
                        logging.info(f'🔌 检测到移动硬盘（POSIX）：{full_path}')
                        print(f'🔌 检测到移动硬盘（POSIX）：{full_path}')
                        return full_path
    return None

move_count = 0

def move_async(src, rel):
    global BACKUP_DISK, move_count
    if not os.path.exists(f'{BACKUP_DISK}:\\'):
        new_disk = detect_backup_disk()
        if new_disk:
            BACKUP_DISK = new_disk
        else:
            print('❌ 未检测到可用的移动硬盘，跳过搬运。')
            return
    import time
    start_time = time.time()
    print(f'🚚 正在开始移动：{rel}')
    print(f'📤 开始搬运 {rel} 到 {BACKUP_DISK}:\\archive_backup')
    dst = os.path.join(f'{BACKUP_DISK}:\\archive_backup', rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    logging.info(f'搬运 → {dst}')
    print(f'搬运 → {dst}')
    shutil.move(src, dst)
    logging.info(f'搬运完成 → {dst}')
    elapsed = time.time() - start_time
    print(f'✅ 搬运完成：{rel}，耗时 {elapsed:.2f} 秒')
    move_count += 1

def extract_tar(tar_path, override_extract_path=None):
    filter_keyword = simpledialog.askstring("部分解压（可选）", "输入要解压的子目录或文件关键词（留空表示全部解压）：")
    archive_name = os.path.splitext(os.path.basename(tar_path))[0]
    disk = find_disk()
    if not disk:
        raise RuntimeError("无磁盘可用")

    base_extract_path = override_extract_path or os.path.join(f'{disk}:\\unpack_temp', archive_name)
    os.makedirs(base_extract_path, exist_ok=True)
    print(f'使用磁盘 {disk}:\\')

    if tar_path.endswith(".tar.gz") or tar_path.endswith(".tgz"):
        with tarfile.open(tar_path, 'r:gz') as tar:
            idx = 0
            for member in tqdm(tar, desc="解压中", unit="file"):
                if filter_keyword and filter_keyword not in member.name:
                    continue
                if not member.name or member.isdir():
                    continue
                idx += 1
                print(f'➡️ 解压中：{member.name}')
                print(f'   📦 已完成数量：{idx} 个')
                print(f'   💽 当前磁盘({disk}:\\)剩余空间：{get_free_gb(disk):.2f} GB')
                top = member.name.split('/')[0]
                rel_path = os.path.join('unpack_temp', archive_name, member.name)
                target_path = os.path.join(f'{disk}:\\', rel_path)
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                try:
                    tar.extract(member, path=os.path.join(f'{disk}:\\unpack_temp', archive_name))
                    logging.info(f'已解压：{member.name} -> {disk}:\\{rel_path}')
                except Exception as e:
                    logging.warning(f'解压失败：{member.name} -> {e}')
                    continue
                if get_free_gb(disk) < SWITCH_THRESHOLD_GB:
                    folder_to_move = os.path.join(f'{disk}:\\unpack_temp', archive_name, top)
                    rel_to_move = os.path.join('unpack_temp', archive_name, top)
                    threading.Thread(target=move_async, args=(folder_to_move, rel_to_move)).start()
                    while True:
                        disk = find_disk()
                        if disk:
                            print(f'切换到 {disk}:\\')
                            break
                        print('等待释放空间...')
                        sleep(10)
    elif tar_path.endswith(".zip"):
        with zipfile.ZipFile(tar_path, 'r') as zip_ref:
            zip_ref.extractall(base_extract_path)
            print("✅ ZIP 解压完成")
        sort_extracted_files(base_extract_path)
    else:
        try:
            patoolib.extract_archive(tar_path, outdir=base_extract_path)
            print("✅ 其他压缩格式解压完成")
            try:
                sort_extracted_files(base_extract_path)
            except Exception as e:
                print(f"❌ 分类失败：{e}")
        except Exception as e:
            print(f"❌ 无法解压此格式：{e}")

def clean_temp_dirs():
    removed = 0
    for disk in get_candidate_disks():
        temp_path = os.path.join(f'{disk}:\\unpack_temp')
        if os.path.exists(temp_path):
            try:
                shutil.rmtree(temp_path)
                print(f'🧹 已清理：{temp_path}')
                logging.info(f'🧹 已清理：{temp_path}')
                removed += 1
            except Exception as e:
                print(f'❌ 无法删除 {temp_path}：{e}')
                logging.warning(f'❌ 无法删除 {temp_path}：{e}')
    if removed == 0:
        messagebox.showinfo("清理完成", "没有发现需要清理的临时目录。")
    else:
        messagebox.showinfo("清理完成", f"已清理 {removed} 个磁盘的临时目录。")

def show_disk_usage_bar():
    usage = {}
    for d in get_candidate_disks():
        try:
            total, used, free = shutil.disk_usage(f'{d}:\\')
            usage[d] = (free / total)
        except:
            continue
    if not usage:
        print("⚠️ 无法获取磁盘信息")
        return
    plt.bar(usage.keys(), [v * 100 for v in usage.values()])
    plt.ylabel('剩余空间 (%)')
    plt.title('候选磁盘剩余空间占比')
    plt.ylim(0, 100)
    plt.show()

def sort_extracted_files(base_path):
    categories = {
        '图片': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
        '文档': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'],
        '音视频': ['.mp3', '.wav', '.mp4', '.avi', '.mkv'],
        '安装包': ['.exe', '.msi', '.apk'],
        '其他': []
    }
    sorted_dirs = defaultdict(list)
    for root, dirs, files in os.walk(base_path):
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            moved = False
            for cat, exts in categories.items():
                if ext in exts:
                    sorted_dirs[cat].append(os.path.join(root, file))
                    moved = True
                    break
            if not moved:
                sorted_dirs['其他'].append(os.path.join(root, file))
    for cat, files in sorted_dirs.items():
        cat_path = os.path.join(base_path, f'_分类/{cat}')
        os.makedirs(cat_path, exist_ok=True)
        for f in files:
            try:
                shutil.move(f, os.path.join(cat_path, os.path.basename(f)))
            except Exception as e:
                logging.warning(f'❌ 无法分类文件 {f}：{e}')

def run_gui():
    root = tk.Tk()
    root.title("多磁盘解压工具")
    root.geometry("500x350")

    selected_files = []
    output_dir = tk.StringVar()

    def select_files():
        files = filedialog.askopenfilenames(title="选择压缩包", filetypes=[("压缩包", "*.zip *.rar *.7z *.tar.gz *.tgz")])
        if files:
            selected_files.clear()
            selected_files.extend(files)
            listbox.delete(0, tk.END)
            for f in files:
                listbox.insert(tk.END, os.path.basename(f))

    def select_folder():
        folder = filedialog.askdirectory(title="选择包含多个压缩包的文件夹")
        if folder:
            selected_files.clear()
            listbox.delete(0, tk.END)
            for f in os.listdir(folder):
                if f.endswith(('.zip', '.rar', '.7z', '.tar.gz', '.tgz')):
                    full_path = os.path.join(folder, f)
                    selected_files.append(full_path)
                    listbox.insert(tk.END, f)

    def select_output_dir():
        path = filedialog.askdirectory(title="选择解压输出目录")
        if path:
            output_dir.set(path)
            label_output_dir.config(text=f"输出目录：{path}")

    def select_single_file():
        file = filedialog.askopenfilename(title="选择单个压缩包", filetypes=[("压缩包", "*.zip *.rar *.7z *.tar.gz *.tgz")])
        if file:
            selected_files.clear()
            selected_files.append(file)
            listbox.delete(0, tk.END)
            listbox.insert(tk.END, os.path.basename(file))

    def start_unpack():
        if not selected_files:
            messagebox.showwarning("未选择文件", "请先选择要解压的压缩包文件。")
            return
        base_path_override = output_dir.get() or None
        for archive in selected_files:
            print(f"🚀 开始解压任务：{archive}")
            logging.info(f"🚀 开始解压任务：{archive}")
            try:
                extract_tar(archive, base_path_override)
            except Exception as e:
                print(f"❌ 解压失败：{e}")
                logging.error(f"❌ 解压失败：{e}")
        clean_temp_dirs()
        messagebox.showinfo("完成", f"已完成所有解压任务，搬运目录总数：{move_count}，临时目录已清理")

    tk.Label(root, text="选择需要解压的压缩包：").pack(pady=5)
    tk.Button(root, text="选择压缩包文件", command=select_files).pack(pady=5)
    tk.Button(root, text="扫描压缩包文件夹", command=select_folder).pack(pady=5)
    tk.Button(root, text="选择单个压缩包", command=select_single_file).pack(pady=5)
    listbox = tk.Listbox(root, height=6)
    listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
    tk.Button(root, text="选择输出目录", command=select_output_dir).pack(pady=5)
    label_output_dir = tk.Label(root, text="输出目录：未选择", fg="gray")
    label_output_dir.pack()
    tk.Button(root, text="查看磁盘空间", command=show_disk_usage_bar).pack(pady=5)
    tk.Button(root, text="清理临时目录", command=clean_temp_dirs).pack(pady=5)
    tk.Button(root, text="开始解压", command=start_unpack).pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    import atexit
    def summary():
        print(f'📦 总计完成搬运 {move_count} 个目录')
        logging.info(f'总计完成搬运 {move_count} 个目录')
    atexit.register(summary)
    run_gui()
