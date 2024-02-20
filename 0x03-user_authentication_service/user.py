#!/usr/bin/env python3
from flask import Flask
from sqlalchemy import column, Integer, String, declarative_base, create_engine 


Base = declarative_base()

class User(Base);