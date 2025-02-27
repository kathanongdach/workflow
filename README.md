# Freshservice Ticket Notifier

## 🇮🇳 ภาษาไทย
### 📚 คำอธิบายโปรแกรม
โปรแกรมนี้ถูกพัฒนาเพื่อดึงข้อมูลตั๋ว (Tickets) จากระบบ **Freshservice** ตามสถานะที่กำหนด และส่งการแจ้งเตือนผ่าน **LINE Notify** เพื่อให้ทีมงานทราบถึงสถานะของตั๋วในแต่ละช่วงเวลาโดยอัตโนมัติ

### 🔄 วัตถุประสงค์ของโปรแกรม
- ตรวจสอบสถานะของตั๋วในระบบ Freshservice ตามช่วงเวลาที่กำหนด
- ส่งรายงานสรุปจำนวนตั๋วในแต่ละสถานะไปยัง LINE Notify
- แจ้งรายละเอียดของตั๋วที่อยู่ในสถานะที่กำหนดให้ทีมงานรับทราบ

### 📅 กำหนดเวลาการทำงาน
โปรแกรมจะทำงานวันละ **3 ครั้ง** ตามเวลาต่อไปนี้:
- ⏰ 09:00 น.
- ⏰ 13:00 น.
- ⏰ 15:00 น.

### 🌐 วิธีใช้งาน
1. **ตั้งค่า API Key และ Token**
   - ตั้งค่าค่า **Freshservice API Key** และ **LINE Notify Token** ผ่านตัวแปรแวดล้อม (Environment Variables) หรือแก้ไขค่าโดยตรงในโค้ด (ไม่แนะนำให้ใส่ค่า API Key ตรง ๆ ในโค้ดเพื่อความปลอดภัย)

2. **ติดตั้งไลบรารีที่จำเป็น**
   ```bash
   pip install requests
   ```

3. **รันโปรแกรม**
   ```bash
   python LineNotification_Fresh.py
   ```

4. **ตั้งค่าให้รันอัตโนมัติ**
   - สามารถตั้งเวลาให้โปรแกรมรันอัตโนมัติผ่าน **GitHub Actions** หรือ **Cron Job** บนเซิร์ฟเวอร์ฟรี

### 🔗 API และ Endpoints ที่ใช้
- **Freshservice API:** `https://itcentral.freshservice.com/api/v2/tickets/filter?workspace_id=4&query="status:X"`
- **LINE Notify API:** `https://notify-api.line.me/api/notify`

### 🛠️ ตัวอย่างโค้ดที่สำคัญ
- การดึงข้อมูลตั๋วจาก Freshservice
  ```python
  def get_tickets_by_status(status):
      url = FRESHSERVICE_URL + f'status:{status}'
      response = requests.get(url, headers=HEADERS_FRESHSERVICE)
      data = response.json()
      return data.get("tickets", [])
  ```

- การส่งแจ้งเตือนผ่าน LINE Notify
  ```python
  def send_line_notification(message):
      url = "https://notify-api.line.me/api/notify"
      payload = {"message": message}
      requests.post(url, headers=HEADERS_LINE, data=payload)
  ```

---

## 🇬🇧 English
### 📚 Program Description
This program is designed to retrieve **Freshservice** tickets based on specified statuses and send notifications via **LINE Notify** to inform the team about ticket statuses at scheduled times automatically.

### 🔄 Purpose
- Monitor the status of tickets in Freshservice at scheduled intervals.
- Send a summary report of ticket counts by status to LINE Notify.
- Provide details of tickets in specified statuses to keep the team informed.

### 📅 Scheduled Execution Times
The program runs **three times daily** at:
- ⏰ 09:00 AM
- ⏰ 01:00 PM
- ⏰ 03:00 PM

### 🌐 How to Use
1. **Set API Key and Token**
   - Configure **Freshservice API Key** and **LINE Notify Token** via environment variables or modify the code directly (not recommended for security reasons).

2. **Install Required Libraries**
   ```bash
   pip install requests
   ```

3. **Run the Program**
   ```bash
   python LineNotification_Fresh.py
   ```

4. **Automate Execution**
   - The program can be scheduled using **GitHub Actions** or **Cron Jobs** on a free server.

### 🔗 APIs and Endpoints Used
- **Freshservice API:** `https://itcentral.freshservice.com/api/v2/tickets/filter?workspace_id=4&query="status:X"`
- **LINE Notify API:** `https://notify-api.line.me/api/notify`

### 🛠️ Key Code Examples
- Fetching tickets from Freshservice
  ```python
  def get_tickets_by_status(status):
      url = FRESHSERVICE_URL + f'status:{status}'
      response = requests.get(url, headers=HEADERS_FRESHSERVICE)
      data = response.json()
      return data.get("tickets", [])
  ```

- Sending notifications via LINE Notify
  ```python
  def send_line_notification(message):
      url = "https://notify-api.line.me/api/notify"
      payload = {"message": message}
      requests.post(url, headers=HEADERS_LINE, data=payload)
  ```

---

### 🛡️ Security Notes
- Ensure API keys and tokens are stored securely using environment variables.
- Avoid hardcoding credentials directly in the script.

This program helps automate ticket monitoring and notifications, ensuring the team stays updated with minimal manual effort.

