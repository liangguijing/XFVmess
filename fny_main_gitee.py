# -*- coding: utf-8 -*-
"""
github action
"""
import base64
import requests
import time

from requests import Session


def get_gitee_file_sha(url):
    """
    https://gitee.com/api/v5/repos/{owner}/{repo}/contents(/{path})
    :param url:
    :return:
    """
    url = url
    headers = {
        "accept": "application/json",
        "charset": "UTF-8",
    }
    response = requests.get(url, headers=headers, timeout=10).json()
    if response.get("sha"):
        return response["sha"]


def update_github_file(token, url, string):
    url = url
    headers = {
        "accept": "application/json",
        "charset": "UTF-8",
    }
    data = {
        "access_token": token,
        "content": base64.b64encode(string.encode("utf-8")).decode("utf-8"),
        "message": time.asctime(),
        "sha": get_gitee_file_sha(url)
    }
    resp = requests.put(url=url, headers=headers, json=data, timeout=10)
    if resp.status_code == 200:
        print(f"{ url } updated.")
    else:
        print(f"update { url }  failed! code: { resp.status_code }. text: { resp.text }")


def get_subscribe_content():
    session = Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                                    "(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    # 先获取cookie
    session.get("https://feiniaoyun.xyz/", timeout=10)
    username = get_username()
    data = {
        "email": f"{username}@gmail.com",
        "password": f"{username}",
        "invite_code": "",
        "email_code": "",
    }
    # 注册
    resp = session.post("https://feiniaoyun.xyz/api/v1/passport/auth/register", data=data, timeout=10)
    print(resp.text)
    # 获取订阅链接
    resp = session.get("https://feiniaoyun.xyz/api/v1/user/getSubscribe", timeout=10)
    print(resp.json())
    subscribe_url = resp.json()["data"]["subscribe_url"]
    print("sub url:", subscribe_url)
    resp = session.get(subscribe_url)
    # resp = requests.get(subscribe_url, headers={"User-Agent": "Clash"})
    return resp.text


def get_username():
    ts = str(int(time.time()))
    name = ts + "Robot" + ts[-3:]
    return name


def main():
    _token = input()

    clash_url = "https://gitee.com/api/v5/repos/liangguijing/plain-text/contents/clash1"
    content = get_subscribe_content()
    update_github_file(_token, clash_url, content)

    clash_url = "https://gitee.com/api/v5/repos/liangguijing/plain-text/contents/clash2"
    content = get_subscribe_content()
    update_github_file(_token, clash_url, content)

    print("End", time.asctime())


if __name__ == "__main__":
    main()
