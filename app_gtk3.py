#!/usr/bin/python3

import urllib

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf, Gio

import display
from spotify_client import SpotifyClient

SIZE = display.Hyperpixel.SIZE

def pixbuf_from_url(url):
    response = urllib.request.urlopen(url)
    input_stream = Gio.MemoryInputStream.new_from_data(response.read(), None)
    return GdkPixbuf.Pixbuf.new_from_stream_at_scale(input_stream, SIZE[0], SIZE[1], True)

class SpotifyWidget(Gtk.Image):

    LOGO = 'assets/sp_logo.jpg'
    ID_UNKNOWN = 'unknown'

    def __init__(self):
        super(SpotifyWidget, self).__init__()
        self._sp = SpotifyClient()
        self._last_id = None

        GLib.timeout_add(500, self.update)

    def update(self):
        playing = self._sp.currently_playing()

        if playing is None:
            self._last_id = None
            self.clear()

            return True

        if playing['content']=='song':
            if playing['id'] != self._last_id:
                buf = pixbuf_from_url(playing['image'])
                self.set_from_pixbuf(buf)
                self._last_id = playing['id']

        else:
            buf = GdkPixbuf.Pixbuf.new_from_file_at_scale(self.LOGO, SIZE[0], SIZE[1], True)
            self.set_from_pixbuf(buf)
            self._last_id = self.ID_UNKNOWN

        return True

    def is_active(self):
        return self._last_id is not None


class Application(Gtk.Window):
    def __init__(self):
        super().__init__(title="Cool Display")

        widgets = [SpotifyWidget()]

        for w in widgets:
            self.add(w)

        self.connect("realize", self.on_realize)

        self.hyperpixel = display.Hyperpixel()
        self.hyperpixel.backlight_brightness(0.0)

        GLib.timeout_add(100, self.update, widgets)

    def update(self, widgets):
        any_active = False
        for w in widgets:
            if w.is_active():
                any_active = True
                w.show()
            else:
                w.hide()

        self.hyperpixel.backlight_brightness(0.6 if any_active else 0.0)

        return True

    def on_realize(self, widget):
        display = widget.get_display()
        cursor = Gdk.Cursor.new_for_display(display, Gdk.CursorType.BLANK_CURSOR)
        widget.get_window().set_cursor(cursor)


def main():
    win = Application()
    win.connect("destroy", Gtk.main_quit)
    win.set_default_size(SIZE[0], SIZE[1])
    win.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0,0,0,0))
    win.fullscreen()
    win.show_all()
    Gtk.main()

if __name__ == '__main__':
    main()
