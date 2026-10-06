"""Streamlit deployment entrypoint.

Run locally with:
    streamlit run app.py

Streamlit Community Cloud should also use this file as the app entrypoint.
The UI remains in frontend/app.py so the project structure stays clear.
"""

from frontend.app import main


if __name__ == "__main__":
    main()
