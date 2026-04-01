"""Quick Mem0 connectivity and storage test."""
import os, time, json
from dotenv import load_dotenv
from mem0 import MemoryClient

load_dotenv()

client = MemoryClient(api_key=os.getenv("MEM0_API_KEY"))
USER = "alice"
RUN = "alice-session-1"

# Try all filter combinations to find stored memories
print("Checking what's actually stored for alice...")

print("\na) filters user_id:")
r = client.get_all(filters={"user_id": USER})
print("   Count:", len(r.get("results", [])), r.get("results", [])[:1])

print("\nb) filters run_id:")
r = client.get_all(filters={"run_id": RUN})
print("   Count:", len(r.get("results", [])), r.get("results", [])[:1])

print("\nc) filters user_id AND run_id:")
r = client.get_all(filters={"AND": [{"user_id": USER}, {"run_id": RUN}]})
print("   Count:", len(r.get("results", [])), r.get("results", [])[:1])

# Also check mem0_test_user from previous test
USER2 = "mem0_test_user"
print(f"\nd) filters {USER2}:")
r = client.get_all(filters={"user_id": USER2})
print("   Count:", len(r.get("results", [])))
for m in r.get("results", []):
    print("  -", m.get("memory", ""))
