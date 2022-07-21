import os
import re
import shutil

from typing import Type

from exel.import_exel_files import ImportExcelFile
from contains.app_contains import AppContains
from models.parameter_config import ParameterConfig
from models.table_property import TableProperty


class Laravel:
    """
    Laravel用のファイルを書き出す処理
    """
    _parameter_config: ParameterConfig
    _import_exel_files: ImportExcelFile
    _template_dir: str

    def __init__(self, parameter_config: ParameterConfig, import_exel_files: ImportExcelFile):
        """
        初期化
        :param parameter_config:
        :param import_exel_files:
        """
        self._parameter_config = parameter_config
        # 出力先のフォルダの初期化設定
        if self._parameter_config.output_dir_path == '':
            self._parameter_config.output_dir_path = 'output_database_laravel'
        self.import_exel_files = import_exel_files
        # テンプレートソースのフォルダを指定する
        self._template_dir = os.path.dirname(__file__) + '/../template/laravel'

    def make(self):
        """
        ファイルの書き出し
        :return:
        """
        # 作成しているフォルダを削除する
        if os.path.isdir(self._parameter_config.output_dir_path):
            shutil.rmtree(self._parameter_config.output_dir_path)

        # Entityに関するファイルを作成する
        self.__make_entities_files()

        # テーブル作成のマイグレーションファイルを作成する
        self.__make_migration_create_table()

        # 外部キーの設定
        self.__make_migration_foreign_key()

        # インデックスファイルの作成
        self.__make_migration_index()

    def __make_entities_files(self):
        """
        Entityに関するファイルの書き出し
        :return:
        """
        # 保存先のフォルダを作成する
        output_dirs_entity = self._parameter_config.output_dir_path + AppContains.EntitiesDirPath
        os.makedirs(output_dirs_entity, exist_ok=True)
        output_dirs_ext_entity = self._parameter_config.output_dir_path + AppContains.ExtEntitiesDirPath
        os.makedirs(output_dirs_ext_entity, exist_ok=True)

        # Entity.phpファイルの初期化
        source_entity_base_file = open(output_dirs_entity + '/Entity.php', 'w')

        # 基本となるEntityファイルソースを取得して保存する
        entity_base_file = open(self._template_dir + '/Entity.php', 'r')
        entity_base_source = entity_base_file.read()
        source_entity_base_file.write(entity_base_source)
        source_entity_base_file.close()

        # テーブルごとのEntityファイルを作成する
        for table_info in self.import_exel_files.table_info_list:
            # 複数形式となっているテーブル名称を修正する
            table_name = table_info.table_name
            if table_name.endswith('ies'):
                # 最後に「ies」場合は「y」に変換する（例: histories -> history)
                table_name = table_name[0:len(table_name) - 3]
                table_name = table_name + 'y'
            elif table_name.endswith('s'):
                # 最後が「s」の場合はその「s」を削除する
                table_name = table_name[0:len(table_name) - 1]

            print('Create entity files: ' + table_name)

            # ソースのテンプレートを取得する
            entity_file = open(self._template_dir + '/Entities.php', 'r')
            entity_source = entity_file.read()
            entity_source = entity_source.replace('__table_name__', table_info.table_name)

            # テーブル名称からパスカルケースの名称を作成する
            pascal_table_name = re.sub("_(.)", lambda x: x.group(1).upper(), table_name.capitalize())
            entity_name = pascal_table_name + 'Entity'
            entity_source = entity_source.replace('__entity_name__', entity_name)

            # 各ソースの設定を作成する
            # コメントの作成
            entity_source = entity_source.replace('__comment__', table_info.table_display_name)

            # SoftDeleteのフラグ
            if table_info.is_soft_deleted:
                entity_source = entity_source.replace('__soft_delete__', r'use \Illuminate\Database\Eloquent\SoftDeletes;')
            else:
                entity_source = entity_source.replace('__soft_delete__', '')

            # PrimaryKeyの設定
            if len(table_info.primary_keys) == 0:
                # 主キーが存在しない場合
                entity_source = entity_source.replace('__primary_key__', '')
            elif len(table_info.primary_keys) == 1:
                # 主キーが1つの場合
                primary_key = 'protected $primaryKey = \'{}\';'.format(table_info.primary_keys[0])
                entity_source = entity_source.replace('__primary_key__', primary_key)
            else:
                primary_key = 'protected $primaryKey = [\'{}\'];'.format('\',\''.join(table_info.primary_keys))
                entity_source = entity_source.replace('__primary_key__', primary_key)

            # is_incrementing の設定
            if table_info.is_incrementing:
                entity_source = entity_source.replace('__incrementing__', 'true')
            else:
                entity_source = entity_source.replace('__incrementing__', 'false')

            # dates の設定
            if len(table_info.dates) == 0:
                entity_source = entity_source.replace('__dates__', '')
                entity_source = entity_source.replace('__date_format__', '')
            else:
                dates = 'protected $dates = [\'{}\'];'.format('\',\''.join(table_info.dates))
                date_format = 'protected $dateFormat =\'{}\';'.format(table_info.date_format)
                entity_source = entity_source.replace('__dates__', dates)
                entity_source = entity_source.replace('__date_format__', date_format)

            # timestamps の設定
            if table_info.is_timestamps:
                entity_source = entity_source.replace('__time_stamps__', 'true')
            else:
                entity_source = entity_source.replace('__time_stamps__', 'false')

            # ソースコードを書き込み保存する
            source_entity_file = open(output_dirs_entity + '/{}.php'.format(entity_name), 'w')
            source_entity_file.write(entity_source)
            source_entity_file.close()

            # ExtEntityファイルの作成
            self.__make_ext_entities_files(output_dirs_ext_entity, table_info.table_display_name, entity_name)

    def __make_ext_entities_files(self, output_dirs: str, comment: str, entity_name: str):
        """
        ExtEntityファイルの作成
        :return:
        """
        # ソースのテンプレートを取得する
        ext_entity_file = open(self._template_dir + '/ExtEntities.php', 'r')
        ext_entity_source = ext_entity_file.read()
        ext_entity_source = ext_entity_source.replace('__ext_entity_name__', 'Ext' + entity_name)
        ext_entity_source = ext_entity_source.replace('__entity_name__', entity_name)
        ext_entity_source = ext_entity_source.replace('__comment__', comment)

        # ソースコードを書き込み保存する
        source_entity_file = open(output_dirs + '/{}.php'.format('Ext' + entity_name), 'w')
        source_entity_file.write(ext_entity_source)
        source_entity_file.close()

    def __make_migration_create_table(self):
        """
        テーブル作成のマイグレーションファイルを作成する
        :return:
        """
        base_name = '_00000_create_'
        class_base = 'Create'
        console_message = 'Create migration create table: '
        # 保存先のフォルダを作成する
        output_dirs_migrations = self._parameter_config.output_dir_path + AppContains.MigrationDirPath
        os.makedirs(output_dirs_migrations, exist_ok=True)

        # テーブルごとのEntityファイルを作成する
        for table_info in self.import_exel_files.table_info_list:
            # 「migration」テーブルは作成しない
            if table_info.table_name == 'migrations':
                continue

            # クラス名の作成
            file_top_date = self._parameter_config.date.replace('-', '_')
            pascal_table_name = re.sub("_(.)", lambda x: x.group(1).upper(), table_info.table_name.capitalize())
            if self._parameter_config.version != '0':
                # バージョンが0以外の場合は後ろに何も設定しない
                file_name = file_top_date + base_name + table_info.table_name + '_table.php'
                # クラス名を作成する
                class_name = class_base + pascal_table_name + 'Table'
                print(console_message + file_name)
            else:
                # バージョンが0以外の場合は後ろに何も設定しない
                file_name = file_top_date + base_name + table_info.table_name + \
                            '_' + self._parameter_config.version + '_table.php'
                # クラス名を作成する
                class_name = class_base + pascal_table_name + self._parameter_config.version + 'Table'
                print(console_message + file_name)

            # テンプレートソースコードを取得する
            template_source_file = open(self._template_dir + '/migration_create_table.php', 'r')
            template_source = template_source_file.read()
            template_source = template_source.replace('__table_name_display__', table_info.table_display_name)
            template_source = template_source.replace('__table_name__', table_info.table_name)
            template_source = template_source.replace('__class_name__', class_name)

            # カラムのソースコードを設定する
            colum_source = ''
            for colum_info in table_info.column_list:
                # timestampsが設定されている場合は「created_at」と「updated_at」は設定しない
                if table_info.is_timestamps and \
                        (colum_info.colum_name == 'created_at' or colum_info.colum_name == 'updated_at'):
                    continue

                colum_source += '            '
                # カラムの種類を取得する
                colum_type = self.__get_colum_type_migrations_mysql(colum_info.colum_type)
                if colum_type == '':
                    print('Not set colum_type' + colum_info.colum_type)
                    continue

                # 桁数を設定する
                if colum_info.length is not None \
                        and colum_info.length > 0 \
                        and colum_info.decimal is not None \
                        and colum_info.decimal > 0:
                    # 少数の場合
                    colum_source += '$table->{}(\'{}\', {}, {})'.format(colum_type, colum_info.colum_name,
                                                                        colum_info.length, colum_info.decimal)
                elif colum_info.length is not None and colum_info.length > 0:
                    # 桁数が設定されていた場合
                    colum_source += '$table->{}(\'{}\', {})'.format(colum_type, colum_info.colum_name,
                                                                    colum_info.length)
                elif colum_type.startswith('timestamp') and (colum_info.length is None or colum_info.length == 0):
                    # timestampの場合は小数点まで設定できるようにする
                    colum_source += '$table->{}(\'{}\', 3)'.format(colum_type, colum_info.colum_name)
                else:
                    # 桁数が設定されていない場合は通常の設定
                    colum_source += '$table->{}(\'{}\')'.format(colum_type, colum_info.colum_name)

                # Not null 設定 (Not nullの場合にnullableを設定する)
                if not colum_info.is_not_null:
                    colum_source += '->nullable()'

                # Unique 設定
                if colum_info.is_unique:
                    colum_source += '->unique()'

                # default 設定
                if colum_info.default_value is not None and colum_info.default_value != '':
                    colum_source += '->default(\'{}\')'.format(colum_info.default_value)
                elif colum_type.startswith('int') and not colum_info.is_auto_increment:
                    colum_source += '->default(\'0.0\')'

                # is_auto_increment 設定
                if colum_info.is_auto_increment:
                    colum_source += '->autoIncrement()'

                # コメント・カラム理論名
                colum_source += '->comment(\'{}\')'.format(colum_info.colum_comment)
                colum_source += ';\n'

            colum_source += '\n'

            # プライマリキーの設定
            primary_kes = self.__get_primary_key_for_migration(table_info)
            if len(primary_kes) == 1:
                colum_source += '            $table->primary(\'{}\', \'{}\');\n'.format(primary_kes[0],
                                                                                        table_info.table_name + '_pkey')
            if len(primary_kes) > 1:
                colum_source += '            $table->primary([\'{}\'], \'{}\');\n'.format(
                    '\', \''.join(primary_kes),
                    table_info.table_name + '_pkey')

            # timestamps の設定
            if table_info.is_timestamps:
                colum_source += '            $table->timestamps();'

            template_source = template_source.replace('__source_code__', colum_source)
            source_migration_file = open(output_dirs_migrations + '/{}.php'.format(file_name), 'w')
            source_migration_file.write(template_source)
            source_migration_file.close()

    def __make_migration_foreign_key(self):
        """
        foreign key ファイルを作成する
        :return:
        """
        base_name = '_00001_add_foreign_keys_to_'
        class_base = 'AddForeignKeysTo'
        console_message = 'Create migration foreign key: '
        # 保存先のフォルダを作成する
        output_dirs_migrations = self._parameter_config.output_dir_path + AppContains.MigrationDirPath
        os.makedirs(output_dirs_migrations, exist_ok=True)

        # テーブルごとのEntityファイルを作成する
        for table_info in self.import_exel_files.table_info_list:
            # 外部キーが存在しない場合は次の処理を行う
            if len(table_info.foreign_keys) == 0:
                continue

            # ファイル名の作成
            file_top_date = self._parameter_config.date.replace('-', '_')
            pascal_table_name = re.sub("_(.)", lambda x: x.group(1).upper(), table_info.table_name.capitalize())
            if self._parameter_config.version != '0':
                # バージョンが0以外の場合は後ろに何も設定しない
                file_name = file_top_date + base_name + table_info.table_name + '.php'
                # クラス名を作成する
                class_name = class_base + pascal_table_name
                print(console_message + file_name)
            else:
                # バージョンが0以外の場合は後ろに何も設定しない
                file_name = file_top_date + base_name + table_info.table_name + \
                            '_' + self._parameter_config.version + '.php'
                # クラス名を作成する
                class_name = class_base + pascal_table_name + self._parameter_config.version
                print(console_message + file_name)

            # テンプレートソースコードを取得する
            template_source_file = open(self._template_dir + '/migration_foreign_key.php', 'r')
            template_source = template_source_file.read()
            template_source = template_source.replace('__table_name__', table_info.table_name)
            template_source = template_source.replace('__class_name__', class_name)

            # カラムのソースコードを設定する
            foreign_key_source = ''
            drop_source = ''
            for foreign_key in table_info.foreign_keys:
                foreign_key_source += '            $table'
                foreign_key_name = table_info.table_name + '_' + foreign_key.colum_name + '_foreign'

                # drop foreign の設定
                drop_source += '            $table->dropForeign(\'{}\');\n'.format(foreign_key_name)

                # 外部キーの設定
                foreign_key_source += '->foreign(\'{}\', \'{}\')'.format(foreign_key.colum_name, foreign_key_name)

                # references の設定
                foreign_key_source += '->references(\'{}\')'.format(foreign_key.ref_key)

                # on の設定
                foreign_key_source += '->on(\'{}\')'.format(foreign_key.ref_table)

                # onUpdate と onDeleteの設定
                foreign_key_source += '->onUpdate(\'NO ACTION\')'
                foreign_key_source += '->onDelete(\'NO ACTION\');\n'

            template_source = template_source.replace('__source_code__', foreign_key_source)
            template_source = template_source.replace('__drop_source_code__', drop_source)

            # ソースコードの書き出し
            source_migration_file = open(output_dirs_migrations + '/{}.php'.format(file_name), 'w')
            source_migration_file.write(template_source)
            source_migration_file.close()

    def __make_migration_index(self):
        """
        インデックス ファイルを作成する
        :return:
        """
        base_name = '_00002_add_index_to_'
        class_base = 'AddIndexTo'
        console_message = 'Create migration indexes: '
        # 保存先のフォルダを作成する
        output_dirs_migrations = self._parameter_config.output_dir_path + AppContains.MigrationDirPath
        os.makedirs(output_dirs_migrations, exist_ok=True)

        # テーブルごとのEntityファイルを作成する
        for table_info in self.import_exel_files.table_info_list:
            # インデックスが存在しない場合は処理を行わない
            if len(table_info.index_list) == 0:
                continue

            # ファイル名の作成
            file_top_date = self._parameter_config.date.replace('-', '_')
            pascal_table_name = re.sub("_(.)", lambda x: x.group(1).upper(), table_info.table_name.capitalize())
            if self._parameter_config.version != '0':
                # バージョンが0以外の場合は後ろに何も設定しない
                file_name = file_top_date + base_name + table_info.table_name + '.php'
                # クラス名を作成する
                class_name = class_base + pascal_table_name
                print(console_message + file_name)
            else:
                # バージョンが0以外の場合は後ろに何も設定しない
                file_name = file_top_date + base_name + table_info.table_name + \
                            '_' + self._parameter_config.version + '.php'
                # クラス名を作成する
                class_name = class_base + pascal_table_name + self._parameter_config.version
                print(console_message + file_name)

            # テンプレートソースコードを取得する
            template_source_file = open(self._template_dir + '/migration_index.php', 'r')
            template_source = template_source_file.read()
            template_source = template_source.replace('__table_name__', table_info.table_name)
            template_source = template_source.replace('__class_name__', class_name)

            # カラムのソースコードを設定する
            index_source = ''
            drop_source = ''
            for index_info in table_info.index_list:
                index_name = index_info.index_name

                if len(index_info.colum_list) == 1:
                    index_source += '			$table->index(\'{}\', \'{}\');\n'.format(
                        '\', \''.join(index_info.colum_list), index_name)
                else:
                    index_source += '			$table->index([\'{}\'], \'{}\');\n'.format(
                        '\', \''.join(index_info.colum_list), index_name)

                drop_source = '            $table->dropIndex(\'{}\');'.format(index_name)

            template_source = template_source.replace('__source_code__', index_source)
            template_source = template_source.replace('__drop_source_code__', drop_source)

            # ソースコードの書き出し
            source_migration_file = open(output_dirs_migrations + '/{}.php'.format(file_name), 'w')
            source_migration_file.write(template_source)
            source_migration_file.close()

    def __get_colum_type_migrations_mysql(self, colum_type: str) -> str:
        """
        カラムの種類をマイグレーション用に返却する
        :param colum_type:
        :return:
        """
        check_str = colum_type.lower()
        # 定義されているカラムの種類に応じてマイグレーションで使用する文字列に変換する
        if check_str.startswith('char') or check_str.startswith('varchar') or check_str.startswith('bytea'):
            return 'string'
        elif check_str.startswith('text'):
            return 'text'
        elif check_str.startswith('timestamp with time zone') or check_str.startswith('timestamp(p) with time zone'):
            return 'timestampTz'
        elif check_str.startswith('timestamp'):
            return 'timestamp'
        elif check_str.startswith('int'):
            return 'integer'
        elif check_str.startswith('bigint'):
            return 'bigInteger'
        elif check_str.startswith('smallint'):
            return 'smallInteger'
        elif check_str.startswith('tinyint'):
            return 'tinyInteger'
        elif check_str.startswith('tinytext'):
            return 'tinyText'
        elif check_str.startswith('year'):
            return 'year'
        elif check_str.startswith('time'):
            return 'time'
        elif check_str.startswith('datetime'):
            return 'datetime'
        elif check_str.startswith('float'):
            return 'float'
        elif check_str.startswith('boolean'):
            return 'boolean'
        elif check_str.startswith('binary'):
            return 'binary'
        elif check_str.startswith('double'):
            return 'double'
        elif check_str.startswith('decimal'):
            return 'decimal'
        elif check_str.startswith('date'):
            return 'date'

        return ''

    def __get_primary_key_for_migration(self, table_info: TableProperty) -> list[str]:
        """
        マイグレーション作成用のプライマリーキーを作成する
        :return array:
        """
        primary_keys = table_info.primary_keys
        # プライマリーキーの中にオートインクリメントの設定があれば削除する
        for colum_info in table_info.column_list:
            if colum_info.is_auto_increment and colum_info.colum_name in primary_keys:
                primary_keys.remove(colum_info.colum_name)

        return primary_keys
