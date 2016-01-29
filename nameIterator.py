

def iterateLast(string):
    """
    Iterates the number at the end of an input string
    """
    j=1
    index=""
    for i in range(1,len(string)):
        try:
            int(string[-i])
            index=string[-i]+index
        except:
            j=i-1
            print j
            break
    return string[:-j]+str(int(index)+1)

def iterateChip(string):
    j=string.find("_chip")+5
    k=string[j:].find("_")
    print j,k
    return string.replace(string[j:j+k],str(int(string[j:j+k])+1))

print iterateChip("test_chip643_device12")
