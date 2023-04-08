<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * __comment__ テーブルのテストデータを作成する
 */
class __factory_name__ extends Factory
{
    /**
     * The name of the factory's corresponding model.
     *
     * @var string
     */
    protected $model = \App\ExtEntities\Entities\__entity_name__::class;

    /**
     * Define the model's default state.
     *
     * @return array
     */
    public function definition(): array
    {
        return [
__columns__
        ];
    }
}

/**
 * Example
__factory_name__::new()->count(10)->create();
 */