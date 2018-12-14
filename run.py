# -*- coding:utf-8 -*-
import requests
import re
import logging
import gevent


class GaoDe():

    def __init__(self, addr_name):
        self.addr_name = addr_name
        self.url = "https://www.amap.com/service/poiInfo"
        self.params = {"query_type": "TQUERY",
                     "keywords": addr_name
                    }
        with open("./input/run.conf") as f:
            content = f.read()
            cookie = eval(content)["cookie"]
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": cookie,
            "Host": "www.amap.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36 }"
        }
        logging.basicConfig(
            level=logging.DEBUG,
            filename="./log.txt",
            filemode="a",
            format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
        )
        self.name_infos = list()

    def get_index(self):
        session = requests.Session()
        response = session.get(self.url, params=self.params, headers=self.headers, timeout=10)
        content = response.text
        print(content)
        longitude = re.search(r"\"longitude\":\"(.*?)\"", content, re.S)
        latitude = re.search(r"\"latitude\":\"(.*?)\"", content, re.S)
        if longitude and latitude:
            self.save_info(longitude.group(1), latitude.group(1))
        else:
            logging.info("not found the index of city: [%s]" % self.addr_name)

    def duplication(self):
        """
        去重处理
        :return:是否有重复, True表示有重复
        """
        try:
            with open("./output/infos.txt", "rb") as f:
                lines = f.readlines()
        except:
            with open("./output/infos.txt", "w"):
                logging.info("creat new file: infos.txt")
                return False
        else:
            for line in lines:
                ret = eval(str(line.decode("utf-8")))
                self.name_infos.append(ret["city"])

        if self.addr_name in self.name_infos:
            logging.debug("value of the key 'city' is duplication: %s" % self.addr_name)
            return True
        else:
            return False

    def save_info(self , longitude, latitude):
        duplicate_ret = self.duplication()
        if not duplicate_ret:
            with open("./output/infos.txt", "a", encoding="utf-8") as f:
                f.write("{'city':'" + self.addr_name + "', 'longitude':'" + longitude + "', 'latitude':'" + latitude + "'}\n")
                logging.debug("save successful: %s[%s,%s]" % (self.addr_name, longitude, latitude))


def get_city():
    """获得地址名称，以生成器形式返回"""
    try:
        with open("./input/city_names.txt", "r") as f:
            city_names = f.read()
            logging.info("read file successful: city_names.txt")
    except Exception as e:
        with open("./input/city_names.txt", "w"):
            logging.info("create new file: city_names.txt")
    else:
        names = city_names.split(",")
        names_len = len(names)
        for i in range(names_len):
            re_name = "\"%s\"" % names[i]
            names[i] = re.sub(r".*", re_name, names[i])
        text = ",".join(names)
        text = list(eval(text))

        if len(text):
            i = 0
            while i < len(text):
                ret = text[i]
                yield ret
                i += 1
        else:
            return False


def create_object(city):
    """创建GaoDe对象"""
    g = GaoDe(city)
    g.get_index()


def main():
    city = get_city()
    while True:
        if get_city():
            try:
                g = gevent.spawn(create_object, city.__next__())
                g.start()
                g.join()
            except StopIteration:
                print("数据读取完毕")
                break
        else:
            city = input("文件中没有数据，请输入要查询的地点:")
            create_object(city)
            break


if __name__ == '__main__':
    main()
