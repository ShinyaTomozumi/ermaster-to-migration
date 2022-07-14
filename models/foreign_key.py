class ForeignKey:
    """
    紐付けキーの設定情報
    """
    colum_name_display = ''    # カラム名 (論理名)
    colum_name = ''     # カラム名 (物理名)
    ref_table = ''      # 参照テーブル
    ref_key = ''    # 参照キー

    def __init__(self):
        self.colum_name_display = ''    # カラム名 (論理名)
        self.colum_name = ''     # カラム名 (物理名)
        self.ref_table = ''      # 参照テーブル
        self.ref_key = ''    # 参照キー

