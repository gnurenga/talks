#!/usr/bin/env python

from gi.repository import GLib

import dbus
import dbus.service
import dbus.mainloop.glib

class ChennaiPy(dbus.service.Object):

    @dbus.service.method("com.chennaipy.usergroup",
                         in_signature='s', out_signature='s')
    def HelloWorld(self, hello_message):
        print (str(hello_message))
        return "Hello" + " " + hello_message

    @dbus.service.method("com.chennaipy.usergroup",
                         in_signature='', out_signature='s')
    def GetLocation(self):
        return "Chennaipy December meetup @ Ajira"

    @dbus.service.method("com.chennaipy.usergroup",
                         in_signature='', out_signature='')
    def Exit(self):
        mainloop.quit()


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("com.chennaipy.usergroup", session_bus)
    object = ChennaiPy(session_bus, '/chennaipy/demo')

    mainloop = GLib.MainLoop()
    print "Running example service."
    mainloop.run()
