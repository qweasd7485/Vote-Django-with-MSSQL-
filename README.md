# VoteMSSQL

<p>Django實作使用Microsoft SQL Server - 投票系統</p>

## 運行環境  
<p>1.Windows 10 Professional 64bit/Windows 7 Professional 64bit</p>
<p>2.Python 3.8.3</p>
<p>3.Microsoft SQL Server 2019</p>
<p>4.作業系統環境詳細配置如圖</p>

![image](https://github.com/qweasd7485/VoteMSSQL/blob/master/Pictures/OS環境配置圖.PNG)

## 工具
<p>1.Eclipse IDE for Eclipse Committers Version:2020-03(4.15.0) </p>
<p>2.Microsoft SQL Server Management Studio v18.5 </p>
<p></p>
<p></p>

## 前置部署作業 

### 一、虛擬環境
<p>1.(一般建於我的文件中)</p>

...>python -m venv <虛擬環境名稱>

<p>下圖為建立[voteVenv](紅框處)</p>

![image](https://github.com/qweasd7485/VoteMSSQL/blob/master/Pictures/VirtualenvCreate.PNG)

<p>2.進入虛擬環境中</p>
<p>先進入剛剛建立的虛擬環境路徑資料夾Scripts中(紅框處)</p>

...>activate

![image](https://github.com/qweasd7485/VoteMSSQL/blob/master/Pictures/VenvEntry.png)

<p>接續命令提示字元會自己刷新並在路徑前面顯示(虛擬環境名稱)</p>

![image](https://github.com/qweasd7485/VoteMSSQL/blob/master/Pictures/VirtalenvEntrySuccess.png)

<p>3.虛擬環境中需安裝的套件與版本</p>

(venv)...>pip freeze

![image](https://github.com/qweasd7485/VoteMSSQL/blob/master/Pictures/Venvpipfreeze.png)

