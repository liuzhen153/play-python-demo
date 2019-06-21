import requests
import random
from wxpy import *
import json
import os
import time
import threading


def get_img(msg):
    '''获取表情图并下载到本地
    :param msg:string 表情包信息
    :return img_name | 表情包路径
    '''
    # 拼出要获取的表情图地址
    idnum = random.randint(1, 5000)
    url = 'http://image.baidu.com/meme/api/drawer?id=' + str(idnum) + '&type=1&word=' + msg

    # 文件存储路径
    img_name = './image/' + str(int(time.time())) + '.jpg'
    # 下载文件    
    r = requests.get(url)

    with open(img_name, 'wb') as f:
        f.write(r.content) 
        
    return img_name



def get_gif(msg,type_ = 1):
    '''获取表情图并下载到本地
    :param msg:string 表情包信息
    :return img_name | 表情包路径
    '''
    # 拼出要获取的表情图地址
    url = 'http://image.baidu.com/meme/api/searchresult?pn=0&rn=60&gif=' + str(type_) + '&query=' + msg + '&emoji=1'

    
    # 下载文件    
    r = requests.get(url)
    data = json.loads(r.text)['data']['ac']

    # 文件存储路径
    idnum = random.randint(0, len(data) - 1)
    
    img = data[idnum]['objUrl'].replace('https', 'http')

    
        
    headers = {
        'Host': 'img4.imgtn.bdimg.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    if type_ == 1:
        headers['Host'] = 'timgsa.baidu.com'
    
    img_arr = img.split('.')

    # 文件存储路径
    img_name = './image/' + str(int(time.time())) + '.' + img_arr[len(img_arr) - 1]

    
    # 下载文件    
    r = requests.get(img, headers=headers)
    with open(img_name, 'wb') as f:
        f.write(r.content) 
    
    
    media_id = bot.upload_file(img_name)

    if type_ == 1:
        return '.gif', media_id, img_name
    else:
        return '', media_id, img_name



def img_reply(msg):
    t = threading.Thread(name='reply_' + str(int(time.time())), target=reply,args=(msg,))
    t.start()
    t.join()

def reply(msg, count = 1):
    '''回复表情图信息
    :param msg:object 接收到的群消息
    '''
#     print('hi')
    # 只处理文字信息
    if msg.type == 'Text':
        # 返回帮助内容
        if msg.text == 'help' or msg.text == '帮助':
            print(msg.text)
            msg.reply_msg('斗图使用技巧： \n 图 表情内容 \n 斗 关键字 \n 动 关键字')
            
        msgarr = msg.text.split(' ')
        # 判断是否需要返回表情图
        img_reply_list = ['图', '动', '斗']
        reply_ret = False
        
        if len(msgarr) > 1 and (msgarr[0] in img_reply_list):
            try:
                key = msgarr[0]
                msgarr.remove(msgarr[0])
                if key == '图':
                    print('tu')
                    # 将关键字去除后的部分拼成文字并发送获取表情图
                    img_name = get_img(''.join(msgarr).strip())
                    msg.reply_image(img_name)
                    os.remove(img_name)
                    reply_ret = True
                    return

                if key == '斗':
                    gif, media_id, img_name = get_gif(''.join(msgarr).strip(), 0)


                if key == '动':
                    gif, media_id, img_name = get_gif(''.join(msgarr).strip())

                msg.reply_image(gif, media_id=media_id)
                os.remove(img_name)

                reply_ret = True
            except Exception as e:
                pass
            finally:
                if not reply_ret and count <= 3:
                    count += 1
                    return reply(msg, count)
                elif not reply_ret and count > 3:
                    msg.reply_msg('未查到该表情包：' + ''.join(msgarr).strip())
            
            



# 微信登录
bot = Bot()  

# 打印来自其他好友、群聊和公众号的消息
@bot.register(except_self=False)
def print_others(msg):
    print(msg)


# 自动接受新的好友请求
@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    # 接受好友请求
    new_friend = msg.card.accept()
    # 向新的好友发送消息
    new_friend.send('嗨，我自动接受了你的好友请求~')

img_group = ensure_one(bot.groups().search('表情图'))
print(img_group)
# 自动发送表情
@bot.register(img_group,except_self=False)
def img_group_message(msg):
    img_reply(msg)
