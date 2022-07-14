<?php

namespace App\Entities;

use Illuminate\Database\Eloquent\Model;

abstract class Entity extends Model
{
    const CONNECTION = "__sql__";

    // firstOrNewをデフォルトで許可
    protected $guarded = [];

    protected function asDateTime($value)
    {
        // postgresSQLから取得したときにmicro秒が抜けた場合の対応を行う
        if (is_string($value)) {
            $date = \DateTime::createFromFormat('Y-m-d H:i:sP', $value);
            if ($date !== false) {
                return $date;
            }
        }

        return parent::asDateTime($value);
    }
}