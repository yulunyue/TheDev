import base64
import json
import hmac
import hashlib
import sys


def b64encode(s: bytes) -> str:
    s_bin = base64.urlsafe_b64encode(s)
    s_bin = s_bin.replace(b"=", b"")
    return s_bin.decode("ascii")


class EncDecUtil:
    def jws_encode(self, payload, key: str, alg="HS256"):
        header = dict()
        message = json.dumps(payload).encode("utf-8")
        header = dict(typ="JWT", alg=alg)
        header_b64 = b64encode(
            json.dumps(header, separators=(",", ":")).encode("ascii")
        )
        message_b64 = b64encode(message)
        signing_message = header_b64 + "." + message_b64
        signature = hmac.new(
            key.encode("utf-8"), signing_message.encode("ascii"), hashlib.sha256
        ).digest()
        signature_b64 = b64encode(signature)
        return signing_message + "." + signature_b64

    def test(self):
        pass

    def debug(self):
        import jwt

        ak = jwt.jwk.OctetJWK(b"a")
        jwt.JWT().encode(dict(a=1), ak)
        msg = self.jws_encode(dict(a=1), ak.key.decode())
        print(jwt.JWT().decode(msg, ak, do_verify=True))


if __name__ == "__main__":
    getattr(EncDecUtil(), sys.argv[1])()
