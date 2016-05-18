# -*- coding: utf-8 -*-

import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk, Gdk, Pango


class TnView:

  def __init__(self, parent_window, debug=False):

    self.parent_window = parent_window
    self.changed = False
    self.debug = debug

    self.treestore = Gtk.TreeStore(str)
    self.treeview = Gtk.TreeView(model=self.treestore)
    self.treeview.set_headers_visible(False)
    self.treeview.set_grid_lines(Gtk.TreeViewGridLines.HORIZONTAL)
    self.treeview.set_reorderable(True)
    self.treeview.connect("key-press-event", self.on_key_press_event)

    self.renderer = Gtk.CellRendererText()
    self.renderer.set_property("editable", True)
    #self.renderer.set_property("wrap-mode", Pango.WrapMode.CHAR)
    #self.renderer.set_property("wrap-width", 80)
    self.renderer.connect("edited", self.on_text_edited)

    self.column = Gtk.TreeViewColumn("", self.renderer, text=0)
    self.treeview.append_column(self.column)

    #self.selection = self.treeview.get_selection()
    #self.selection.set_mode(Gtk.SelectionMode.MULTIPLE)

    if self.debug:
      self.count = 0

  def get_widget(self):
    return self.treeview
  def get_store(self):
    return self.treestore

  def clear_changed(self):
    self.changed = False
  def get_changed(self):
    return self.changed

  def on_key_press_event(self, widget, event):
    if event.keyval == Gdk.KEY_Right:
      self.view_expand()
      return True
    elif event.keyval == Gdk.KEY_Left:
      self.view_fold()
      return True
    return False

  def on_text_edited(self, widget, path, new_text):
    old_text = self.treestore[path][0]
    if new_text != old_text:
      self.treestore[path][0] = new_text
      self.changed = True

  def edit_add_after(self):
    path, column = self.treeview.get_cursor()
    if path != None:
      itr = self.treestore.get_iter(path)
      new_itr = self.treestore.insert_after(self.treestore.iter_parent(itr),
                                            itr)
    else:
      new_itr = self.treestore.append(None)

    new_path = self.treestore.get_path(new_itr)
    self.treeview.set_cursor(new_path)
    self.changed = True

    if self.debug:
      self.treestore[new_itr][0] = self.debug_row_id()

  def edit_add_before(self):
    path, column = self.treeview.get_cursor()
    if path != None:
      itr = self.treestore.get_iter(path)
      new_itr = self.treestore.insert_before(self.treestore.iter_parent(itr),
                                             itr)
    else:
      new_itr = self.treestore.append(None)

    new_path = self.treestore.get_path(new_itr)
    self.treeview.set_cursor(new_path)
    self.changed = True

    if self.debug:
      self.treestore[new_itr][0] = self.debug_row_id()

  def edit_add_child(self):
    path, column = self.treeview.get_cursor()
    if path != None:
      itr = self.treestore.get_iter(path)
      new_itr = self.treestore.append(itr)
      self.changed = True

      self.treeview.expand_row(path, False)

      if self.debug:
        self.treestore[new_itr][0] = self.debug_row_id()

  def edit_delete(self):
    path, column = self.treeview.get_cursor()
    if path != None:
      itr = self.treestore.get_iter(path)
      self.treestore.remove(itr)
      self.changed = True

  def view_expand(self):
    path, column = self.treeview.get_cursor()
    if path != None:
      self.treeview.expand_row(path, False)
  def view_fold(self):
    path, column = self.treeview.get_cursor()
    if path != None:
      self.treeview.collapse_row(path)

  def view_expand_all(self):
    self.treeview.expand_all()
  def view_fold_all(self):
    self.treeview.collapse_all()

  def debug_row_id(self):
    id = self.count
    self.count += 1
    return str(id)

# end of file
