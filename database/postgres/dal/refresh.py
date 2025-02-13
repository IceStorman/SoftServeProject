from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from datetime import datetime

from database.models.refresh_token_tracking import refresh_token_tracking
from database.models.token_blocklist import Token_Blocklist
from database.postgres.dto.jwt import jwtDTO

class RefreshTokenDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save_refresh_token(self, jwt_dto: jwtDTO, last_ip: str, last_device: str) -> Optional[int]:
        try:
            # Перевіряємо, чи вже є такий токен
            if jwt_dto.id and (refresh_entry := self.get_refresh_token_by_id(jwt_dto.id)):
                refresh_entry.user_id = jwt_dto.user_id
                refresh_entry.last_ip = last_ip
                refresh_entry.last_device = last_device
            else:
                refresh_entry = refresh_token_tracking(
                    id=refresh_dto.id, 
                    user_id=refresh_dto.user_id,
                    last_ip=last_ip,
                    last_device=last_device
                )
                self.db_session.add(refresh_entry)

            self.db_session.commit()
            self.db_session.refresh(refresh_entry)
            return refresh_entry.id
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Error in save_refresh_token: {e}")
            return None

    def get_refresh_token_by_id(self, refresh_id: int) -> Optional[refresh_token_tracking]:
        return self.db_session.query(refresh_token_tracking).filter(refresh_token_tracking.id == refresh_id).first()

    def get_refresh_token_by_user(self, user_id: int) -> Optional[refresh_token_tracking]:
        return self.db_session.query(refresh_token_tracking).filter(refresh_token_tracking.user_id == user_id).first()

    def revoke_refresh_token(self, refresh_id: int) -> bool:
        try:
            refresh_entry = self.get_refresh_token_by_id(refresh_id)
            if refresh_entry:
                token_entry = self.db_session.query(Token_Blocklist).filter(Token_Blocklist.id == refresh_id).first()
                if token_entry and token_entry.token_type == "refresh":
                    token_entry.revoked = True
                    token_entry.updated_at = datetime.utcnow()
                    self.db_session.commit()
                    return True
            return False
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Error in revoke_refresh_token: {e}")
            return False

    def revoke_all_refresh_tokens_for_user(self, user_id: int) -> int:
        try:
            refresh_entries = self.db_session.query(refresh_token_tracking).filter(
                refresh_token_tracking.user_id == user_id
            ).all()
            
            revoked_count = 0
            for entry in refresh_entries:
                token_entry = self.db_session.query(Token_Blocklist).filter(Token_Blocklist.id == entry.id).first()
                if token_entry and token_entry.token_type == "refresh":
                    token_entry.revoked = True
                    token_entry.updated_at = datetime.utcnow()
                    revoked_count += 1
            
            self.db_session.commit()
            return revoked_count
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Error in revoke_all_refresh_tokens_for_user: {e}")
            return 0