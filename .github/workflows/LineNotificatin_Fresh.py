import requests
import json
import os
import base64

# --- Configuration ---
FRESHSERVICE_API_KEY = os.environ.get("FRESHSERVICE_API_KEY", "fOXn9aKFyCDjX53U4Ut")  
LINE_NOTIFY_TOKEN = os.environ.get("LINE_NOTIFY_TOKEN", "Dpkgr0TtrzhITYb7PrPjM0eeBD6hkVKAQCbbV0Bd9qH")  

FRESHSERVICE_URL = "http://itcentral.freshservice.com/api/v2/tickets/filter?workspace_id=4&query="

# Encode API Key (Base64)
api_key_encoded = base64.b64encode(f"{FRESHSERVICE_API_KEY}:X".encode()).decode()

HEADERS_FRESHSERVICE = {
    "Authorization": f"Basic {api_key_encoded}",
    "Content-Type": "application/json"
}

HEADERS_LINE = {
    "Authorization": f"Bearer {LINE_NOTIFY_TOKEN}",
    "Content-Type": "application/x-www-form-urlencoded"
}

# --- Functions ---
def get_tickets_by_status(status):
    """Fetches tickets from Freshservice API for a given status."""
    query = f'"status:{status}"'  # ต้องใช้เครื่องหมายอัญประกาศรอบ query
    url = FRESHSERVICE_URL + query
    try:
        response = requests.get(url, headers=HEADERS_FRESHSERVICE)
        response.raise_for_status()
        data = response.json()
        return data.get("tickets", [])
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP Error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Request Error: {req_err}")
    
    print(f"🔍 Debug Info: URL = {url}, Headers = {HEADERS_FRESHSERVICE}")
    return []

def send_line_notification(message):
    """Sends a message to Line Notify."""
    url = "https://notify-api.line.me/api/notify"
    payload = {"message": message}
    try:
        response = requests.post(url, headers=HEADERS_LINE, data=payload)
        response.raise_for_status()
        print(f"✅ Line notification sent: {message}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending Line notification: {e}")

def format_ticket_details(tickets, status_name):
    """Format the ticket details to be shown in Line."""
    if not tickets:
        return f"No tickets in {status_name}"
    
    message = f"--- Tickets in {status_name} ---\n"
    for ticket in tickets[:5]:  # จำกัด 5 รายการเพื่อป้องกันข้อความยาวเกินไป
        message += f"- ID: {ticket['id']}\n"
        message += f"  Subject: {ticket['subject'][:255]}...\n"
        message += f"  Created: {ticket['created_at']}\n"
        message += f"  Updated: {ticket['updated_at']}\n"
        message += "----------------------------\n"
    return message

def main():
    """Main function to orchestrate the ticket monitoring and Line notifications."""
    statuses = {
        2: "Open",
        3: "Pending",
        5: "Closed"
    }
    
    overall_summary_message = "--- Ticket Status Summary ---\n"
    
    for status, status_name in statuses.items():
        tickets = get_tickets_by_status(status)
        ticket_count = len(tickets)
        overall_summary_message += f"- {status_name}: {ticket_count} ticket(s)\n"

        if ticket_count > 0:
            detail_message = format_ticket_details(tickets, status_name)
            send_line_notification(detail_message)

    send_line_notification(overall_summary_message)

if __name__ == "__main__":
    main()
