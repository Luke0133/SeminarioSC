# Using elliptic curve algorithm Ed25519 (EdDSA with Curve25519)
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey


def generate_private_key() -> Ed25519PrivateKey:
    """A wrapper function to generate an Elliptic Curve private key.

    Returns:
        Ed25519PrivateKey: The private key that was generated
    """
    privkey = Ed25519PrivateKey.generate()
    return privkey


def generate_public_key(privkey: Ed25519PrivateKey) -> Ed25519PublicKey:
    """A wrapper function to generate an Elliptic Curve public key.

    Args:
        privkey (Ed25519PrivateKey): A previously generated private key.

    Returns:
        Ed25519PublicKey: The public key that was generated
    """
    pubkey = privkey.public_key()
    return pubkey
