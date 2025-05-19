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
    else:
        print("接続失敗")
