from psycopg_pool import ConnectionPool
DATABASE_URL = "postgresql://postgres:benny123@localhost:5440/stock_db"
pool = ConnectionPool(DATABASE_URL)

