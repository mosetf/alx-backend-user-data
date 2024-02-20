#!/usr/bin/env python3
"""User module"""
from sqlalchemy import column, Integer, String, declarative_base, create_engine 


Base = declarative_base()

class User(Base):
    """User class"""
    __tablename__ = 'users'
    id = column(Integer, primary_key=True)
    email = column(String(250), nullable=False)
    hashed_password = column(String(250), nullable=False)
    session_id = column(String(250), nullable=True)
    reset_token = column(String(250), nullable=True)