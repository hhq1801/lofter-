import tkinter as tk
import requests
import time
import os
import json
import urllib
import random
import tkinter.messagebox as messagebox

init_window = tk.Tk()
init_window.title("lofter我的喜欢下载  by AlessiaH")
init_window.geometry('400x400+10+10')

labe_iddr = tk.Label(init_window, text="lofter个人网址(如我的网址是sublatin.lofter.com)")
labe_iddr.pack()
text_iddr_default = tk.StringVar()
text_iddr = tk.Entry(init_window, textvariable=text_iddr_default)
text_iddr_default.set("sublatin")
text_iddr.pack()

labe_like1 = tk.Label(init_window, text="你\"喜欢\"的文档数量：\n 从\n(默认填0即从最新喜欢的开始下载，如果分批下载可以填上一次下载数)")
labe_like1.pack()
text_like1_default = tk.StringVar()
text_like1 = tk.Entry(init_window, textvariable=text_like1_default)
text_like1_default.set("0")
text_like1.pack()

labe_like2 = tk.Label(init_window, text="到")
labe_like2.pack()
text_like2_default = tk.StringVar()
text_like2 = tk.Entry(init_window, textvariable=text_like2_default)
text_like2_default.set("4780")
text_like2.pack()

def get_like():
    global vstate
    vstate = v.get()
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
    likecount1 = text_like1.get()
    likecount2 = text_like2.get()
    likecount1 = likecount1.split('(')[0]

    try:
        int(likecount1)
        int(likecount2)
    except:
        messagebox.showinfo(title='failed', message='请输入整数')

    l1 = []
    # try:
    for i in range(1):
        url = 'http://api.lofter.com/v1.1/batchdata.api?product=lofter-android-6.9.2'
        step = int(likecount2)-int(likecount1)+1
        if step >= 1000:
            step = 1000
        elif step >= 500:
            step = 500
        for offset in range(int(likecount1), int(likecount2), step):
            lb.insert(tk.END, '开始爬取',offset)
            lb.pack()
            init_window.update()
            data = 'supportposttypes=1%2C2%2C3%2C4%2C5%2C6&blogdomain={}.lofter.com&offset={}&method=favorites&postdigestnew=1&returnData=1&limit={}'.format(
                blogname, offset, step)
            a = s.post(url, headers=heads, data=data, timeout=45)
            items = json.loads(a.text)['response']['items']
            for i in range(len(items)):
                try:
                    row = items[i]['post']  # ['postCollection']# ['content']#['blogInfo']
                    img = ''
                    if row['type']==2:
                        photoLinks = json.loads(row['photoLinks'])
                        for link in photoLinks:
                            img += """<p><img src="{}"  alt="无法访问" /></p> \n""".format(link['raw'])
                    row['pubTime'] = time.strftime("%Y-%m-%d", time.localtime(float(row['publishTime']) / 1000))
                    postid, title, type_, pubTime, content, post_url, author, author_url, tags = (
                        row['id'], row['title'], row['type'],
                        row['pubTime'], row['content'], row['blogPageUrl'],
                        row['blogInfo']['blogNickName'], row['blogInfo']['homePageUrl'], row['tagList'])
                    try:
                        tag1 = tags[0]
                    except:
                        tag1 = ''
                    tag_out = ''
                    for t in tags:
                        if tag_out != '':
                            tag_out += ', '
                        tag_out += """<a href="http://www.lofter.com/tag/{}">{}</a>""".format(urllib.parse.quote(t), t)

                    r = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
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
      {}
    </div>
</div>

<div id="afterword">
  <h2 class="toc-heading">Afterword</h2>


  <p class="message">如果你喜欢这篇post <a href="{}">请访问原页面</a>让作者感受到你的爱!</p>
  <p class="message">本页面参考<a href="http://archiveofourown.org">archive of our own</a>导出</p>
</div>
<p id ="if you have any further questions, please contact hhq1801@hotmail.com"><p>
</body>
</html>""".format(title, post_url, post_url, tag_out, pubTime, title, author_url, author, title, img, content, post_url)
                    filename =format('{}-{}-{}.html'.format(postid, title, author))
                    if vstate!=1:
                        print(vstate)
                        if vstate == 2:
                            path = author
                            filename = format(author)+'\\'+ filename
                        if vstate == 3:
                            path = tag1
                            if tag1=='':
                                tag1='无tag'
                            filename = format(tag1)+ '\\' + filename
                        if not os.path.exists(path):
                            os.makedirs(path)
                    print(filename)
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(r)
                    lb.insert(tk.END, filename)
                    lb.pack()
                    init_window.update()
                except:
                    None
            time.sleep(random.randint(2, 4))


        messagebox.showinfo(title='successed', message='已成功下载\n 请查看该程序所在文件夹')
        print(1)

        # init_window.destroy()
        # init_window.mainloop()


# 定义变量
v = tk.IntVar()
# 设置第二个未默认
v.set(1)
# 单选框
r1 = tk.Radiobutton(init_window, text="默认保存至当前路径", value=1, variable=v)
r1.pack()
r2 = tk.Radiobutton(init_window, text="按作者保存至不同文件夹", value=2, variable=v)
r2.pack()
r3 = tk.Radiobutton(init_window, text="按首tag保存至不同文件夹", value=3, variable=v)
r3.pack()

# 获取状态

button_sure = tk.Button(init_window, text="确定", width=15,
                        height=2, command=get_like)
button_sure.pack()

lb = tk.Listbox(init_window)
yscrollbar = tk.Scrollbar(lb, command=lb.yview)
yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
lb.config(yscrollcommand=yscrollbar.set)
lb.pack(fill=tk.BOTH,expand=True)
def format(t):
    return t.replace('/', '').replace('\\', '').replace(
                            '|', '').replace('<', '').replace('>', '').replace('?', '').replace('*', '').replace(':',
                             '').replace('\"', '')
init_window.mainloop()

