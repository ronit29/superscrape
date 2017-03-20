import requests
import re
import math
from bs4 import BeautifulSoup
import xlsxwriter
import json
s = requests.Session()


def login():
  URL = "https://www.zomato.com/php/asyncLogin.php?"
  params = {"login": "ronit.dhingra@io-media.com", "password" : "zomato123", "rememberFlag" : "checked"}
  head = {"referer":"https://www.zomato.com/",'origin': "https://www.zomato.com","Accept":"application/x-www-form-urlencoded; charset=UTF-8"}
  signin = s.post(URL, data = params, headers = head)
  print(signin) 

def mylist():
  titles = {}
  my_list = []
  headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
  sorce = requests.get("https://www.zomato.com/bangalore/restaurants", headers=headers)
  sorce_text = sorce.text
  soup = BeautifulSoup(sorce_text, "html.parser")
  section = soup.find('section')
  if section:  
    row1 = section.find("div", {"class" :"row"})
    for row2 in row1.findAll("div", {"class" :"col-l-16"}):
      row3 = row2.find("div", {"class" :"row"})
      if row3:
        mt10 = row3.find("div",{"class":"mt10"})
        if mt10:
          mt11 = mt10.find("div",{"class":"search-start"})
          if mt11:
            div1 = mt11.find("div", {"class" :"search_results"})
            section2 = div1.find("section")
            div2 = section2.find("div", {"class" :"orig-search-list-container"})
            for row in div2.findAll("div",{"class" :"search-snippet-card"}):
              div3 = row.find("div", { "class" :"content"})
              art = div3.find("article",{"class":"search-result"})
              costdiv1 = art.find("div",{"class":"search-page-text"})
              if costdiv1:
                costdiv2 = costdiv1.find("div",{"class":"res-cost"})
                costspan = costdiv2.find("span",{"class":"pl0"})
                cost = costspan.text
              div4 = art.find("div",{"class":"row"})
              div5 = div4.find("div",{"class":"col-s-12"})
              title = div5.find("a",{"class":"result-title"})
              if title:
               text = title['href'] 
               text2 = title.text
               key = str(text2.strip()) + '_' + str(cost)
               titles[key] = text.strip()
            my_list = titles
  return my_list


def mypage(url):
  known_for = ''
  ftime_dict = ''
  faddress =''
  fphone = ''
  fcuisines = ''
  highlits = ''
  headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
  page = requests.get(url, headers=headers)
  page_text = page.text
  pagesoup = BeautifulSoup(page_text, "html.parser")
  main_div1 = pagesoup.find("div",{"class","container"})
  main_div2 = main_div1.find("div",{"class","mtop"})
  main_div3 = main_div2.find("div",{"class","row"})
  main_div4 = main_div3.find("div",{"class","mbot"})
  main_div5 = main_div4.find("div",{"class","row"})
  if main_div5:
    for cols in main_div5.findAll("div",{"class","pr20"}):
  	  # Phone number
      phone_div1 = cols.find("div",{"class","res-main-phone"})
      if phone_div1:
        phone_div2 = phone_div1.find("div",{"class","phone"})
        phone_span1 = phone_div2.find("span",{"class","res-tel"})
        phone_span2 = phone_span1.find("span",{"class","tel"})
        phone = phone_span2.text
      if phone:
        fphone = phone.strip()  
      # Cuisine
      cuisine_div1 = cols.find("div",{"class","res-info-group"})
      if cuisine_div1:
        cuisine_div2 = cuisine_div1.find("div",{"class","res-info-cuisines"})
        if cuisine_div2:
          cuisines = ''
          for cns in cuisine_div2.findAll("a"):
            cns = cns.text
            cuisines += str(cns) + ","  
          cuisines = cuisines.rstrip(',')
        if cuisines:
          fcuisines = cuisines  
	  #Timings 
      time_div1 = cols.find("div",{"class","res-info-group"})
      if time_div1:
        time_div2 = time_div1.find("div",{"class","res-info-detail"})
        if time_div2:
          time_div3 = time_div2.find("div",{"class","res-info-timings"})
          if time_div3:
            time_div4 = time_div3.find("div",{"class","res-week-timetable"})
            time_table = time_div4.find("table") 
            titem = ''
            for time_tr in time_table.findAll("tr"):
              day = time_tr.find("td",{"class":"pr10"})
              day = str(day.text) 
              time = time_tr.find("td",{"class":"pl10"})
              titem += day+'_'+str(time.text) + ','
              time_list = titem.rstrip(',')
            if time_list:
              ftime_dict = time_list  
      # Address
      addrs_div1 = cols.find("div",{"class":"mbot0"})
      if addrs_div1:
        addrs_div2 = addrs_div1.find("div",{"class":"res-main-address"})
        if addrs_div2:
          addrs_span1 = addrs_div2.find("span")
          address = addrs_span1.text
        if address:
          faddress = address.strip()     
      #  Highlights
      hilits_div1 = cols.find("div",{"class","pbot0"})
      if hilits_div1:
        hilits_div2 = hilits_div1.find("div",{"class","res-info-highlights"})
        if hilits_div2:
          highlits= ''
          for hlits in hilits_div2.findAll("div",{"class","res-info-feature-text"}):
            # hilit = hlits.find("div",{"class","res-info-feature-text"})
            highlits += str(hlits.text) + "," 
          highlits = highlits.rstrip(',') 
      # Known for
      known_div1 = cols.find("div",{"class":"res-info-known-for-text"})
      if known_div1:
        known_for = known_div1.text
        known_for = known_for.strip() 
    data = {"timimgs":ftime_dict,"address":faddress,"phone":fphone,"cuisines":fcuisines,"highlits":highlits,"knownfor":known_for}     
    return data

def mymenu(url):
  url = str(url) + "/menu"  
  headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
  menu = requests.get(url, headers=headers)
  menu_text = menu.text
  menusoup = BeautifulSoup(menu_text, "html.parser")
  menu_div1 = menusoup.find("div",{"class","container"})
  script = menu_div1.find("script")
  script = str(script)
  m = re.findall('https(.+?)jpg', script)
  if m:
    m = set(m)
    urls = ''
    for x in m:
      x = str(x)
      x = x.replace("\\","")
      x = "https"+x+"jpg"
      urls += str(x) + " ,\n"
    urls = urls.rstrip(',')  
    urls = urls.lstrip('https://')
    return urls   

def myreviews():
  headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
  reviews = s.get("https://www.zomato.com/bangalore/koramangala-social-koramangala-7th-block/reviews", headers=headers)
  reviews_text = reviews.text
  reviewssoup = BeautifulSoup(reviews_text, "html.parser")
  head = reviewssoup.find("head")
  meta1 = head.find("meta",{"name":"twitter:data2"})['content']
  review_count = meta1.split(' ')
  review_count = review_count[0]
  meta2 = head.find("meta",{"name":"twitter:app:url:iphone"})['content']
  entity_id = meta2.split('/')
  entity_id = entity_id[3]
  page_numbers = int(review_count)/5
  total_pages = math.floor(page_numbers)
  i = 1
  for z in range(2,total_pages):
    params = {"entity_id": entity_id, "profile_action":"reviews-dd" , "page": z , "limit": 5}
    head = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8","Referer":"https://www.zomato.com/","Accept":"*/*"}
    fetch = s.post("https://www.zomato.com/php/social_load_more.php", data = params, headers = head)
    if fetch.status_code == 200:
      ft = fetch.text
      ft = json.loads(ft)
      ft = ft['html']
      fetch_text = BeautifulSoup(ft, "html.parser")
      # reviews_div1 = reviewssoup.find("div",{"class","container"})
      # reviews_div2 = reviews_div1.find("div",{"class","zs-following-list"})
      if fetch_text:
        for revdivs in fetch_text.findAll("div",{"class","res-review-body"}):
          reviews_name = revdivs.find("div",{"class","item"})
          reviews_name2 = reviews_name.find("div",{"class","mb10"})
          reviews_name3 = reviews_name2.find("div",{"class","res-large-snippet"})
          reviews_name4 = reviews_name3.find("div",{"class","content"})
          reviews_name5 = reviews_name4.find("a")
          reviews_div3 = revdivs.find("div",{"class","rev-text"})
          review = str(reviews_div3.text)
          name = str(reviews_name5.text)
          name = name.rstrip('\n')
          name = name.lstrip('\n')
          review = review.lstrip('\nRated\n')
          review = re.sub(u'\xa0','', review)
          review = review.lstrip()
          name =  re.sub(u'\xa0','', name)
          name = name.rstrip()
          wrt = str(i) + ' ' + name + '\n' + review + '\n\n'
          f.write(wrt) 
          i = i+1
      out = "page "+str(z)+" done"
      print(out)
  print("File Ready")      


def write():
  list1 = mylist()  
  i = 0
  scrap = {}
  for key,url in list1.items():
    split = key.split("_")
    title = split[0]
    cost = split[1]
    data = mypage(url)
    if data:
      if cost:
        data["cost"] = str(cost)
      if title:
        data["title"] = str(title)
      data["menu"] = mymenu(url) 
      scrap[i] = data
      i = i+1
  workbook = xlsxwriter.Workbook('Expenses01.xlsx')
  worksheet = workbook.add_worksheet()
  wrap = workbook.add_format({'text_wrap':True})
  row = 0
  for index,item in scrap.items():
    col = 0
    for key,value in item.items():   
      worksheet.write(row, col,value,wrap)
      col = col + 1
    row += 1  
  print("Completed")  



# write()
f = open('reviews', 'a')
myreviews()