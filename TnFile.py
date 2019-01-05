# -*- coding: utf-8 -*-

import sys, io

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk, Gdk, Pango

import json, re

import TnDef

class TnFile:

  def __init__(self, parent_window, treestore):
    self.parent_window = parent_window
    self.filename = None
    self.treestore = treestore

  def get_filename(self):
    return self.filename


  def new_file(self):
    self.filename = None
    self.treestore.clear()

  def open_file(self):
    response, filename = self.open_file_dialog()
    if response == Gtk.ResponseType.OK:
      self.filename = filename
      self.treestore.clear()
      self.load_store_from_file()
    return response

  def save_file(self):
    response = Gtk.ResponseType.CANCEL
    if self.filename == None:
      response, self.filename = self.save_file_dialog()
    if response == Gtk.ResponseType.OK:
      self.save_store_to_file()
    return response

  def save_file_as(self):
    response, filename = self.save_file_dialog()
    if response == Gtk.ResponseType.OK:
      self.filename = filename
      self.save_store_to_file()
    return response

  def close_file(self):
    self.new_file()


  def save_changes_dialog(self): # return YES/NO

    message = "Would you like to save your changes?"
    dialog = Gtk.MessageDialog(self.parent_window, 0,
      Gtk.MessageType.QUESTION,
      Gtk.ButtonsType.YES_NO, message)
    response = dialog.run()
    dialog.destroy()

    return response

  def get_filter(self):
    filter = Gtk.FileFilter()
    filter.set_name(TnDef.FILE_FORMAT)
    filter.add_pattern(TnDef.FILE_PATTERN)
    return filter

  def open_file_dialog(self): # return OK/CANCEL
    dialog = Gtk.FileChooserDialog('Open File', self.parent_window,
                                   Gtk.FileChooserAction.OPEN,
                                   (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

    dialog.add_filter(self.get_filter())

    filename = None
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
      filename = dialog.get_filename()
    dialog.destroy()

    return [response, filename]

  def save_file_dialog(self): # return OK/CANCEL
    dialog = Gtk.FileChooserDialog('Save File', self.parent_window,
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

    return [response, filename]


  def save_store_to_file(self):

    data = self.copy_data_from_store();

    f = io.open(self.filename, 'w', encoding='utf-8')
    f.write(TnDef.FILE_HEADER + "\n")

    # json.dumps return utf-8 as str. it is a bug.
    dump_utf8 = unicode(json.dumps(data, encoding='utf-8'))
    f.write(dump_utf8)

    f.close

  def load_store_from_file(self):

    f = io.open(self.filename, 'r', encoding='utf-8')
    first_line = f.readline().rstrip()
    if first_line != TnDef.FILE_HEADER:
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
