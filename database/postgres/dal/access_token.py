from sqlalchemy.orm import Session
from database.models.token_blocklist import TokenBlocklist
from database.postgres.dto.jwt import JwtDTO
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from datetime import datetime
from exept.exeptions import TokenRevokingError


class AccessTokensDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save_access_token(self, jwt_dto: JwtDTO) -> Optional[int]:
        jwt_entry = self.get_jwt_by_id(jwt_dto.id) if jwt_dto.id else None
        if jwt_entry:
            jwt_entry.user_id = jwt_dto.user_id
            jwt_entry.jti = jwt_dto.jti
            jwt_entry.token_type = jwt_dto.token_type
            jwt_entry.revoked = jwt_dto.revoked
            jwt_entry.expires_at = jwt_dto.expires_at
            jwt_entry.updated_at = datetime.utcnow()
        else:
            jwt_entry = TokenBlocklist(**jwt_dto.dict(exclude={"id", "updated_at"}), updated_at=datetime.utcnow())
            self.db_session.add(jwt_entry)

        self.db_session.commit()
        self.db_session.refresh(jwt_entry)
        return jwt_entry.id

    def save_access_tokens(self, jwt_dto_list: List[JwtDTO]):
        for jwt in jwt_dto_list:
            self.save_access_token(jwt)

    def get_access_token_by_id(self, jwt_id: int) -> Optional[TokenBlocklist]:
        return self.db_session.query(TokenBlocklist).filter(TokenBlocklist.id == jwt_id).first()

    def get_access_token_by_jti(self, jti: str) -> Optional[TokenBlocklist]:
        return self.db_session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).first()

    def revoke_access_token(self, jti: str) -> bool:
        try:
            jwt_entry = self.get_access_token_by_jti(jti)
            if jwt_entry:
                jwt_entry.revoked = True
                jwt_entry.updated_at = datetime.utcnow()
                self.db_session.commit()

        except SQLAlchemyError as e:
            raise TokenRevokingError(f"{"token": jti}")

    def revoke_refresh_token(self, jti: str) -> bool:
        jwt_entry = self.get_jwt_by_jti(jti)
        if jwt_entry and jwt_entry.token_type == "refresh":
            jwt_entry.revoked = True
            jwt_entry.updated_at = datetime.utcnow()
            self.db_session.commit()