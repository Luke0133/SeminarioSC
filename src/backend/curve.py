# Using elliptic curve algorithm Ed25519 (EdDSA with Curve25519)
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography import exceptions

__relevant_hash = hashes.SHA3_512()


def generate_private_key() -> ec.EllipticCurvePrivateKey:
    """A wrapper function to generate an Elliptic Curve private key.

    Returns:
        ec.EllipticCurvePrivateKey: The private key that was generated
    """
    private_key = ec.generate_private_key(ec.SECP256R1())
    return private_key


def generate_public_key(privkey: ec.EllipticCurvePrivateKey) -> ec.EllipticCurvePublicKey:
    """A wrapper function to generate an Elliptic Curve public key.

    Args:
        privkey (ec.EllipticCurvePrivateKey): A previously generated private key.

    Returns:
        ec.EllipticCurvePublicKey: The public key that was generated
    """
    digest = hashes.SHA256()
    hasher = hashes.Hash(digest)
    dug = hasher.finalize()
    pubkey = privkey.public_key()
    return pubkey


def sign(key: ec.EllipticCurvePrivateKey, data_file) -> bytes:
    """ECDSA Signing for files. Uses SHA3-512 for hashing.

    Args:
        key (ec.EllipticCurvePrivateKey): Private key for signing
        data_file (File object): File that needs signing

    Returns:
        bytes: Signature
    """
    digest = __hash(data_file=data_file)

    # Generate signature
    signature = key.sign(
        digest,
        ec.ECDSA(utils.Prehashed(__relevant_hash))
    )

    return signature


def verify(key: ec.EllipticCurvePublicKey, data_file, signature: bytes) -> bool:
    """ECDSA Verification for files. Uses SHA3-512 for hashing.

    Args:
        key (ec.EllipticCurvePublicKey): Public key for verification
        data_file (File object): The file that needs verification
        signature (bytes): The signature that needs verification

    Returns:
        bool: False if verification failed, True if it's a valid signature
    """
    # Hashing file
    digest = __hash(data_file=data_file)

    try:
        key.verify(
            signature,
            digest,
            ec.ECDSA(utils.Prehashed(hashes.SHA3_512()))
        )
    except exceptions.InvalidSignature:
        return False
    return True


def serialize_private_key(key: ec.EllipticCurvePrivateKey, password: bytes) -> bytes:

    serialized_private = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password)
    )
    # clear password from memory
    for i in range(0, len(password)):
        password[i] = 0
    return serialized_private


def serialize_public_key(key: ec.EllipticCurvePublicKey) -> bytes:

    serialized_public = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password)
    )
    return serialized_public


def load_public_key(serialized_key_file) -> ec.EllipticCurvePublicKey:
    serialized_key_data = serialized_key_file.read()

    public_key = serialization.load_pem_public_key(
        serialized_key_data
    )
    return public_key


def load_private_key(serialized_key_file, password: bytes) -> ec.EllipticCurvePrivateKey:
    serialized_key_data = serialized_key_file.read()

    private_key = serialization.load_pem_private_key(
        serialized_key_data,
        password=password
    )
    return private_key


def __hash(data_file) -> bytes:
    """ Auxiliary hash function for curve module """
    data_file.seek(0)

    # Hashing file
    hasher = hashes.Hash(__relevant_hash)
    byte: bytes = data_file.read(1)
    while byte:
        hasher.update(byte)
        byte = data_file.read(1)
    digest = hasher.finalize()
    return digest
