from uuid import UUID
from sqlalchemy.orm import Session

from app.utils.database import db_dep
from app.models.nomination import Nomination
from app.schemas import Nomination as DbNomination

class NominationsRepo:
    db: Session

    def __init__(self, db: Session = db_dep) -> None:
        self.db = db

    def add_nomination(self, nomination: Nomination, voting_id: UUID) -> Nomination:
        db_nomination = DbNomination(**nomination.dict())
        db_nomination.voting_id = voting_id
        self.db.add(db_nomination)
        self.db.commit()

        return Nomination.from_orm(db_nomination)
