from typing import cast, Dict

from django.contrib.auth.models import AbstractUser
from ninja import Schema
from ninja_extra import api_controller, route
from ninja_extra.permissions import AllowAny
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.schema import TokenObtainPairInputSchema
from ninja_jwt.tokens import RefreshToken


"""
This module contains the controller and related schemas for the token generation
"""


class UserSchema(Schema):
    first_name: str
    email: str
    username: str


class MyTokenObtainPairOutSchema(Schema):
    refresh: str
    access: str
    user: UserSchema
    duration: int


class MyTokenObtainPairSchema(TokenObtainPairInputSchema):
    def output_schema(self):
        out_dict = self.get_response_schema_init_kwargs()
        out_dict.update(user=UserSchema.from_orm(self._user))
        return MyTokenObtainPairOutSchema(**out_dict)

    @classmethod
    def get_token(cls, user: AbstractUser) -> Dict:
        values = {}
        refresh = RefreshToken.for_user(user)
        refresh = cast(RefreshToken, refresh)
        values["refresh"] = str(refresh)
        values["access"] = str(refresh.access_token)
        values["duration"] = refresh.access_token.payload['exp'] - refresh.access_token.payload['iat']
        return values


@api_controller('/token', permissions=[AllowAny], tags=["Auth"], auth=None)
class MyTokenObtainPairController(NinjaJWTDefaultController):
    @route.post(
        "/pair", response=MyTokenObtainPairOutSchema, url_name="token_obtain_pair"
    )
    def obtain_token(self, user_token: MyTokenObtainPairSchema):
        return user_token.output_schema()
