from neo4j import GraphDatabase
import pandas as pd
import os

# ==============================================================================
# 1. DATABASE CONNECTION SETTINGS FOR MEMGRAPH
# ==============================================================================
# The default Memgraph Docker instance runs on this URI and does not require a password.
uri = "bolt://localhost:7687"

# ==============================================================================
# 2. DATA LOADING
# ==============================================================================
# Construct an absolute path to the data file to avoid any path issues
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_path = os.path.join(project_root, "data", "synthetic_bank_data.csv")
    
    print(f"Loading data from: {data_path}")
    df = pd.read_csv(data_path)
    # Use a sample of the data for a quicker loading process
    df_sample = df.head(5000)
    print(f"Data loaded successfully. Processing {len(df_sample)} records.")
except FileNotFoundError:
    print(f"Error: Data file not found at {data_path}")
    print("Please ensure the data generation notebooks have been run.")
    exit()

# ==============================================================================
# 3. GRAPH DATABASE LOADER CLASS (ADAPTED FOR MEMGRAPH)
# ==============================================================================
class GraphLoader:
    def __init__(self, uri):
        # Connect to the database without authentication
        self.driver = GraphDatabase.driver(uri)

    def close(self):
        # Close the connection
        self.driver.close()
        
    def clear_database(self):
        # A helpful function to clear the database before loading new data
        with self.driver.session() as session:
            print("Clearing existing database...")
            session.run("MATCH (n) DETACH DELETE n")
            print("Database cleared.")

    def load_data(self, df):
        with self.driver.session() as session:
            # Note: Memgraph doesn't support the same "CREATE CONSTRAINT" syntax.
            # Uniqueness is handled by the MERGE command itself.
            
            # Convert the DataFrame to a list of dictionaries for the query
            records = df.to_dict('records')
            
            # Use an UNWIND query for efficient, batch-loading of data
            load_query = """
            UNWIND $records AS row
            MERGE (u:User {name: row.Name})
            MERGE (p:Phone {number: row['Phone Number']})
            MERGE (e:Email {address: row.Email})
            MERGE (u)-[:HAS_PHONE]->(p)
            MERGE (u)-[:HAS_EMAIL]->(e)
            """
            
            print("Loading data into Memgraph... This may take a moment.")
            session.run(load_query, records=records)
            print("Data loading complete.")

# ==============================================================================
# 4. EXECUTE THE LOADING PROCESS
# ==============================================================================
if __name__ == "__main__":
    # Create an instance of our loader
    loader = GraphLoader(uri)
    
    # Clear the database to ensure a fresh start
    loader.clear_database()
    
    # Load the new data
    loader.load_data(df_sample)
    
    # Close the connection
    loader.close()
    
    print("\nProcess finished. Your Memgraph database is now populated.")
    print("You can now run queries in Memgraph Lab at http://localhost:7444")
    