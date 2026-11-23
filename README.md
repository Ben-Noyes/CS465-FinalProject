### Installation and Setup
    Everything that needs to be downloaded is in requirements.txt
    simply run;
        python -m pip install -r requirements.txt
    Once everything is downloaded:
        python -m streamlit run webapp.py

### Database Connection Setup

The application connects to the SQLite database agency.db using Python's built-in sqlite3 library. The database file is stored in the same directory as webapp.py and the application uses a get_connection() function to establish a connection whenever a database operation is needed.

Foreign key constraints are enabled to maintain relationships between the tables. 

The application also uses sqlite3.Row so query results can be accessed by column names instead of column positions.

