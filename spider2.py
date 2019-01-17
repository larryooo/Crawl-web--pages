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
    summary_info = soup.select('.col-md-6.col-xs-12')
    summary_info_str = summary_info[1].text
    blank_line = re.compile('\n+')
    summary_info_str = blank_line.sub('', summary_info_str)
    # print(summary_info_str)

    # 正文
    main_body = soup.select('.col-xs-12')
    main_content = main_body[7].text
    m_str = re.compile('\n+')
    main_content = m_str.sub('', main_content)
    # print(main_content)


    # write file
    if not os.path.exists('/maximum-security.txt'):
        content = 'title:'+title_str+'\nsummary_info:'+summary_info_str+'\nmain_content:'+main_content
        print(content)
        with open("maximum-security.txt", 'w') as f:
            f.write(content)


if __name__ == '__main__':
    getResponse('https://esupport.trendmicro.com/en-us/home/pages/technical-support/maximum-security/home.aspx')
