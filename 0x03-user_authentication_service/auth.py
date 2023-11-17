#!/usr/bin/env python3
"""
Hash Password
"""


import bcrypt
from db import DB
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """
    Hash the input password with bcrpt
    
    Args:
        password (str): The input passwoed to be hashed
        
    Returns: 
        bytes: The salted hash of the input password
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user.

        Args:
            email (str): User's email address.
            password (str): User's password.

        Returns:
            User: User object representing the registered user.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        # Check if the user already exists
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except ValueError:
            # User does not exist, proceed with registration
            pass

        # Hash the password
        hashed_password = _hash_password(password)

        # Add the new user to the database
        new_user = self._db.add_user(email, hashed_password)

        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the provided login credentials are valid.

        Args:
            email (str): User's email address.
            password (str): User's password.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            # Check if the provided password matches the stored hashed password
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
        except ValueError:
            # User not found
            return False

    def _generate_uuid() -> str:
        """Generate a new UUID and return its string representation.

        Returns:
            str: String representation of the generated UUID.
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """Create a session for the user and return the session ID.

        Args:
            email (str): User's email address.

        Returns:
            str: Session ID.
        """
        try:
            user = self._db.find_user_by(email=email)

            # Generate a new UUID as the session ID
            session_id = self._generate_uuid()

            # Store the session ID in the database for the user
            user.session_id = session_id
            self._db._session.commit()  # Note: Using a private method for demonstration purposes

            return session_id
        except ValueError:
            # User not found
            return None

    def get_user_from_session_id(self, session_id: str) -> User or None:
        """Get user corresponding to the session ID.

        Args:
            session_id (str): Session ID.

        Returns:
            User or None: User object corresponding to the session ID, or None if not found.
        """
        if session_id is None:
            return None

        try:
            # Use public method to find user by session_id
            user = self._db.find_user_by(session_id=session_id)
            return user
        except ValueError:
            # Session ID not found
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy the session for the corresponding user.

        Args:
            user_id (int): User's ID.

        Returns:
            None
        """
        # Use public method to update the user's session ID to None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Get reset password token for the user.

        Args:
            email (str): User's email.

        Returns:
            str: Reset password token.
        """
        try:
            # Use public method to find user by email
            user = self._db.find_user_by(email=email)
        except ValueError:
            # If user does not exist, raise a ValueError
            raise ValueError(f"User with email {email} not found.")

        # Generate a UUID for the reset password token
        reset_token = self._generate_uuid()

        # Update the user's reset_token in the database
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, new_password: str) -> None:
        """Update user's password using the reset token.

        Args:
            reset_token (str): Reset password token.
            new_password (str): New password.

        Returns:
            None
        """
        try:
            # Use public method to find user by reset token
            user = self._db.find_user_by(reset_token=reset_token)
        except ValueError:
            # If user does not exist, raise a ValueError
            raise ValueError(f"User with reset token {reset_token} not found.")

        # Hash the new password
        hashed_password = _hash_password(new_password)

        # Update the user's hashed_password and reset_token fields in the database
        self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)
