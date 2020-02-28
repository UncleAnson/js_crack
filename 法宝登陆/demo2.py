#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/28 1:17 下午
# @Author  : Anson
# @Contact : 1047053860@qq.com
# @Software: PyCharm
# @content :


import asyncio
import time, random
from pyppeteer.launcher import launch  # 控制模拟浏览器用


async def main(username, pwd, url):  # 定义main协程函数，
    # 以下使用await 可以针对耗时的操作进行挂起
    browser = await launch({'headless': False, 'args': ['--no-sandbox'], })  # 启动pyppeteer 属于内存中实现交互的模拟器
    page = await browser.newPage()  # 启动个新的浏览器页面
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')

    await page.goto(url)  # 访问登录页面
    # 替换淘宝在检测浏览时采集的一些参数。
    # 就是在浏览器运行的时候，始终让window.navigator.webdriver=false
    # navigator是windiw对象的一个属性，同时修改plugins，languages，navigator 且让
    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')  # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

    # 使用type选定页面元素，并修改其数值，用于输入账号密码，修改的速度仿人类操作，因为有个输入速度的检测机制
    # 因为 pyppeteer 框架需要转换为js操作，而js和python的类型定义不同，所以写法与参数要用字典，类型导入
    await page.type('.J_UserName', username, {'delay': input_time_random() - 50})
    await page.type('#J_StandardPwd input', pwd, {'delay': input_time_random()})

    # await page.screenshot({'path': './headless-test-result.png'})    # 截图测试
    time.sleep(2)

    # 检测页面是否有滑块。原理是检测页面元素。
    slider = await page.Jeval('#nocaptcha', 'node => node.style')  # 是否有滑块

    if slider:
        print('当前页面出现滑块')
        await page.screenshot({'path': './headless-login-slide.png'})  # 截图测试
        flag, page = await mouse_slide(page=page)  # js拉动滑块过去。
        if flag:
            await page.keyboard.press('Enter')  # 确保内容输入完毕，少数页面会自动完成按钮点击
            print("print enter", flag)
            await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')  # 如果无法通过回车键完成点击，就调用js模拟点击登录按钮。

            time.sleep(2)
            # cookies_list = await page.cookies()
            # print(cookies_list)
            await get_cookie(page)  # 导出cookie 完成登陆后就可以拿着cookie玩各种各样的事情了。
    else:
        await page.keyboard.press('Enter')
        print("print enter")
        # 需要调用page.waitForNavigation()等待页面跳转完毕
        await page.waitForNavigation()
        # await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')  # <<
        # await page.waitForNavigation()

        try:
            global error  # 检测是否是账号密码错误
            print("error_1:", error)
            error = await page.Jeval('.error', 'node => node.textContent')
            print("error_2:", error)
        except Exception as e:
            error = None
        finally:
            if error:
                print('确保账户安全重新入输入')
                # 程序退出。
                loop.close()
            else:
                print(page.url)
                cookies = await get_cookie(page)
                print(cookies)
        time.sleep(5)
        await page.screenshot({'path': './headless-login-success.png'})  # 截图测试


# 获取登录后cookie
async def get_cookie(page):
    # res = await page.content()
    cookies_list = await page.cookies()
    cookies = ''
    for cookie in cookies_list:
        str_cookie = '{0}={1};'
        str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        cookies += str_cookie
    return cookies


def retry_if_result_none(result):
    return result is None


async def mouse_slide(page=None):
    await asyncio.sleep(2)
    try:
        # 鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
        await page.hover('#nc_1_n1z')  # 不同场景的验证码模块能名字不同。
        await page.mouse.down()
        await page.mouse.move(2000, 0, {'delay': random.randint(1000, 2000)})
        await page.mouse.up()
    except Exception as e:
        print(e, ':验证失败')
        return None, page
    else:
        await asyncio.sleep(2)
        # 判断是否通过
        slider_again = await page.Jeval('.nc-lang-cnt', 'node => node.textContent')
        if slider_again != '验证通过':
            return None, page
        else:
            # await page.screenshot({'path': './headless-slide-result.png'}) # 截图测试
            print('验证通过')
            return 1, page


def input_time_random():
    return random.randint(100, 151)


if __name__ == '__main__':
    username = 'xxxxx'  # 淘宝用户名
    pwd = 'xxxxx'  # 密码
    url = 'https://login.taobao.com/member/login.jhtml?style=mini&css_style=b2b&from=b2b&full_redirect=true&redirect_url=https://login.1688.com/member/jump.htm?target=https://login.1688.com/member/marketSigninJump.htm?Done=http://login.1688.com/member/taobaoSellerLoginDispatch.htm&reg= http://member.1688.com/member/join/enterprise_join.htm?lead=http://login.1688.com/member/taobaoSellerLoginDispatch.htm&leadUrl=http://login.1688.com/member/'
    loop = asyncio.get_event_loop()  # 协程，开启个无限循环的程序流程，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。
    loop.run_until_complete(main(username, pwd, url))  # 将协程注册到事件循环，并启动事件循环
    '''
    _nk_=156yp3321;isg=BGVlUBdlVzwUy7PgED4tLdArdCefohk0IipDFWdKIRyrfoXwL_IpBPOcCOMI5THs;lid=156yp3321;sg=149;lc=Vyu3p7spYtxSgRzLWdY%3D;uc4=nk4=0%40UOxwmw8zuCPVAVvO%2BvgLWcqN0%2Bg%3D&id4=0%40UOEy1an8UFoCv0IZXpAIAJM1EHSU;skt=7058ef0aad6963aa;dnk=156yp3321;cookie17=UonYssURj5qbjA%3D%3D;csg=680c13c4;tg=0;_cc_=VFC%2FuZ9ajQ%3D%3D;_tb_token_=3bea6eb5e4b4d;uc3=vt3=F8dBxd31Y7He3pXKU1M%3D&nk2=UoTaUW59hUsd&lg2=URm48syIIVrSKA%3D%3D&id2=UonYssURj5qbjA%3D%3D;cna=0bXfFvdtlncCAdoRcL8OgNh5;existShop=MTU4Mjg3NjYzNQ%3D%3D;t=3cb050373552b3cb42840c56a748df22;tfstk=cSjCBdO_Y_INK9AQQwww4Zw0wQtRwLnBQJOGdNsU0K8HbI1mFmRcUVBo6ouJC;lgc=156yp3321;log=lty=Ug%3D%3D;l=dBIvi5i7QhLTAmQ2BOCwC4Y6gWQOSIRYYukkCZIJi_5Qp6T_aIQOoRB3MF96VjXft7TBq2FvhwJ9-etbZ7DmndIpXUJ6CxDc.;_l_g_=Ug%3D%3D;uc1=cookie15=WqG3DMC9VAQiUQ%3D%3D&cookie21=Vq8l%2BKCLjhS4UhJVbhgU&lng=zh_CN&tag=8&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&pas=0&cookie14=UoTUOLtXfHN7vg%3D%3D&existShop=false;_samesite_flag_=true;unb=1833961034;sgcookie=DCByTlQ3KSOA1aSDK7Ww7;cookie1=VAMTIBHn32nI5fYqo%2FqSOoD0tFkN%2Bl3sHEjzp6eDgHo%3D;tracknick=156yp3321;cookie2=1e4f2f6ab2390e5da6e31965f0d634d5;_uab_collina=158287661067987999612624;
    '''