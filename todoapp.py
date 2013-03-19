#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from pickle import dump, load

# GUI
from Tkinter import *
import tkMessageBox

# ToDo
from todoitem import ToDoItem
from todocontainer import ToDoContainer


# データ保存用ファイル名
DUMPFILE = 'todo.dat'

class ToDoApp(Frame):
    """
    ToDo GUIアプリ
    """


    def createwidgets(self):
        """
        ウィンドウに部品を配置
        """

        # スクロールバー付きリストボックス
        self.frame1 = Frame(self)
        frame = self.frame1
        self.listbox = Listbox(frame, height=10, width=30,
                                selectmode = SINGLE,
                                takefocus = 1)
        self.yscroll = Scrollbar(frame, orient=VERTICAL)

        # 配置を決める
        self.listbox.grid(row=0, column=0, sticky=NS)
        self.yscroll.grid(row=0, column=1, sticky=NS)

        # binding
        self.yscroll.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.yscrol1.set)
        self.listbox.bind("<ButtonRelease-1>", self.selectitem)
        self.frame1.grid(row=0, column=0)


    def setlistitems(self):
        """
        ToDo項目をlistboxに表示する
        """
        self.listbox.delete(0, END)
        for todo in self.todos.get_remaining_todos():
            d = todo.duedate
            t = todo.title.ljust(20)
            if todo.duedate < datetime.now():
                # ToDoの期限が過ぎていたら'*'をつける
                t = '* ' + t
            item = "%s %4d/%02d/%02d %02d:%02d" % (
                    t, d.year, d.month, d.day, d.hour, d.minute)
            self.listbox.insert(END, item)

    def refrectententries(self, todo):
        """
        フィールドに入力された文字列をToDoItemインスタンスに反映する
        """
        todo.title = self.title_e.get()
        todo.description = self.description_e.get()
        dt = datetime.strptime(self.duedate_e.get()+' :00', '%Y/%m/%d %H:%M:%S')
        todo.duedate = dt
        if self.finished_v.get() != 0:
            todo.finishe()

    def createitem(self):
        """
        新しいToDoアイテムを創る
        """
        todo = ToDoItem('', '', datetime.now())
        self.refrectententries(todo)
        self.todos += todo
        self.clearentries()
        self.setlistitems()
        self.sel_index = -1
        self.save()

    def refreshitems(self):
        """
        指定時間になったら警告を出す
        ToDo項目のうち時間になった者があればダイアログでしらせる
        """
        dirty = False
        for todo in self.todos.get_remaining_todos():
            td = datetime.now()
            d = todo.duedate
            if (d.year   == td.year   and
                d.month  == td.month  and
                d.day    == td.day    and
                d.hour   == td.hour   and
                d.minute == td.minute):
                msg = u"[%s] \n %s\n %s" % (
                        todo.title, todo.description,
                        todo.duedate.strftime('%Y/%m/%d %H:%M'))
            tkMessageBox.showwarning(u"時間です", msg)
            dirty = True
        sec = datetime.now().second
        self.after((60-sec)*1000, self.refreshitems)

        if dirty:
            self.setlistitems()

    def load(self):
        """
        ToDo項目のデータを読み込む
        """
        try:
            f = open(DUMPFILE, 'r')
            self.todos = load(f)
        except IOError:
            self.todos = ToDoContainer()

    def save(self):
        """
        ToDo項目データをファイルに保存
        """
        f = open(DUMPFILE, 'w')
        dump(self.todos, f)



