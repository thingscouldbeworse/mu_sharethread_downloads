from LinkFuncs import GetThread, GetLinks


thread = GetThread()
print thread
if thread != "404":
    links = GetLinks(thread)
    print links

