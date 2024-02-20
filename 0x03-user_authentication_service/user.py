#!/usr/bin/env python3
"""
User model module
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """
    Class representing a record from user table
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Colum(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Colum(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)