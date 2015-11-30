from LinkFuncs import GetHTML

def AddHTTP( links ):
    GoodLinks = []
    for link in links:
        NewLink = 'https://' + link
        GoodLinks.append( NewLink )

    return GoodLinks

def IdentifyLink( link ):
    page = GetHTML( link )
    if page.find("Download through") > 0:
        #This is the good kind of link, one to a zipped album instead of a folder view of songs
        return 'zip'
    else:
        return 'else'

