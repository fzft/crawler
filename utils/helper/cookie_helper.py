from collections import defaultdict
from yarl import URL
from http.cookies import SimpleCookie


def cookiejar2str(cookie):
    # cookies ={}
    cookies_tr = ''
    try:
        for i in cookie:
            cookies_tr = cookies_tr + i.key + "=" + i.value + ";"
    except Exception as e:
        print(e)
    return cookies_tr


def update_cookie(cookie, domain=""):
    # cookies = {}
    try:
        for i in cookie:
            i['path'] = '/'
            if domain:
                i['domain'] = domain
            # cookies[i.key] = i.value
    except Exception as e:
        print(e)

    # cookie = cookie.update_cookies(cookie,url)
    return cookie


def cookie_add(cookie, cookiedic, domain=''):
    try:
        addCookie = SimpleCookie()
        for key in cookiedic:
            addCookie[key] = cookiedic[key]
            if domain:
                addCookie[key]["domain"] = domain
            addCookie[key]["path"] = "/"
        cookie.update_cookies(addCookie)
        # print(str(cookie))
    except Exception as e:
        print(e)


def get_cookie_str(cookies):
        result = ''
        for idx, item in enumerate(cookies.items()):
            k, v = item
            if v:
                result += (k + "=" + v)
                if idx < (len(cookies.items()) - 1):
                    result += '; '
        return result