from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from datetime import datetime
from database.models.refresh_token_tracking import RefreshTokenTracking
from database.models.users import User
from database.models.token_blocklist import TokenBlocklist
from database.postgres.dto.refresh import RefreshTokenDTO
from marshmallow import ValidationError
from exept.exeptions import CustomQSportException, TokenUpdatingError, TokenRevokingError, TokenSavingError
from exept.handle_exeptions import get_custom_error_response
from service.api_logic.models.api_models import REFRESH



class RefreshTokenDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save_refresh_token(self, refresh_dto: RefreshTokenDTO) -> Optional[int]: 
            try:
                refresh_entry = None
                
                if refresh_dto.id:
                    refresh_entry = self.get_refresh_token_by_id(refresh_dto.id)

                if refresh_entry:
                    refresh_entry.user_id = refresh_dto.user_id
                    refresh_entry.last_ip = refresh_dto.last_ip
                    refresh_entry.last_device = refresh_dto.last_device
                    refresh_entry.nonce = refresh_dto.nonce
                else:
                    refresh_entry = RefreshTokenTracking(
                        id = refresh_dto.id,
                        user_id=refresh_dto.user_id,
                        last_ip=refresh_dto.last_ip,
                        last_device=refresh_dto.last_device,
                        nonce=refresh_dto.nonce
                    )
                    self.db_session.add(refresh_entry)

                self.db_session.commit()
                self.db_session.refresh(refresh_entry)
                return refresh_entry.id
            except SQLAlchemyError as e:
                raise (f"Error in save_refresh_token: {e}")
  


    def get_refresh_token_by_id(self, refresh_id: int) -> Optional[RefreshTokenTracking]:
        return self.db_session.query(RefreshTokenTracking).filter(RefreshTokenTracking.id == refresh_id).first()

    def get_valid_refresh_token_by_user(self, user_id: int) -> Optional[RefreshTokenTracking]:
        return (
            self.db_session.query(RefreshTokenTracking)
            .filter(
                RefreshTokenTracking.user_id == user_id,
                TokenBlocklist.revoked == False,  
                TokenBlocklist.expires_at > datetime.utcnow()
            )
            .first()
        )
    
    def get_user_info_by_nonce(self, nonce) -> int:
        token_entry = self.db_session.query(RefreshTokenTracking).filter(RefreshTokenTracking.nonce == nonce).first()
        user_info = self.db_session.query(User).filter(User.user_id == token_entry.user_id)
        return user_info if user_info else None

    def verify_nonce(self, user_id: int, nonce: str) -> bool:
        token_entry = self.db_session.query(RefreshTokenTracking).filter_by(user_id=user_id, nonce=nonce).first()
        return token_entry is not None

    def is_nonce_used(self,user_id: int, nonce: str) -> bool:
        nonce = self.db_session.query(RefreshTokenTracking).filter_by(user_id=user_id, nonce=nonce).first()
        return nonce is not None
        
    def update_refresh_token(self, user_id: int, refresh_dto: RefreshTokenDTO):
        entry = (self.db_session.query(RefreshTokenTracking)
            .filter(RefreshTokenTracking.user_id == user_id)
            .with_for_update()
            .first()
        )
        if entry:
            entry.user_id = refresh_dto.user_id
            entry.nonce = refresh_dto.nonce
            entry.last_ip = refresh_dto.last_ip
            entry.last_device = refresh_dto.last_device
            self.db_session.commit()
        else:
            self.save_refresh_token(refresh_dto)


    def revoke_refresh_token(self, refresh_id: int) -> bool:
        refresh_entry = self.get_refresh_token_by_id(refresh_id)
        if refresh_entry:
            token_entry = self.db_session.query(TokenBlocklist).filter(TokenBlocklist.id == refresh_id).first()
            if token_entry and token_entry.token_type == REFRESH:
                token_entry.revoked = True
                token_entry.updated_at = datetime.utcnow()
                self.db_session.commit()

    def revoke_all_refresh_and_access_tokens_for_user(self, user_id: int) -> int:
        revoked_count = (
            self.db_session.query(TokenBlocklist)
            .join(RefreshTokenTracking, RefreshTokenTracking.id == TokenBlocklist.id)
            .filter(
                RefreshTokenTracking.user_id == user_id,
                TokenBlocklist.token_type.in_(["refresh", "access"])
            )
            .update({"revoked": True, "updated_at": datetime.utcnow()}, synchronize_session=False)
        )
            
        self.db_session.commit()
            
        return revoked_count
    
    