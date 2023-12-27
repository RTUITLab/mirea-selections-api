from uuid import UUID
from random import shuffle
from fastapi import APIRouter, Depends, HTTPException, Body

from app.models.nominant import Nominant
from app.utils.security import JwtAuthDep
from app.models.user import PermissionNames
from app.models.nomination import UserNomination, UserVote
from app.services.user_service import UserService
from app.services.voting_service import VotingService
from app.models.voting import Voting, CreateVotingReq, ActiveVotingResp


votings_router = APIRouter(prefix='/votings', tags=['Voting'])


@votings_router.get('/active')
def get_active_voting(voting_service: VotingService = Depends(VotingService)) -> ActiveVotingResp:
    try:
        return voting_service.get_one(active=True)
    except KeyError:
        raise HTTPException(status_code=404)
    except ValueError:
        raise HTTPException(status_code=400)


@votings_router.get('/{voting_id}/nominations/{nomination_id}')
def get_nomination_info(
    voting_id: UUID,
    nomination_id: UUID,
    voting_service: VotingService = Depends(VotingService),
    user_service: UserService = Depends(UserService),
    user_id: UUID = Depends(JwtAuthDep(PermissionNames.ADMIN))
) -> UserNomination:
    try:
        nomination = UserNomination.model_validate(voting_service.get_nomiantion(voting_id, nomination_id))
        shuffle(nomination.nominants)
        nomination.vote = user_service.get_nomination_vote(nomination.id, user_id)

        return nomination
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



@votings_router.post('/{voting_id}/vote')
def vote_by_user(
    voting_id: UUID,
    nomination_id: UUID = Body(alias='nomination_id'),
    nominant_id: UUID = Body(alias='nominant_id'),
    user_service: UserService = Depends(UserService),
    voting_service: VotingService = Depends(VotingService),
    user_id: UUID = Depends(JwtAuthDep(''))
) -> UserVote:
    try:
        nomination = voting_service.check_voting_status(voting_id, nomination_id)
        return user_service.vote(nomination.id, nominant_id, user_id)
    except KeyError:
        raise HTTPException(status_code=404)
    except:
        raise HTTPException(status_code=400)


# TODO: Block after start
