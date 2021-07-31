
import base64
import requests
import time
import yaml

from Crypto.Cipher import AES
from utils import country_mapping, get_server_location
from vmess import Vmess


def aes_decrypt(text):
    """
    解密API返回的数据
    :param text:
    :return: vmess://..
    """
    key = b"awdtif20190619ti"
    iv = b"awdtif20190619ti"
    aes = AES.new(key, 2, iv)  # CBC
    dec = base64.decodebytes(text.encode("utf-8"))
    return aes.decrypt(dec).decode("utf-8").strip(b"\x00".decode())


def get_enc_text():
    """
    从API获取数据
    :return: 加密了的vmess链接
    """
    url = "https://www.jd7009724.xyz:20000/api/evmess"
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        print("从API获取数据出错:", e)
        return False


vmess_exp = {
    "add": "46.182.107.27",
    "aid": "64",
    "host": "www.59299999.xyz",
    "id": "3e016c4d-986e-42df-838c-6046f3d89ecf",
    "net": "ws",
    "path": "/footers",
    "port": 443,
    "ps": "Netherlands-46.182.107.27-426",
    "tls": "tls",
    "type": "dtls",
    "v": "2",
}

if __name__ == "__main__":
    links = set()
    for i in range(50):
        enc_text = get_enc_text()
        if not enc_text:  # 跳过API获取出错
            continue
        vmess = aes_decrypt(enc_text)
        links.add(vmess)
        time.sleep(0.1)
    print(f"已获取vmess链接:{len(links)}条")
    # 将备注改为"国家-IP 原来的编号"
    vmess_links = set()
    clash_links = {}
    for v in links:
        vmess = Vmess(v)
        alias = get_server_location(vmess.config["add"])  # "Netherlands-46.18.10.27"
        emoji = country_mapping.get(alias.split("-")[0], "")
        alias = f"{emoji}{alias} {str(vmess.config['ps'])}"  # "Netherlands-46.18.10.27 188"
        vmess.config["ps"] = alias
        vmess_links.add(vmess.shared_link)

        clash = {
            "name": vmess.config["ps"],
            "server": vmess.config["add"],
            "port": vmess.config["port"],
            "type": "vmess",
            "uuid": vmess.config["id"],
            "alterId": vmess.config["aid"],
            "cipher": vmess.config.get("scy", "auto"),
            "tls": True if vmess.config["tls"] == "tls" else False,
            "skip-cert-verify": False,
            "network": vmess.config["net"],
            "ws-path": vmess.config["path"],
            "ws-headers": {"Host": vmess.config["host"]}
        }
        clash_links.update({vmess.config["ps"]: clash})
    # 保存vmess
    with open("vmess.txt", "w", encoding="utf-8") as f:
        val = "\n".join(v for v in sorted(vmess_links))
        f.write(val)
        print("文件vmess.txt保存成功！")

    # 保存clash
    with open("base.yml", encoding="utf-8") as base:
        data = yaml.load(base, Loader=yaml.FullLoader)
    for name, clash in clash_links.items():
        if data["proxies"]:
            data["proxies"].append(clash)
        else:
            data["proxies"] = [clash]
        for grp in data["proxy-groups"]:
            if grp["proxies"]:
                grp["proxies"].append(name)
            else:
                grp["proxies"] = [name]
    with open("clash.yml", encoding="utf-8", mode="w") as f:
        yaml.dump(data, f, allow_unicode=True)
        print("文件clash.yml保存成功！")
