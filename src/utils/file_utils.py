"""
File Utilities - File operations and validation
文件工具 - 文件操作和验证
"""
import os
import shutil
from pathlib import Path
from typing import List, Tuple


class FileUtils:
    """File operation utilities"""

    SUPPORTED_AUDIO_EXTENSIONS = [".mp3"]

    @staticmethod
    def validate_directory(dir_path: str) -> Tuple[bool, str]:
        """
        Validate directory exists and has proper permissions
        Returns: (is_valid, error_message)
        """
        if not dir_path:
            return False, "目录路径不能为空"

        path = Path(dir_path)
        if not path.exists():
            return False, "所选目录不存在，请重新选择"

        if not os.access(path, os.R_OK):
            return False, "目录无读权限，请调整权限或更换目录"

        if not os.access(path, os.W_OK):
            return False, "目录无写权限，请调整权限或更换目录"

        return True, ""

    @staticmethod
    def get_audio_files(directory: str, recursive: bool = True) -> List[str]:
        """Get all MP3 files in directory
        Args:
            directory: directory path
            recursive: if True, search subdirectories recursively
        """
        path = Path(directory)
        audio_files = []
        for ext in FileUtils.SUPPORTED_AUDIO_EXTENSIONS:
            if recursive:
                audio_files.extend(path.rglob(f"*{ext}"))
            else:
                audio_files.extend(path.glob(f"*{ext}"))
        return sorted([str(f) for f in audio_files])

    @staticmethod
    def filter_files_by_rule(files: List[str], rule: str, value: str) -> List[str]:
        """
        Filter files by matching rule
        rule: keyword, prefix, suffix
        """
        if not value:
            return files

        filtered = []
        for file_path in files:
            filename = Path(file_path).name.lower()
            value_lower = value.lower()

            if rule == "keyword":
                keywords = [k.strip() for k in value.split(",") if k.strip()]
                if any(kw in filename for kw in keywords):
                    filtered.append(file_path)
            elif rule == "prefix":
                if filename.startswith(value_lower):
                    filtered.append(file_path)
            elif rule == "suffix":
                # Default filter for .mp3, allow custom
                suffix = value_lower if value_lower.startswith(".") else f".{value_lower}"
                if filename.endswith(suffix):
                    filtered.append(file_path)

        return filtered

    @staticmethod
    def generate_new_filename(original: str, rule: str, prefix: str, index: int, digits: int) -> str:
        """Generate new filename based on rule
        rule: preserve (保留原名), prefix_seq (前缀+序号), sequential (仅序号)
        """
        orig_name = Path(original).stem
        ext = Path(original).suffix
        seq = str(index).zfill(digits)

        if rule == "preserve":
            new_name = f"{prefix}{orig_name}" if prefix else orig_name
        elif rule == "prefix_seq":
            # 前缀 + 序号 + 原名
            new_name = f"{prefix}{seq}_{orig_name}" if prefix else f"{seq}_{orig_name}"
        else:  # sequential
            new_name = f"{prefix}{seq}" if prefix else seq

        return f"{new_name}{ext}"

    @staticmethod
    def organize_files(files: List[str], output_dir: str, new_names: List[str], mode: str) -> Tuple[int, int]:
        """
        Organize files to output directory
        Returns: (success_count, fail_count)
        """
        success = 0
        failed = 0

        for src_file, new_name in zip(files, new_names):
            dest = Path(output_dir) / new_name
            try:
                if mode == "copy":
                    shutil.copy2(src_file, dest)
                else:  # move
                    shutil.move(src_file, dest)
                success += 1
            except Exception as e:
                print(f"Failed to {mode} {src_file}: {e}")
                failed += 1

        return success, failed

    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Get file size in bytes"""
        return os.path.getsize(file_path)

    @staticmethod
    def open_directory(dir_path: str):
        """Open directory in file explorer"""
        os.startfile(dir_path)

    @staticmethod
    def open_file(file_path: str):
        """Open file with default application"""
        os.startfile(file_path)