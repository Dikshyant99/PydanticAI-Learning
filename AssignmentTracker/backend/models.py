from datetime import date, datetime, timezone
from enum import Enum
from pydantic import EmailStr

from sqlmodel import Field, SQLModel

#The only allowed values for status
class Status(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

#Users info
class AssignmentBase(SQLModel):
    title:str=Field(min_length=1,max_length=200)
    subject: str = Field(max_length=100)
    due_date: date
    status: Status = Status.pending
    notes: str | None = None

#the actual database model

class Assignment(AssignmentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    owner_id: int | None = Field(default=None, foreign_key="user.id", index=True)
    
# What the user sends to CREATE an assignment
class AssignmentCreate(AssignmentBase):
    pass


# What the API RETURNS (includes database-generated fields)
class AssignmentPublic(AssignmentBase):
    id: int
    created_at: datetime


# What the user sends to UPDATE (every field optional)
class AssignmentUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    subject: str | None = Field(default=None, max_length=100)
    due_date: date | None = None
    status: Status | None = None
    notes: str | None = None

# ---------- USERS ----------

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    full_name: str = Field(min_length=1, max_length=100)


# The database table
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# What the user sends to SIGN UP
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=72)


# What the API RETURNS about a user (never the password!)
class UserPublic(UserBase):
    id: int
    created_at: datetime


# What the API returns after LOGIN
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
    
