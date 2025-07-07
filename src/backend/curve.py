# Using elliptic curve algorithm Ed25519 (EdDSA with Curve25519)
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec


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
        Ed25519PublicKey: The public key that was generated
    """
    pubkey = privkey.public_key()
    return pubkey
