"""コンテキストマネージャー（with 文）の仕組みを示すサンプル。"""
from types import TracebackType
from typing import Any

class DatabaseConnection:
    """with 文で使うデータベース接続の例。

    with ブロックに入るときに接続し、抜けるときに接続を閉じる。
    """

    def __enter__(self) -> Any:
        """データベースに接続し、接続を返す。

        Returns
        -------
        Any
            データベースの接続（このサンプルでは None）。
        """
        print
        self.conn = self.connect_to_database()
        return self.conn

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """データベースの接続を閉じる。

        Parameters
        ----------
        exc_type : type[BaseException] | None
            with ブロック内で発生した例外の型。発生していなければ None。
        exc_value : BaseException | None
            with ブロック内で発生した例外。発生していなければ None。
        traceback : TracebackType | None
            例外のトレースバック。発生していなければ None。
        """
        print("データベース接続を閉じています")
        self.close_connection(self.conn)

    def connect_to_database(self) -> Any:
        """データベースに接続する。

        Returns
        -------
        Any
            データベースの接続（このサンプルでは処理を書いていないので None）。
        """
        # データベースに接続する処理
        pass

    def close_connection(self, conn: Any) -> None:
        """データベースの接続を閉じる。

        Parameters
        ----------
        conn : Any
            閉じる接続。
        """
        # データベース接続を閉じる処理
        pass

with DatabaseConnection() as db_conn:
    print("データベース接続を使用中:", db_conn)
    # データベースを操作する
    # db_conn.execute("SELECT * FROM table")
    # db_conn.commit()
    # db_conn.rollback()