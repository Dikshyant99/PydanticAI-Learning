from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from auth import CurrentUser, create_access_token, hash_password, verify_password
from database import create_db_and_tables, get_session
from models import (
    Assignment,
    AssignmentCreate,
    AssignmentPublic,
    AssignmentUpdate,
    Token,
    User,
    UserCreate,
    UserPublic,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Assignment Tracker API", lifespan=lifespan)

# Reusable shortcut: "this endpoint needs a database session"
SessionDep = Annotated[Session, Depends(get_session)]


# ---------- HOME: send visitors to the frontend ----------
@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse(url="/app/")


# ---------- AUTH ----------
@app.post("/auth/signup", response_model=UserPublic, status_code=201)
def signup(user_in: UserCreate, session: SessionDep):
    existing = session.exec(select(User).where(User.email == user_in.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User.model_validate(
        user_in, update={"hashed_password": hash_password(user_in.password)}
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.post("/auth/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
):
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=create_access_token(user.id))


@app.get("/auth/me", response_model=UserPublic)
def read_me(current_user: CurrentUser):
    return current_user


# ---------- HELPER: fetch an assignment only if it belongs to the user ----------
def get_owned_assignment(assignment_id: int, session: Session, user: User) -> Assignment:
    assignment = session.get(Assignment, assignment_id)
    if not assignment or assignment.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment


# ---------- ASSIGNMENTS: CREATE ----------
@app.post("/assignments", response_model=AssignmentPublic, status_code=201)
def create_assignment(
    assignment: AssignmentCreate, session: SessionDep, current_user: CurrentUser
):
    db_assignment = Assignment.model_validate(
        assignment, update={"owner_id": current_user.id}
    )
    session.add(db_assignment)
    session.commit()
    session.refresh(db_assignment)
    return db_assignment


# ---------- ASSIGNMENTS: READ (all of MY assignments) ----------
@app.get("/assignments", response_model=list[AssignmentPublic])
def list_assignments(
    session: SessionDep,
    current_user: CurrentUser,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    statement = (
        select(Assignment)
        .where(Assignment.owner_id == current_user.id)
        .order_by(Assignment.due_date)
        .offset(offset)
        .limit(limit)
    )
    return session.exec(statement).all()


# ---------- ASSIGNMENTS: READ (one) ----------
@app.get("/assignments/{assignment_id}", response_model=AssignmentPublic)
def get_assignment(assignment_id: int, session: SessionDep, current_user: CurrentUser):
    return get_owned_assignment(assignment_id, session, current_user)


# ---------- ASSIGNMENTS: UPDATE ----------
@app.patch("/assignments/{assignment_id}", response_model=AssignmentPublic)
def update_assignment(
    assignment_id: int,
    assignment: AssignmentUpdate,
    session: SessionDep,
    current_user: CurrentUser,
):
    db_assignment = get_owned_assignment(assignment_id, session, current_user)
    db_assignment.sqlmodel_update(assignment.model_dump(exclude_unset=True))
    session.add(db_assignment)
    session.commit()
    session.refresh(db_assignment)
    return db_assignment


# ---------- ASSIGNMENTS: DELETE ----------
@app.delete("/assignments/{assignment_id}", status_code=204)
def delete_assignment(assignment_id: int, session: SessionDep, current_user: CurrentUser):
    db_assignment = get_owned_assignment(assignment_id, session, current_user)
    session.delete(db_assignment)
    session.commit()


# ---------- FRONTEND: serve the HTML/CSS/JS files at /app ----------
# frontend/ sits next to backend/ in the project root
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/app", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")