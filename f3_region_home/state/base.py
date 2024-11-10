"""Base state for the application. All other states inherit from this state."""

from typing import Optional

import reflex as rx
from reflex_magic_link_auth import MagicLinkAuthState

from ..database.db_manager import DbManager
from ..database.models import Org, User
from ..database.queries import RegionData, get_user_roles
from ..utilities import send_magic_link

REGION_LIST = Org.get_all_regions()


class BaseState(MagicLinkAuthState):
    """The base state for the app."""

    user: Optional[User] = None
    user_is_admin: bool = False
    region: Optional[Org] = None
    region_data: Optional[RegionData] = None
    region_list: list[tuple[str, str]] = REGION_LIST
    login_error: str = ""
    magic_link: Optional[str] = None
    awaiting_otp: bool = False

    # def logout(self):
    #     """Log out a user."""
    #     self.reset()
    #     return

    def full_logout(self):
        self.logout()
        self.user = None
        self.user_is_admin = False

    def check_login(self):
        """Check if a user is logged in."""
        if not self.session_is_valid:
            self.user = None
        else:
            if self.user is None:
                self.user = DbManager.find_first_record(User, [User.email == self.auth_session.email])
                self.awaiting_otp = False
                # redirect to user profile page if user is not in the database

    def switch_region(self, region_id: str):
        """Switch the region."""
        self.region = DbManager.get(Org, int(region_id))
        self.region_data = RegionData(self.region.id)
        if self.user:
            self.user_is_admin = "Admin" in get_user_roles(self.user.id, self.region.id)

    @rx.var
    def logged_in(self) -> bool:
        """Check if a user is logged in."""
        return self.user is not None

    @rx.var
    def region_id_str(self) -> str:
        """Get the region ID as a string."""
        if self.region:
            return str(self.region.id)
        else:
            return "0"

    @rx.var
    def region_selected(self) -> bool:
        """Check if a region is selected."""
        return self.region is not None

    @rx.var(cache=True)
    def is_prod_mode(self):
        return rx.utils.exec.is_prod_mode()

    async def handle_submit_login(self, form_data):
        # magic_link = await self.get_state(MagicLinkAuthState)
        self.login_error = ""
        record, otp = self._generate_otp(form_data["email"])
        if otp is None:
            if record is not None:
                self.login_error = "Too many attempts. Please try again later."
            else:
                self.login_error = "Invalid email, or too many attempts. Please try again later."
            return
        # if self.is_prod_mode:
        #     recaptcha_state = await self.get_state(
        #         reflex_google_recaptcha_v2.GoogleRecaptchaV2State
        #     )
        #     if not recaptcha_state.token_is_valid:
        #         self.login_error = "Captcha verification failed. Please try again."
        #         return
        self.awaiting_otp = True
        # yield rx.redirect("/check-your-email")
        if self.is_prod_mode:
            pass
            # try:
            #     send_magic_link_mailgun(
            #         record.email,
            #         magic_link._get_magic_link(record, otp),
            #     )
            # except Exception as e:
            #     print(e)
        else:
            print(self._get_magic_link(record, otp))
            self.magic_link = self._get_magic_link(record, otp)
            send_magic_link(record.email, self.magic_link)
