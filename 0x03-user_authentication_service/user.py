#!/usr/bin/env python3
from flask import Flask
from sqlalchemy import column, Integer, String, declarative_base, create_engine 


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = column(Integer, primary_key=True)
    email = column(String(250), nullable=False)