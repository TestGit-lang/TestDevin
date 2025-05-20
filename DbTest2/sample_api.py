import configparser
import psycopg2
import os

def read_config():
    """
    設定ファイルsetting.iniから設定内容を読み出す
    """
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'setting.ini')
    config.read(config_path)
    
    db_config = {
        'endpoint': config['Database']['EndPoint'],
        'database': config['Database']['DatabaseName'],
        'user': config['Database']['User'],
        'password': config['Database']['Password']
    }
    
    return db_config

def get_connection():
    """
    PostgreSQLへの接続を取得する
    """
    db_config = read_config()
    
    try:
        conn = psycopg2.connect(
            host=db_config['endpoint'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        return conn
    except Exception as e:
        raise Exception(f"データベース接続エラー: {str(e)}")

def create_table():
    """
    テーブルdevin_testを作成する
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS devin_test (
                id INT PRIMARY KEY,
                name TEXT,
                data TEXT
            )
        """)
        
        conn.commit()
        print("テーブルdevin_testが作成されました")
    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"テーブル作成エラー: {str(e)}")
    finally:
        if conn:
            conn.close()

def insert_data():
    """
    テーブルdevin_testにデータを追加する
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        data_to_insert = [
            (1, 'test1', 'sample1'),
            (2, 'test2', 'sample2'),
            (3, 'test3', 'sample3'),
            (4, 'test4', 'sample4')
        ]
        
        for data in data_to_insert:
            cursor.execute("""
                INSERT INTO devin_test (id, name, data)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, data)
        
        conn.commit()
        print("データが追加されました")
    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"データ追加エラー: {str(e)}")
    finally:
        if conn:
            conn.close()

def update_data():
    """
    テーブルdevin_testのデータを更新する
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE devin_test
            SET data = 'sample22'
            WHERE id = 2
        """)
        
        if cursor.rowcount == 0:
            raise Exception("更新対象のデータが見つかりませんでした")
        
        conn.commit()
        print("データが更新されました")
    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"データ更新エラー: {str(e)}")
    finally:
        if conn:
            conn.close()

def delete_data():
    """
    テーブルdevin_testのデータを削除する
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM devin_test
            WHERE id = 3
        """)
        
        if cursor.rowcount == 0:
            raise Exception("削除対象のデータが見つかりませんでした")
        
        conn.commit()
        print("データが削除されました")
    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"データ削除エラー: {str(e)}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    try:
        create_table()
        insert_data()
        update_data()
        delete_data()
        print("すべての操作が正常に完了しました")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
