# -*- codeing = utf-8 -*-
# @Time : 2022/4/12 22:16
# @Author : jszmwq
# @File : globalvar.py
# @Software: PyCharm


class globalvar():
    _instance = None
    init_flag = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if globalvar.init_flag:
            return
        else:
            self._global_dict = {}
            globalvar.init_flag = True

    def set_value(self, name, value):
        self._global_dict[name] = value

    def get_value(self, name, defValue=None):
        try:
            return self._global_dict[name]
        except KeyError:
            return defValue
