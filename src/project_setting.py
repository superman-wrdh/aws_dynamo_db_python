DB_HOST = "http://192.168.199.199:8000"
REGION = "us-west-1"


def list_table():
    from pynamodb.connection import Connection
    conn = Connection(host=DB_HOST)
    tables = conn.list_tables()
    print(tables)
    return tables
