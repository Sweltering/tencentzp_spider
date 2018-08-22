import requests
from lxml import etree

BASE_URL = 'https://hr.tencent.com/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    'Referer': 'https://hr.tencent.com/social.php'
}


# 爬取职位的url
def spider():
    page_url = 'https://hr.tencent.com/position.php?keywords=python&lid=0&tid=0&start={}'
    positions = []  # 存放职位url
    # 总共52页招聘职位
    for i in range(0, 53):
        pages = i * 10
        page_url = page_url.format(pages)  # 页面url

        # 发起职位页面请求
        response = requests.get(page_url, headers=HEADERS)
        html = etree.HTML(response.text)
        # 爬取每个职位的href
        url_positions = html.xpath('//tr[@class="even" or @class="odd"]//a/@href')
        for url in url_positions:
            position_url = BASE_URL+url
            get_position_info(position_url)


# 爬取职位信息
def get_position_info(url):
    positions = {}  # 存放职位信息

    response = requests.get(url, headers=HEADERS)
    html = etree.HTML(response.text)
    position_name = html.xpath('//td[@id="sharetitle"]/text()')
    tds = html.xpath('//tr[@class="c bottomline"]/td/text()')
    address = tds[0]  # 工作地点
    job_categories = tds[1]  # 职位类别
    nums = tds[2]  # 招聘人数
    infos = html.xpath('//td[@colspan="3"]//ul[@class="squareli"]')
    job_responsibilities = infos[0].xpath('.//text()')
    work_requirements = infos[1].xpath('.//text()')

    positions['职位'] = position_name
    positions['工作地点'] = address
    positions['职位类别'] = job_categories
    positions['招聘人数'] = nums
    positions['工作职责'] = job_responsibilities
    positions['工作要求'] = work_requirements

    print(positions)
    return positions


if __name__ == '__main__':
    spider()