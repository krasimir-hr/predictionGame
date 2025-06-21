from urllib.parse import unquote

def url_decoder(raw_url):
   url = raw_url.replace('https://am-a.akamaihd.net/image?resize=64:&f=', '') 
   return unquote(url)

print(url_decoder('https://am-a.akamaihd.net/image?resize=64:&f=http%3A%2F%2Fstatic.lolesports.com%2Fteams%2F1682322954525_Bilibili_Gaming_logo_20211.png'))