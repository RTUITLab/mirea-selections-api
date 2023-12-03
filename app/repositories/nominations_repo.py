from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.utils.database import db_dep
from app.models.nominant import Nominant
from app.models.nomination import Nomination
from app.schemas import Nominant as DbNominant
from app.schemas import Nomination as DbNomination


class NominationsRepo:
    db: Session

    def __init__(self, db: Session = db_dep) -> None:
        self.db = db

    def _from_orm(self, nomination: DbNomination) -> Nomination | None:
        if nomination == None:
            return None

        return Nomination.from_orm(nomination)

    def get_voting_nomination(self, voting_id: UUID, nomination_id: UUID) -> Nomination | None:
        nomination = self.db.execute(
            select(DbNomination).where(DbNomination.id ==
                                       nomination_id and DbNomination.voting_id == voting_id)
        ).scalar_one_or_none()

        return self._from_orm(nomination)

    def add_nomination(self, nomination: Nomination, voting_id: UUID) -> Nomination:
        db_nomination = DbNomination(**nomination.dict())
        db_nomination.voting_id = voting_id
        self.db.add(db_nomination)
        self.db.commit()

        return Nomination.from_orm(db_nomination)

    def add_nominant(self, nomination_id: UUID, nominant: Nominant):
        nomination = self.db.execute(
            select(DbNomination).where(DbNomination.id == nomination_id)
        ).scalar_one()

        db_nominant = DbNominant(**nominant.dict())
        nomination.nominants.append(db_nominant)
        self.db.commit()

        return Nominant.from_orm(db_nominant)
