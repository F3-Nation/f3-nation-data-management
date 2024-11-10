"""The authentication state."""

import reflex as rx
from sqlmodel import select

from .base import BaseState, User


class AuthState(BaseState):
    """The authentication state for sign up and login page."""

    email: str
    password: str
    confirm_password: str
    login_dialog_open: bool = False

    def signup(self):
        """Sign up a user."""
        with rx.session() as session:
            if self.password != self.confirm_password:
                return rx.window_alert("Passwords do not match.")
            if session.exec(select(User).where(User.email == self.email)).first():
                return rx.window_alert("Email already exists.")
            self.user = User(email=self.email, password=self.password)
            session.add(self.user)
            session.expire_on_commit = False
            session.commit()
            return rx.redirect("/")

    def login(self):
        """Log in a user."""
        with rx.session() as session:
            user = session.exec(select(User).where(User.email == self.email)).first()
            if user and user.password == self.password:
                self.user = user
                # return rx.redirect("/")
                return rx.toast.success("Logged in successfully!")
            else:
                return rx.window_alert("Invalid email or password.")

    def show_tooltip(self):
        """Show a tooltip."""
        print("showing tooltip")
        yield rx.tooltip("hey there", open=True)
        return
