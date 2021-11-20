from utils.components import Components


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

class Mule:
    def __init__(self, **kwargs):
        self.search: str = ""
        self.minPrice = 1
        self.maxPrice: int = None
        self.period: int = None

        if "search" in kwargs:
            self.search = kwargs["search"]
        if "minPrice" in kwargs:
            self.minPrice = kwargs["minPrice"]
        if "maxPrice" in kwargs:
            self.maxPrice = kwargs["maxPrice"]
        if "period" in kwargs:
            self.period = kwargs["period"]

    def template(self):
        content = self.search + "\n"
        content += "최소 가격: " + str(self.minPrice) + "원\n"
        content += "최대 가격: " + str(self.maxPrice) + "원\n"
        content += "기간: " + str(self.period) + "\n"

        components = Components()
        components.addActionRow(
            Components.make(type=2, label="최소 가격 설정", style=1, custom_id="mule_min_price"),
            Components.make(type=2, label="최대 가격 설정", style=1, custom_id="mule_max_price")
        )
        components.addActionRow(
            Components.make(type=2, label="검색", style=1, custom_id="mule_search")
        )

        payload = {}
        payload["content"] = content
        payload["components"] = components.get()
        return payload