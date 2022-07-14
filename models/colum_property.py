class ColumProperty:
    """
    データベースに関するプロパティ情報の定義
    """
    colum_name = ''     # カラム名 (物理名)
    colum_comment = ''  # カラム名 (論理名)
    colum_type = ''     # 型
    database_colum_type = ''    #
    length = 0     # 長さ
    decimal = 0     # 小数
    is_primary = False  # 主キー
    is_not_null = False  # NOT NULL
    is_unique = False  # UNIQUE
    is_auto_increment = False  # オートインクリメント
    default_value = ''  # デフォルト値
    description = ''  # 説明

    def __init__(self):
        self.colum_name = ''     # カラム名 (物理名)
        self.colum_comment = ''  # カラム名 (論理名)
        self.colum_type = ''     # 型
        self.database_colum_type = ''    #
        self.length = 0     # 長さ
        self.decimal = 0     # 小数
        self.is_primary = False  # 主キー
        self.is_not_null = False  # NOT NULL
        self.is_unique = False  # UNIQUE
        self.is_auto_increment = False  # オートインクリメント
        self.default_value = ''  # デフォルト値
        self.description = ''  # 説明
