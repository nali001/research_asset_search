from notebooksearch import postgres_tools
class UserInteractions():
    def __init__(self): 
        postgres_tools.create_databases("notebook_search")

