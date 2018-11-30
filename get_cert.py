# coding: utf8
# Author:xuyang.li
# Date:2018/11/24
"""
   Get Root CA, generate key and apply a certificate 
"""
import ConfigParser

import requests
from OpenSSL import crypto

from enosapi.client.EnOSDefaultClient import EnOSDefaultClient
from enosapi.request.ApplyCertificateByDeviceKeyRequest import ApplyCertificateByDeviceKeyRequest


def get_root_cert(url):
    r = requests.get(url)
    r.raise_for_status()
    return r.content


def get_subject_msg(cert):
    sub = cert.get_subject()
    return sub.C, sub.ST, sub.O, sub.L, sub.OU, sub.CN


def get_csr_req():
    req = crypto.X509Req()
    return req


def is_empty_str(string):
    return string is None or string == ""


def fill_req(req, cert, conf, PKey):
    C, ST, O, L, OU, CN = get_subject_msg(cert)
    subject = req.get_subject()
    subject.C = C
    subject.ST = ST
    subject.O = O

    subject.L = L if (is_empty_str(conf.get("option", "LOCATION"))) else conf.get("option", "LOCATION")
    subject.OU = OU if (is_empty_str(conf.get("option", "OU"))) else conf.get("option", "OU")
    subject.CN = conf.get("required", "CN")

    req.set_pubkey(PKey)
    req.sign(PKey, "sha256")


def write_file(file_name, context):
    f = open(file_name, 'w')
    f.write(context)


def get_private_key(public_key, password):
    cipher = None
    password = password
    passphrase = None

    called = []

    def cb(writing):
        called.append(writing)
        return password

    if not is_empty_str(password):
        passphrase = cb
        cipher = "blowfish"

    return crypto.dump_privatekey(crypto.FILETYPE_PEM, public_key, cipher=cipher, passphrase=passphrase)


if __name__ == '__main__':
    print "start create key and certificate "

    cf = ConfigParser.ConfigParser()
    cf.read("get_cert.ini")

    root_cert_str = get_root_cert(cf.get("required", "root_cert_url"))
    write_file("edge_ca.pem", root_cert_str)
    root_cert = crypto.load_certificate(crypto.FILETYPE_PEM, root_cert_str)

    public_key = crypto.PKey()
    public_key.generate_key(crypto.TYPE_RSA, 2048)

    private_key = get_private_key(public_key, cf.get("option", "password"))
    write_file("edge.key", private_key)

    csr_req = get_csr_req()
    fill_req(csr_req, root_cert, cf, public_key)

    req_str = crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr_req)
    csr = '\"' + req_str.replace("\n", "\\n") + '\"'

    request = ApplyCertificateByDeviceKeyRequest(org_id=cf.get("required", "org_id"),
                                                 product_key=cf.get("required", "product_key"),
                                                 device_key=cf.get("required", "device_key"),
                                                 csr=csr)

    client = EnOSDefaultClient(cf.get("required", "api_url"),
                               cf.get("required", "app_key"),
                               cf.get("required", "app_secret"))

    response = client.execute(request)

    if response.is_success():
        write_file("edge.pem", response.data['cert'])
    else:
        raise RuntimeError(response.msg)

    print "finish  create key and certificate"
