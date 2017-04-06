# _*_ coding: utf-8 _*_
import requests
import top

#邮件服务调用mailgun的API   https://www.mailgun.com/ 
#也可使用python的smtplib和email两个模块    
def send_mail(imglist):
    with open('mail.html', 'r') as f:
        html_tmp = f.read().replace('IMG1', imglist[0]).replace('IMG2', imglist[1])
    url = "https://api.mailgun.net/xx/xxxxxxxx/messages"
    auth = ("api", "key-xxxxxx")
    imgs = [("inline", open(imglist[0])), ("inline", open(imglist[1]))]
    payload = {"from": "Raspberry Pi<Raspi_notice@mirgo.com>",
               "to": ["xxxxxxx@xxx.com"],
               "subject": "来自树莓派",
               "html": html_tmp}
    try:
        r = requests.post(url, auth=auth, files=imgs, data=payload)
    except:
	pass

#短信调用阿里大于的API   可以pip install top直接使用
def send_sms():
    url = 'gw.api.taobao.com'
    appkey = 'xxxxxx'
    secret = 'xxxxxx'
    port = 80
    req = top.api.AlibabaAliqinFcSmsNumSendRequest(url, port)
    req.set_app_info(top.appinfo(appkey, secret))
    
    req.format = "json"
    req.extend = "123456"
    req.sms_type = "normal"
    req.sms_free_sign_name = "XXX"          #申请好的模板名字
    req.rec_num = '181xxxxxxxx'
    req.sms_template_code = "SMS_xxxxxx"

    try:
        r = req.getResponse()
    except Exception as e:
        print(e)
    
#阿里大于同时提供语音服务
def send_voice():
    pass
