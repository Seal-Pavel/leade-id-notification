def _is_update_automatically(admin_panel) -> bool:
    return admin_panel.set_admin_bearer()


def is_bearer_valid(admin_panel) -> bool:
    if not admin_panel.is_admin_bearer_valid() and not _is_update_automatically(admin_panel):
        return False
    else:
        return True
