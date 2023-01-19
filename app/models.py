from sqlalchemy import Column, Integer, String, ForeignKey
from app.config import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from datetime import datetime


# создаем модель, объекты которой будут храниться в бд
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"))
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    u_userdata_rel = relationship("UserData", back_populates="u_user_rel")
    role_rel = relationship("Role", back_populates="r_user_rel")


class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, nullable=False)
    rolename = Column(String, nullable=False, unique=True)

    r_user_rel = relationship("Users", back_populates="role_rel")


class UserData(Base):
    __tablename__ = 'userdata'
    id = Column(Integer, primary_key=True, nullable=False)
    d_user_id = Column(Integer, ForeignKey("users.id"))
    audit_id = Column(Integer, ForeignKey("audit.id"))
    savedresults_id = Column(Integer, ForeignKey("savedresults.id"))

    u_user_rel = relationship("Users", back_populates="u_userdata_rel")
    audit_rel = relationship("Audit", back_populates="a_userdata_rel")
    u_savedresults_rel = relationship("SavedResults", back_populates="s_userdata_rel")


class Audit(Base):
    __tablename__ = 'audit'
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    last_visit = Column(TIMESTAMP(timezone=True), nullable=False)

    a_userdata_rel = relationship("UserData", back_populates="audit_rel")


class SavedResults(Base):
    __tablename__ = 'savedresults'
    id = Column(Integer, primary_key=True, nullable=False)
    index_id = Column(Integer, ForeignKey("index.id"))
    periodsnum = Column(Integer, nullable=True, unique=False)
    rate = Column(Integer, nullable=True, unique=False)
    futurevalue = Column(Integer, nullable=True, unique=False)
    initialinvest = Column(Integer, nullable=True, unique=False)
    accrualperiodsnum = Column(Integer, nullable=True, unique=False)
    annualincome = Column(Integer, nullable=True, unique=False)
    grandtotal = Column(Integer, nullable=True, unique=False)

    index_rel = relationship("Index", back_populates="i_savedresults_rel")
    s_userdata_rel = relationship("UserData", back_populates="u_savedresults_rel")


class Index(Base):
    __tablename__ = 'index'
    id = Column(Integer, primary_key=True, nullable=False)
    indexname = Column(String, nullable=False, unique=True)

    i_savedresults_rel = relationship("SavedResults", back_populates="index_rel")
