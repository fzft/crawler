import json

def load(text):
    try:
        load=json.loads(text)
        return load
    except Exception as e:
        return None


def json_string(dic):
    try:
        load=json.dumps(dic)
        return load
    except Exception as e:
        return None


def json_get(json, l_key, default=None):  
    ret = json
    if (type(l_key) is int) or (type(l_key) is str):
        l_key = [l_key]
    for k in l_key:  
        if type(k) is int:  
                if k < 0 : return default  
                if not (type(ret) is list): return default  
                if len(ret) <= k: return default  
        elif type(k) is str:  
                if not (type(ret) is dict): return default  
                if not k in ret: return default  
        else:  
                return default  
        ret = ret[k]  
  
    return ret  


def key_exist(json,l_key, default=False):
    try:
        ret = json
        if (type(l_key) is int) or (type(l_key) is str):
            l_key = [l_key]
        for k in l_key:  
            if type(k) is int:  
                if k < 0 : return default  
                if not (type(ret) is list): return default  
                if len(ret) <= k: return default  
            elif type(k) is str:  
                if not (type(ret) is dict): return default  
                if not k in ret: return default  
            else:  
                return default  
            ret = ret[k]  

        return True

    except Exception as e:
        return False


def key_len_exist(json,l_key, default=False):
    try:
        ret = json
        if (type(l_key) is int) or (type(l_key) is str):
            l_key = [l_key]
        for k in l_key:  
            if type(k) is int:  
                if k < 0 : return default  
                if not (type(ret) is list): return default  
                if len(ret) <= k: return default  
            elif type(k) is str:  
                if not (type(ret) is dict): return default  
                if not k in ret: return default  
            else:  
                return default  
            ret = ret[k]  
        if ret and len(ret):
            return True
        else:
            return False

    except Exception as e:
        return False