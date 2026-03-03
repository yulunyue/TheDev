from common.third_util.crypto.crypto_util import CryptoGraphy
from common.util.export import Node, b64_code, File, file_cls


class Util:
    API_ROUTE = "/app/util"

    def cert_dump(self, data: str, **kw):
        return Node(value=CryptoGraphy().load_from_data(data))

    def b64_code(self, code: str, **kw):
        return Node(value=b64_code(code))

    def restart(self, path: str):
        f = File(path)
        f.unzip("./")
        return Node()
