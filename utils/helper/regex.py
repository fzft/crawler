import re

def search(str,str1):
    try:
        se=re.search(str,str1)
        if(se):
            return se.group(1)
        else:
            return ""
    except:
        return ""

def replace(pattern,str,str1):
    return re.sub(pattern,str1,str)

def is_match_sucess(str,str1):
    se = re.search(str,str1)
    if se:
        return True
    else:
        return False


def findsingle(str,str1,flag=0):
    se=re.findall(str,str1,re.S)
    if(se):
        return se[0]
    else:
        return ""

def find_all(str,str1):
    se=re.findall(str,str1,re.S)
    if(se):
        return se
    else:
        return []

