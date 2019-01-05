# -*- coding: utf-8 -*-

import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk, Gdk, Pango


class TnView:

  def __init__(self, parent_window):

    self.parent_window = parent_window
    self.changed = False

    self.treestore = Gtk.TreeStore(str)
    self.treestore.connect("row_changed", self.on_row_changed)
    self.treestore.connect("row_inserted", self.on_row_inserted)
    self.treestore.connect("row_deleted", self.on_row_deleted)

    self.treeview = Gtk.TreeView(model=self.treestore)
    self.treeview.set_headers_visible(False)
    self.treeview.set_enable_tree_lines(True)
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

  def get_widget(self):
    return self.treeview
  def get_store(self):
    return self.treestore

  def clear_changed(self):
    self.changed = False
  def get_changed(self):
    return self.changed

    #

  def edit_add_after(self):
    path, _ = self.treeview.get_cursor()
    if path != None:
      itr = self.treestore.get_iter(path)
      new_itr = self.treestore.insert_after(self.treestore.iter_parent(itr),
                                            itr)
    else:
      new_itr = self.treestore.append(None)

    new_path = self.treestore.get_path(new_itr)
    self.treeview.set_cursor(new_path)

  def edit_add_before(self):
    path, _ = self.treeview.get_cursor()
    if path != None:
      itr = self.treestore.get_iter(path)
      new_itr = self.treestore.insert_before(self.treestore.iter_parent(itr),
                                             itr)
    else:
      new_itr = self.treestore.append(None)

    new_path = self.treestore.get_path(new_itr)
    self.treeview.set_cursor(new_path)

  def edit_add_child(self):
    path, _ = self.treeview.get_cursor()
    if path != None:
      itr = self.treestore.get_iter(path)
      new_itr = self.treestore.append(itr)

      self.treeview.expand_row(path, False)

  def edit_delete(self):
    path, _ = self.treeview.get_cursor()
    if path != None:
      itr = self.treestore.get_iter(path)
      self.treestore.remove(itr)

  def view_expand(self):
    path, _ = self.treeview.get_cursor()
    if path != None:
      self.treeview.expand_row(path, False)
  def view_fold(self):
    path, _ = self.treeview.get_cursor()
    if path != None:
      self.treeview.collapse_row(path)

  def view_expand_all(self):
    self.treeview.expand_all()
  def view_fold_all(self):
    self.treeview.collapse_all()

    #

  def on_row_changed(self, tree_model, path, iter):
    self.changed = True
  def on_row_inserted(self, tree_model, path, iter):
    self.changed = True
  def on_row_deleted(self, tree_model, path):
    self.changed = True

  def on_key_press_event(self, widget, event):

    if event.state & Gdk.ModifierType.CONTROL_MASK:
      if event.keyval == Gdk.KEY_a:
        self.edit_add_after()
        return True
      elif event.keyval == Gdk.KEY_b:
        self.edit_add_before()
        return True
      elif event.keyval == Gdk.KEY_c:
        self.edit_add_child()
        return True
      elif event.keyval == Gdk.KEY_d:
        self.edit_delete()
        return True

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

# end of file
