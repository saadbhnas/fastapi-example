from fastapi import FastAPI , Response , status ,HTTPException , Depends , APIRouter
from .. import schemas , utils , models , oauth2
from typing import List , Optional
from ..database import engine , get_db 
from sqlalchemy.orm import Session 
from sqlalchemy import func

router = APIRouter(
    prefix= '/posts',
    tags=['Posts']
)

#@router.get("/" , response_model=List[schemas.PostOut])
@router.get("/")
def root(db:Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user) , limit:int=6 , skip:int=0 
         ,search:Optional[str] = ""):
    #curser.execute("""SELECT * FROM posts""")
    #posts = curser.fetchall()

    #to get all posts for all users 
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote , models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).all()
    #to get all posts for the current user
    #posts = db.query(mode.Post).filter(models.Post.owner_id == current_user.id).all()
    
    formatted_results = [
        {"post":{"id": post.id,
            "title": post.title,
            "content": post.content,
            "owner_id": post.owner_id,},
            
            "votes": votes
        }
        for post, votes  in results
    ]

    return formatted_results


@router.post("/",status_code=status.HTTP_201_CREATED , response_model=schemas.Post)
def creating_post(post : schemas.CreatePost , db:Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)):
    #curser.execute("""INSERT INTO posts (title,content  ) VALUES (%s , %s  ) RETURNING *""" ,
    #               (post.title , post.content ))
    #new_post = curser.fetchone()
    #conn.commit()

    new_post = models.Post(owner_id=current_user.id ,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get('/{id}' , response_model=schemas.Post)
def get_post(id : int , response : Response , db:Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)):
    #curser.execute(""" SELECT * FROM posts WHERE id = %s """ , (str(id) ,))
    #post = curser.fetchone()
    

    """
    for p in my_posts:
        if p['id'] == id:
             return {"the post" : p}
    """
    #get all posts of all specific id numbers
    post = db.query(models.Post).filter(models.Post.id == id ).first()


    #to get only post with id matches owner id extra step that make sure no one can retrive posts with id deffrent than the id they have 
    #if post.owner_id != current_user.id :
    #    raise(HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="not aothurized to do that action"))


    if post :
       return post

    else :
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message" : f"post with id : {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id : {id} was not found")
        
@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int , db:Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)):
    #curser.execute("""DELETE FROM posts WHERE id = %s RETURNING *""" , (str(id) , ))
    #deleted_post = curser.fetchone()
    #conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id == id)

    if  post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
                            detail=f"post with id : {id} dosent exist")
    
    if post.first().owner_id != current_user.id :
        raise(HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="not aothurized to do that action"))

    post.delete(synchronize_session=False)
    db.commit()
    
    return {"deleted_post" : post}

    #my_posts.pop(index)
    #return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}' , response_model=schemas.Post)
def updating_posts(id:int , post : schemas.CreatePost , db:Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)):
    #curser.execute(""" UPDATE posts SET title = %s , content = %s WHERE id = %s RETURNING * """ , 
    #               (post.title , post.content , str(id)))
    #updated_post = curser.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
                            detail=f"post with id : {id} dosent exist")
    
    if post_query.first().owner_id != current_user.id :
        raise(HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="not aothurized to do that action"))
    
    post_query.update(post.dict() , synchronize_session=False)
    db.commit()
    
    return post_query.first()