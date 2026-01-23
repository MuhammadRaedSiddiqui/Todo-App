## Getting Your Groq API Key

1. Visit: https://console.groq.com
2. Sign up or log in
3. Navigate to "API Keys" section
4. Click "Create API Key"
5. Copy the key (starts with "gsk_")

**Important**:
- Free tier: 30 requests/minute
- Keep your API key secure
- Never commit it to version control

Once you have your key, add it to backend/.env:

```bash
GROQ_API_KEY=gsk_your_actual_key_here
```
