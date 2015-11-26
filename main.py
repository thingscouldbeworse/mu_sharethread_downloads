from LinkFuncs import GetThread, GetLinks


thread = GetThread()
print thread
if thread != "404":
    links = GetLinks(thread)
    for link in links:
        print link

