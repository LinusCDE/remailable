from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from pynamodb.constants import PAY_PER_REQUEST_BILLING_MODE


class UserModel(Model):
    """
    A Remailable User
    """

    class Meta:
        table_name = "remailable-user"
        region = "us-east-1"
        billing_mode = PAY_PER_REQUEST_BILLING_MODE

    email = UnicodeAttribute(hash_key=True)
    device = UnicodeAttribute()
    user = UnicodeAttribute()


if not UserModel.exists():
    UserModel.create_table(wait=True)


class UserLookerUpper:
    def __init__(self):
        pass

    def get_config_for_user(self, user_email: str) -> dict:
        try:
            cfg = UserModel.get(user_email)
        except:
            raise KeyError(f"Failed key lookup for {user_email}.")
        return {"devicetoken": cfg.device, "usertoken": cfg.user}

    def add_user_config(self, user_email: str, config: dict) -> bool:
        # TODO: Should do an upsert here.
        # When inevitably someone double-registers, this will bork.
        # Probably it'll be me, and I'll be so upset at first, and then I'll be
        # so glad I wrote this comment.
        UserModel(
            email=user_email, device=config["devicetoken"], user=config["usertoken"]
        ).save()
        return True

    def renew_user_token(self, user_email: str) -> bool:
        raise NotImplementedError()


def sanitize_email(user_email: str) -> str:
    """
    Given a formatted email like "Jordan M <remailable@getneutrality.org>",
    return just the "remailable@getneutrality.org" part.
    """
    email_part = user_email.split()[-1]
    if email_part.startswith("<"):
        email_part = email_part[1:]
    if email_part.endswith(">"):
        email_part = email_part[:-1]
    return email_part


def get_config_for_user(user_email: str) -> dict:
    """
    Returns a config dict for the given user, based upon email.
    """
    user_email = sanitize_email(user_email)
    return UserLookerUpper().get_config_for_user(user_email)


def set_config_for_user(user_email: str, new_cfg: dict) -> bool:
    """
    Sets a config dict for the given user, based upon email.
    """
    user_email = sanitize_email(user_email)
    return UserLookerUpper().add_user_config(user_email, new_cfg)
