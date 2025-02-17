from sqlalchemy.orm import Session
from database.models.token_blocklist import Token_Blocklist
from database.postgres.dto.jwt import jwtDTO
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from datetime import datetime

class jwtDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save_jwt(self, jwt_dto: jwtDTO) -> Optional[int]:
        try:
            if jwt_dto.id and (jwt_entry := self.get_jwt_by_id(jwt_dto.id)):
                jwt_entry.user_id = jwt_dto.user_id
                jwt_entry.jti = jwt_dto.jti
                jwt_entry.token_type = jwt_dto.token_type
                jwt_entry.revoked = jwt_dto.revoked
                jwt_entry.expires_at = jwt_dto.expires_at
                jwt_entry.updated_at = datetime.utcnow()
            else:
                jwt_entry = Token_Blocklist(
                    user_id=jwt_dto.user_id,
                    jti=jwt_dto.jti,
                    token_type=jwt_dto.token_type,
                    revoked=jwt_dto.revoked,
                    expires_at=jwt_dto.expires_at,
                    updated_at=datetime.utcnow()
                )
                self.db_session.add(jwt_entry)

            self.db_session.commit()
            self.db_session.refresh(jwt_entry)
            return jwt_entry.id
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Error in save_jwt: {e}")
            return None

    def save_jwts(self, jwt_dto_list: List[jwtDTO]):
        for jwt in jwt_dto_list:
            self.save_jwt(jwt)

    def get_jwt_by_id(self, jwt_id: int) -> Optional[Token_Blocklist]:
        return self.db_session.query(Token_Blocklist).filter(Token_Blocklist.id == jwt_id).first()

    def get_jwt_by_jti(self, jti: str) -> Optional[Token_Blocklist]:
        return self.db_session.query(Token_Blocklist).filter(Token_Blocklist.jti == jti).first()

    def revoke_jwt(self, jti: str) -> bool:
 
        try:
            jwt_entry = self.get_jwt_by_jti(jti)
            if jwt_entry:
                jwt_entry.revoked = True
                jwt_entry.updated_at = datetime.datetime.utcnow()
                self.db_session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Error in revoke_jwt: {e}")
            return False

    def revoke_refresh_token(self, jti: str) -> bool:
        try:
            jwt_entry = self.get_jwt_by_jti(jti)
            if jwt_entry and jwt_entry.token_type == "refresh":
                jwt_entry.revoked = True
                jwt_entry.updated_at = datetime.datetime.utcnow()
                self.db_session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Error in revoke_refresh_token: {e}")
            return False

    def delete_expired_tokens(self) -> int:
        try:
            expired_count = self.db_session.query(Token_Blocklist).filter(
                Token_Blocklist.expires_at < datetime.datetime.utcnow()
            ).delete(synchronize_session=False)
            self.db_session.commit()
            return expired_count
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Error while deleteng : {e}")
            return 0
