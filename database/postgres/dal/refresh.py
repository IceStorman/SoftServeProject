from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from datetime import datetime
from database.models.refresh_token_tracking import RefreshTokenTracking
from database.models.token_blocklist import TokenBlocklist
from database.postgres.dto.refresh import RefreshTokenDTO
from marshmallow import ValidationError
from exept.exeptions import CustomQSportException, TokenUpdatingError, TokenRevokingError, TokenSavingError
from exept.handle_exeptions import get_custom_error_response


REFRESH = "refresh"

class RefreshTokenDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save_refresh_token(self, refresh_dto: RefreshTokenDTO) -> Optional[int]:
        try:
            refresh_entry = None
            
            if refresh_dto.id:
                refresh_entry = self.get_refresh_token_by_id(refresh_dto.id)

            if refresh_entry:
                data = self.schema.dump(refresh_dto)
                for key, value in data.items():
                    setattr(refresh_entry, key, value)
            else:
                refresh_entry = RefreshTokenTracking(**self.schema.load(refresh_dto.dict()))
                self.db_session.add(refresh_entry)

            self.db_session.commit()
            self.db_session.refresh(refresh_entry)
            return refresh_entry.id

        except ValidationError as ve:
            raise f"Validation error: {ve.messages}"
        except TokenSavingError as e:
            raise get_custom_error_response(e)


    def get_refresh_token_by_id(self, refresh_id: int) -> Optional[RefreshTokenTracking]:
        return self.db_session.query(RefreshTokenTracking).filter(RefreshTokenTracking.id == refresh_id).first()

    def get_valid_refresh_token_by_user(self, user_id: int) -> Optional[RefreshTokenTracking]:
        return (
            self.db_session.query(RefreshTokenTracking)
            .filter(
                RefreshTokenTracking.user_id == user_id,
                RefreshTokenTracking.refresh_token.has(revoked=False),  
                TokenBlocklist.expires_at > datetime.utcnow()
            )
            .first()
        )

    def verify_nonce(self, user_id: int, nonce: str) -> bool:
        token_entry = self.db_session.query(RefreshTokenTracking).filter_by(user_id=user_id, nonce=nonce).first()
        return token_entry is not None

    def is_nonce_used(self,user_id: int, nonce: str) -> bool:
        nonce = self.db_session.query(RefreshTokenTracking).filter_by(user_id=user_id, nonce=nonce).first()
        if nonce: 
            return True
        return False
        
    def update_refresh_token(self, user_id: int, refresh_dto: RefreshTokenDTO):
        try:
            entry = (self.db_session.query(RefreshTokenTracking)
                .filter(RefreshTokenTracking.user_id == user_id)
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
        except TokenUpdatingError as e:
            return get_custom_error_response(e)

    def revoke_refresh_token(self, refresh_id: int) -> bool:
        try:
            refresh_entry = self.get_refresh_token_by_id(refresh_id)
            if refresh_entry:
                token_entry = self.db_session.query(TokenBlocklist).filter(TokenBlocklist.id == refresh_id).first()
                if token_entry and token_entry.token_type == REFRESH:
                    token_entry.revoked = True
                    token_entry.updated_at = datetime.utcnow()
                    self.db_session.commit()
        except CustomQSportException as e:
            TokenRevokingError(e)

    def revoke_all_refresh_and_access_tokens_for_user(self, user_id: int) -> int:
        try:
            revoked_count = (
                self.db_session.query(TokenBlocklist)
                .filter(
                    self.db_session.query(TokenBlocklist).join(RefreshTokenTracking, RefreshTokenTracking.id == TokenBlocklist.id).filter(
                        RefreshTokenTracking.user_id == user_id,
                        TokenBlocklist.token_type == "refresh" 
                    )
                )
                .update({"revoked": True, "updated_at": datetime.utcnow()}, synchronize_session=False)
            )

            self.db_session.commit()
            
            return revoked_count
        except TokenRevokingError as e:
            get_custom_error_response(e)