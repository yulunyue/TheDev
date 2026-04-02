from common.util.export import (
    is_base64_code,
    File,
    base64_encode,
    base64_decode,
    logger,
)
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import sys


class CryptoGraphy:
    def __init__(self):
        self.root_dir = File("data/cert/gen")

    def load_from_cert(self, cert_data: str):
        if is_base64_code(cert_data):
            cert_data = base64_decode(cert_data)
        if isinstance(cert_data, str):
            cert_data = cert_data.encode()
        try:
            if b"-----BEGIN CERTIFICATE-----" in cert_data:
                self.cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            else:
                self.cert = x509.load_der_x509_certificate(cert_data, default_backend())
        except Exception as e:
            raise Exception(e, cert_data[:100])
        return self

    def load_from_jks(self, data: str, password: str):
        pass

    def to_json(self):
        return dict(
            Subject=self.cert.subject.rfc4514_string(),
            Issuer=self.cert.issuer.rfc4514_string(),
            Serial=format(self.cert.serial_number, "X"),
            Version=self.cert.version.name,
            Valid_from=str(self.cert.not_valid_before_utc),
            Valid_until=str(self.cert.not_valid_after_utc),
        )


if __name__ == "__main__":
    print(CryptoGraphy().load_from_data("").to_json())
