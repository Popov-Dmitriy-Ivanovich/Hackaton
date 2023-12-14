import db.db_classes as db
from pydantic import BaseModel
from typing import List


class ProfileFormResult(BaseModel):
    login: str
    choises: List[str]


class ProcessResponce(BaseModel):
    status: str


def process_favourites(form_res: ProfileFormResult):
    try:
        conn = db.connect_db()
        user = (
            conn.session.query(db.UsersTable)
            .filter_by(
                id=conn.session.query(db.LoginDataTable)
                .filter_by(login=form_res.login)
                .first()
                .user_id
            )
            .first()
        )
        user_fav = (
            conn.session.query(db.FavouritesTable).filter_by(user_id=user.id).all()
        )
        for i in user_fav:
            conn.session.delete(i)

        for i in form_res.choises:
            conn.session.add(db.FavouritesTable(name=i, user_id=user.id))
        conn.session.commit()
        return ProcessResponce(status="OK")
    except:
        return ProcessResponce(status="ERR")
