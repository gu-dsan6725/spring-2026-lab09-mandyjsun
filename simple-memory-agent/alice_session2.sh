#!/bin/bash

echo "" >> alice_output.txt
echo "=== Alice Session 2 (New Session) ===" >> alice_output.txt
echo "" >> alice_output.txt

echo "User: What do you remember about me?" >> alice_output.txt
response=$(curl -s -X POST http://127.0.0.1:9090/invocation \
  -H "Content-Type: application/json" \
  -d '{"user_id": "alice", "run_id": "alice-session-2", "query": "What do you remember about me?"}' | jq -r '.response')
echo "Agent: $response" >> alice_output.txt
echo "" >> alice_output.txt
sleep 15

echo "User: What project am I working on?" >> alice_output.txt
response=$(curl -s -X POST http://127.0.0.1:9090/invocation \
  -H "Content-Type: application/json" \
  -d '{"user_id": "alice", "run_id": "alice-session-2", "query": "What project am I working on?"}' | jq -r '.response')
echo "Agent: $response" >> alice_output.txt
echo "" >> alice_output.txt

echo "Session 2 complete. Output appended to alice_output.txt"
