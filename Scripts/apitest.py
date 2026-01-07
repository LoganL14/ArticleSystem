
from groq import Groq
import os
from config import GROQ_API_KEY


print(GROQ_API_KEY)

# def check_groq_auth():
#     # Prefer environment variable; strip whitespace
#     key = API_KEY

#     client = Groq(api_key=key)

#     try:
#         models = client.models.list()
#         print("✅ Auth OK. Models available:")
#         for m in models.data:
#             print("-", m.id)
#     except Exception as e:
#         # This is where you'd see 401 invalid/expired jwt if the key is wrong
#         raise RuntimeError(f"Groq auth failed: {e}")

# if __name__ == "__main__":
#     check_groq_auth()
