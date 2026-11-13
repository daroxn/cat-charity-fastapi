from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation, User
from app.repositories.base import BaseCharityRepository


class DonationRepository(BaseCharityRepository):
    """Репозиторий для работы с пожертвованиями."""

    async def get_by_user(
        self,
        session: AsyncSession,
        user: User,
    ) -> Sequence[Donation]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = DonationRepository(Donation)
