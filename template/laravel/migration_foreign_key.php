<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;

/**
 * __table_name__ の外部キー設定
 */
return new class extends Migration
{

	/**
	 * Run the migrations.
	 *
	 * @return void
	 */
	public function up()
	{
		Schema::table('__table_name__', function(Blueprint $table)
		{
__source_code__
        });
    }


    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::table('__table_name__', function(Blueprint $table)
        {
__drop_source_code__
        });
    }

};