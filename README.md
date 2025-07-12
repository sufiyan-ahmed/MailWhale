# 🐋 MailWhale - Gmail Email Automation

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Gmail](https://img.shields.io/badge/Gmail-SMTP-red.svg)](https://support.google.com/mail/answer/7126229)
[![MailWhale](https://img.shields.io/badge/MailWhale-🐋-blue.svg)](#)

**Dive deep into email automation!** 🌊

MailWhale is a powerful Python tool that makes waves in email marketing by automating personalized email campaigns through your Gmail account. Like a whale navigating the vast ocean, MailWhale handles massive email lists with grace and precision.

## 🌊 Features That Make Waves

- 🐋 **Whale-Scale Sending** - Handle massive email lists like a gentle giant
- 🎯 **Deep Personalization** - Dive into dynamic content with smart placeholders
- 📝 **Ocean of Templates** - JSON-based email templates that flow seamlessly
- 📎 **Treasure Attachments** - Send files along with your messages
- 📊 **Sonar Logging** - Track every email's journey through the depths
- 🛡️ **Whale Wisdom** - Intelligent error handling and retry logic
- ⏱️ **Tide Control** - Smart delays to avoid spam detection currents
- 🔒 **Deep Sea Security** - Credentials protected in the ocean depths

## 🌊 Getting Started - Dive In!

### 1. 🔐 Enable Gmail App Password

1. Go to your Google Account settings
2. Enable 2-Factor Authentication if not already enabled
3. Go to Security → 2-Step Verification → App passwords
4. Generate a new app password for "Mail"
5. Copy the 16-character password

### 2. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. 🌊 Configure Your Ocean (Environment Variables)

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your Gmail credentials:
```env
GMAIL_EMAIL=your_email@gmail.com
GMAIL_PASSWORD=your_16_character_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

⚠️ **Important**: Never commit `.env` to version control!

### 4. 📜 Prepare Your School of Fish (Recipients List)

Edit `recipients.csv` with your recipient data:
```csv
name,email,company,position
John Doe,john.doe@example.com,Tech Corp,Developer
Jane Smith,jane.smith@example.com,Design Inc,Designer
```

### 5. 📜 Craft Your Message Bottle (Email Template)

Edit `email_template.json`:
```json
{
    "subject": "Hello {name}, Important Update",
    "body": "Dear {name},\n\nYour message here...\n\nBest regards"
}
```

## 🐋 Usage - Let MailWhale Swim!

### 🌊 Basic Usage
```python
from email_sender import EmailSender

# Initialize
sender = EmailSender()

# Send bulk emails
result = sender.send_bulk_emails(
    recipients_file='recipients.csv',
    template_file='email_template.json',
    delay_seconds=2
)

print(f"Success: {result['success']}, Failed: {result['failed']}")
```

### 📬 Send Single Message
```python
sender.send_single_email(
    recipient_email="example@example.com",
    subject="Test Subject",
    body="Test message"
)
```

### 🚀 Launch MailWhale
```bash
python email_sender.py
```

## 📁 File Structure

```
├── email_sender.py      # Main automation script
├── .env.example         # Example environment variables
├── .env                 # Your environment variables (create from example)
├── recipients.csv       # Recipient list
├── email_template.json  # Email template
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore file
├── LICENSE             # MIT License
├── CONTRIBUTING.md     # Contribution guidelines
├── SECURITY.md         # Security policy
├── README.md          # This file
└── email_log.txt      # Generated log file (auto-created)
```

## Personalization

Use placeholders in your email template that match CSV column headers:
- `{name}` → Recipient's name
- `{email}` → Recipient's email
- `{company}` → Recipient's company
- `{position}` → Recipient's position

## Security Best Practices

- ✅ Never commit `email_config.json` with real credentials
- ✅ Use Gmail App Passwords, not your main password
- ✅ Add delays between emails to avoid spam detection
- ✅ Monitor sending limits (Gmail: 500 emails/day for free accounts)

## Troubleshooting

### Common Issues:

1. **Authentication Error**: Make sure you're using an App Password, not your regular Gmail password
2. **Connection Error**: Check your internet connection and Gmail SMTP settings
3. **Spam Detection**: Increase delay between emails or reduce batch size
4. **File Not Found**: Ensure all required files exist in the same directory

### Gmail Limits:
- Free accounts: 500 emails/day
- Google Workspace: 2000 emails/day
- Rate limit: ~100 emails/hour recommended

## Logging

All activities are logged to:
- Console output
- `email_log.txt` file

Log levels include successful sends, failures, and connection status.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute:
- 🐛 Report bugs
- 💡 Suggest new features
- 📖 Improve documentation
- 🔧 Submit pull requests

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⭐ Show Your Support

If this project helped you, please consider:
- ⭐ Starring this repository
- 🍴 Forking it for your own use
- 📢 Sharing it with others
- 🐛 Reporting issues
- 💡 Suggesting improvements

## 📞 Support

If you encounter any issues:
1. Check the [troubleshooting section](#troubleshooting)
2. Search [existing issues](../../issues)
3. Create a [new issue](../../issues/new) if needed

## ⚖️ Legal Notice

⚠️ **Important**: Always comply with:
- CAN-SPAM Act and similar regulations
- Recipient consent requirements
- Your organization's email policies
- Gmail's Terms of Service

Only send emails to recipients who have opted in to receive them.

---

**Made with ❤️ and 🐋 for the open source community**

*"In the vast ocean of email automation, MailWhale swims with purpose and grace."* 🌊
