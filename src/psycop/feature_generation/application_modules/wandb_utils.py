"""Wandb utils.""" ""
import traceback

import wandb


def wandb_alert_on_exception(func):  # noqa
    """Alerts wandb on exception."""

    def wrapper(*args, **kwargs):  # noqa
        try:
            return func(*args, **kwargs)
        except Exception as e:
            wandb.alert(title="Run crashed", text=traceback.format_exc())
            raise e

    return wrapper
