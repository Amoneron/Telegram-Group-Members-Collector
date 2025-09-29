# Telegram Group Members Collector

A professional Python tool for collecting information about Telegram group/channel members with two parsing modes: direct members list and message-based extraction.

## Features

- **Two Parsing Modes:**
  - **Members Mode**: Direct extraction from group members list
  - **Messages Mode**: Extract unique users from message history (useful when member list is hidden)

- **Professional Architecture:**
  - Modular code structure with separate parsers
  - Rate limiting to respect Telegram API limits
  - Progress bar with ETA for long operations
  - Efficient deduplication (processes each user only once)

- **Data Export:**
  - JSON format with complete user information
  - Organized output in `results/` directory
  - Timestamped files for version control

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Amoneron/Telegram-Group-Members-Collector.git
cd Telegram-Group-Members-Collector
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API credentials (optional):
```bash
cp .env.example .env
# Edit .env with your API credentials
```

## Usage

### First Time Authorization

Before first use, you need to authorize with Telegram:

```bash
python main.py --auth
```

Enter your phone number and verification code when prompted.

### Parsing Modes

#### 1. Members List Mode

Extract members directly from the group's member list:

```bash
python main.py -c CHAT_ID -m members
```

Example:
```bash
python main.py -c -1001358652190 -m members
```

#### 2. Messages Mode

Extract unique users from message history (useful when member list is restricted):

```bash
python main.py -c CHAT_ID -m messages -d DAYS
```

Parameters:
- `-c, --chat`: Chat ID (required)
- `-m, --mode`: Parsing mode: `members` or `messages` (required)
- `-d, --days`: Number of days to scan (default: 7, for messages mode only)

Example:
```bash
python main.py -c -1001358652190 -m messages -d 30
```

### Getting Chat ID

To find a chat's ID:
1. Forward a message from the chat to @userinfobot
2. Or use web.telegram.org and check the URL
3. Group IDs typically start with -100

## Running in Background (tmux)

For long-running parsing sessions, use tmux:

```bash
# Create new tmux session
tmux new -s telegram_parser

# Activate virtual environment
source venv/bin/activate

# Run parser (example: 60 days of messages)
python main.py -c -1001358652190 -m messages -d 60

# Detach from tmux: Press Ctrl+B, then D

# Reattach to session later
tmux attach -t telegram_parser

# List all sessions
tmux ls

# Kill session when done
tmux kill-session -t telegram_parser
```

## Output Format

Results are saved in `results/` directory as JSON files:

```json
{
  "chat_name": "Group Name",
  "chat_id": -1001234567890,
  "parsing_mode": "messages",
  "members_count": 150,
  "extraction_date": "2024-01-01T12:00:00",
  "parameters": {
    "days": 30
  },
  "members": [
    {
      "id": 123456789,
      "username": "username",
      "first_name": "First",
      "last_name": "Last",
      "is_premium": true,
      "extracted_at": "2024-01-01T12:00:00"
    }
  ]
}
```

## Project Structure

```
.
├── main.py              # Entry point
├── config.py            # Configuration
├── parsers/            # Parsing modules
│   ├── base.py         # Base parser class
│   ├── members_parser.py  # Members list parser
│   └── messages_parser.py # Messages parser
├── utils/              # Utilities
│   ├── rate_limiter.py  # Rate limiting
│   ├── progress.py     # Progress tracking
│   └── data_export.py  # Data export
├── results/            # Output directory (gitignored)
└── requirements.txt    # Dependencies
```

## Rate Limiting

The tool implements careful rate limiting:
- Automatic delay between requests
- Handles FloodWaitError gracefully
- Respects Telegram's API limits

## Requirements

- Python 3.7+
- Telegram API credentials (API_ID and API_HASH)
- Active Telegram account

## License

MIT

## Contributing

Pull requests are welcome. For major changes, please open an issue first.