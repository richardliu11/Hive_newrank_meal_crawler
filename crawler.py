# 新站账号报价数据抓取 基于selenium
# -*- coding: utf-8 -*-
# Author : richard
# Date : 2022/5/26

from selenium import webdriver
import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import pandas as pd
import re
import os
import time

#
def pattern_return(pattern_str,target):#正则匹配方式
    '''
    :param pattern_str:
    :param html:
    :return:
    '''
    try:
        pattern = re.compile(pattern_str, re.S)
        items = re.findall(pattern, target)
        if len(items) <= 1:
            items = items[0]
    except:
        items = None
    return items

def browser_initial():
    """"
    浏览器初始化,并打开哔哩哔哩广告代理商系统界面（未登录状态）
    """
    os.chdir('D:\\项目\\newrank_crawler')
    browser = webdriver.Chrome()
    browser.get(
        'https://xz.newrank.cn/data/promotion/meal')#打开主页面
    browser.maximize_window()
    return browser




def log(browser):
    browser.find_element(By.XPATH, '//*[@id="__next"]/main/div/div[1]/div[2]/div[1]/button/span').click()
    time.sleep(15)#强制等待15秒 扫码登录
    print('登录成功')


def live_click_event(browser):
    """
    系列点击事件进入数据需求目标页
    """
    # 进入目标页面：
    # 点击事件：各条件筛选
    # zone_list = ['2','3','4','5','7','10','12','19','21']#曹老师需要的9个分区
    zone_list=['21']# 这里输入要抓取的分区编码


    for j in range(0, len(zone_list), 1):

        zone = browser.find_element(By.XPATH, '//*[@id="scrollLayoutContent"]/div/div[2]/div[1]/div[2]/span['+str(zone_list[j])+']').text
        print('正在爬取:',zone,'分区')

        # 点击”xx“分区标签
        browser.find_element(By.XPATH, '//*[@id="scrollLayoutContent"]/div/div[2]/div[1]/div[2]/span['+str(zone_list[j])+']').click()  #点击XX分区（筛选）
        #browser.refresh()
        time.sleep(1)

        result1 = browser.find_element(By.XPATH,'/html/body/div/section/section/main/div/div[2]/div[6]/div[2]/div[3]/span').text

        print('该分区共： ',result1,' 条结果')

        if int(result1)>200 :
            # 执行高级筛选
            print('执行高级筛选')
            browser.find_element(By.XPATH,
                                 '//*[@id="scrollLayoutContent"]/div/div[2]/div[3]/div/div/div[3]/span').click()  # 筛选框
            time.sleep(1)
            browser.find_element(By.XPATH,
                                 '/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/span[2]').click()  # 播放数<1W
            browser.find_element(By.XPATH,
                                 '/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/span[3]').click()  # 播放数1-5W
            browser.find_element(By.XPATH,
                                 '/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/span[4]').click()  # 播放数5-10W
            browser.find_element(By.XPATH,
                                 '/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/span[7]').click()  # 播放数>100W
            browser.find_element(By.XPATH,
                                 '/html/body/div[2]/div/div[2]/div/div[2]/div/div[4]/div[2]/button[2]/span').click()  # 点击确定
            time.sleep(1)

            result2 = browser.find_element(By.XPATH,
                                          '/html/body/div[1]/section/section/main/div/div[2]/div[6]/div[2]/div[4]/span').text  # 筛选结果数
            result1=result2
            time.sleep(1)

        data_list = []  # 创建一个存储数据的空列表

        for i in range(2, int(result1) + 1, 1):
            print('正在爬取第 ', str(i - 1), '条', ';', '共', str(result1), '条')

            # 获取标题
            title = browser.find_element(By.XPATH,
                                         '/html/body/div/section/section/main/div/div[3]/div[1]/div/div/div/div/div[2]/table/tbody/tr[' + str(
                                             i) + ']/td[1]/div/div[2]/div[1]/div[1]').text

            author = browser.find_element(By.XPATH,
                                          '/html/body/div/section/section/main/div/div[3]/div[1]/div/div/div/div/div[2]/table/tbody/tr[' + str(
                                              i) + ']/td[1]/div/div[2]/div[4]/span[1]/span[1]').text

            # 进入中间页
            browser.find_element(By.XPATH,
                                 '/html/body/div/section/section/main/div/div[3]/div[1]/div/div/div/div/div[2]/table/tbody/tr[' + str(
                                     i) + ']/td[1]/div/div[2]/div[1]/div[1]').click()  # 点击标题
            time.sleep(1)
            # 切换句柄
            # 获取打开的多个窗口句柄
            windows = browser.window_handles
            # 切换到当前最新打开的窗口
            browser.switch_to.window(windows[-1])
            # 点击UP主跳转至目标页2
            time.sleep(2)
            try:
                browser.find_element(By.XPATH, '/html/body/div/section/section/main/div[1]/div/div[1]/div[1]/div[2]/a/span').click()
            except:
                browser.find_element(By.XPATH, '/html/body/div/section/section/main/div[1]/div/div[2]/ul/li[1]/div[2]/div[1]/span/span/span[1]').click()




            time.sleep(2)

            # 进入目标页面2
            # 获取打开的多个窗口句柄
            windows = browser.window_handles
            # 切换到当前最新打开的窗口
            browser.switch_to.window(windows[-1])
            time.sleep(2)

            input_video = browser.find_element(By.XPATH,
                                               '//*[@id="scrollLayoutContent"]/div[1]/div/div[4]/div[2]/div[1]/div').text  # 植入视频价格（原始）
            input_video_price = pattern_return('￥(.*)', input_video)  # 正则匹配取出目标字段1

            custom_video = browser.find_element(By.XPATH,
                                                '//*[@id="scrollLayoutContent"]/div[1]/div/div[4]/div[2]/div[2]/div').text  # 定制视频价格（原始）
            custom_video_price = pattern_return('￥(.*)', custom_video)  # 正则匹配取出目标字段2

            direct_live = browser.find_element(By.XPATH,
                                               '//*[@id="scrollLayoutContent"]/div[1]/div/div[4]/div[2]/div[3]/div').text  # 直发动态价格（原始）
            direct_live_price = pattern_return('￥(.*)', direct_live)  # 正则匹配取出目标字段3

            forword_live = browser.find_element(By.XPATH,
                                                '//*[@id="scrollLayoutContent"]/div[1]/div/div[4]/div[2]/div[4]/div').text  # 转发动态价格（原始）
            forword_live_price = pattern_return('￥(.*)', forword_live)  # 正则匹配取出目标字段4

            browser.close()  # 关闭UP主页窗口

            time.sleep(1)
            # 获取打开的多个窗口句柄
            windows = browser.window_handles
            # 切换回视频窗口
            browser.switch_to.window(windows[-1])
            browser.close()

            # 获取打开的多个窗口句柄
            windows = browser.window_handles
            # 切换回主窗口
            browser.switch_to.window(windows[-1])
            # 滚动屏幕
            if i == 5:
                browser.execute_script('window.scrollBy(0,285)')  # 滚动浏览器（没有这一步数据加载不全）
            if i>=6:
                browser.execute_script('window.scrollBy(0,160)')  # 滚动浏览器（没有这一步数据加载不全）



            dic = dict(zip(['视频标题', 'UP主昵称', '植入视频', '定制视频', '直发动态', '转发动态', '分区'],
                           [title, author, input_video_price, custom_video_price, direct_live_price,
                            forword_live_price,zone]))
            data_list.append(dic)
            #print(data_list)
            print('第', str(i-1), '条抓取完成')


        browser.refresh() #每抓取完一个分区，刷新主页面
        time.sleep(3)#每个分区切换间 休眠3秒

        df = pd.DataFrame(data_list)
        filename = '新站恰饭视频数据_' + str(zone) +'_'+ time.strftime("%Y%m%d") + '.xlsx'#每抓取完一个分区；写出一次
        df.to_excel(filename, encoding='utf8')
        print('数据已写入本地')



if __name__ == "__main__":
    t1 = time.time()
    browser = browser_initial()  # 重置浏览器
    time.sleep(10)


    live_click_event(browser)  # 系列点击事件与投放记录至dic
    browser.quit()  # 关闭浏览器
    # 结束爬虫作业
    print('数据抓取完毕')
    print('模拟Chrome已关闭')
    t2 = time.time()
    print('本次抓取耗时:%s秒' % (t2 - t1))
