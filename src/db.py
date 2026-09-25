import os
import json
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


def create_chat(session_id, title="New Chat"):
    with engine.connect() as conn:
        result = conn.execute(
            text("INSERT INTO chat_sessions (session_id, title) VALUES (:sid, :title) RETURNING id"),
            {"sid": session_id, "title": title}
        )
        conn.commit()
        return str(result.fetchone()[0])


def get_session_chats(session_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, title, created_at FROM chat_sessions WHERE session_id = :sid ORDER BY created_at DESC"),
            {"sid": session_id}
        )
        return [dict(row._mapping) for row in result]


def update_chat_title(chat_id, title):
    with engine.connect() as conn:
        conn.execute(text("UPDATE chat_sessions SET title = :title WHERE id = :cid"),
                     {"title": title, "cid": chat_id})
        conn.commit()


def delete_chat(chat_id):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM chat_sessions WHERE id = :cid"), {"cid": chat_id})
        conn.commit()


def save_message(chat_id, role, content, sources=None):
    with engine.connect() as conn:
        conn.execute(
            text("""INSERT INTO messages (chat_session_id, role, content, sources)
                     VALUES (:cid, :role, :content, :sources)"""),
            {"cid": chat_id, "role": role, "content": content,
             "sources": json.dumps(sources) if sources is not None else None}
        )
        conn.commit()


def get_chat_messages(chat_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT role, content, sources FROM messages WHERE chat_session_id = :cid ORDER BY created_at"),
            {"cid": chat_id}
        )
        return [dict(row._mapping) for row in result]