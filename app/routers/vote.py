from fastapi import status, Depends, HTTPException, APIRouter
from ..schemas import Vote
from ..database import get_db
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user 
from ..models import Vote as Vote_db, Post

router = APIRouter(prefix='/vote', tags=['Vote'])

@router.post('/', status_code=status.HTTP_201_CREATED)
async def vote(vote: Vote, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    vote_qr = db.query(Vote_db).filter(Vote_db.user_id == current_user.id, Vote_db.post_id == vote.post_id)
    found_vote = vote_qr.first()

    post_exists = db.query(Post).filter(Post.id == vote.post_id).first()
    if not post_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    detail="no post with this id: {}".format(vote.post_id))

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail=f'user {current_user.id} already voted on post {vote.post_id}')
        new_vote = Vote_db(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'succesfully added vote'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail='Vote does not exist')
        
        vote_qr.delete(synchronize_session=False)
        db.commit()
        return {'message': 'succesfully deleted vote'}