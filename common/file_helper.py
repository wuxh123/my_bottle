#!/usr/bin/env python
# coding=utf-8

import os
import shutil
from common import log_helper


def read_file(file_path, encoding='utf-8'):
    """读取文本文件内容"""
    all_line = None
    try:
        if exists(file_path):
            fsock = open(file_path, "r", encoding=encoding)
            all_line = fsock.readlines()
            fsock.close()
    except Exception as e:
        pass
    return all_line


def read_file_line(file_path, encoding='utf-8'):
    if not exists(file_path):
        return
    with open(file_path, 'r', encoding=encoding) as f:
        while True:
            block = f.readline()
            if block:
                yield block
            else:
                return


def save_file(file_path, content, encoding='utf-8'):
    """保存内容到文件里"""
    try:
        file_object = open(file_path, 'a', encoding=encoding)
        file_object.write(content)
        file_object.close()
        return True
    except Exception as e:
        return False


def copy_file(file_path, save_path):
    """复制文件"""
    try:
        if shutil.copyfile(file_path, save_path):
            os.remove(file_path)
            return True
    except Exception as e:
        pass
    return False



def remove_file(file_path):
    """删除文件"""
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            return True
    except:
        pass
    return False


def remove_all_file(file_list):
    """批量删除文件"""
    try:
        for file_path in file_list:
            remove_file(file_path)
    except:
        pass


def exists(file_path):
    """检查文件是否存在"""
    return os.path.exists(file_path)


def create_dirs(dirs_path):
    """
    创建文件夹（可一次性创建多层文件夹）
    :param dirs_path: 文件夹路径
    :return:
    """
    try:
        if not exists(dirs_path):
            os.makedirs(dirs_path)
    except:
        pass

def get_file_size(filePath):
    """
    读取文件大小
    :param filePath: 文件存储路径
    :return:
    """
    if not exists(filePath):
        return 0
    try:
        return os.path.getsize(filePath)
    except Exception as e:
        log_helper.info(str(e))
        return 0


def get_dir(dir_path):
    """获取当前路径下所有子目录"""
    for root, dirs, files in os.walk(dir_path):
        return dirs


def get_dir_files(dir_path):
    """获取当前路径下所有非目录子文件"""
    for root, dirs, files in os.walk(dir_path):
        return files


if __name__ == '__main__':
    print(get_dir('f:\\'))