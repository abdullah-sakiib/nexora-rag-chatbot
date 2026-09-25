# from db import sign_up, sign_in, create_chat, save_message, get_chat_messages

# # 1. Sign up a test user
# res = sign_up("sakibabdullah59@gmail.com", "MyPass123!")
# print("Signup:", res)

# user_id = res.user.id
# print("User ID:", user_id)

# # 2. Create a chat
# chat_id = create_chat(user_id, title="Test Chat")
# print("Chat ID:", chat_id)

# # 3. Save messages
# save_message(chat_id, "user", "What's the pricing for the Starter plan?")
# save_message(chat_id, "assistant", "$19/month or $190/year.", sources=["03_pricing_and_plans.pdf (p.0)"])

# # 4. Retrieve
# messages = get_chat_messages(chat_id)
# print("Messages:", messages)

from db import sign_in, create_chat, save_message, get_chat_messages

res = sign_in("sakibabdullah58@gmail.com", "Sakib12345")
print("Signin:", res)

user_id = res.user.id
print("User ID:", user_id)

chat_id = create_chat(user_id, title="Test Chat")
print("Chat ID:", chat_id)

save_message(chat_id, "user", "What's the pricing for the Starter plan?")
save_message(chat_id, "assistant", "$19/month or $190/year.", sources=["03_pricing_and_plans.pdf (p.0)"])

messages = get_chat_messages(chat_id)
print("Messages:", messages)