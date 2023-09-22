import os
import requests
from dotenv import load_dotenv

load_dotenv()

create_message_url = os.getenv('USEDESK_API_CREATE_MSG')
update_ticket_url = os.getenv('USEDESK_API_UPDATE_TICKET')
get_additional_fields_url = os.getenv('USEDESK_API_GET_FIELDS')
api_token = os.getenv('USEDESK_API_TOKEN')


def send_message(message, ticket, fls: list[str] = None, agent_id=247423) -> requests.Response:
    payload = {
        "api_token": api_token,
        "ticket_id": ticket,
        "message": message,
        "type": "public",
        "user_id": agent_id,
        "from": "user",
    }
    b_files = [('files[]', open(f, "rb")) for f in fls] if fls else None
    response = requests.post(create_message_url, data=payload, files=b_files)
    if b_files:
        for _, f in b_files:
            f.close()
    return response


def update_ticket(ticket, category_lid, field_id=19402, status=2) -> requests.Response:
    payload = {
        "api_token": api_token,
        "ticket_id": ticket,
        "field_id": field_id,
        "field_value": category_lid,
        "status": status,
    }
    return requests.post(update_ticket_url, data=payload)
