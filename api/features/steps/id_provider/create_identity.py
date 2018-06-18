import os
import pathlib
from typing import NamedTuple, NewType
import uuid

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import requests

PublicPEMKey = NewType('PublicKey', str)
KEY_STORE_PATH = './keys'
ID_PROVIDER_HOST = 'http://localhost:8100'

def create_identity(namespace: str, identifier: str, ial: float) -> requests.Response:
    pub_key = _create_internal_identity(namespace, identifier)
    request_payload = CreateIdentityRequest(
        namespace=namespace, 
        identifier=identifier,
        ial=ial,
        reference_id=_generate_reference_id(),
        accessor_type='RSA',
        accessor_public_key=pub_key,
        accessor_id='mock-idp'
    )

    return requests.post(ID_PROVIDER_HOST + '/identity', json=request_payload._asdict())


class CreateIdentityRequest(NamedTuple):
    namespace: str
    identifier: str
    reference_id: str
    accessor_type: str
    accessor_public_key: PublicPEMKey
    accessor_id: str
    ial: float


def _generate_reference_id() -> str:
    return str(uuid.uuid1())


def _create_internal_identity(namespace: str, identifier: str) -> PublicPEMKey:
    key_pair = _generate_key_pair()
    _save_key(namespace, identifier, key_pair)

    return str(key_pair.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    

def _generate_key_pair() -> rsa.RSAPrivateKey:
    return rsa.generate_private_key(public_exponent=65537, key_size=2048, 
                                    backend=default_backend())


def _save_key(namespace: str, identifier: str, key_pair: rsa.RSAPrivateKey):
    key_dir = pathlib.Path(KEY_STORE_PATH) / namespace / identifier
    os.makedirs(key_dir)

    with open(key_dir / 'id_rsa', 'wb') as f:
        key_binary = key_pair.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        f.write(key_binary)

    with open(key_dir / 'id_rsa.pub', 'wb') as f:
        key_binary = key_pair.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        f.write(key_binary)
