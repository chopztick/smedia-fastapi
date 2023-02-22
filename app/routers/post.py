from ..schemas import CreatePost, Posts, UpdatePost,PostOut
from typing import Optional
from ..models import Post, Vote
from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from sqlalchemy import func, desc

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[PostOut])
async def conn_alche(db: Session = Depends(get_db), current_user: int = Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):

    join_posts = db.query(Post, func.count(Vote.post_id).label('votes')).join(Vote, isouter=True).group_by(Post.id).order_by(desc(func.count(Vote.post_id).label('Votes')), Post.id)
    posts = join_posts.filter(Post.content.contains(search)).limit(limit).offset(offset=skip).all()
    return posts
    '''
    SQL code with psycopg

async def get_details():
    cursor.execute("SELECT * FROM post;")
    posts= cursor.fetchall()
    return {"data": posts}
    '''
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Posts)
async def add_post(post: CreatePost, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    print(current_user.id)
    new_post = Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

    '''
async def create_post(post: Post):
    cursor.execute("INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *;", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}
    '''

@router.get("/{id}", response_model=PostOut)
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    #pt_post = db.query(Post).filter(Post.id == id).first()
    pt_post = db.query(Post, func.count(Vote.post_id).label('votes')).join(Vote, isouter=True).group_by(Post.id).order_by(desc(func.count(Vote.post_id).label('Votes')), Post.id)
    pt_post = pt_post.filter(Post.id == id).first()
    if not pt_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="no post with this id: {}".format(id))
    return pt_post

    '''
    SQL code with psycopg

async def get_post(id: int):
    cursor.execute("SELECT * FROM post WHERE id = %s;", (id,))
    get_post = cursor.fetchone()
    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="no post with this id: {}".format(id))
    return {"data": get_post}
    '''

@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_qr = db.query(Post).filter(Post.id == id)
    post_st = post_qr.first()
    if not post_st:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="no post with this id: {}".format(id))
    if current_user.id != post_st.owner_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not allowed to delete others post")
    post_qr.delete(synchronize_session=False)
    db.commit()

    '''
async def delete_post(id: int):
    cursor.execute("DELETE FROM post WHERE id = %s RETURNING *;", (id,))
    del_post = cursor.fetchone()
    if not del_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="no post with this id: {}".format(id))
    conn.commit()
    return {"deleted": del_post}
    '''

@router.put("/{id}", response_model=Posts)
async def update_post(id: int, post: UpdatePost, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_qr = db.query(Post).filter(Post.id == id)
    post_up = post_qr.first()
    if not post_up:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    detail="no post with this id: {}".format(id))
    if current_user.id != post_up.owner_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not allowed to update others post")
    post_qr.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_qr.first()


    '''
async def update_post(id: int, post: Post):
    cursor.execute("UPDATE post SET title= %s, content= %s, published= %s WHERE id = %s RETURNING *;", (post.title, post.content, post.published, id))
    post_item = cursor.fetchone()
    if not post_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="no post with this id: {}".format(id))
    conn.commit()
    return {"updated": post_item}
    '''