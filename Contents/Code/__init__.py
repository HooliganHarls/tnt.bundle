#xbmc-nfo importer
#spec'd from: http://wiki.xbmc.org/index.php?title=Import_-_Export_Library#Video_nfo_Files
import os

class xbmcnfo(Agent.Movies):
  name = 'XBMC .nfo Importer'
  languages = [Locale.Language.English]
  primary_provider = False
  contributes_to = ['com.plexapp.agents.imdb']
  
  def search(self, results, media, lang):
    results.Append(MetadataSearchResult(
        id    = 'null',
        score = 100    ))
    
  def update(self, metadata, media, lang):
    Log('UPDATE: ' + media.items[0].parts[0].file)
    path = os.path.dirname(media.items[0].parts[0].file)
    nfoFile=''
    if os.path.exists(path):
      for f in os.listdir(path):
        if f.split(".")[-1].lower() == "nfo":
          nfoFile = os.path.join(path, f)
          nfoText = Core.storage.load(nfoFile)
          #nfoText = t.read()
          nfoTextLower = nfoText.lower()
          if nfoTextLower.count('<movie>') > 0 and nfoTextLower.count('</movie>') > 0:
            #likely an xbmc nfo file
            nfoXML = XML.ElementFromString(nfoText).xpath('//movie')[0]
            
            #title
            try: metadata.title = nfoXML.xpath('./title')[0].text
            except: pass
            #summary
            try: metadata.summary = nfoXML.xpath('./outline')[0].text
            except: pass            
            #year
            try: metadata.year = int(nfoXML.xpath('./year')[0].text)
            except: pass
            #rating
            try: metadata.rating = float(nfoXML.xpath('./rating')[0].text)
            except: pass
            Log(metadata.rating)
            #content rating
            try: metadata.content_rating = nfoXML.xpath('./mpaa')[0].text
            except: pass   
            Log(metadata.content_rating)
            Log(metadata.title)
            Log(metadata.year)
            Log(metadata.summary)
            
            data = HTTP.Request(nfoXML.xpath('./thumb')[0].text)
            name = 'xbmc-nfo-thumb'
            if name not in metadata.posters:
              metadata.posters[name] = Proxy.Media(data)
            break
          else:
            continue
            
    #ratings = {}
    #for rating in HTML.ElementFromURL(RT_BASE_URL + metadata.id).xpath('//div[@class="movie_info_area"]//li/a'):
    #  ratingText = rating.get('title')
     # if ratingText != "N/A" and len(ratingText) > 0:
      #  ratings[rating.xpath('span')[0].text] = float(ratingText.replace('%',''))/10
    #metadata.rating = ratings['T-Meter Critics']