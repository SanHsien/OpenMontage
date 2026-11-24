---
name: api-key-setup
description: How to obtain and configure a BFL API key
---

# API Key Setup

> **Important:** Always verify your API key before attempting image generation. Missing or invalid keys result in "Not authenticated" errors.

## Quick Validation

Check presence only; this does not validate the key with the provider:

```bash
# Check if key is set
python -c "import os; print('OK: Key configured' if os.environ.get('BFL_API_KEY') else 'Error: BFL_API_KEY not set')"
```

If not set, follow the steps below.

## Get a Key

1. Go to **https://dashboard.bfl.ai/get-started**
2. Click **"Create Key"**
3. Select organization (ask user if multiple options)
4. Copy the key (starts with `bfl_`)

## For Agents Making Direct API Calls

When `BFL_API_KEY` is not set in the current session:

1. Direct the user to create a key at https://dashboard.bfl.ai/get-started.
2. Have the user configure `BFL_API_KEY` privately in their local environment or `.env`;
   never request raw API keys in chat. Never read or display `.env` contents,
   credential assignments, or the key itself in agent output.
3. Ensure `.env` is ignored by Git. The application's dotenv loader can load it;
   a presence check only sees the current process environment. If using a shell
   directly, have the user configure that shell privately before starting the agent.
4. Re-run the presence check above and report only configured / not configured.
   This check does not confirm authentication; API errors must be handled separately.
