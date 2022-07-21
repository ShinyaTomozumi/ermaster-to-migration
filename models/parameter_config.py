class ParameterConfig:
    """
    コマンドで受け取ったパラメータの設定
    """
    input_files_path: str  # 取り込むファイルのパス
    output_dir_path: str  # 書き出すフォルダの名称
    sql_type: int  # sqlのタイプ
    date_format: str  # 日付フォーマット
    date: str  # 作成日時
    project_type: str  # Migrationとモデルを使用するプロジェクトの種類
    version: str  # バージョン

    def __init__(self):
        self.input_files_path = ''  # 取り込むファイルのパス
        self.output_dir_path = ''  # 書き出すフォルダの名称
        self.sql_type = 1  # sqlのタイプ
        self.date_format = 'Y-m-d H:i:s.u'  # 作成日時
        self.project_type = ''  # Migrationとモデルを使用するプロジェクトの種類
        self.version = '0'  # バージョン
