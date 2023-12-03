from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body

from app.utils.security import JwtAuthDep
from app.models.user import PermissionNames
from app.models.voting import Voting, CreateVotingReq, ActiveVotingResp
from app.models.nominant import Nominant
from app.services.voting_service import VotingService


votings_router = APIRouter(prefix='/votings', tags=['Voting'])


@votings_router.get('/active', response_model=ActiveVotingResp)
def get_active_voting(voting_service: VotingService = Depends(VotingService)):
    try:
        return voting_service.get_one(active=True)
    except KeyError:
        raise HTTPException(status_code=404)
    except ValueError:
        raise HTTPException(status_code=400)


@votings_router.post('/')
def create_voting(
    voting_data: CreateVotingReq,
    voting_service: VotingService = Depends(VotingService),
    user_id: UUID = Depends(JwtAuthDep(PermissionNames.ADMIN))
) -> Voting:
    # try:
    voting = voting_service.add_voting(
        voting_data.title,
        voting_data.description,
        voting_data.start_date,
        voting_data.finish_date,
        user_id if voting_data.admin == None else voting_data.admin
    )

    # except:
    #     print('error')
    return voting


@votings_router.post('/{voting_id}/activate')
def activate_voting(
    voting_id: UUID,
    voting_service: VotingService = Depends(VotingService),
    user_id: UUID = Depends(JwtAuthDep(PermissionNames.ADMIN))
) -> Voting:
    try:
        return voting_service.activate_voting(voting_id)
    except KeyError:
        raise HTTPException(status_code=404)


@votings_router.post('/{voting_id}/addNominant')
def add_nominant(
    voting_id: UUID,
    nomination_id: UUID = Body(alias='nomination_id'),
    nominant: Nominant = Body(alias='nominant'),
    voting_service: VotingService = Depends(VotingService),
    user_id: UUID = Depends(JwtAuthDep(PermissionNames.ADMIN))
) -> Nominant:
    try:
        return voting_service.add_nominant(voting_id, nomination_id, nominant)
    except KeyError:
        raise HTTPException(status_code=404)
    except ValueError:
        raise HTTPException(status_code=400)


# TODO: Block after start
