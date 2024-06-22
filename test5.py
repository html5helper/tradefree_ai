from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-4-0125-preview",
  # model="gpt-4-turbo-preview",
  # model="gpt-4",

  # model="gpt-3.5-turbo-instruct",
  # model="gpt-3.5-turbo",


  # response_format={ "type": "json_cobject" },
  messages=[
    {"role": "system", "content": "You are a helpful assistant designed to give keywords from youtube video descript."},
    # {"role": "user", "content": "the keywords for the youtube video in chinese"},
    #clear{"role": "assistant", "content": "The 15 keywords."},
    {"role": "user", "content": "give me the keywords array in chinese from the following comments:"+'''
@xipingzhang1092
@xipingzhang1092
4天前
我买了Tesla Y。今天试了自动驾驶，非常震撼😊要开始远途旅行了！
22
谢嘉琪
回复


1 条回复
@ycy899
@ycy899
4天前
V12.3昨天安装试用了一下，进步是明显的，一些场景靠写代码解决不了的问题，这次解决了。原来的版本急加速或者急刹车，我使用时倒是极少碰到，但是交叉口方向盘晃来晃去是常有的，这次就相对平稳了，驾驶感受好很多。
38
谢嘉琪
回复


谢嘉琪
·

12 条回复
@user-kb3jl9ci8m
@user-kb3jl9ci8m
4天前
10倍TSLA要來臨
16
谢嘉琪
回复

@52088
@52088
4天前
小弟謝謝你的更新👍🏻。
3
谢嘉琪
回复

@yongxiangkuak2656
@yongxiangkuak2656
4天前
该上车了！GOGOGO～
8
谢嘉琪
回复

@vincentliu4760
@vincentliu4760
4天前
感谢
2
谢嘉琪
回复

@byrony3842
@byrony3842
3天前
特斯拉的自动驾驶前景一片光明，令人振奋！
1
回复

@ishuanw2001
@ishuanw2001
4天前
🎉特斯拉真的 很強
1
谢嘉琪
回复

@acidfish0403
@acidfish0403
4天前
如果通用型AI可以只靠設計憑空產生那人類目前的科技水平絕對不只這樣的水準，大量各種不同環境的不斷試錯才是關鍵，我認為目前只有特斯拉走在合理的道路上，能不能達成通用型AI在於這AI對情境的判讀能力跟人類生活匹配度高到什麼程度，而不是某個機構或那些特定人士的認定才叫通用型AI，當絕大多數人都能很好的使用一套AI系統你會說他不是一個通用型AI嗎?所以為什麼老馬現在極盡推廣使用，很多人是以刺激銷售量或股價來看這件事，但事實上只有極大化使用者數量才能讓FSD跨過能通用的門檻，能促成這件事的是使用者們而不是某個很厲害的工程師
9
谢嘉琪
回复


1 条回复
@GeJiayu
@GeJiayu
4天前（修改过）
很多人會說特斯拉現在只是lv.2
然後說奔馳已經lv.3 blablabla的，只能說非常可笑
還在糾結lv幾誰來負責等等
我看他們是真的不懂

還有另個在X上看到的消息，有waymo工程師跳到特斯拉了XD
我現在就在此正式宣布!今年就是特斯拉自動駕駛的元年!
14
谢嘉琪
回复


谢嘉琪
·

8 条回复
@kevinyang4929
@kevinyang4929
4天前
受益良多
2
谢嘉琪
回复


谢嘉琪
·

1 条回复
@gwpeng6793
@gwpeng6793
3天前
🎉🎉支持
谢嘉琪
回复

@yangzhang6754
@yangzhang6754
4天前
赶紧买了点特斯拉的股票
8
谢嘉琪
回复

@eldahini01
@eldahini01
3天前
今天就來買TSLA!!!
1
谢嘉琪
回复

@tmc4832
@tmc4832
4天前
Time to all in!
4
谢嘉琪
回复

@yi_huimeng1936
@yi_huimeng1936
2天前（修改过）
發明電動車等於去救fox527AB==303B==903O 他們本應該是汽油oil在內燃機裡不斷受苦燃燒 ...現在都換battery114B受苦了😢
1
回复

@josephkohishii6001
@josephkohishii6001
4天前
我心動了！
誰還去買激光雷達電動車？
3
谢嘉琪
回复

@jkg2001
@jkg2001
2天前
在很多機車環繞的塞車環境能用嗎能用嗎
回复

@Vision_Future.2024
@Vision_Future.2024
4天前
🎉🎉
1
谢嘉琪
回复

@Niki-bh4wx
@Niki-bh4wx
4天前
您在中文翻譯字幕中沒翻譯U turn，建議您翻譯成「迴轉」或「調頭」'''}
  ]
)

#print(completion.choices[0].message)
print(completion.choices)
