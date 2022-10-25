from typing import Dict
import requests


def getStationWeather(s: str):
    url = "http://www.nmc.cn/rest/weather?stationid=" + s
    res = requests.get(url)
    # decode by utf
    res.encoding = 'utf-8'
    res.close()
    if (res.status_code == 200):
        return res.json()
    else:
        return None


def getWeatherJson(city: str):
    url = "http://www.nmc.cn/essearch/api/autocomplete"
    # q=  city  &limit=10&timestamp=1666698187568&_=1666698178583"
    para = {
        "q": city,
        "limit": 10,
        "timestamp": 1666698187568,
        "_": 1666698178583
    }
    res = requests.get(url, params=para)
    res.close()
    if (res.status_code == 200):
        j = res.json()
        if (len(j) > 0 and j['data'] != None):
            return getStationWeather((j['data'][0]).split("|")[0])
        else:
            return None


def getSimpleWeather(city: str) -> Dict:
    j = getWeatherJson(city)
    if (j != None):
        ret = {}
        ret['city'] = j['data']['real']['station']['city']
        ret['feelst'] = j['data']['real']['weather']['feelst']
        ret['humidity'] = j['data']['real']['weather']['humidity']
        ret['info'] = j['data']['real']['weather']['info']
        ret['rain'] = j['data']['real']['weather']['rain']
        ret['temperature'] = j['data']['real']['weather']['temperature']
        return ret
    return None


def getSimpleWeatherStr(city: str) -> str:
    result = getSimpleWeather(city)
    if (result == None):
        return "地区不存在"
    return f"{result['city']}当前天气信息：\n天气:{result['info']}\n温度:{str(result['temperature'])}℃\n湿度:{str(result['humidity'])}%\n降水量:{result['rain']}mm\n体感温度:{str(result['feelst'])}℃"


def getComplexWeather(city: str) -> Dict:
    j = getWeatherJson(city)
    if (j != None):
        ret = {}
        ret['city'] = j['data']['real']['station']['city']
        ret['feelst'] = j['data']['real']['weather']['feelst']
        ret['humidity'] = j['data']['real']['weather']['humidity']
        ret['info'] = j['data']['real']['weather']['info']
        ret['rain'] = j['data']['real']['weather']['rain']
        ret['temperature'] = j['data']['real']['weather']['temperature']

        ret['winddegree'] = j['data']['real']['wind']['degree']
        ret['windpower'] = j['data']['real']['wind']['power']
        ret['winddirection'] = j['data']['real']['wind']['direct']
        ret['windspeed'] = j['data']['real']['wind']['speed']

        ret['radarurl'] = "http://www.nmc.cn" + (j['data']['radar']['image'])

        ret['predict'] = j['data']['predict']['detail']
        return ret
    return None


def getComplexWeatherStr(city: str) -> list:
    result = getComplexWeather(city)
    if (result == None):
        return ["地区不存在"]
    ret = []
    ret.append(f"{result['city']}当前天气信息：\n天气:{result['info']}\n温度:{str(result['temperature'])}℃\n湿度:{str(result['humidity'])}%\n降水量:{result['rain']}mm\n体感温度:{str(result['feelst'])}℃")
    ret.append(
        f"当前状态：\n风向:{result['winddirection'] if result['winddirection']!= '9999' else '风过小'}\n风力:{result['windpower']}\n风速:{str(result['windspeed']) + 'm/s'}\n风向角度:{(str(result['winddegree']) + '°') if result['winddegree']!= 9999 else '风过小'}")
    ret.append('未来天气预报：\n' + "\n".join([f"{i['date']}:\n白:{i['day']['weather']['info']},{i['day']['wind']['direct']},{i['day']['wind']['power']},{i['day']['weather']['temperature']}℃\n夜:{i['night']['weather']['info']},{i['night']['wind']['direct']},{i['night']['wind']['power']},{i['night']['weather']['temperature']}℃" for i in result['predict'][1:]]))
    ret.append(result['radarurl'])
    return ret
