#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

class ToDoItem(object):
    """
    ToDo項目を保持するクラス
    """

    def __init__(self, title, description, duedate, addeddate=None):
        """
        ToDo項目のインスタンスを初期化する
        """
        if not addeddate:
            addeddate = datetime.now()
        self.title = title
        self.description = description
        self.duedate = duedate
        self.finished = False
        self.finisheddate = None

    def finish(self, date=None):
        """
        ToDo項目を終了する
        """
        self.finished = True
        if not date:
            date = datetime.now()
        self.finisheddate = date

    def __repr__(self):
        """
        ToDo項目の表示形式文字列をつくる
        """
        return "<ToDoItem %s, %s>" % (self.title, self.duedate.strftime('%Y/%m/%d %H:%M'))

