# Security Policy

## Supported Versions

We support the latest version of this project. Please ensure you're using the most recent release.

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < Latest| :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please follow these steps:

### 1. Do NOT create a public issue
Security vulnerabilities should not be reported publicly to avoid potential exploitation.

### 2. Contact us privately
- Create a private security advisory on GitHub
- Or email the maintainers directly (if contact info is available)

### 3. Provide detailed information
Include the following in your report:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if you have one)

## Security Best Practices

When using this email automation tool:

### Credential Security
- ✅ **Use Gmail App Passwords** - Never use your main Gmail password
- ✅ **Keep credentials private** - Never commit `.env` to version control
- ✅ **Environment variables** - Credentials are stored securely in `.env` file
- ✅ **Rotate passwords regularly** - Update app passwords periodically

### Email Security
- ✅ **Verify recipients** - Only send to consenting recipients
- ✅ **Rate limiting** - Use delays to avoid being flagged as spam
- ✅ **Monitor logs** - Check logs for suspicious activity
- ✅ **Validate inputs** - Sanitize email addresses and content

### System Security
- ✅ **Keep Python updated** - Use supported Python versions
- ✅ **Secure file permissions** - Restrict access to `.env` file (chmod 600 .env)
- ✅ **Use virtual environments** - Isolate dependencies
- ✅ **Regular updates** - Keep the codebase updated

## Known Security Considerations

### Gmail API Limits
- Gmail has daily sending limits (500 for free accounts, 2000 for Workspace)
- Exceeding limits may result in account suspension
- Use appropriate delays between emails

### SMTP Security
- This tool uses SMTP with TLS encryption
- Credentials are transmitted securely to Gmail's servers
- Local storage of credentials should be secured

### Data Privacy
- Recipient data is stored in CSV files
- Ensure recipient lists are handled according to privacy laws (GDPR, CCPA, etc.)
- Consider encrypting sensitive recipient data

## Reporting Security Issues

We take security seriously. If you find a security issue:

1. **Don't** create a public GitHub issue
2. **Do** report it privately through GitHub's security advisory feature
3. **Do** provide as much detail as possible
4. **Do** allow reasonable time for a fix before public disclosure

Thank you for helping keep this project secure! 🔒
