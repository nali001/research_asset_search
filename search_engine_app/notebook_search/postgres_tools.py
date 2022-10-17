import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# ---------------------------- Global level ---------------------
def create_connection() -> psycopg2.extensions.connection:
    conn = None
    try:
        # Connect to PostgreSQL DBMS
        # con = psycopg2.connect("user=postgres password='aubergine'")
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            user="postgres",
            password="notebooksearch2022")    
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn

def execute_commands(commands) -> psycopg2.extensions.cursor: 
    # check if the `commands` is iterable 
    if not isinstance(commands, list) and not isinstance(commands, tuple):
        print(f'''You need to input a sequence of commands. \n
        If there is only one command, wrap it inside a tuple or a list. ''')
        return False
    conn = create_connection()
    cur = conn.cursor()
    # execute commands one by one
    for command in commands:
        cur.execute(command)
        # print('-----------------Command------------------')
        # print(command)
        # print('------------------------------------------\n')
    # commit the changes
    conn.commit()
    return cur
# ----------------------------------------------------------------


# ---------------------------- Database level ---------------------
def list_databases(): 
    ''' Detele postgres databases

    Args: 
        - database_names: list. A list of database names to be deleted. 
    '''
    commands = ['SELECT datname FROM pg_database;']
    cur = execute_commands(commands)
    results = cur.fetchall()
    databases = []
    for item in results: 
        databases.append(item[0])
    # print('----------------- Databases ---------------')
    # print(databases)
    # print('-------------------------------------------\n')
    return databases

def database_exists(database_name:str): 
    databases = list_databases()
    if database_name in databases: 
        return True
    else: 
        return False

def create_databases(database_names:list): 
    ''' Create postgres databases
    '''
    commands = []
    for item in database_names: 
        commands.append(f'CREATE DATABASE {item};')
    execute_commands(commands)
    return True
    

def delete_databases(database_names: list): 
    ''' Detele postgres databases

    Args: 
        - database_names: list. A list of database names to be deleted. 
    '''
    commands = []
    for item in database_names: 
        commands.append(f'DROP DATABASE {item};')
    execute_commands(commands)
    return True
# ----------------------------------------------------------------


# ---------------------------- Table level ---------------------
def list_tables(commands): 
    commands = [
        """
        SELECT *
        FROM pg_catalog.pg_tables
        WHERE schemaname != 'pg_catalog' AND 
            schemaname != 'information_schema';
        """   
    ]
    cur = execute_commands(commands)
    results = cur.fetchall()
    tables = []
    for item in results: 
        tables.append(item[0])
    # print('----------------- Databases ---------------')
    # print(databases)
    # print('-------------------------------------------\n')
    return tables
    

def create_tables(commands):
    """ create tables in the PostgreSQL database """
    execute_commands(commands)
    return True


def delete_tables(table_names):
    """ create tables in the PostgreSQL database
    """
    commands = []
    for table_name in table_names: 
        commands.append(f'DROP TABLE {table_name};')
    execute_commands(commands)
    return True
# ----------------------------------------------------------------


# if __name__ == '__main__': 
#     create_tables()


# ----- Example Python program to create a database in PostgreSQL using Psycopg2 -----

# import the PostgreSQL client for Python



