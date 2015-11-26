import pycurl
import urllib2
import requests
from StringIO import StringIO



def GetThread():

    buffer = StringIO()
    c = pycurl.Curl()
    sSearch = "sharethread"
    c.setopt(c.URL, 'http://boards.4chan.org/mu/catalog')
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    page = buffer.getvalue()
    # Now that we have the contents of the page, we need to find the current sharethread
    # Or decide that there is none currently

    bShare = False
    if  sSearch in page:
        bShare = True
        index = page.find(sSearch, 0, len(page))
    elif sSearch2 in page:
        bShare = True
        index = page.find(sSearch2, 0, len(page))
    else:
        print( "ERROR: No sharethread found. Try later today?")

    # We now have an index located, we need to grab the thread number associated with this link
    sSub = page[index-500:index]

    sIndexOpenBracket = sSub.find("{")
    sIndexCloseBracket = sSub.find("}")
    sSub2 = sSub[sIndexCloseBracket:sIndexOpenBracket] # The postID is actually in between the reversed open and close bracket because it's in between two identities

    sPostID = sSub2[3:-2]

    thread = "http://boards.4chan.org/mu/thread/"+ sPostID # We now have the actual sharethread


    try:
        r = requests.head("http://stackoverflow.com")
        print(r.status_code)
    except requests.ConnectionError:
        print("No sharethread or wrong ID")
        thread = 404

    return thread


def GetLinks( thread ):

    buffer = StringIO()
    c2 = pycurl.Curl()
    c2.setopt(c2.URL, thread)
    c2.setopt(c2.WRITEDATA, buffer)
    c2.perform()
    c2.close()
    page = buffer.getvalue()

    # We have the HTML of the sharethread itself
    # So we need to iterate through it until we find every mega.nz link

    allValuesFound = False
    index2 = 0
    i = 0
    links = []
    index2 = (page.find("mega"))
    pageWork = page # Make a copy of the HTML to adjust in the loop
    lengthAdjusted = 0
    if index2 < 0:
        return "no links, possibly grabbed wrong thread"

    GoodLinks = []
    BadLinks = []

    while not(allValuesFound):
        pageWork = pageWork[index2+1:]
        if pageWork.find("mega") > -1:
            index2 = (pageWork.find("mega") ) # The index within pageWork that 'mega' was found, this is NOT the same as page
            # print(i)
            # print( index2 )
            link = pageWork[index2:index2+200]
            # print(link)
            links.append(link)
        elif pageWork.find("mega") < 0:
            allValuesFound = True
            print(i, " All Values should be found")
        i = i + 1

    for link in links:
        if (link.find("nz") < 0 ): # No NZ found means it's not a link, just someone saying the word mega
            links.remove(link)
        else:
            if (link.find("<wbr>") <0): # Case 1, there is no need for a split because the link is short. The last "<" should end the string
                indexFirst = link.find("<")
                link = link[:indexFirst]
            elif (link.find("<wbr>") > -1): # Case 2 or 3, there is at least one <wbr> splitting the link
                indexFirst = link.find("<wbr>")
                linkFirstPart = link[:indexFirst]
                linkSecondPart = link[indexFirst+5:]
                indexSecond = linkSecondPart.find("<wbr")
                linkSecondPart = linkSecondPart[:indexSecond]
                link = linkFirstPart + linkSecondPart  # Some links will be complete by this step, so we should sort them and then take care of the remaining improperly formatted links

            if link.find("<") < 0:
                GoodLinks.append(link)
            elif link.find("<") > -1:
                BadLinks.append(link)

    done = False
    while not done:
        for link in BadLinks:
            # Remaining bad links either have a leading "mega:" or just needs the link cat'd up until the next "<"
            indexFirst = link.find("<")
            linkNew = link[:indexFirst]
            GoodLinks.append(linkNew)
            BadLinks.remove(link)
            print "fixed", link
            # Are we done yet?
            if (len(BadLinks) < 1 ):
                done = True
                #print done

    i = 0
    for link in BadLinks:
        print (i, " bad link second: " + link)
        i = i + 1
    for link in GoodLinks:
        print "good link: " + link


    # Page is a string in some encoding.
    # In Python 2, we can print it without knowing what the encoding is.
    # print("Sharethread? ", bShare)
    # print("index of sharethread= ", index)
    print("URL= ", thread)

    return GoodLinks
