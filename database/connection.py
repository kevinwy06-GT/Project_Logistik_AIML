"""
connection.py

Creates a reusable SQLAlchemy connection.

Priority:
1. Use Streamlit secrets (when running the Streamlit app).
2. Fall back to config.py (for scripts like seeder.py or test_database.py).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ==========================================================
# TRY TO LOAD STREAMLIT SECRETS
# ==========================================================

try:
    import streamlit as st

    DATABASE_URI = (
        f"{st.secrets['connections']['mysql']['dialect']}"
        f"+{st.secrets['connections']['mysql']['driver']}://"
        f"{st.secrets['connections']['mysql']['username']}:"
        f"{st.secrets['connections']['mysql']['password']}@"
        f"{st.secrets['connections']['mysql']['host']}:"
        f"{st.secrets['connections']['mysql']['port']}/"
        f"{st.secrets['connections']['mysql']['database']}"
    )

except Exception:
    # If Streamlit isn't running, use config.py instead.
    from config import DATABASE_URI


# ==========================================================
# CREATE ENGINE
# ==========================================================

engine = create_engine(
    DATABASE_URI,
    pool_pre_ping=True,
    future=True
)


# ==========================================================
# SESSION FACTORY
# ==========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True
)


# ==========================================================
# GET DATABASE SESSION
# ==========================================================

def get_session():
    """
    Returns a SQLAlchemy session.

    Example:
        session = get_session()
    """
    return SessionLocal()