#!/usr/bin/env python3
"""
Display a dialog box with a random number of buttons
using gtk3 API.
----------------------------------------------------
Jean MORLET - 2021/10/02
Licence MIT
"""
import argparse
import base64
from threading import Timer

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GLib
from gi.repository.GdkPixbuf import Pixbuf, PixbufAnimation, PixbufLoader

result = 0

# Icones en base 64
QUESTION = 0
INFORMATION = 1
WARNING = 2
ERROR = 3
SABLIER = 4

ICONES = {
    'question': QUESTION,
    'information': INFORMATION,
    'infos': INFORMATION,
    'info': INFORMATION,
    'warning': WARNING,
    'error': ERROR,
    'err': ERROR,
    'hourglass': SABLIER,
    'hg': SABLIER
}


def load_b64_img(name: str) -> Gtk.Image:
    global ICONES

    if name is None:
        return Gtk.Image()
    with open("icones.b64", "rt") as f:
        raw = base64.b64decode(f.read().split()[ICONES[name]])
    try:
        pixbuf_loader = PixbufLoader.new_with_mime_type('image/png')
        pixbuf_loader.write(raw)
        pixbuf_loader.close()
        return Gtk.Image.new_from_pixbuf(pixbuf_loader.get_pixbuf())
    except Exception:
        pass
    try:
        pixbuf_loader = PixbufLoader.new_with_mime_type('image/jpeg')
        pixbuf_loader.write(raw)
        pixbuf_loader.close()
        return Gtk.Image.new_from_pixbuf(pixbuf_loader.get_pixbuf())
    except Exception:
        pass
    try:
        pixbuf_loader = PixbufLoader.new_with_mime_type('image/gif')
        pixbuf_loader.write(raw)
        pixbuf_loader.close()
        return Gtk.Image.new_from_animation(pixbuf_loader.get_animation())
    except Exception:
        pass
    return Gtk.Image()


class MyWindow(Gtk.Window):
    __progressbar = None
    __timeout = None
    __image = None
    __timer = None
    __count = 0
    __label = None
    __title = None
    __buttons = []

    def __init__(self, kwargs):
        global result
        self.__timeout = kwargs['timeout']
        super(MyWindow, self).__init__(title='msgbox')
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("destroy", self.do_nothing)
        self.connect("delete-event", self.do_nothing)
        self.connect("window-state-event", self.do_nothing)
        self.win_layout = Gtk.Box()
        self.win_layout.set_orientation(Gtk.Orientation.VERTICAL)
        self.add(self.win_layout)
        vbox = Gtk.Box()
        vbox.set_orientation(Gtk.Orientation.VERTICAL)
        if kwargs['title'] is not None:
            self.__title = Gtk.Label()
            self.__title.set_name("title")
            self.__titre_msg = kwargs['title']
            self.__title.set_label(self.__titre_msg)
            self.__title.set_justify(Gtk.Justification.CENTER)
            vbox.pack_start(self.__title, False, False, 0)
        vbox.pack_start(Gtk.Label(), True, True, 0)  # <-- Spacer
        hbox = Gtk.Box()
        hbox.set_name('hbox-message')
        hbox.set_orientation(Gtk.Orientation.HORIZONTAL)
        if kwargs['icon'] is not None:
            name: str = kwargs['icon']
            if name in ICONES:
                self.__image = load_b64_img(name)
            elif '.' in name:
                if 'gif' in name:
                    pixbuf = PixbufAnimation.new_from_file(name)
                    self.__image = Gtk.Image.new_from_animation(pixbuf)
                else:
                    pixbuf = Pixbuf.new_from_file_at_scale(filename=name, width=100, height=100,
                                                           preserve_aspect_ratio=True)
                    self.__image = Gtk.Image.new_from_pixbuf(pixbuf)
            else:
                pixbuf = Gtk.IconTheme.get_default().load_icon(name, 64, 0)
                self.__image = Gtk.Image.new_from_pixbuf(pixbuf)
            hbox.pack_start(self.__image, False, True, 0)
        self.__label = Gtk.Label()
        self.__label.set_name("message")
        self.__message = kwargs['message']
        self.__label.set_markup(self.__message)
        self.__label.set_justify(Gtk.Justification.CENTER)
        self.__label.set_line_wrap(True)
        hbox.pack_start(self.__label, True, True, 0)
        vbox.pack_start(hbox, False, True, 0)
        vbox.pack_start(Gtk.Label(), True, True, 0)  # <-- Spacer
        if self.__timeout is not None:
            self.__timer = Timer(self.__timeout, self.dialog_timeout)
            self.__timer.start()
        buttons = kwargs['btn_msg'].split(';')
        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label(), True, True, 0)
        for num in range(len(buttons)):
            self.__buttons.append(Gtk.Button())
            btn = self.__buttons[num]
            btn.set_label(buttons[num])
            btn.connect("clicked", self.btn_clicked, num)
            hbox.pack_start(btn, True, True, 5)
            hbox.pack_start(Gtk.Label(), True, True, 0)
        vbox.pack_start(hbox, False, False, 0)

        def progress_update():
            self.__progressbar.set_fraction(self.__count / (10 * self.__timeout))
            self.__count -= 1
            GLib.timeout_add(100, progress_update)

        if self.__timeout:
            self.__progressbar = Gtk.ProgressBar()
            vbox.pack_start(self.__progressbar, False, True, 0)
            self.__count = self.__timeout * 10
            progress_update()
        self.win_layout.pack_start(vbox, True, True, 0)
        self.show_all()

    def dialog_timeout(self, nothing=None):
        global result
        result = -1
        if self.__timer is not None:
            self.__timer.cancel()
        Gtk.main_quit()
        exit(result)

    def btn_clicked(self, btn, value):
        global result
        result = value
        if self.__timer is not None:
            self.__timer.cancel()
        Gtk.main_quit()
        exit(result)

    def quit(self, nothing=None):
        if self.__timer is not None and self.__timer.is_alive():
            self.__timer.cancel()
        Gtk.main_quit()
        exit(result)

    def do_nothing(self, *args):
        return True


def main(args: argparse.Namespace):
    try:
        css = Gio.File.new_for_path('./MsgBox.css')
        css_provider = Gtk.CssProvider()
        css_provider.load_from_file(css)
        context = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    except gi.repository.GLib.Error:
        pass
    _ = MyWindow(args.__dict__)
    try:
        Gtk.main()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--title', action='store', type=str, dest='title',
                        help="Dialog title")
    parser.add_argument('-m', '--message', action='store', type=str, dest='message',
                        default='! Totally uninteresting default message !', help="Message to display")
    parser.add_argument('-b', '--buttons', action='store', type=str, dest='btn_msg', default='OK;Cancel',
                        help="';' separated label of buttons")
    parser.add_argument('--timeout', action='store', type=float, dest='timeout',
                        help="Optional timeout in seconds.")
    parser.add_argument('--icon', action='store', type=str, dest='icon')
    main(parser.parse_args())
    exit(result)
