# -*- coding: utf-8 -*-
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: Pycharm
# @Create  : 2022/8/27 12:07
# @Update  : 2024/3/12 13:26
# @Detail  : 描述

import os
import traceback
from concurrent.futures import as_completed
from typing import Optional
from Utils.type_hints import StrPath

from loguru import logger


def log_result(fs, func_name, region: Optional[str] = '', log_path: StrPath = ''):
    """
    对异步函数的结果进行日志记录
    :param fs: 迭代对象
    :param func_name: 函数名
    :param region: 地区
    :param log_path: 日志路径
    :return:
    """
    _log_file = os.path.join(log_path, f'{func_name}.{region}.log')
    error_list = []
    for f in as_completed(fs):
        try:
            f.result()
        except Exception as exc:
            error_list.append((fs[f], exc))
            logger.warning(f'{func_name}, 遇到错误: {exc}, {fs[f]}')
            traceback.print_exc()

        else:
            logger.debug(f'{func_name}, 完成: {fs[f]}')

    if error_list:
        logger.error(f'{func_name}, 以下文件遇到错误: {error_list}')

    with open(_log_file, 'a+', encoding='utf-8') as f:
        for item in error_list:
            f.write(f'{item}\n')
