# _*_ coding: utf-8 _*_

'''
以树莓派为服务端，把H.264编码视频流放到8000tcp端口, 推流到七牛的pili平台，具体七牛的pili平台设置见官方文档
利用七牛的pili库，生成推流地址，python调用shell利用之前编译好的FFMPEG连接8000端口,

ffmpeg的编译参考官网: https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu  和 \
廖雪峰 http://www.liaoxuefeng.com/article/001456198314370db046cbe5e5a45388bf3ade4bc2c5cb0000
七牛的pili推流文档：https://github.com/pili-engineering/pili-sdk-python
树莓派摄像头的python库文档：http://picamera.readthedocs.io/en/release-1.12/
'''

import socket
import time
import picamera
import pili
import os
import sys
from monitor import monitoring
import multiprocessing


#生成七牛云的推流地址 也可在七牛直播流管理里面获得但刷新变换
#在自己的域名管理中CNAME设置pili-publish,pili-live-rtmp/hls等
def gen_url():
    mac = pili.Mac('xxxxxx', 'xxxxxx')    #七牛的密钥管理
    hub = 'xxx'                         #空间名
    key = 'xxx'                         #创建的流名
    publish = 'pili-publish.xxx.xxx'   #后面为你的域名
    rtmp = 'pili-live-rtmp.xxx.xxx'
    hls = 'pili-live-hls.xxx.xxx'
    publish_url = pili.rtmp_publish_url(publish, hub, key, mac, 3600)
    rtmp_url = pili.rtmp_play_url(rtmp, hub, key)
    print('rtmp player url: %s' % rtmp_url)
    return publish_url


def recoding():
    camera = picamera.PiCamera()
    camera.resolution = (860, 480)
    camera.framerate = 36
    s = socket.socket()
    s.bind(('0.0.0.0', 8000))
    s.listen(5)
    connection = s.accept()[0].makefile('wb')
    try:
        camera.start_recording(connection, format='h264')
        while 1:
            camera.wait_recording(10)       #十秒截取一张图片
            camera.capture(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())+'.jpeg', use_video_port=True)
        camera.stop_recording()
    finally:
        connection.close()
        s.close()


def pushing():
    url = gen_url()
    time_title = "fontfile=/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf:x=w-tw:fontcolor=white:fontsize=30:text='%{localtime\:%X}'"
    cmd = 'ffmpeg -i tcp://127.0.0.1:8000 -vf vflip -r 36 -codec copy -threads 8 -preset ultrafast  -an -b:v 1000k -vcodec libx264 -s 860x480 -vf drawtext="' + time_title + '" -f flv "' + url + '"'
    time.sleep(1)
    try:
        os.system(cmd)
    except Exception as e:
	print('Push living stream faild, error is %s' % e)


def main():
    worker_1 = multiprocessing.Process(target=recoding, args=())
    worker_2 = multiprocessing.Process(target=pushing, args=())
    worker_3 = multiprocessing.Process(target=monitoring, args=())
    worker_1.start()
    worker_2.start()
    worker_3.start()
    worker_1.join()
    worker_2.join()
    worker_3.join()


if __name__ == '__main__':
    main()
