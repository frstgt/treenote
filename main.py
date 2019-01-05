# -*- coding: utf-8 -*-

import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk, Gdk, Pango

import TnView, TnFile, TnDef

# This would typically be its own file
MENU_XML="""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <submenu>
      <attribute name="label" translatable="yes">File</attribute>
      <section>
        <item>
          <attribute name="action">win.new</attribute>
          <attribute name="label" translatable="yes">_New</attribute>
          <attribute name="accel">&lt;Primary&gt;n</attribute>
        </item>
        <item>
          <attribute name="action">win.open</attribute>
          <attribute name="label" translatable="yes">_Open</attribute>
          <attribute name="accel">&lt;Primary&gt;o</attribute>
        </item>
        <item>
          <attribute name="action">win.save</attribute>
          <attribute name="label" translatable="yes">_Save</attribute>
          <attribute name="accel">&lt;Primary&gt;s</attribute>
        </item>
        <item>
          <attribute name="action">win.save_as</attribute>
          <attribute name="label" translatable="yes">Save As</attribute>
        </item>
        <item>
          <attribute name="action">win.close</attribute>
          <attribute name="label" translatable="yes">Close</attribute>
        </item>
      </section>
      <section>
        <item>
          <attribute name="action">app.quit</attribute>
          <attribute name="label" translatable="yes">_Quit</attribute>
          <attribute name="accel">&lt;Primary&gt;q</attribute>
        </item>
      </section>
    </submenu>
    <submenu>
      <attribute name="label" translatable="yes">Edit</attribute>
      <section>
        <item>
          <attribute name="action">win.add_after</attribute>
          <attribute name="label" translatable="yes">Add _After</attribute>
        </item>
        <item>
          <attribute name="action">win.add_before</attribute>
          <attribute name="label" translatable="yes">Add _Before</attribute>
        </item>
        <item>
          <attribute name="action">win.add_child</attribute>
          <attribute name="label" translatable="yes">Add _Child</attribute>
        </item>
        <item>
          <attribute name="action">win.delete</attribute>
          <attribute name="label" translatable="yes">_Delete</attribute>
        </item>
      </section>
    </submenu>
    <submenu>
      <attribute name="label" translatable="yes">View</attribute>
      <section>
        <item>
          <attribute name="action">win.expand_all</attribute>
          <attribute name="label" translatable="yes">Expand All</attribute>
        </item>
        <item>
          <attribute name="action">win.fold_all</attribute>
          <attribute name="label" translatable="yes">Fold All</attribute>
        </item>
      </section>
    </submenu>
  </menu>
</interface>
"""

class AppWin(Gtk.ApplicationWindow):

  def __init__(self, *args, **kwargs):
    super(AppWin, self).__init__(*args, **kwargs)

    self.set_default_size(640, 480)

    self.scrolledwin = Gtk.ScrolledWindow()
    self.tnview = TnView.TnView(parent_window=self)
    self.tnfile = TnFile.TnFile(parent_window=self,
                                treestore=self.tnview.get_store())

    self.scrolledwin.add(self.tnview.get_widget())
    self.add(self.scrolledwin)

    self.scrolledwin.show()
    self.tnview.get_widget().show()

    #

    action = Gio.SimpleAction.new("new", None)
    action.connect("activate", self.on_new)
    self.add_action(action)

    action = Gio.SimpleAction.new("open", None)
    action.connect("activate", self.on_open)
    self.add_action(action)

    action = Gio.SimpleAction.new("save", None)
    action.connect("activate", self.on_save)
    self.add_action(action)

    action = Gio.SimpleAction.new("save_as", None)
    action.connect("activate", self.on_save_as)
    self.add_action(action)

    action = Gio.SimpleAction.new("close", None)
    action.connect("activate", self.on_close)
    self.add_action(action)

    action = Gio.SimpleAction.new("add_after", None)
    action.connect("activate", self.on_add_after)
    self.add_action(action)

    action = Gio.SimpleAction.new("add_before", None)
    action.connect("activate", self.on_add_before)
    self.add_action(action)

    action = Gio.SimpleAction.new("add_child", None)
    action.connect("activate", self.on_add_child)
    self.add_action(action)

    action = Gio.SimpleAction.new("delete", None)
    action.connect("activate", self.on_delete)
    self.add_action(action)

    action = Gio.SimpleAction.new("expand_all", None)
    action.connect("activate", self.on_expand_all)
    self.add_action(action)

    action = Gio.SimpleAction.new("fold_all", None)
    action.connect("activate", self.on_fold_all)
    self.add_action(action)

    #

  def save_changes(self):
    res = Gtk.ResponseType.NO
    if self.tnview.get_changed() == True:
      res = self.tnfile.save_changes_dialog()
    return res

  def on_new(self, action, param):
    if self.tnview.get_changed() == True:
      res = self.tnfile.save_changes_dialog()
      if res == Gtk.ResponseType.YES:
        return
    self.tnfile.new_file()
    self.tnview.clear_changed()
    self.set_title(TnDef.APP_NAME)

  def on_open(self, action, param):
    if self.tnview.get_changed() == True:
      res = self.tnfile.save_changes_dialog()
      if res == Gtk.ResponseType.YES:
        return
    res = self.tnfile.open_file()
    if res == Gtk.ResponseType.OK:
      self.tnview.clear_changed()
      self.set_title(TnDef.APP_NAME + " - " + self.tnfile.get_filename())

  def on_save(self, action, param):
    if self.tnview.get_changed() == True:
      res = self.tnfile.save_file()
      if res == Gtk.ResponseType.OK:
        self.tnview.clear_changed()
        self.set_title(TnDef.APP_NAME + " - " + self.tnfile.get_filename())

  def on_save_as(self, action, param):
    res = self.tnfile.save_file_as()
    if res == Gtk.ResponseType.OK:
      self.tnview.clear_changed()
      self.set_title(TnDef.APP_NAME + " - " + self.tnfile.get_filename())

  def on_close(self, action, param):
    self.on_new(action, param)

  def on_add_after(self, action, param):
    self.tnview.edit_add_after()
  def on_add_before(self, action, param):
    self.tnview.edit_add_before()
  def on_add_child(self, action, param):
    self.tnview.edit_add_child()
  def on_delete(self, action, param):
    self.tnview.edit_delete()

  def on_expand_all(self, action, param):
    self.tnview.view_expand_all()
  def on_fold_all(self, action, param):
    self.tnview.view_fold_all()


class App(Gtk.Application):

  def __init__(self, *args, **kwargs):
    super(App, self).__init__(*args, application_id="org.frstgt.treenote",
                      flags=Gio.ApplicationFlags.HANDLES_OPEN,
                      **kwargs)
    self.window = None

  def do_startup(self):
    Gtk.Application.do_startup(self)
    
    action = Gio.SimpleAction.new("quit", None)
    action.connect("activate", self.on_quit)
    self.add_action(action)

    builder = Gtk.Builder.new_from_string(MENU_XML, -1)
    self.set_app_menu(builder.get_object("app-menu"))

  def do_activate(self):
    if not self.window:
      self.window = AppWin(application=self, title=TnDef.APP_NAME)
      self.window.connect("delete-event", self.on_delete_event)

    self.window.present()

  def on_quit(self, action, param):
    res = self.window.save_changes()
    if res == Gtk.ResponseType.YES:
      return
    self.quit()

  def on_delete_event(self, widget, event):
    res = self.window.save_changes()
    if res == Gtk.ResponseType.YES:
      return True
    return False

if __name__ == "__main__":
  app = App()
  app.run(sys.argv)

# end of file
