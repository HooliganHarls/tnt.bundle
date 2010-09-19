# PMS plugin framework
import datetime,re


##################################################################################################TNT
VIDEO_PREFIX     = "/video/TNT"
NAME          = L('Title')

TNT_URL                     = "http://www.tnt.tv"
TNT_FULL_EPISODES_SHOW_LIST = "http://www.tnt.tv/series"

TNT_FEED                    = "http://www.TNT.com/"
DEBUG                       = False
TNTart                      ="art-default.jpg"
TNTthumb                    ="icon-default.jpg"

####################################################################################################

def Start():
  Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, 'TNT',TNTthumb,TNTart)
  Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
  Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
  
  MediaContainer.art        =R(TNTart)
  MediaContainer.title1     = NAME
  DirectoryItem.thumb       =R(TNTthumb)

####################################################################################################
#def VideoMainMenu():
#    dir = MediaContainer(mediaType='video') 
#    dir.Append(Function(DirectoryItem(all_shows, "All Shows"), pageUrl = TNT_FULL_EPISODES_SHOW_LIST))
#    return dir
    
####################################################################################################
def VideoMainMenu():
    pageUrl=TNT_FULL_EPISODES_SHOW_LIST
    dir = MediaContainer(viewGroup="List")
    content1 = XML.ElementFromURL(pageUrl, isHTML="True")
    showMap = dict()
    shownum=0
    for item in content1.xpath('//div[@id="navfullepisodes"]/table/tr'):
        Log(item.findall('td/'))
        things = item.findall('./td/a')
        
        for thingies in things:
          shownum =shownum+1
          showID=shownum
          Log(thingies)
          title=thingies.text
          titleUrl=thingies.get('href')
          titleUrl=TNT_URL + titleUrl
          thumb=TNTthumb
          Log(titleUrl)
          Log(title)
      #  Log(thumb)
          showList = showMap.get(title)
          if showList == None:
		      showList = []
		      showMap[title] = showList
		  # Tuple order here matters
          showList.append((showID,titleUrl, thumb, title))
          Log(showList)
    shows=showMap.keys()
    Log(shows)
    shows.sort()
    Log(shows)
    shownum=0
    #for shownames in shows:
    #  shownum=shownum+1
    #  showList.append((shownum,shownames.titleUrl,shownames.thumb, shownames.title))
    for showkey in shows:
      Log(showkey)
      for show in showMap[showkey]:
        Log(show)
        title=show[3]
        url=show[1]
        thumb=show[2]
        Log("Show: " + title + " | link: " + url)
        dir.Append(Function(DirectoryItem(showxml, title=title), pageUrl = url))
      
    
    return dir 

####################################################################################################
def showxml(sender, pageUrl):
  dir = MediaContainer(title2=sender.itemTitle, viewGroup="InfoList", noCache=True)
  showID=re.compile('cid=([0-9]+)').findall(pageUrl)[0]
  link="http://www.tnt.tv/processors/services/getCollectionByContentId.do?offset=0&sort=&limit=200&id=" + showID
  shows=XML.ElementFromURL(link).xpath('//episode')
  for show in shows:
    #episodeID  
    epID=show.get('id')

    #title
    title=show.xpath('./title')[0].text

    #thumb
    thumb=show.xpath('./thumbnailUrl')[0].text
    #summary
    summary=show.xpath('./description')[0].text
    clip="http://www.tnt.tv/dramavision/index.jsp?oid=" + epID    
    
    
##########   This section knows the location of the flv file, but the stream is rtmpe
##########   I am keeping the code in here so it doesn't get lost so when     
#    vidlink="http://www.tnt.tv/video_cvp/cvp/videoData/?id=" + epID
#    showLinks=XML.ElementFromURL(vidlink).xpath('//video/files/file[@type="hd"]')
#    Log("++++++++++++++")
#    clip=showLinks[0].text.replace("/tveverywhere","")
#    vidname=clip.split("/")[-1]
#    date1=clip.split("/")[-2]
#    date2=date1.split("-")[-1]
#    date3=date1.split("-")[-2]
#    clip="/flash/" + date2 + "-" + date3 + "/" + vidname
#    
#    Log(clip)
#    player="http://i.cdn.turner.com/xslo/cvp/player/cvp_1.3.6.24.swf?player=fw_main&domId=cvp_1&playerWidth=640&playerHeight=360"



    dir.Append(WebVideoItem(clip, title=title, thumb=thumb, summary=summary))
    Log("epID: " + epID + " | title: " + title + " | thumb: " + thumb + " | Description: " + summary)
    
  
  return dir
