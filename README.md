# Virtual Girlfriend(虛擬女友) - 小優
## 1. Intro
* 主題發想：
近年來科技大幅進步卻也拉大了人與人之間的距離，生活步調日漸加速，與身邊人相處交心的機會卻也消逝減少；
部分人選擇了交友網站，卻敗給自己的不擅言詞，疫情期間也不能擅自外出遊樂，所以選擇製作出一款 LineBot 的虛擬女友。
* 目的：
給予使用者一個可以生動聊天、提供天氣預報、電影、音樂推薦還有簡單小遊戲的陪伴依靠
* 使用技術：
運用linebot結合NLP做出的聊天機器人。

  * 使用自然語言意理解處理(NLI)訓練機器人，讓機器人能更像真實人類回話。
  * 利用圖文選單，讓使用者有更簡單的操作。
  * 內涵天氣預報、推薦音樂和電影，讓使用者有更便利的生活。
  * 簡易的小遊戲讓使用者能夠度過無聊的時光。
* 使用流程：
![image](https://user-images.githubusercontent.com/64915975/122666323-298dc080-d1df-11eb-9a2c-6a5d65eccb1f.png)

## 2. Build process
* 前端顯示、功能測試
  * **創建Linebot**

    ![image](https://user-images.githubusercontent.com/64915975/122666871-6b6c3600-d1e2-11eb-9706-857602094649.png)

  * **在Line Developer建立Linebot圖文選單**

    ![image](https://user-images.githubusercontent.com/64915975/122667035-4a581500-d1e3-11eb-99f3-91f956c2240e.png)
    
  * **對話測試**
 
    ![image](https://user-images.githubusercontent.com/64915975/122668529-0e28b280-d1eb-11eb-99dd-af507aa1c3ff.png)


* 後端運用  

  * **`config.ini` 存放**  
  
    linebot 的 *Channel_Access_Token*、*Channel_Secret*  

    olami 的 *APP_KEY*、 *APP_SECRET*
  * **olami 對話訓練**   ( olami介紹在最下面補充)
  
    ![image](https://user-images.githubusercontent.com/64915975/122667592-2b0eb700-d1e6-11eb-9546-5c55e2ee9d47.png)
  * **`girlfriend.py`為主要的main檔**，import `Flask` 、`Linebot`、 `nlp`等 相關套件，讓聊天機器人能運作
  * **新增 `__init__.py`** 為了讓 `girlfriend.py` import `nlp` 的時候認定 `nlp` 是一個 Module
  * **新增 `olami.py`** 實作 request OLAMI NLI API 的 method
  * **將程式部署到Heroku**  
    * **新增`Procfile`**，告訴Heroku如何啟動這個app
    * **新增`requirements.txt`**，告訴Heroku這個app的環境需要哪些其他套件
    * **新增`runtime.txt`**，告訴Heroku這個app指定的python版本


## 3. Details of the approach
* `olami.py`  

  * type變數為nli模組名稱，利用type變數判斷使用者的功能需求，並用對應的function回應
  ``` Python
  type = nli_obj['type']
  desc = nli_obj['desc_obj']
  data = nli_obj.get('data_obj', [])
  semantic_ = nli_obj.get('semantic',[])
  ```
  * 即時新聞function，利用自由時報娛樂新聞API，抓取裡面的item標籤後將需要的值存起來後回傳

  ```Python
  def monoNum():
    final_news = ""
    for n in range (3):
    con = requests.get('https://news.ltn.com.tw/rss/entertainment.xml')
    tree = ET.fromstring(con.text)
    items = list(tree.iter(tag='item'))
    title = items[n][0].text
    ptext = items[n][1].text
    link_text = items[n][2].text
    date_text = items[n][3].text
    ptext = ptext.replace('<description>','').replace('</description','\n')
    final_news += title+ptext+"\n\n"+link_text+"\n\n"+date_text+"\n\n"
    return final_news
  ```
  * 天氣預報function，與即時新聞相同作法，改成抓取中央氣象局桃園區天氣API，再將需要的值回傳
  ```python
  def monoWea(chk):
    final_wea = ""
    con = requests.get('https://www.cwb.gov.tw/rss/forecast/36_05.xml')
    con.encoding='utf-8'
    tree = ET.fromstring(con.text)
    items = list(tree.iter(tag='item'))
    title = items[chk][1].text
    ptext = items[chk][3].text
    ptext = ptext.replace('<description>','').replace('<br>','').replace('<BR>','').replace('</description','\n')
    final_wea = title+"\n"+ptext+"\n\n"
    return final_wea
  ```
  * 推薦音樂與推薦電影因為時間不足，為數據內容隨機推薦，沒有使用API功能
  ```python
  def monoMus(chk2):
    songTitle=[["Eric周興哲《怎麼了》-｜YouTube FanFest 2020｜","https://www.youtube.com/watch?v=i4LdeOdTxpY"],
      ["Eric周興哲《我很快樂 I'm Happy》Official Music Video","https://www.youtube.com/watch?v=Ezd_DLawfHI"],
      ["Eric周興哲《In the Works》Official Music Video","https://www.youtube.com/watch?v=vtVWs2npVAs"],
      ["Eric周興哲《相信愛 Always Believe in Love》MV Teaser","https://www.youtube.com/watch?v=lZeuJTv-3fI"],
      ["Eric周興哲《其實你並沒那麼孤單 You Are Not Alone》Official Music Video","https://www.youtube.com/watch?v=YB6g7HtJmvY"]]
    ptext = "推薦你這首歌陪你度過寂靜的時光：" + songTitle[chk2][0] +"\n" +songTitle[chk2][1]
    return ptext

  def monoMov(chk3):
    movTitle=['空中謎航(2D)','拆彈專家2(2D)','水漾的女人(2D)','靈魂急轉彎','真愛鄰距離','腿(2D)','神力女超人1984','魔物獵人(2D)']
    ptext = "我想看" + movTitle[chk3] +" 霸脫~~"
    return ptext
  ```
  * 使用者輸入無意義話語，例如:好的，小優會選擇已讀，更貼近正常人的回覆  

    若輸入小優還未訓練、無法判斷的話語，將跳出提示訊息
  ```python
  elif type == 'shut':
    return ''
  elif type == 'ds':
    return desc['result'] + '\n 輸入"功能表"可以告訴你小優可以做到的事哦~'
  ```

* `girlfriend.py`  

   * 建立Flask物件，設定Channel secret及Channel access token
   ```python
   app = Flask(__name__)
   config = configparser.ConfigParser()
   config.read("config.ini")
   line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
   handler = WebhookHandler(config['line_bot']['Channel_Secret'])
   ```

  * 建立callback路由，檢查 LINE Bot的資料是否正確
   ```python
   @app.route("/callback", methods=['POST'])
   def callback():
     signature = request.headers['X-Line-Signature']
     body = request.get_data(as_text=True)
     app.logger.info("Request body: " + body)
     try:
         handler.handle(body, signature)
     except InvalidSignatureError:
         abort(400)
     return 'OK'
    ```
  * 如果接到使用者傳送的訊息，將接到的文字訊息傳入olami

   ```python
   @handler.add(MessageEvent, message=TextMessage)
   def handle_message(event):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=Olami().nli(event.message.text)))
   ```

## 4. Results

![image](https://user-images.githubusercontent.com/64915975/122668817-89d72f00-d1ec-11eb-9e54-ec3a95a4b95e.png)
**說明書:**  
第一次使用小優的人，可以利用說明書功能，使用快速上手  

**天氣預報與即時新聞:**  
近年天氣千變萬化，有時缺水有時淹水，有了每日天氣資訊，使用者可搭配天氣狀況穿著合適之衣物，好好照顧自己。

![image](https://user-images.githubusercontent.com/64915975/122668842-a8d5c100-d1ec-11eb-8970-583c4402a4ec.png)
**音樂推薦:**  
在悲傷獨處的時刻，音樂將成為其最佳的療癒力量，陪伴使用者度過所有難熬的時光與困難。  

**近期電影推薦:**  
將推薦近期上映之電影，人性化的回覆將給您猶如實際女友與你提出邀約一同去看電影的逼真體驗!  

![image](https://user-images.githubusercontent.com/64915975/122668851-b428ec80-d1ec-11eb-92ce-3a1ee81795a6.png)

**即時新聞:**  
可令使用者更加關注周遭時事，希望其能更貼近現實生活，與旁人有更多共通話題、希望其在現實世界中能有所突破與他人產生交流。  
**簡易遊戲:**  
點擊圖文選單將獲得遊戲說明，為你與小優的日常生活中多些互動增添樂趣。

## :link:References
 1. Linebot NLP 結合+爬蟲 – 
  
    a. 實戰篇－打造人性化 Telegram Bot  
      https://zaoldyeck.medium.com/%E5%AF%A6%E6%88%B0%E7%AF%87-%E6%89%93%E9%80%A0%E4%BA%BA%E6%80%A7%E5%8C%96-telegram-bot-ed9bb5b8a6d9  
   
    b. （二）為 Chatbot 增加 NLP 功能  
      https://zaoldyeck.medium.com/%E5%88%A9%E7%94%A8-olami-open-api-%E7%82%BA-chatbot-%E5%A2%9E%E5%8A%A0-nlp-%E5%8A%9F%E8%83%BD-e6b37940913d  
    
    c. （三）為 Chatbot 添加新技能  
      https://zaoldyeck.medium.com/add-custom-skill-into-chatbot-cef9bfeeef52  
    
    d. Line Bot 助手機器人實作  
      https://skywalker0803r.medium.com/line-bot%E5%8A%A9%E6%89%8B%E6%A9%9F%E5%99%A8%E4%BA%BA%E5%AF%A6%E4%BD%9C-893e24db0ab5  
    
    e. [Python 網路爬蟲]YAHOO 電影-電影院,放映類型,放映時間(使用Yahoo API)  
      https://medium.com/@ethan.chen927/python%E7%B6%B2%E8%B7%AF%E7%88%AC%E8%9F%B2-yahoo%E9%9B%BB%E5%BD%B1-%E9%9B%BB%E5%BD%B1%E9%99%A2-%E6%94%BE%E6%98%A0%E9%A1%9E%E5%9E%8B-%E6%95%B8%E4%BD%8D-3d-imax-3d-%E6%94%BE%E6%98%A0%E6%99%82%E9%96%93-fc723e55727a

 2. olami 語法參考 https://tw.olami.ai/wiki/?mp=osl&content=osl1.html
 3. API 使用  
    a. 自由時報 https://news.ltn.com.tw/rss/entertainment.xml  
    b. 中央氣象局 https://www.cwb.gov.tw/rss/forecast/36_05.xml  
    c. olami https://tw.olami.ai/cloudservice/api  
## 補充-olami小介紹
![image](https://user-images.githubusercontent.com/64915975/122672071-471d5300-d1fc-11eb-8e07-6d904ce83fc0.png)
