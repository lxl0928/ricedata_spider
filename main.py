# coding: utf-8

"""
# 说明
ricedata.cn的某个列表页面的爬虫


url: http://www.ricedata.cn/gene/accessions_switch.aspx?p={}&cloned=true

# 数据结构
data = {
    "title": ["GeneID", "基因名称或注释", "基因符号", "RAP_Locus", "MSU_Locus", "cDNAs", "RefSeq_Locus", "Uniprots"]
    "page_1": [
        ["2515", "窄叶基因;WUSCHEL相关的同源框基因", "NAL3; OsWOX3A", "Os12g0101600", "LOC_Os12g01120", "AB218893", "XM_015764119→XP_015619605", ''],
        ["2516", "窄叶基因;WUSCHEL相关的同源框基因", "NAL3; OsWOX3A", "Os12g0101600", "LOC_Os12g01120", "AB218893", "XM_015764119→XP_015619605", ''],
        ["2517", "窄叶基因;WUSCHEL相关的同源框基因", "NAL3; OsWOX3A", "Os12g0101600", "LOC_Os12g01120", "AB218893", "XM_015764119→XP_015619605", ''],
        ...
    ],
    "page_2": [
        ["2518", "窄叶基因;WUSCHEL相关的同源框基因", "NAL3; OsWOX3A", "Os12g0101600", "LOC_Os12g01120", "AB218893", "XM_015764119→XP_015619605", ''],
        ["2519", "窄叶基因;WUSCHEL相关的同源框基因", "NAL3; OsWOX3A", "Os12g0101600", "LOC_Os12g01120", "AB218893", "XM_015764119→XP_015619605", ''],
        ["2510", "窄叶基因;WUSCHEL相关的同源框基因", "NAL3; OsWOX3A", "Os12g0101600", "LOC_Os12g01120", "AB218893", "XM_015764119→XP_015619605", ''],
        ...
    ],
    ...
}
"""

import json
import urllib.request
from datetime import datetime
from collections import OrderedDict

from lxml import etree
from pyexcel_xls import save_data


cnt_now = datetime.now()
cnt_time = "{}{}{}{}{}".format(cnt_now.year, cnt_now.month, cnt_now.day, cnt_now.hour, cnt_now.minute)

url = "http://www.ricedata.cn/gene/accessions_switch.aspx?p={}&cloned=true"
user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
headers = {"User-Agent": user_agent}

result_path = "./doc/{}.xlsx".format(cnt_time)
xls_data = OrderedDict()
result_biao = []

# 存储目标数据结构
result_data = dict()

# 确定每列的标题
result_data['title'] = ["GeneID", "基因名称或注释", "基因符号", "RAP_Locus", "MSU_Locus", "cDNAs", "RefSeq_Locus", "Uniprots"]

for page in range(1, 96):
    """ 该url一共95页，页码是: 1~95
    """

    # 存储每页的数据
    page_data = list()

    try:
        # 爬取每页数据
        response = urllib.request.urlopen(url.format(page))
        html = response.read()  # 获取到页面的源代码

        new_html = etree.HTML(html.decode("utf-8"))
        tr_elements = new_html.xpath('//tr')
    except Exception as e:
        print("\n\n\n", url.format(page), "爬取失败, 失败原因: {}".format(e), "\n\n\n")
        continue

    for i in range(3, len(tr_elements)):
        # 第1, 2 tr是无效数据，剔除, 最后一个tr也是无效数据, 剔除
        """ 注意Chrome 浏览器通过 inspect -> copy -> copy Xpath得到的如下Xpath, 需要去掉'/tbody'部分
        //*[@id="TBResult"]/tbody/tr[3]/td[1]/a
        //*[@id="TBResult"]/tbody/tr[3]/td[2]
        //*[@id="TBResult"]/tbody/tr[3]/td[3]/em
        //*[@id="TBResult"]/tbody/tr[3]/td[4]/a
        //*[@id="TBResult"]/tbody/tr[3]/td[5]/a
        //*[@id="TBResult"]/tbody/tr[3]/td[6]/a
        //*[@id="TBResult"]/tbody/tr[3]/td[7]
        //*[@id="TBResult"]/tbody/tr[3]/td[8]/a
        """
        try:
            tr_data = list()
            td_1 = new_html.xpath('//*[@id="TBResult"]/tr[{}]/td[1]/a'.format(i))[0].text
            td_2 = new_html.xpath('//*[@id="TBResult"]/tr[{}]/td[2]'.format(i))[0].text

            td_3 = new_html.xpath('//*[@id="TBResult"]/tr[{}]/td[3]/em'.format(i))
            td_3_latest = td_3[0].text if td_3 else ''

            td_4 = new_html.xpath('//*[@id="TBResult"]/tr[{}]/td[4]/a'.format(i))
            td_4_latest = td_4[0].text if td_4 else ''

            td_5 = new_html.xpath('//*[@id="TBResult"]/tr[{}]/td[5]/a'.format(i))
            td_5_latest = td_5[0].text if td_5 else ''

            td_6 = new_html.xpath('//*[@id="TBResult"]/tr[{}]/td[6]/a'.format(i))
            td_6_latest = td_6[0].text if td_6 else ''

            td_7 = new_html.xpath('//*[@id="TBResult"]/tr[{}]/td[7]/a'.format(i))
            td_7_0 = td_7[0].text if td_7 else ''
            td_7_1 = td_7[1].text if td_7 and len(td_7) == 2 else ''
            td_7_latest = td_7_0 + "->" + td_7_1 if td_7 and td_7_1 else td_7_0

            td_8 = new_html.xpath('//*[@id="TBResult"]/tr[{}]/td[8]/a'.format(i))
            td_8_latest = td_8[0].text if td_8 else ''

            tr_data_list = [int(td_1), td_2, td_3_latest, td_4_latest, td_5_latest, td_6_latest if td_6_latest else '', td_7_latest, td_8_latest if td_8_latest else '']
            tr_data.extend(tr_data_list)
        except Exception as e:
            print("\n\n\n", url.format(page), "tr: {}".format(i), "爬取失败, 失败原因: {}".format(e), "\n\n\n")
            continue

        page_data.append(tr_data)

    print("crawling ", url.format(page), "       success.")
    result_data['page_{}'.format(page)] = page_data


# 存储爬取结果进json文件
with open("./json_data/{}.json".format(cnt_time), "w+") as fp:
    fp.write(json.dumps(result_data))
    print("\n\n\nwrite json success.")

# 读取json文件
with open("./json_data/{}.json".format(cnt_time), "r+") as fp:
    json_data = json.loads(fp.read())
    print("\n\n\nread json success.")


result_biao.append(json_data['title'])

for page in range(1, 96):
    page_data = json_data["page_{}".format(page)]
    for tr in page_data:
        result_biao.append(tr)
        print("page_{}: ".format(page), tr)
    print("\n")

xls_data.update({u"sheet1": result_biao})
save_data(result_path, xls_data)

print("\n\n\nsave {} success.".format(result_path))
