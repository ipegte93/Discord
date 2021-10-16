def mule_search(name, min=1, max=None, period=None):
    path = "https://www.mule.co.kr/bbs/market/sell"
    query = "?qf=title"
    query += "&qs=" + name
    query += "&start_price=" + str(min)

    if max==None:
        max = ""
    query += "&end_price=" + str(max)

    return_data = list() #첫번째는 상태 코드 -1이 아니면 에러임
    return_data.append(-1)

    if period != None:
        if period != 6 or period != 12:
            return_data.append(period)

        if period<2013 or period>2021:
            return_data.append(period)

    else:
        period=""
    query += "&period=" + str(period)

    return_data.append(path+query)
    return return_data[1]