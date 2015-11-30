from LinkFuncs import GetThread, GetLinks
from DownloadFuncs import IdentifyLink, AddHTTP

thread = GetThread()
print thread
if thread != "404":
    links = GetLinks(thread)
    links = AddHTTP(links)
    for link in links:
        print link

