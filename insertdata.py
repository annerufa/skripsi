import pandas as pd
import psycopg2
import os

# Here you want to change your database, username & password according to your own values
param_dic = {
    "host"      : "localhost",
    "database"  : "skripsi_db",
    "user"      : "postgres",
    "password"  : "warwhere"
}

def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        os.sys.exit(1) 
    print("Connection successful")
    return conn


def execute_mogrify(conn, df, table):
    """
    Using cursor.mogrify() to build the bulk insert query
    then cursor.execute() to execute the query
    """
    
    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    # Comma-separated dataframe columns
    cols = ','.join(list(df.columns))
    # SQL quert to execute
    cursor = conn.cursor()
    values = [cursor.mogrify("(%s,%s,%s,%s,%s,%s)", tup).decode('utf8') for tup in tuples]
    query  = f'INSERT INTO {table}(%s) VALUES ' % (cols) + ",".join(values)
    # print(query)
    
    try:
        cursor.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("execute_mogrify() done")
    cursor.close()

    
#-----------------------------------------------
# Main code
#-----------------------------------------------

# Reading the csv file, change to meet your own requirements
csv_file = "ekonomi.csv"
df = pd.read_csv(csv_file)
df = df.rename(columns={
    "judul": "judul", 
    "abstrak": "abstrak",
    "fakultas": "id_fakultas",
    "bahasa": "bahasa",
    "keywords": "keywords",
    "link": "linkn"
})

conn = connect(param_dic) # connect to the database
execute_mogrify(conn, df, "dokumen") # Run the execute_many strategy
conn.close() # close the connection
