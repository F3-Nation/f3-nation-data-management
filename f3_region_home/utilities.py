import os
import smtplib
from email.message import EmailMessage
from typing import Any


def clear_form_blanks(form_data: dict[str, str]):
    for key, value in form_data.items():
        if value == "":
            form_data[key] = None
    return form_data


def safe_get_convert(data, *keys, conversion: callable = None, args: list = None) -> Any | None:
    if not data:
        return None
    try:
        result = data
        for k in keys:
            if isinstance(k, int) and isinstance(result, list):
                result = result[k]
            elif result.get(k):
                result = result[k]
            else:
                return None
        if conversion:
            args = args or []
            try:
                return conversion(result, *args)
            except TypeError:
                return None
        else:
            return result
    except KeyError:
        return None


def send_magic_link(send_address: str, magic_link: str):
    msg = EmailMessage()
    msg.set_content(
        f"I see you are trying to log into F3's data management portal. Please click this link to log in: {magic_link}"
    )
    msg["Subject"] = "F3 Login"
    msg["From"] = "it.admin@f3nation.com"
    msg["To"] = send_address
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("it.admin@f3nation.com", os.environ.get("F3_EMAIL_PASSWORD"))
    server.send_message(msg)
    server.close()
