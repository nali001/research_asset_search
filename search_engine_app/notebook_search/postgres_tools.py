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
            password="aubergine")    
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
        commands.append(f'create database {item};')
    execute_commands(commands)
    print()
    return True
    

def delete_databases(database_names: list): 
    ''' Detele postgres databases

    Args: 
        - database_names: list. A list of database names to be deleted. 
    '''
    commands = []
    for item in database_names: 
        commands.append(f'drop database {item};')
    execute_commands(commands)
    return True
# ----------------------------------------------------------------


# ---------------------------- Table level ---------------------
def create_table(schema):
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE vendors (
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        )
        """,
        """ CREATE TABLE parts (
                part_id SERIAL PRIMARY KEY,
                part_name VARCHAR(255) NOT NULL
                )
        """,
        """
        CREATE TABLE part_drawings (
                part_id INTEGER PRIMARY KEY,
                file_extension VARCHAR(5) NOT NULL,
                drawing_data BYTEA NOT NULL,
                FOREIGN KEY (part_id)
                REFERENCES parts (part_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE vendor_parts (
                vendor_id INTEGER NOT NULL,
                part_id INTEGER NOT NULL,
                PRIMARY KEY (vendor_id , part_id),
                FOREIGN KEY (vendor_id)
                    REFERENCES vendors (vendor_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (part_id)
                    REFERENCES parts (part_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
    execute_commands(commands)
# ----------------------------------------------------------------


# if __name__ == '__main__':
#     create_tables()


# ----- Example Python program to create a database in PostgreSQL using Psycopg2 -----

# import the PostgreSQL client for Python



