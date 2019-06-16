import requests
import random
from wxpy import *


def get_img(msg):
    '''获取表情图并下载到本地
    :param msg:string 表情包信息
    :return img_name | 表情包路径
    '''
    # 拼出要获取的表情图地址
    idnum = random.randint(1, 5000)
    url = 'http://image.baidu.com/meme/api/drawer?id=' + str(idnum) + '&type=1&word=' + msg
    
    # 文件存储路径
    img_name = './image/' + str(idnum) + '.jpg'
    # 下载文件    
    r = requests.get(url)
    with open(img_name, 'wb') as f:
        f.write(r.content) 
    
    return img_name

def img_reply(msg):
    '''回复表情图信息
    :param msg:object 接收到的群消息
    '''
    # 只处理文字信息
    if msg.type == 'Text':
        # 返回帮助内容
        if msg.text == 'help' or msg.text == '帮助':
            print(msg.text)
            msg.reply_msg('斗图使用技巧： \n ls/find/get/img/图 表情内容')
            
        msgarr = msg.text.split(' ')
        # 判断是否需要返回表情图
        img_reply_list = ['get', 'find', 'img', 'ls', '图']
        if len(msgarr) > 1 and (msgarr[0] in img_reply_list):
            msgarr.remove(msgarr[0])
            # 将关键字去除后的部分拼成文字并发送获取表情图
            msg.reply_image(get_img(''.join(msgarr).strip()))



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
