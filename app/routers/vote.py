from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List


router = APIRouter(
    tags=["Vote"],
    prefix="/vote"
)

@router.get("/", response_model=List[schemas.VoteCount], status_code=status.HTTP_200_OK)
def read_votes(db: Session = Depends(database.get_db)):
    #read count of votes for all post and return as list of VoteCount order by id
    query_result = (db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).order_by(models.Post.id).all())
    result = []
    for post, votes in query_result:
        post.votes_count = votes
        result.append(post)
    return result

    

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first() 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} does not exist")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted for post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully voted for post"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}