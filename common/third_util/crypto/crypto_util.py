from common.util.export import (
    is_base64_code,
    File,
    base64_encode,
    base64_decode,
    logger,
    sys,
)
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import pkcs12


def data_to_bin(cert_data):
    if is_base64_code(cert_data):
        cert_data = base64_decode(cert_data)
    if isinstance(cert_data, str):
        cert_data = cert_data.encode()
    return cert_data


class CryptoGraphy:
    def __init__(self, name="tmp"):
        self.name = name
        self.root_dir = File("data/cert/gen").make_dir_if_not_exist(True)
        self.cert: x509.Certificate = None

    def load_from_cert(self, cert_data: str):
        if isinstance(cert_data, (str, bytes)):
            cert_data = data_to_bin(cert_data)
            if b"-----BEGIN CERTIFICATE-----" in cert_data:
                self.cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            else:
                self.cert = x509.load_der_x509_certificate(cert_data, default_backend())
        else:
            self.cert = cert_data
        return self

    def load_from_pks12(self, data, password, **kw):
        pfx_data = data_to_bin(data)
        if isinstance(password, str):
            password = password.encode()
        private_key, certificate, additional_certificates = (
            pkcs12.load_key_and_certificates(pfx_data, password)
        )
        self.load_from_cert(certificate)
        # private_key 和 certificate 就是你要的私钥和证书对象
        return self

    def load_from_jks(self, data: str, password: str, key_password=None):
        import jks
        import base64

        data = data_to_bin(data)
        jks_file = self.root_dir.child(f"{self.name}.jks")
        jks_file.write_file(data)
        logger.info(jks_file)
        ks = jks.KeyStore.load(jks_file.path, password)

        # 2. 遍历所有私钥条目
        for alias, pk in ks.private_keys.items():
            print(f"找到私钥条目: {alias}")

            # 如果密钥密码与文件密码不同，需要解密
            if key_password and key_password != password:
                pk.decrypt(key_password)
            else:
                pk.decrypt(password)

            # 3. 提取私钥并保存为PEM文件
            key_file = self.root_dir.child(f"{self.name}_{alias}.key")
            if pk.algorithm_oid == jks.util.RSA_ENCRYPTION_OID:
                private_key_pem = f"-----BEGIN RSA PRIVATE KEY-----\n{base64.encodebytes(pk.pkey).decode('ascii')}-----END RSA PRIVATE KEY-----"
            else:
                private_key_pem = f"-----BEGIN PRIVATE KEY-----\n{base64.encodebytes(pk.pkey_pkcs8).decode('ascii')}-----END PRIVATE KEY-----"
            key_file.write_file(private_key_pem)
            print(f"私钥已保存至: {key_file}")

            # 4. 提取证书链并保存为PEM文件
            cert_file = self.root_dir.child(f"{self.name}_{alias}_cert.pem")
            pem_cert = ""
            for cert in pk.cert_chain:
                pem_cert += f"-----BEGIN CERTIFICATE-----\n{base64.encodebytes(cert.cert).decode('ascii')}-----END CERTIFICATE-----\n"
            cert_file.write_file(pem_cert)
            print(f"证书链已保存至: {cert_file}")
        return self

    def to_json(self):
        return dict(
            Subject=self.cert.subject.rfc4514_string(),
            Issuer=self.cert.issuer.rfc4514_string(),
            Serial=format(self.cert.serial_number, "X"),
            Version=self.cert.version.name,
            Valid_from=str(self.cert.not_valid_before),
            Valid_until=str(self.cert.not_valid_after),
        )


if __name__ == "__main__":
    f = File("data/tmp/tmp.json").write_if_not_exists(dict(data="", password=""))
    logger.info(f)
    print(CryptoGraphy().load_form_pks12(**f.read_file()).to_json())
