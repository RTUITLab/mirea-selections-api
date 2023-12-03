from uuid import UUID
from fastapi import APIRouter, Depends

from app.utils.security import JwtAuthDep
from app.models.user import PermissionNames
from app.models.voting import Voting, CreateVotingReq
from app.services.voting_service import VotingService


votings_router = APIRouter(prefix='/votings', tags=['Voting'])


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
