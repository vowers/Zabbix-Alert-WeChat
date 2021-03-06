#!/usr/bin/python
#_*_coding:utf-8 _*_
import requests,sys,json

reload(sys)
sys.setdefaultencoding('utf-8')

def GetToken(Corpid,Secret):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    Data = {
        "corpid":Corpid,
        "corpsecret":Secret
    }
    r = requests.get(url=Url,params=Data)
    Token = r.json()['access_token']
    return Token

def SendMessage(Token,User,Partid,Agentid,Subject,Content):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
    Data = {
        "touser": User,                                 # 成员ID列表（消息接收者，多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为@all，则向该企业应用的全部成员发送
        "toparty" : Partid,                             # 部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为@all时忽略本参数
        #"totag": Tagid,                                # 标签ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为@all时忽略本参数
        "msgtype": "text",                              # 消息类型。
        "agentid": Agentid,                             # 企业号中的应用id。
        "text": {
            "content": Subject + '\n' + Content
        },
        "safe": "0"
    }
    r = requests.post(url=Url,data=json.dumps(Data))
    return r.text


if __name__ == '__main__':
    User = sys.argv[1]                                                              # zabbix传过来的第一个参数
    Subject = sys.argv[2]                                                           # zabbix传过来的第二个参数
    Content = sys.argv[3]                                                           # zabbix传过来的第三个参数
    if User == '1':#zabbix收件人  自定义按需求修改
        User = User
        Partid = "2"             # 部门ID
        Agentid = "2"            # 企业号中的应用id。
        Secret = "xx"            # 应用设置页面查看
    elif User == '2':
        User = User
        Partid = "3"
        Agentid = "xxx"
        Secret = "xx"
    else:
        User = "@all"
        Partid = "2"                                                                     
        Agentid = "xx"   
        Secret = "xx"    
    Corpid = "xxxxxxx"          # CorpID是企业号的标识

    Token = GetToken(Corpid, Secret)
    Status = SendMessage(Token,User,Partid,Agentid,Subject,Content)

    print Status
