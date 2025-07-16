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


def serialize_private_key(key: ec.EllipticCurvePrivateKey, password: bytearray) -> bytes:
    """Serialization for Elliptic Curve private keys using a password for encrypting the data

    Args:
        key (ec.EllipticCurvePrivateKey): The key to be serialized.
        password (bytearray): The password to be used for encryption of the key. It is cleared from memory after use

    Returns:
        bytes: The serialized PEM formatted key, ready to be written to a file.
    """
    serialized_private = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(bytes(password))
    )

    for i in range(0, len(password)):
        password[i] = 0

    return serialized_private


def serialize_public_key(key: ec.EllipticCurvePublicKey) -> bytes:
    """Serialization for Elliptic Curve public keys

    Args:
        key (ec.EllipticCurvePublicKey): The key to be serialized

    Returns:
        bytes: The serialized PEM formatted key, ready to be written to a file.
    """
    serialized_public = key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return serialized_public


def load_public_key(serialized_key_file) -> ec.EllipticCurvePublicKey:
    """Loading for public keys serialized into PEM format files

    Args:
        serialized_key_file (File object): The file object containing the serialized key

    Returns:
        ec.EllipticCurvePublicKey: The public key
    """
    serialized_key_data = serialized_key_file.read()

    public_key = serialization.load_pem_public_key(
        serialized_key_data
    )
    return public_key


def load_private_key(serialized_key_file, password: bytearray) -> ec.EllipticCurvePrivateKey:
    """Loading for public keys serialized into PEM format files (requires password)

    Args:
        serialized_key_file (File object): The file object containing the serialized key
        password (bytes): The password for decrypting the key

    Returns:
        ec.EllipticCurvePrivateKey: The private key
    """
    serialized_key_data = serialized_key_file.read()

    private_key = serialization.load_pem_private_key(
        serialized_key_data,
        password=bytes(password)
    )

    for i in range(0, len(password)):
        password[i] = 0

    return private_key


def __hash(data_file) -> bytes:
    """ Auxiliary hash function for curve module """
    data_file.seek(0)

    # Hashing file
    hasher = hashes.Hash(__relevant_hash)
    byte: bytes = data_file.read(2048)
    while byte:
        hasher.update(byte)
        byte = data_file.read(2048)
    digest = hasher.finalize()
    return digest
