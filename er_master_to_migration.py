#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import library
import sys
import os
from models.parameter_config import ParameterConfig
from contains import sql_type
from exel.import_exel_files import ImportExcelFile
from make.laravel import Laravel

# Main function
if __name__ == '__main__':
    """
    Main function
    """

    # Show console log
    print('Start er_master_to_migration files...')

    # パラメータを受け取る
    args = sys.argv

    # 引数の初期化
    parameter_config = ParameterConfig
    parameter_config.output_dir_path = 'output_files'

    # 受け取ったパラメータを引数に設定する。
    i = 0
    for arg in args:
        # Sqlタイプを設定する
        if arg == '-sql':
            if (i + 1) < len(args):
                if args[i + 1].lower() == 'postgresql':
                    parameter_config.sql_type = sql_type.SqlType.PostgreSQL
        # 日付を設定する
        if arg == '-date':
            if (i + 1) < len(args):
                parameter_config.date = args[i + 1]
        # ファイルのパスを取得する
        if arg == '-i':
            if (i + 1) < len(args):
                parameter_config.input_files_path = args[i + 1]
        # 出力先のパスを取得する
        if arg == '-o':
            if (i + 1) < len(args):
                parameter_config.output_dir_path = args[i + 1]
        # プロジェクトの種類を設定する
        if arg == '-project':
            if (i + 1) < len(args):
                parameter_config.project_type = args[i + 1]
        i += 1

    # プロジェクトの種類が設定されていない場合はエラーを返却する
    if parameter_config.project_type == '':
        print('Set the project type (-project).\n - laravel')
        exit()

    # 取り込むファイルが設定されていない場合はエラーを返却する
    if parameter_config.input_files_path == '':
        print('Set the file path (-i).')
        exit()

    # 日付を設定しない場合はエラーを返却する
    if parameter_config.date == '':
        print('Set the date (-date). format is \'Y-m-d\'')
        exit()

    # ファイルが存在しない場合はエラーを返却する
    if not os.path.isfile(parameter_config.input_files_path):
        print(f'The specified file does not exist. {parameter_config.input_files_path}')
        exit()

    # ファイルの拡張子が「xls」もしくは「xlsx」以外の場合はエラーを返却する
    if not parameter_config.input_files_path.endswith('xls') and not parameter_config.input_files_path.endswith('xlsx'):
        print('The specified file is not a "xls" or "xlsx" file.')
        exit()

    # エクセルを読み込みデータベース情報を返却する
    import_exel_files = ImportExcelFile(parameter_config)
    import_exel_files.import_exel()

    # プロジェクトの種類によって書き出すファイルを設定する
    if parameter_config.project_type == 'laravel':
        laravel = Laravel(parameter_config, import_exel_files)
        laravel.make_files()

    print('Finish er_master_to_migration...')
