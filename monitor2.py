# _*_ coding: utf-8 _*_ 

import notice
import phash


def monitoring():
    print('Start diff imges...')
    # 如果两幅图指纹不同, 发送邮件和短信, 最后只保留最后一张图片
    if phash.imgs_diff(files[-2], files[-1]):
        notice.send_mail(files[-2:])
        notice.send_sms()
    for img in files[:-1]:
        os.remove(img)

	
if __name__ == '__main__':
    monitoring()
