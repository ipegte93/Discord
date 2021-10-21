def mule_search(name, max, period):
    path = "https://www.mule.co.kr/bbs/market/sell"
    query = "?qf=title"
    query += "&qs=" + name
    query += "&start_price=" + "1"

    if max==None:
        max = ""
    query += "&end_price=" + str(max)

    return_data = list() #첫번째는 상태 코드 -1이 아니면 에러임
    return_data.append(-1)

    if period != None:
        if int(period) != 6 or int(period) != 12:
            return_data.append(period)

        elif int(period)<2013 or int(period)>2021:
            return_data.append(period)

    else:
        period=""
    query += "&period=" + str(period)

    return_data.append(path+query)
    print(return_data)
    return return_data[2]