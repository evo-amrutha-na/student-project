from project.component.loggings import set_up_logging
from sqlalchemy import create_engine
from sqlalchemy.orm import Session,sessionmaker, scoped_session
from sqlalchemy.ext.automap import automap_base
from pydantic import BaseModel, EmailStr, validator
from project.config.config import DATABASE_URI
import re



logger = set_up_logging()

Base = automap_base()
engine = create_engine(DATABASE_URI)
Base.prepare(engine, reflect=True)
session = Session(engine)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a scoped session
ScopedSession = scoped_session(SessionLocal)

def get_session():
    """
    Dependency function for getting a SQLAlchemy session with rollback and commit handling.
    """
    local_session = ScopedSession()
    try:
        yield local_session
        local_session.commit()  # Commit transaction if no exception occurs
    except:
        local_session.rollback()  # Rollback transaction if an exception occurs
        raise  # Re-raise the exception to handle it further up the stack
    finally:
        local_session.close()


Student= Base.classes.Student
StudentOtp= Base.classes.StudentOtp

class ValidateStudentCreate(BaseModel):
    id: int
    fname: str
    lname: str
    mobile: str
    email: str

    @validator('email')
    def validate_email(cls, v):
        if v:
            if len(v) < 4:
                raise ValueError('Email must have at least 4 characters')

            if len(v) > 50:
                raise ValueError('Email must have  at most 50 characters only')

            if not (re.match("^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", v)):
                raise ValueError('Invalid email')

            split_email = v.split("@")[1].split(".")[1]

            if split_email not in ['com', 'in', 'org', 'co', 'net', 'edu', 'me', 'uk']:
                raise ValueError('Invalid email domain')

        return v
    
    @validator('mobile')
    def validate_mobile(cls, v):
        if v:
            if not (re.match("^[5-9]{1}[0-9]{9}$", v)):
                raise ValueError('Invalid phone number')

        return v

class validateDeleteStudent(BaseModel):
    id:int

class ValidateAccount(BaseModel):
    fname: str
    lname: str
    mobile: str
    email: EmailStr
    password: str
    @validator('mobile')
    def validate_mobile(cls, v):
        if v:
            if not (re.match("^[5-9]{1}[0-9]{9}$", v)):
                raise ValueError('Invalid phone number')

        return v
    @validator('password')
    def validate_password(cls, v):
        if len(v)<3:
            raise ValueError('Password not long enough')
        return v
    
 
class StudentLogin(BaseModel):
    email: EmailStr
    password: str

class ValidateForgotPassword(BaseModel):
    email: EmailStr

class ValidateVerifyOTP(BaseModel):
    email: EmailStr
    otp:int

class ValidateResetPassword(BaseModel):
    email: EmailStr
    password: str
