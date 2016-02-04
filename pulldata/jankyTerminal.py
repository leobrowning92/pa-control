import nameIterator as nmi


def handler(cmd,filename):
    if cmd == 'q':
        return "nosave", False
    elif cmd == 'n':
        filename = raw_input("please input full initial filename: ")
    elif cmd == 'c':
        filename = nmi.iterateChip(filename)
    elif cmd == 'd':
        filename = nmi.iterateDevice(filename)
    else:
        print "That is an invalid input"
    return filename, True





def inputLoop():

    filename = raw_input("please input full initial filename: ")
    loop=True
    while loop == True:
        cmd = raw_input(
            "Iterate chip (c) or device (d), new (n), or quit (q): ")
        filename, loop = handler(cmd,filename)

        print "will save as: " + filename


    print "End of input. Thanks for using this Janky Terminal hack - Leo"

#inputLoop()
