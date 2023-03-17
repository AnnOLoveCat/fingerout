# fingerout
此專案使以Python、Django完成
安裝參考：https://www.learncodewithmike.com/2020/06/python-line-bot.html

僅只有設定公開網址具有HTTPS，LINE頻道(Channel)才有辦法連結部分，是使用fly.io完成

## 開發事前準備
安裝python
開啟控制台並前往至專案資料夾
執行`python -m venv venv`
開啟虛擬環境`.\venv\Scripts\activate`
安裝`pip install -r requirements.txt`
設定安裝line套件`pip install line-bot-sdk`
設置`.env檔`
## 注意事項
開發過程中，先注意目前自己在哪個支條上
不要再main支條上做編輯，如果知道你在幹什麼
不要隨便和別人的支條做合併，會很嚴重
如果有pip install任何模組，請記得要在虛擬環境下安裝，並記得要pip freeze > requirements.txt
