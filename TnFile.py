# -*- coding: utf-8 -*-

import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk, Gdk, Pango

import json, re


FILE_FORMAT = "<TNF v0.1>"
FILE_PATTERN = "*.tnf"

OK = 0
CANCEL = -1

class TnFile:

  def __init__(self, parent_window, treestore):
    self.parent_window = parent_window
    self.filename = None
    self.treestore = treestore


  def new_file(self):
    self.filename = None
    self.treestore.clear()

  def open_file(self):
    filename = self.open_dialog()
    if filename != None:
      self.filename = filename
      self.load_store_from_file()

  def save_file(self):
    if self.filename == None:
      self.filename = self.save_dialog()

    if self.filename != None:
      self.save_store_to_file()
      return OK
    else:
      return CANCEL

  def save_file_as(self):
    filename = self.save_dialog()
    if filename != None:
      self.filename = filename
      self.save_store_to_file()
      return OK
    else:
      return CANCEL

  def close_file(self):
    self.new_file()


  def get_filename(self):
    return self.filename


  def changed_dialog(self, message):
    message = "There are some changes.\n Would you like to save it?"
    dialog = Gtk.MessageDialog(self.parent_window,
                               Gtk.DialogFlags.MODAL,
                               Gtk.MessageType.QUESTION,
                               Gtk.ButtonsType.YES_NO,
                               message)
    response = dialog.run()
    dialog.destroy()

    if response == Gtk.ResponseType.YES:
      ret = self.save_file()
      if ret == CANCEL:
        return CANCEL
    elif response == Gtk.ResponseType.NO:
      pass
    else:
      return CANCEL

    return OK

  def get_filter(self):
    filter = Gtk.FileFilter()
    filter.set_name("Text files")
    filter.add_mime_type("text/plain")
    filter.add_pattern(FILE_PATTERN)
    return filter

  def open_dialog(self):
    dialog = Gtk.FileChooserDialog("Open File", self.parent_window,
                                   Gtk.FileChooserAction.OPEN,
                                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

    dialog.add_filter(self.get_filter())

    filename = None
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
      filename = dialog.get_filename()
    dialog.destroy()

    return filename

  def save_dialog(self):
    dialog = Gtk.FileChooserDialog("Save File", self.parent_window,
                                   Gtk.FileChooserAction.SAVE,
                                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

    dialog.add_filter(self.get_filter())
    dialog.set_do_overwrite_confirmation(True)

    filename = None
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
      filename = dialog.get_filename()
    dialog.destroy()

    return filename


  def save_store_to_file(self):

    data = self.copy_data_from_store();

    f = open(self.filename, "w", encoding="UTF-8")
    f.write(FILE_FORMAT + "\n")
    json.dump(data, f)
    f.close

  def load_store_from_file(self):

    f = open(self.filename, "r", encoding="UTF-8")
    first_line = f.readline().rstrip()
    if first_line != FILE_FORMAT:
      return
    data = json.load(f)
    f.close

    self.copy_data_to_store(data)


  def copy_data_from_store(self):

    def recursive_read(itr):
      data = []

      while itr != None:
        path_str = self.treestore.get_string_from_iter(itr)
        text = self.treestore[itr][0]
        data.append((path_str, text))

        child_itr = self.treestore.iter_children(itr)
        if child_itr != None:
          child_data = recursive_read(child_itr)
          data += child_data

        itr = self.treestore.iter_next(itr)

      return data

    itr = self.treestore.get_iter_first()
    data = recursive_read(itr)

    return data

  def copy_data_to_store(self, data):

    for path_str, text in data:
      path_list = re.split(r':', path_str)
      del path_list[-1]
      if len(path_list) > 0:
        path_str = ':'.join(path_list)
        itr = self.treestore.get_iter_from_string(path_str)
      else:
        itr = None
      self.treestore.append(itr, (text,))


# end of file
