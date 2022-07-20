class IndexProperty:
    """
    インデックスに関するプロパティ
    """
    index_name: str = ''  # インデックス名
    type: str = ''  # タイプ
    is_unique: bool = False  # ユニークフラグ
    description: str = ''  # 説明
    table_name: str = ''  # テーブル名
    colum_list: list[str] = []  # 対象カラム一覧

    def __init__(self):
        self.index_name = ''  # インデックス名
        self.type = ''  # タイプ
        self.is_unique = False  # ユニークフラグ
        self.description = ''  # 説明
        self.table_name = ''  # テーブル名
        self.colum_list = []  # 対象カラム一覧
