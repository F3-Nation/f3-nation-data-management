from typing import List, Optional

import reflex as rx

from ..database.models import User
from ..database.queries import user_search
from ..state.base import BaseState


class SettingsState(BaseState):
    top_search_users: List[User] = []

    def delete_admin_user(self, user: User):
        print("Delete admin user")
        pass

    def add_admin_user(self, user: User):
        print("Add admin user")
        pass

    def search_users(self, search_str: str):
        self.top_search_users = []
        if search_str:
            self.top_search_users = user_search(search_str, region=self.region, limit=5)
        return
