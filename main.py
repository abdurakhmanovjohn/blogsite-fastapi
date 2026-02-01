# pyright: reportAttributeAccessIssue=false


import re
from math import ceil
from typing import List

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog Site with FastAPI")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

POSTS_PER_PAGE = 4


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text.strip("-")


@app.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    page: int = 1,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    # posts = db.query(models.Post).order_by(models.Post.created_at.desc()).all()
    # return templates.TemplateResponse("home.html", {"request": request, "posts": posts})
    query = db.query(models.Post)

    if search:
        query = query.filter(
            or_(
                models.Post.title.ilike(f"%{search}%"),
                models.Post.content.ilike(f"%{search}%"),
                models.Post.author.ilike(f"%{search}%"),
            )
        )

    total_posts = query.count()
    total_pages = max(ceil(total_posts / POSTS_PER_PAGE), 1)

    posts = (
        query.order_by(models.Post.created_at.desc())
        .offset((page - 1) * POSTS_PER_PAGE)
        .limit(POSTS_PER_PAGE)
        .all()
    )

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "posts": posts,
            "page": page,
            "total_pages": total_pages,
            "search": search or "",
        },
    )


@app.get("/post/{slug}", response_class=HTMLResponse)
def view_post(request: Request, slug: str, db: Session = Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.id == post_id).first()
    # return templates.TemplateResponse("post.html", {"request": request, "post": post})

    post = db.query(models.Post).filter(models.Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post Not Found")

    return templates.TemplateResponse("post.html", {"request": request, "post": post})


@app.get("/create", response_class=HTMLResponse)
def create_page(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@app.post("/create")
def create_post(
    title: str = Form(...),
    content: str = Form(...),
    author: str = Form(...),
    slug: str | None = Form(None),
    db: Session = Depends(get_db),
):
    final_slug = slugify(slug) if slug else slugify(title)
    existing = db.query(models.Post).filter(models.Post.slug == final_slug).first()
    if existing:
        raise HTTPException(
            status_code=400, detail="Slug already exists, choose another one."
        )

    new_post = models.Post(title=title, slug=final_slug, content=content, author=author)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return RedirectResponse(url=f"/post/{new_post.slug}", status_code=303)


@app.get("/post/{post_id}/edit", response_class=HTMLResponse)
def edit_post_page(
    post_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return templates.TemplateResponse(
        "edit.html",
        {"request": request, "post": post},
    )


@app.post("/post/{post_id}/edit")
def edit_post(
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    author: str = Form(...),
    db: Session = Depends(get_db),
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post Not Found")

    post.title = title
    post.content = content
    post.author = author

    db.commit()

    return RedirectResponse(url=f"/post/{post.slug}", status_code=303)


@app.post("/post/{post_id}/delete")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post Not Found")

    db.delete(post)
    db.commit()

    return RedirectResponse(url="/", status_code=303)


@app.get("/api/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()
