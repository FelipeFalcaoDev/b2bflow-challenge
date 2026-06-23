# b2bflow WhatsApp Message Sender

Python script that reads contacts from Supabase and sends personalized WhatsApp messages via Z-API.

## Setup

### 1. Database Table

Create the `contacts` table in your Supabase project using the SQL Editor:

```sql
CREATE TABLE contacts (
  id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name VARCHAR(100) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

Grant SELECT permission to the anonymous role:

```sql
GRANT SELECT ON public.contacts TO anon;
```

### 2. Insert Sample Contacts

Add contacts to the table (use international phone format):

```sql
INSERT INTO contacts (name, phone) VALUES
  ('João Silva', '5585988776655'),
  ('Maria Santos', '5585987654321'),
  ('Pedro Costa', '5585986543210');
```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_API_KEY=your-anon-key-here
SUPABASE_TABLE_NAME=contacts

# Z-API Configuration
ZAPI_URL=https://api.z-api.io/instances/YOUR_INSTANCE_ID/token/YOUR_TOKEN/send-text
```

**Get these values from:**
- **Supabase:** Settings → API → Project URL and anon key
- **Z-API:** Your instance settings in the dashboard

## How to Run

1. **Clone the repository:**

```bash
git clone https://github.com/FelipeFalcaoDev/b2bflow-challenge.git
cd b2bflow-challenge
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**

Copy `.env.example` to `.env` and fill in your credentials.

4. **Run the script:**

```bash
python main.py
```

### Expected Output

```
2026-06-23 16:38:54,853 - INFO - Starting b2bflow WhatsApp Message Sender
2026-06-23 16:38:54,854 - INFO - ✓ Configuration loaded successfully
2026-06-23 16:38:55,038 - INFO - ✓ Found 3 contact(s)
2026-06-23 16:38:55,834 - INFO - ✓ Z-API client initialized
2026-06-23 16:38:56,017 - INFO - ✓ Sending completed: 3 sent, 0 failed
```

## Project Structure

```
b2bflow-challenge/
├── src/
│   ├── config.py
│   ├── supabase_client.py
│   └── whatsapp_sender.py
├── .env.example
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Notes

- Messages are limited to 3 contacts per run (default) to comply with Z-API free tier quotas
- Phone numbers must be in international format (e.g., country code + area code + number)
- Each contact must have both `name` and `phone` fields or will be skipped