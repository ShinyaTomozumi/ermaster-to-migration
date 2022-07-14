class IndexProperty:
    """
    インデックスに関するプロパティ
    """
    index_name = ''     # インデックス名
    type = ''           # タイプ
    is_unique = False   # ユニークフラグ
    description = ''    # 説明
    table_name = ''     # テーブル名
    colum_list = []     # 対象カラム一覧

    def __init__(self):
        self.index_name = ''     # インデックス名
        self.type = ''           # タイプ
        self.is_unique = False   # ユニークフラグ
        self.description = ''    # 説明
        self.table_name = ''     # テーブル名
        self.colum_list = []     # 対象カラム一覧
