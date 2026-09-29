class DatabaseConnection:
    def __enter__(self):
        print
        self.conn = self.connect_to_database()
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        print("データベース接続を閉じています")
        self.close_connection(self.conn)

    def connect_to_database(self):
        # データベースに接続する処理
        pass

    def close_connection(self, conn):
        # データベース接続を閉じる処理
        pass

with DatabaseConnection() as db_conn:
    print("データベース接続を使用中:", db_conn)
    # データベースを操作する
    # db_conn.execute("SELECT * FROM table")
    # db_conn.commit()
    # db_conn.rollback()