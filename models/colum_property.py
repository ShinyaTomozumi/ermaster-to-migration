class ColumProperty:
    """
    データベースに関するプロパティ情報の定義
    """
    colum_name: str  # カラム名 (物理名)
    colum_comment: str  # カラム名 (論理名)
    colum_type: str  # 型
    length: int  # 長さ
    decimal: float  # 小数
    is_primary: bool  # 主キー
    is_not_null: bool  # NOT NULL
    is_unique: bool  # UNIQUE
    is_auto_increment: bool  # オートインクリメント
    default_value: str  # デフォルト値
    description: str  # 説明

    def __init__(self):
        self.colum_name = ''  # カラム名 (物理名)
        self.colum_comment = ''  # カラム名 (論理名)
        self.colum_type = ''  # 型
        self.length = 0  # 長さ
        self.decimal = 0  # 小数
        self.is_primary = False  # 主キー
        self.is_not_null = False  # NOT NULL
        self.is_unique = False  # UNIQUE
        self.is_auto_increment = False  # オートインクリメント
        self.default_value = ''  # デフォルト値
        self.description = ''  # 説明
