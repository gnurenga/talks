import dbus

def main():
    bus = dbus.SessionBus()
    message = "Hello evey one"
    remote_object = bus.get_object("com.chennaipy.usergroup",
                                      "/chennaipy/demo")

    iface = dbus.Interface(remote_object, "com.chennaipy.usergroup")

    location = iface.GetLocation()
    hello_reply = iface.HelloWorld(message)
    print "location: %s\n" % location
    print "HelloWorld(%s): %s" % (message, hello_reply)
    print "killing service"
    iface.Exit()
    
if __name__ == '__main__':
    main()
