#!/usr/bin/env python3
"""
A module for encrypting passwords.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Function that hashes a password using a random salt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Function that checks if hashed password was formed from given password.

    Args:
        hashed_password (bytes): The hashed password to be checked.
        password (str): The password to compare against the hashed password.

    Returns:
        bool: True if the hashed password matches the given password, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)