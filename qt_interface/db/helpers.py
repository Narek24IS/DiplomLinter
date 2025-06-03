from qt_interface.db.pgsql_connection import select

from qt_interface.settings import settings


from .pgsql_connection import select

def get_columns(table_name):
    query = """
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_schema = 'public' AND table_name = %s 
    ORDER BY ordinal_position;
    """
    result = select(query, (table_name,))
    return [row["column_name"] for row in result]

def get_column_info(table_name, column_name):
    query = """
    SELECT 
        column_name,
        data_type,
        is_nullable,
        column_default,
        (SELECT EXISTS (
            SELECT 1 
            FROM information_schema.key_column_usage 
            WHERE table_schema = 'public' 
            AND table_name = %s 
            AND column_name = %s
            AND position_in_unique_constraint IS NOT NULL
        )) AS is_foreign_key
    FROM information_schema.columns 
    WHERE table_schema = 'public' 
    AND table_name = %s 
    AND column_name = %s;
    """
    result = select(query, (table_name, column_name, table_name, column_name))
    return result[0] if result else None

def get_foreign_key_info(table_name, column_name):
    query = """
    SELECT 
        ccu.table_name AS referenced_table_name,
        ccu.column_name AS referenced_column_name
    FROM 
        information_schema.table_constraints AS tc 
        JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage AS ccu
            ON ccu.constraint_name = tc.constraint_name
            AND ccu.table_schema = tc.table_schema
    WHERE 
        tc.constraint_type = 'FOREIGN KEY' 
        AND tc.table_schema = 'public'
        AND tc.table_name = %s 
        AND kcu.column_name = %s;
    """
    result = select(query, (table_name, column_name))
    if result:
        return result[0]["referenced_table_name"], result[0]["referenced_column_name"]
    return None, None