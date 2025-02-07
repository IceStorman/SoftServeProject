from sqlalchemy.orm import Session
from database.models.token_blocklist import TokenBlocklist
from database.postgres.dto.jwt import jwtDTO
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
import datetime

class jwtDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save_jwt(self, jwt_dto: jwtDTO) -> int:
        if jwt_dto.id:
            jwt_entry = self.get_jwt_by_id(jwt_dto.id)
        else:
            jwt_entry = None

        if jwt_entry:
            jwt_entry = self.update_jwt(jwt_dto.id, jwt_dto)
        else:
            jwt_entry = self.create_jwt(jwt_dto)

        return jwt_entry.id
    
    def save_jwts(self, jwt_dto_list: List[jwtDTO]):
        for jwt in jwt_dto_list:
            self.save_jwt(jwt)

    def create_jwt(self, jwt_dto: jwtDTO) -> TokenBlocklist:
        new_jwt = TokenBlocklist(
            user_id=jwt_dto.user_id,
            jti=jwt_dto.jti,
            token_type=jwt_dto.token_type,
            revoked=jwt_dto.revoked,
            expires_at=jwt_dto.expires_at,
            updated_at=jwt_dto.updated_at or datetime.datetime.utcnow()
        )
        self.db_session.add(new_jwt)
        self.db_session.commit()
        self.db_session.refresh(new_jwt)
        return new_jwt

    def update_jwt(self, jwt_id: int, jwt_dto: jwtDTO) -> TokenBlocklist:
        jwt_entry = self.get_jwt_by_id(jwt_id)
        if jwt_entry:
            jwt_entry.user_id = jwt_dto.user_id
            jwt_entry.jti = jwt_dto.jti
            jwt_entry.token_type = jwt_dto.token_type
            jwt_entry.revoked = jwt_dto.revoked
            jwt_entry.expires_at = jwt_dto.expires_at
            jwt_entry.updated_at = datetime.datetime.utcnow()
            self.db_session.commit()
        return jwt_entry

    def get_jwt_by_id(self, jwt_id: int) -> Optional[TokenBlocklist]:
        return self.db_session.query(TokenBlocklist).filter(TokenBlocklist.id == jwt_id).first()

    def get_jwt_by_jti(self, jti: str) -> Optional[TokenBlocklist]:
        return self.db_session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).first()

    def revoke_jwt(self, jti: str) -> bool:
        jwt_entry = self.get_jwt_by_jti(jti)
        if jwt_entry:
            jwt_entry.revoked = True
            jwt_entry.updated_at = datetime.datetime.utcnow()
            self.db_session.commit()
            return True
        return False

    def delete_expired_tokens(self):
        self.db_session.query(TokenBlocklist).filter(
            TokenBlocklist.expires_at < datetime.datetime.utcnow()
        ).delete(synchronize_session=False)
        self.db_session.commit()
