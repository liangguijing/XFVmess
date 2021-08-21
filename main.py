
import base64
import requests
import time
import yaml

from Crypto.Cipher import AES
from utils import bs64_encode, country_mapping, get_server_location, update_github_file
from vmess import Vmess


UPDATE_GITHUB = True
CLASH_URL = "https://api.github.com/repos/liangguijing/XFVmess/contents/subscriptions/clash.yml"
QUANTUMULT_URL = "https://api.github.com/repos/liangguijing/XFVmess/contents/subscriptions/quantumult.txt"
V2RAY_URL = "https://api.github.com/repos/liangguijing/XFVmess/contents/subscriptions/v2ray.txt"


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
    vmess_links = []
    clash_links = {}
    for v in links:
        vmess = Vmess(v)
        alias = get_server_location(vmess.config["add"])  # "Netherlands-46.18.10.27"
        emoji = country_mapping.get(alias.split("-")[0], "")
        alias = f"{emoji}{alias} {str(vmess.config['ps'])}"  # "Netherlands-46.18.10.27 188"
        vmess.config["ps"] = alias
        vmess_links.append(vmess.shared_link)

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
    # 保存vmess for v2ray
    with open("subscriptions/v2ray.txt", "w", encoding="utf-8") as f:
        v2ray = "\n".join(v for v in sorted(vmess_links))
        f.write(v2ray)
        print("文件v2ray.txt保存成功！")

    # 保存clash for clash
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
    with open("subscriptions/clash.yml", encoding="utf-8", mode="w") as f:
        yaml.dump(data, f, allow_unicode=True)
        clash_yaml = yaml.dump(data, allow_unicode=True)
        print("文件clash.yml保存成功！")

    # 保存Quantumult for ios quantumult
    # ** ios \r为换行 **  改\n
    # +要替换为-
    # [SERVER] 格式
    # 🇺🇸 United States-142.0.136.171-328 = vmess, 142.0.136.171, 443, chacha20-ietf-poly1305,
    # "3f2ed494-f7a0-4563-bba5-4ab42fde87e6", group=V2RayProvider, over-tls=true, tls-host=www.acc913.xyz,
    # certificate=1, obfs=ws, obfs-path="/footers", obfs-header="Host: www.acc913.xyz"
    qtm_configs = []
    ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 " \
         "(KHTML, like Gecko) Mobile/16A5366a"
    for vmess in vmess_links:
        vmess = Vmess(vmess)
        v_config = vmess.config
        add = v_config["add"]
        port = str(v_config["port"])
        scy = v_config.get("scy", "chacha20-ietf-poly1305")
        uid = v_config["id"]
        tls = "true" if v_config["tls"] == "tls" else "false"
        tls_host = v_config.get("host", v_config["add"])

        # 混肴选项
        obfs = "ws" if v_config["net"] == "ws" else "http"
        obfs_path = v_config.get("path", "/")
        obfs_header = f'"Host: { tls_host }"'
        # 取消ua
        # obfs_header += f"[Rr][Nn]User-Agent:{ ua }"
        qtm = [
            "vmess",
            f'{ add },{ port },{ scy },"{ uid }"',
            "group=V2RayProvider",
            f"over-tls={ tls }",
            f"tls-host={ tls_host }",
            "certificate=1",
        ]
        if v_config.get("type") and v_config["net"] == "ws":
            qtm.extend([
                f"obfs={ obfs }",
                f"obfs-path={ obfs_path }",
                f"obfs-header={ obfs_header }",
            ])
        qtm_config = v_config["ps"] + " = " + ", ".join(qtm)
        qtm_config = bs64_encode(qtm_config)
        qtm_config = "vmess://" + qtm_config.replace("+", "-").replace("=", "")  # 转换，不清楚
        qtm_configs.append(qtm_config)
    quantumult = "\n".join(qtm_configs)
    quantumult = bs64_encode(quantumult)
    with open("subscriptions/quantumult.txt", encoding="utf-8", mode="w") as f:
        f.write(quantumult)
        print("文件quantumult.txt保存成功！")

    # 更新github文件
    if UPDATE_GITHUB:
        token = input()
        update_github_file(token, CLASH_URL, clash_yaml)
        update_github_file(token, QUANTUMULT_URL, quantumult)
        update_github_file(token, V2RAY_URL, v2ray)
