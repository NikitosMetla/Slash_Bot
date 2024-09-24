from .admin_repo import AdminRepository
from .ai_recommendations_repo import AiRecommendationsRepository
from .ai_requests_repo import AiRequestsRepository
from .design_level_repo import DesignLevelRepository
from .earnings_level_repo import EarningsLevelRepository
from .mentor_repo import MentorRepository
from .operations_repo import OperationRepository
from .send_link_repo import SendLinkRepository
from .users_repo import UserRepository


users_repository = UserRepository()
operation_repository = OperationRepository()
ai_requests_repository = AiRequestsRepository()
mentor_repository = MentorRepository()
send_link_repository = SendLinkRepository()
design_level_repository = DesignLevelRepository()
earnings_level_repository = EarningsLevelRepository()
admin_repository = AdminRepository()
ai_recommendations_repository = AiRecommendationsRepository()

__all__ = ['users_repository',
           'operation_repository',
           'ai_requests_repository',
           'send_link_repository',
           'design_level_repository',
           'earnings_level_repository',
           'mentor_repository',
           'admin_repository',
           'ai_recommendations_repository'
          ]