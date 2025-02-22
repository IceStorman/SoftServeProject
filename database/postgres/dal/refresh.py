from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from datetime import datetime

from database.models.refresh_token_tracking import refresh_token_tracking
from database.models.token_blocklist import Token_Blocklist
from database.postgres.dto.refresh import refreshDTO

class RefreshTokenDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save_refresh_token(self, refresh_dto: refreshDTO, last_ip: str, last_device: str) -> Optional[int]:
        try:
            if refresh_dto.id and (refresh_entry := self.get_refresh_token_by_id(refresh_dto.id)):
                refresh_entry.user_id = refresh_dto.user_id
                refresh_entry.last_ip = last_ip
                refresh_entry.last_device = last_device
                refresh_entry.nonce = refresh_dto.nonce
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

    def get_valid_refresh_token_by_user(self, user_id: int) -> Optional[refresh_token_tracking]:
        return (
            self.db_session.query(refresh_token_tracking)
            .filter(
                refresh_token_tracking.user_id == user_id,
                refresh_token_tracking.refresh_token.has(revoked=False),  
                Token_Blocklist.expires_at > datetime.utcnow()
            )
            .first()
        )

    def get_nonce_by_user_id(self, user_id: int) -> Optional[str]:
        entry = self.db_session.query(refresh_token_tracking).filter(refresh_token_tracking.user_id == user_id).first()
        return entry.nonce if entry else None
    
    def verify_nonce(self, user_id: int, nonce: str) -> bool:
        token_entry = self.db_session.query(refresh_token_tracking).filter_by(user_id=user_id, nonce=nonce).first()
        return token_entry is not None
    
    def update_refresh_token(self, user_id: int, refresh_dto: refreshDTO):
        try:
            entry = (self.db_session.query(refresh_token_tracking)
                .filter(refresh_token_tracking.user_id == user_id)
                .with_for_update()
                .first()
            )
            if entry:
                entry.refresh_token = refresh_dto.refresh_token
                entry.nonce = refresh_dto.nonce
                entry.last_ip = refresh_dto.last_ip
                entry.last_device = refresh_dto.last_device
                self.db_session.commit()
            else:
                self.save_refresh_token(refresh_dto)
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Error in update_refresh_token: {e}")


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
            revoked_count = (
                self.db_session.query(Token_Blocklist)
                .filter(
                    Token_Blocklist.id.in_(
                        self.db_session.query(refresh_token_tracking.id)
                        .filter(refresh_token_tracking.user_id == user_id)
                    ),
                    Token_Blocklist.token_type == "refresh"
                )
                .update({"revoked": True, "updated_at": datetime.utcnow()}, synchronize_session=False)
            )

            self.db_session.commit()
            
            return revoked_count
        except SQLAlchemyError as e:
            self.db_session.rollback()
            return 0