from enum import  Enum

class ContentFlag(Enum):

    all = 'all'
    call = 'call'
    sms = 'sms'
    busi = 'busi' 
    bill = 'bill'
    balance = 'balance'
    recharge = 'recharge'


def is_execute(spider,flag):
    try:
        content = spider.task_params['ContentFlag']
        if content:
            ls = content.lower().split(';')
            if ls and ('all' in ls or flag.lower() in ls):
                return True
        return False
    except:
        return False