#!/bin/bash

# Configuration
KESTRA_URL="https://flow.organ.dev.br/api/v1/executions/webhook/dev.organ.automation/chatwoot_audio_process"
# KESTRA_URL="http://localhost:8080/api/v1/executions/webhook/dev.organ.automation/chatwoot_audio_process" # Use this if testing locally against localhost

echo "Sending test webhook to: $KESTRA_URL"

curl -X POST "$KESTRA_URL" \
-H "Content-Type: application/json" \
-d '{
  "event": "message_created",
  "message_type": "incoming",
  "content": "Olá Maya, gostaria de saber sobre apartamentos em São Paulo",
  "account": {
    "id": 1,
    "name": "Test Account"
  },
  "conversation": {
    "id": 1
  },
  "sender": {
    "id": 1,
    "name": "Test User",
    "email": "test@example.com"
  },
  "attachments": []
}'

echo -e "\n\nWebhook sent! Check Kestra executions at: https://flow.organ.dev.br/ui/executions"
