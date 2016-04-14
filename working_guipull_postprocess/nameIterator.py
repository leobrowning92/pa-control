

def iterateLast(string):
    """
    Iterates the number at the end of an input string
    """
    j = 1
    index = ""
    for i in range(1, len(string)):
        try:
            int(string[-i])
            index = string[-i] + index
        except:
            j = i - 1
            print j
            break
    return string[:-j] + str(int(index) + 1)


def iterateChip(string):
    """
    Iterates the number that X (can be of arbitrary non-sero length)
    That is situated in a filename of type
    blahblah_chipX_deviceY_notesyblah.blah
    """
    # Finds the start stop indeces of the chip number
    j = string.find("_chip") + 5
    k = string[j:].find("_")

    # Finds the start stop indeces of the device number
    string = string.replace(
        "_chip" + string[j:j + k], "_chip" + str(int(string[j:j + k]) + 1))

    l = string.find("_device") + 7
    m = string[l:].find("_")

    # changes to device 1. Must happen before chip change to keep indices good
    string = string.replace("_device" + string[l:l + m], "_device1")
    return string


def iterateDevice(string):
    """
    Iterates the number that Y (can be of arbitrary non-sero length)
    That is situated in a filename of type
    blahblah_chipX_deviceY_notesyblah.blah
    """

    # Finds the start stop indeces of the device number
    j = string.find("_device") + 7
    k = string[j:].find("_")

    return string.replace("_device" + string[j:j + k], "_device" + str(int(string[j:j + k]) + 1))

#
# print iterateChip("test_chip1234_device123.txt")  # for testing
