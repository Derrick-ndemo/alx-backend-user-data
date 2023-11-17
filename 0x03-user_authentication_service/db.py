#!/usr/bin/env python3
"""
DB Module
"""


from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError, IntegrityError
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Parameters:
        - email (str): The email of the user.
        - hashed_password (str): The hashed password of the user.

        Returns:
        - User: The User object representing the added user.
        """
        # Create a new User object
        new_user = User(email=email, hashed_password=hashed_password)
        # Add the user to the session
        self._session.add(new_user)
        try:
            # Commit the changes to the database
            self._session.commit()
        except IntegrityError:
            # Handle IntegrityError (e.g., if the email is not unique)
            self._session.rollback()
            raise ValueError("User with this email already exists.")
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by specified attributes.
        Parameters:
        - kwargs: Arbitrary keyword arguments rep attributes
        Returns:
        - User: The User object found based on the query.
        Raises:
        - NoResultFound: If no results are found.
        - InvalidRequestError: If wrong query arguments are passed.
        """
        try:
            # Query the database for the user based on the provided arguments
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound("No user found with the provided criteria.")
            return user
        except InvalidRequestError as e:
            # Handle InvalidRequestError (e.g., incorrect query arguments)
            raise InvalidRequestError("Invalid query arguments.") from e
    
    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user based on a given id.
        """
        try:
            # Find the user based on user_id
            user = self.find_user_by(id=user_id)

            # Update user attributes
            for key, value in kwargs.items():
                # Check if the argument corresponds to a user attribute
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError(f"Invalid argument: {key}")

            # Commit changes to the database
            self._session.commit()
        except NoResultFound:
            # Handle NoResultFound (user not found)
            raise ValueError(f"User with ID {user_id} not found.")
        except InvalidRequestError as e:
            # Handle InvalidRequestError (e.g., incorrect query arguments)
            self._session.rollback()
            raise InvalidRequestError("Invalid query arguments.") from e
