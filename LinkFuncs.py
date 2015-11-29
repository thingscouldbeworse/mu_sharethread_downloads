import pycurl
import urllib2
import requests
from StringIO import StringIO

def testURL(url):
    try:
        r = requests.head(url)
        return r.status_code
    except requests.ConnectionError:
        return 404

def GetHTML(url):
    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    page = buffer.getvalue()

    return page

def GetThread():

    sSearch = "sharethread"
    sSearch2 = "share-thread"
    page = GetHTML( 'http://boards.4chan.org/mu/catalog')
    # Now that we have the contents of the page, we need to find the current sharethread
    # Or decide that there is none currently

    bShare = False
    if  sSearch in page:
        bShare = True
        index = page.find(sSearch, 0, len(page))
    elif sSearch2 in page:
        bShare = True
        index = page.find(sSearch2)
        sSearch = sSearch2
    else:
        print( "ERROR: No sharethread found. Try later today?")

    # We now have an index located, we need to grab the thread number associated with this link
    # The ID is behind the word "sharethread". There's probably a better way to search for it but oh well...
    sSub = page[::-1] # Reverse page so we can count forward to find the stuff behind
    sSearchReverse = sSearch[::-1] # Reverse our search string to go looking for its index
    index = sSub.find(sSearchReverse)
    sSub = sSub[index:]

    indexFirst = sSub.find("{")  # Find the first open bracket after the "sharethread" index
    sSub = sSub[indexFirst+1:]
    indexFirst = sSub.find("{")  # The next open bracket is the first bookend
    indexSecond = sSub.find("}") # The closed bracket bookends the end (the non reversed beginning) of the thread ID

    sPostID = sSub[indexFirst:indexSecond]
    sPostID = sPostID[::-1] # Reverse the now grabbed reverse ID



    sPostID = sPostID[2:-3]

    thread = "http://boards.4chan.org/mu/thread/"+ sPostID # We now have the actual sharethread

    if testURL(thread) == '404':
        print 'sharethread 404, something went wrong'
        return '404'

    return thread


def GetLinks( thread ):

    page = GetHTML(thread)

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

    # Page is a string in some encoding.
    # In Python 2, we can print it without knowing what the encoding is.
    # print("Sharethread? ", bShare)
    # print("index of sharethread= ", index)
    print("URL= ", thread)

    return GoodLinks
