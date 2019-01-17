import requests
import re
from bs4 import BeautifulSoup
import os


def getResponse(url):

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    # 标题
    title_str = ''
    title_list = soup.select('.product-title-container.container.title-container h1')
    for title in title_list:
        str = '%s'%title
        res_tr = r'<h1>(.*?)</h1>'
        m_tr = re.findall(res_tr, str, re.S | re.M)
        title_str = ''.join(m_tr)

    # 摘要
    summary = ''
    summary_info = soup.select('.col-md-6.col-xs-12')
    summary_info_list = summary_info[1]
    re_str = r'<\w.?>(.*?)</\w.?>'
    re_pattern = r'<\w.*>?'
    for info in summary_info_list:
        str1 = '%s'%info
        m_str = re.findall(re_str, str1, re.S | re.M)
        summary_str = ''.join(m_str)  # 有多余的a标签  str
        summary_info_list1 = re.findall(re_pattern, summary_str, re.S | re.M)
        summary_info_str = ''.join(summary_info_list1)
        summary = summary + summary_str.replace(summary_info_str, '')  # 无多余的a标签  str

    # 正文
    main_content = ''
    main_body = soup.select('.col-xs-12')
    p = re.compile("<[^>]+>|\n+|MainTab|Setup|Subscription")
    for i in main_body[6]:
        str = '%s' % i
        main_body_str = p.sub("", str)
        if len(main_body_str) == 0:
            continue
        main_content = main_content + main_body_str

    # write file
    if not os.path.exists('mobile-security-for-ios.txt'):
        content = 'title:'+title_str+'\nsummary_info:'+summary+'\nmain_content:'+main_content
        with open("mobile-security-for-ios.txt", 'w') as f:
            f.write(content)


if __name__ == '__main__':
    getResponse('https://esupport.trendmicro.com/en-us/home/pages/technical-support/mobile-security-for-ios/home.aspx')
