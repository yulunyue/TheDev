from common.third_util.crypto.crypto_util import CryptoGraphy
from common.util.export import Node, b64_code, File
from common.tool.export import DomFile, FrontTable


class Util:

    def cert_dump(self, data: str, **kw):
        return CryptoGraphy().load_from_cert(data)

    def jks_pks12_dump(self, data: str, password: str, **kw):
        return CryptoGraphy().load_from_pks12(data, password)

    def b64_code(self, code: str, **kw):
        return Node(value=b64_code(code))
