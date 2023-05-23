from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from typing import List
from pydantic import BaseModel, Field
from enum import Enum
from sqlalchemy.ext.declarative import declarative_base
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, Form, Response, HTTPException, Request
import time
from starlette.responses import Response
app = FastAPI(debug=True)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define the database URL
database_url = "postgresql://prog_club_website_database_user:SWtTkh5nXvcd9MJx0sFFtCTJbWt254ST@dpg-cgd9vfg2qv2aq5jp1s7g-a.singapore-postgres.render.com/prog_club_website_database"

# Create the SQLAlchemy engine and session
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Reflect the database schema
Base = declarative_base()

metadata = MetaData()

events_table = Table(
    "api_event",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("subtitle", String),
    Column("description", String),
    Column("type", String),
    Column("image", String),
)


class EventChoices(str, Enum):
    Upcoming = "Upcoming"
    Ongoing = "Ongoing"
    Past = "Past"


class EventCreate(BaseModel):
    title: str = Field(..., title="Event Title")
    subtitle: str = Field(..., title="Subtitle")
    description: str = Field(..., title="Description")
    type: EventChoices = Field(..., title="Type")
    image: str = Field(..., title="Poster")


class EventUpdate(BaseModel):
    title: str = Field(None, title="Event Title")
    subtitle: str = Field(None, title="Subtitle")
    description: str = Field(None, title="Description")
    type: EventChoices = Field(None, title="Type")
    image: str = Field(None, title="Poster")


class Event(Base):
    __table__ = events_table


class EventDelete(BaseModel):
    id: int


class EventResponse(BaseModel):
    id: int
    title: str = Field(..., title="Event Title")
    subtitle: str = Field(..., title="Subtitle")
    description: str = Field(..., title="Description")
    type: EventChoices = Field(..., title="Type")
    image: str = Field(..., title="Poster")


class EventList(BaseModel):
    events: List[EventResponse]

    class Config:
        arbitrary_types_allowed = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/events", response_model=EventList)
async def get_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    event_responses = [EventResponse(**event.__dict__) for event in events]
    return {"events": event_responses}


projects_table = Table(
    "api_project",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("subtitle", String),
    Column("domain", String),
    Column("category", String),
    Column("description", String),
    Column("image", String),
    Column("github", String),
)


class Project(Base):
    __table__ = projects_table


class ProjectResponse(BaseModel):
    id: int
    title: str = Field(..., title="Project Title")
    subtitle: str = Field(..., title="Project Subtitle")
    domain: str = Field(..., title="Domain")
    category: str = Field(..., title="Category")
    description: str = Field(..., title="Description")
    image: str = Field(..., title="Image")
    github: str = Field(..., title="Repository")
    image_preview: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Project Title",
                "subtitle": "Project Subtitle",
                "domain": "Domain",
                "category": "Category",
                "description": "Project description.",
                "image": "https://example.com/image.jpg",
                "github": "https://github.com/example",
                "image_preview": "<img src='https://example.com/image.jpg' width='100' height='100' />",
            }
        }


class ProjectList(BaseModel):
    projects: List[ProjectResponse]

    class Config:
        arbitrary_types_allowed = True



@app.get("/projects", response_model=ProjectList)
async def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    project_responses = []
    for project in projects:
        image_preview = ""
        if project.image:
            image_preview = f'<img src="{project.image}" width="100" height="100" />'
        project_response = ProjectResponse(
            id=project.id,
            title=project.title,
            subtitle=project.subtitle,
            domain=project.domain,
            category=project.category,
            description=project.description,
            image=project.image,
            github=project.github,
            image_preview=image_preview,
        )
        project_responses.append(project_response)
    return {"projects": project_responses}


team_table = Table(
    "api_team",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("email", String),
    Column("position", String),
    Column("division", String),
    Column("year", String),
    Column("github", String),
    Column("codeforces", String),
    Column("linkedin", String),
    Column("image", String),
)


class TeamPositionChoices(str, Enum):
    President = "President"
    Member = "Member"
    Volunteer = "Volunteer"


class TeamDivisionChoices(str, Enum):
    CompetitiveProgramming = "Competitive Programming"
    CyberSecurity = "Cyber Security"
    SoftwareDevelopment = "Software Development"


class TeamYearChoices(str, Enum):
    First = "First"
    Second = "Second"
    Third = "Third"
    Fourth = "Fourth"


class Team(Base):
    __table__ = team_table


class TeamResponse(BaseModel):
    id: int
    name: str = Field(..., title="Name")
    email: str = Field(..., title="Email")
    position: TeamPositionChoices = Field(..., title="Position")
    division: TeamDivisionChoices = Field(..., title="Division")
    year: TeamYearChoices = Field(..., title="Year")
    github: str = Field(..., title="GitHub Profile")
    codeforces: str = Field(..., title="Codeforces Profile")
    linkedin: str = Field(..., title="LinkedIn Profile")
    image: str = Field(..., title="Image")
    image_preview: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "position": "President",
                "division": "Competitive Programming",
                "year": "First",
                "github": "https://github.com/johndoe",
                "codeforces": "https://codeforces.com/johndoe",
                "linkedin": "https://linkedin.com/in/johndoe",
                "image": "https://example.com/image.jpg",
                "image_preview": "<img src='https://example.com/image.jpg' width='100' height='100' />",
            }
        }


class TeamList(BaseModel):
    team_members: List[TeamResponse]

    class Config:
        arbitrary_types_allowed = True

@app.get("/team", response_model=TeamList)
def get_team_members(db: Session = Depends(get_db)):
    team_members = db.query(Team).all()
    team_responses = []
    for member in team_members:
        image_preview = ""
        if member.image:
            image_preview = f'<img src="{member.image}" width="100" height="100" />'
        team_response = TeamResponse(
            id=member.id,
            name=member.name,
            email=member.email,
            position=member.position,
            division=member.division,
            year=member.year,
            github=member.github,
            codeforces=member.codeforces,
            linkedin=member.linkedin,
            image=member.image,
            image_preview=image_preview,
        )
        team_responses.append(team_response)
    return {"team_members": team_responses}



alumni_table = Table(
    "api_alumni",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("passing_year", Integer),
    Column("division", String),
    Column("image", String),
    Column("LinkedIn_Profile", String),
)

class AlumniChoices(str, Enum):
    CompetitiveProgramming = "Competitive Programming"
    CyberSecurity = "Cyber Security"
    SoftwareDevelopment = "Software Development"

class Alumni(Base):
    __table__ = alumni_table

class AlumniCreate(BaseModel):
    name: str = Field(..., title="Alumni's Name")
    passing_year: int = Field(..., title="Alumni's Passing Year")
    division: AlumniChoices = Field(..., title="Alumni's Division")
    image: str = Field(..., title="Image")
    LinkedIn_Profile: str = Field(..., title="Alumni's LinkedIn Profile")

class AlumniResponse(BaseModel):
    id: int
    name: str = Field(..., title="Alumni's Name")
    passing_year: int = Field(..., title="Alumni's Passing Year")
    division: AlumniChoices = Field(..., title="Alumni's Division")
    image: str = Field(..., title="Image")
    LinkedIn_Profile: str = Field(..., title="Alumni's LinkedIn Profile")
    image_preview: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Alumni's Name",
                "passing_year": 2023,
                "division": "Competitive Programming",
                "image": "https://example.com/image.jpg",
                "LinkedIn_Profile": "https://example.com/linkedin",
                "image_preview": "<img src='https://example.com/image.jpg' width='100' height='100' />",
            }
        }

class AlumniList(BaseModel):
    alumni: List[AlumniResponse]

class AlumniDelete(BaseModel):
    id: int


@app.get("/alumni", response_model=AlumniList)
def get_alumni(db: Session = Depends(get_db)):
    alumni = db.query(Alumni).all()
    alumni_responses = []
    for member in alumni:
        image_preview = ""
        if member.image:
            image_preview = f'<img src="{member.image}" width="100" height="100" />'
        alumni_response = AlumniResponse(
            id=member.id,
            name=member.name,
            passing_year=member.passing_year,
            division=member.division,
            image=member.image,
            LinkedIn_Profile=member.LinkedIn_Profile,
            image_preview=image_preview,
        )
        alumni_responses.append(alumni_response)
    return {"alumni": alumni_responses}