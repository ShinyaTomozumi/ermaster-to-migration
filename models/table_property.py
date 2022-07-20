from typing import List
from models.index_property import IndexProperty
from models.colum_property import ColumProperty


class TableProperty:
    """
    テーブルに関する情報
    """
    table_name: str = ''  # テーブル名
    table_display_name: str = ''  # テーブル表示名
    primary_keys: list[str] = []  # 設定されている主キー（複数あることを想定して配列で定義)
    dates: list[str] = []  # タイムスタンプを使用しているカラム名の設定（複数あることを想定して配列で定義）
    date_format: str = ''  # 時間のフォーマット(デフォルトはMySQLは「Y-m-d H:i:s.u」、PostgresSqlは「Y-m-d H:i:s.uP」となる。
    is_incrementing: bool = False  # オートインクリメントかどうか
    is_timestamps: bool = False  # Laravelで使用する「timestamps」の設定
    foreign_keys: list[str] = []  # 紐づいているキーの設定情報
    column_list: List[ColumProperty] = []  # カラム情報の配列(ColumProperty)
    is_soft_deleted: bool = False  # ソフトデリート機能のテーブルになるかどうか
    index_list: List[IndexProperty] = []  # インデックスの一覧

    def __init__(self):
        self.table_name = ''  # テーブル名
        self.table_display_name = ''  # テーブル表示名
        self.primary_keys = []  # 設定されている主キー（複数あることを想定して配列で定義)
        self.dates = []  # タイムスタンプを使用しているカラム名の設定（複数あることを想定して配列で定義）
        self.date_format = 'Y-m-d H:i:s.u'  # 時間のフォーマット(デフォルトはMySQLは「Y-m-d H:i:s.u」、PostgresSqlは「Y-m-d H:i:s.uP」となる。
        self.is_incrementing = False  # オートインクリメントかどうか
        self.is_timestamps = False  # Laravelで使用する「timestamps」の設定
        self.foreign_keys = []  # 紐づいているキーの設定情報
        self.column_list = []  # カラム情報の配列(ColumProperty)
        self.is_soft_deleted = False  # ソフトデリート機能のテーブルになるかどうか
        self.index_list = []  # インデックスの一覧
