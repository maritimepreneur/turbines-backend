from sqlalchemy.orm import Session
from app.models.profiles import Profile
from app.services.base_service import BaseService
from app.utils import response


class ProfileService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db, Profile).__annotations__

    def create(self, profile_data):
        """ Create Profile """
        return super().create(profile_data)

    def get_profile_by_id(self, profile_id):
        """ Get Profile by ID """
        profile = self._get_by_id(profile_id)
        if not profile:
            return response(404, "Profile not found", None)
        return response(200, "Success", profile)

    def update_profile_by_id(self, profile_id, updated_data):
        """ Update Profile """
        profile = self._get_by_id(profile_id)
        if not profile:
            return response(404, "Profile not found", None)
        return super().update(profile_id, updated_data)

    def delete_profile_by_id(self, profile_id):
        """ Delete Profile """
        profile = self._get_by_id(profile_id)
        if not profile:
            return response(404, "Profile not found", None)
        return super().delete(profile_id)
