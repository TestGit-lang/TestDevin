import configparser
import os
import psycopg2


def read_config(config_path=None):
    """
    設定ファイルから PostgreSQL 接続情報を読み込む
    Args:
        config_path: 設定ファイルのパス（デフォルトは同じディレクトリの setting.ini）
    Returns:
        dict: 接続情報を含む辞書
    """
    if config_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, 'setting.ini')
    config = configparser.ConfigParser()
    config.read(config_path)
    return {
        'endpoint': config['Database']['EndPoint'],
        'database': config['Database']['DatabaseName'],
        'user': config['Database']['User'],
        'password': config['Database']['Password']
    }


def connect_to_database(config=None):
    """
    PostgreSQL データベースに接続する
    Args:
        config: 接続情報を含む辞書（デフォルトは設定ファイルから読み込む）
    Returns:
        connection: データベース接続オブジェクト
    """
    if config is None:
        config = read_config()
    try:
        connection = psycopg2.connect(
            host=config['endpoint'],
            database=config['database'],
            user=config['user'],
            password=config['password']
        )
        return connection
    except Exception as e:
        print(f"データベース接続エラー: {e}")
        return None


def execute_query(query, params=None, config=None):
    """
    SQLクエリを実行する
    Args:
        query: 実行するSQLクエリ
        params: クエリパラメータ
        config: 接続情報を含む辞書（デフォルトは設定ファイルから読み込む）
    Returns:
        list: クエリ結果
    """
    connection = connect_to_database(config)
    if connection is None:
        return None
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            connection.commit()
            return True
    except Exception as e:
        print(f"クエリ実行エラー: {e}")
        return None
    finally:
        connection.close()


def create_devin_test_table(config=None):
    """
    devin_testテーブルを作成する
    Args:
        config: 接続情報を含む辞書（デフォルトは設定ファイルから読み込む）
    Returns:
        bool: 成功した場合はTrue、失敗した場合はFalse
    """
    query = """
    CREATE TABLE IF NOT EXISTS devin_test (
        id INT PRIMARY KEY,
        name TEXT,
        data TEXT
    );
    """
    return execute_query(query, config=config)


def insert_devin_test_data(config=None):
    """
    devin_testテーブルに初期データを挿入する
    Args:
        config: 接続情報を含む辞書（デフォルトは設定ファイルから読み込む）
    Returns:
        bool: 成功した場合はTrue、失敗した場合はFalse
    """
    data = [
        (1, 'test1', 'sample1'),
        (2, 'test2', 'sample2'),
        (3, 'test3', 'sample3'),
        (4, 'test4', 'sample4')
    ]
    success = True
    for record in data:
        query = """
        INSERT INTO devin_test (id, name, data)
        VALUES (%s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """
        result = execute_query(query, record, config=config)
        if not result:
            success = False
    return success


def update_devin_test_data(config=None):
    """
    devin_testテーブルのid=2のレコードを更新する
    Args:
        config: 接続情報を含む辞書（デフォルトは設定ファイルから読み込む）
    Returns:
        bool: 成功した場合はTrue、失敗した場合はFalse
    """
    query = """
    UPDATE devin_test
    SET data = 'sample22'
    WHERE id = 2;
    """
    return execute_query(query, config=config)


def delete_devin_test_data(config=None):
    """
    devin_testテーブルのid=3のレコードを削除する
    Args:
        config: 接続情報を含む辞書（デフォルトは設定ファイルから読み込む）
    Returns:
        bool: 成功した場合はTrue、失敗した場合はFalse
    """
    query = """
    DELETE FROM devin_test
    WHERE id = 3;
    """
    return execute_query(query, config=config)


if __name__ == "__main__":
    config = read_config()
    print("設定ファイルから読み込んだ接続情報:")
    print(f"EndPoint: {config['endpoint']}")
    print(f"DatabaseName: {config['database']}")
    print(f"User: {config['user']}")
    print(f"Password: {'*' * len(config['password'])}")  # セキュリティのためパスワードは表示しない
    print("\nデータベース接続テスト...")
    connection = connect_to_database(config)
    if connection:
        print("接続成功！")
        connection.close()
        print("\ndevin_testテーブル作成...")
        if create_devin_test_table(config):
            print("テーブル作成成功！")
            print("\nデータ挿入...")
            if insert_devin_test_data(config):
                print("データ挿入成功！")
                print("\nデータ更新（id=2）...")
                if update_devin_test_data(config):
                    print("データ更新成功！")
                    print("\nデータ削除（id=3）...")
                    if delete_devin_test_data(config):
                        print("データ削除成功！")
                    else:
                        print("データ削除失敗")
                else:
                    print("データ更新失敗")
            else:
                print("データ挿入失敗")
        else:
            print("テーブル作成失敗")
    else:
        print("接続失敗")
