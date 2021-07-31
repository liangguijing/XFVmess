
import json

from utils import (
    bs64_decode,
    bs64_encode,
    get_unicode,
    get_server_location,
)


class Vmess:
    def __init__(self, subs):
        self.subs = subs
        self._config = {}

        self._get_vmess_config()

    @property
    def shared_link(self):
        """
        :return: vmess配置链接
        vmess://eyd2JzogJzInLCAncHMnOiAnXHU3ZjhlXHU1NmZkXHU2NWU3XHU5MAXxXHU1YzcxJywgJ2FkZCc6
                ICcxNTQuODQuMS46MTAnLCAncG9ydCc8ICc0NDMnLCAnaWQnOiAnNGUyZmM2ZTctNTZlNi00YTAy
                LTk5MTItYWZjNzU5M2NjOTllJywgJ2FpZCc6ICc2NCcsICduZXQnOiAnd3MnLCAndHlwZSc6ICdk
                dGxzJywgJ2hvc3Q1OiAnd3d3LjA5MjE5NzYzNTQueHl6JywgJ3BhdGgnOiAnL2Zvb3RlcnMnLCAn
                dGxzJzogJ3Rscyd9
        """
        return "vmess://" + bs64_encode(get_unicode(str(self._config).replace("'", '"')))

    @property
    def config(self):
        """
        :return: 服务器配置dict
                 {'v': '2', 'ps': 'US', 'add': '154.*.*.110', 'port': '443',
                  'id': '4e2fc6e7-56e6-4a02-9912-afc7593cc99e', 'aid': '64', 'net': 'ws',
                  'type': 'dtls', 'host': 'www.***.com', 'path': '/freess', 'tls': 'tls'}
        """
        return self._config

    @config.setter
    def config(self, v):
        #  修改dict用不上这个方法
        pass

    def _get_vmess_config(self):
        """
        通过分享链接获取Vmess配置
        """
        config = bs64_decode(self.subs[8:])  # vmess://...
        self._config = json.loads(config)
