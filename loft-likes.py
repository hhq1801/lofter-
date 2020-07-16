from tkinter import *
import requests
import time
import json
import urllib
import random
import tkinter.messagebox as messagebox

init_window = Tk()  # 实例化出一个父窗口
# 设置窗口属性
init_window.title("lofter我的喜欢下载  by AlessiaH")
init_window.geometry('700x400+10+10')


# 建立输入框
# 地址
labe_iddr = Label(init_window, text="lofter个人网址(如我的网址是sublatin.lofter.com)")
labe_iddr.pack()
text_iddr_default = StringVar()
text_iddr = Entry(init_window, textvariable=text_iddr_default)
text_iddr_default.set("sublatin")
text_iddr.pack()

# 账户
labe_like = Label(init_window, text="你\"喜欢\"的文档数量")
labe_like.pack()
text_like_default = StringVar()
text_like = Entry(init_window, textvariable=text_like_default)
text_like_default.set("4780")
text_like.pack()


# 密码
# labe_pwd = Label(init_window, text="密码")
# labe_pwd.pack()
# text_pwd_default = StringVar()
# text_pwd = Entry(init_window, textvariable = text_pwd_default)
# text_pwd_default.set("root")
# text_pwd.pack()
def get_like():
    urllog = 'https://yaolu.yuedu.163.com/statistics/log/app/upload.json'
    headers = {'SDK-Ver': '2.1.7',
               'x-upload-time': str(int(time.time())),
               'Content-Type': 'application/x-gzip',
               'Hashed-APPKEY': 'acbd5c82e945459ffd7b672d9cf4a9e0f02b9e94',
               'Content-Length': '0',
               'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.0.0; VIE-AL10 Build/HUAWEIVIE-AL10)',
               'Host': 'yaolu.yuedu.163.com',
               'Connection': 'Keep-Alive',
               'Accept-Encoding': 'gzip',
               }
    s = requests.Session()
    a = s.post(urllog, headers=headers, data='')
    heads = {'User-Agent': 'LOFTER-Android 6.9.0 (VIE-AL10; Android 8.0.0; null) WIFI',
             'Host': 'api.lofter.com',
             'Connection': 'Keep-Alive',
             'Accept-Encoding': 'gzip',
             'Content-Length': '107',
             'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
             'deviceid': 'ffffffff',
             'dadeviceid': '',
             'androidid': ''}
    blogname = text_iddr.get()
    likecount = text_like.get()
    l1 = []
    # try:
    for i in range(1):
        url = 'http://api.lofter.com/v1.1/batchdata.api?product=lofter-android-6.9.2'
        for offset in range(0, int(likecount), 500):
            print(offset)
            data = 'supportposttypes=1%2C2%2C3%2C4%2C5%2C6&blogdomain={}.lofter.com&offset={}&method=favorites&postdigestnew=1&returnData=1&limit=10'.format(
                blogname, offset)
            a = s.post(url, headers=heads, data=data, timeout=45)
            items = json.loads(a.text)['response']['items']
            for i in range(len(items)):
                try:
                    row = items[i]['post']  # ['postCollection']# ['content']#['blogInfo']
                    row['pubTime'] = time.strftime("%Y-%m-%d", time.localtime(float(row['publishTime']) / 1000))
                    postid, title, type_, pubTime, content, post_url, author, author_url, tags = (
                        row['id'], row['title'], row['type'],
                        row['pubTime'], row['content'], row['blogPageUrl'],
                        row['blogInfo']['blogNickName'], row['blogInfo']['homePageUrl'], row['tagList'])
                    print(title)
                    try:
                        tag1 = tags[0]
                    except:
                        tag1 = ''
                    tag_out = ''
                    for t in tags:
                        if tag_out != '':
                            tag_out += ', '
                        tag_out += """<a href="http://www.lofter.com/tag/{}">{}</a>""".format(urllib.parse.quote(t), t)

                    r = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <meta charset="utf-8"/>
  <meta http-equiv="x-ua-compatible" content="ie=edge"/>
  <title>{} - {} - {}</title> """.format(title, author, tag1) + """
  <style type="text/css">p.message{text-align:center}.meta h1{font-size:1.5em;text-align:center}.meta h2{font-size:1.25em;text-align:center}.meta h2{page-break-before:always}.meta .byline{text-align:center}.meta dl.tags{border:1px solid;padding:1em}.meta dd{margin:-1em 0 0 10em}.meta .endnote-link{font-size:.8em}#chapters{font-family:"Nimbus Roman No9 L","Times New Roman",serif;padding:1em}.userstuff{font-family:"Nimbus Roman No9 L","Times New Roman",serif;padding:1em}.toc-heading{display:none}</style>
</head>
<body>
""" + """
<div id="preface">
  <h2 class="toc-heading">Preface</h2>

  <p class="message">
    <b>{}</b><br/>
    Posted originally on the <a href="http://www.lofter.com/">Lofter</a> at <a href="{}">http://{}</a>.
  </p>

  <div class="meta">
    <dl class="tags">
          <dt>Tags:</dt>
          <dd>{}</dd>
      <dt>Stats:</dt>
      <dd>
        Published: {}
      </dd>
    </dl>
    <h1>{}</h1>
    <div class="byline">by <a rel="author" href="{}">{}</a></div>

  </div>
</div>


<div id="chapters" class="userstuff">
    <h2 class="toc-heading">{}</h2>
    <div class="userstuff">
      {}
    </div>
</div>

<div id="afterword">
  <h2 class="toc-heading">Afterword</h2>


  <p class="message">如果你喜欢这篇post <a href="{}">请访问原页面</a>让作者感受到你的爱!</p>
  <p class="message">本页面参考<a href="http://archiveofourown.org">archive of our own</a>导出</p>
</div>

</body>
</html>""".format(title, post_url, post_url, tag_out, pubTime, title, author_url, author, title,
                                      content,
                                      post_url)
                    with open(r'{}-{}-{}.html'.format(postid, title, author).replace('/', '').replace('\\', ''), 'w',
                              encoding='utf-8') as f:
                        f.write(r)
                except:
                    None
            time.sleep(random.randint(2, 4))

        messagebox.showinfo(title='successed', message='已成功下载')
        print(1)

        init_window.destroy()
        init_window.mainloop()
    # except:
    #     print("ERROR")
    #     messagebox.showinfo(title='failed', message='失败')



# 建立按钮
# 通过command属性来指定Button的回调函数
button_sure = Button(init_window, text="确定", width=15,
                     height=2, command=get_like)
button_sure.pack()
init_window.mainloop()
# 6.按钮回调函数，拷贝输入框的字符串，然后将字符串用于连接数据库
