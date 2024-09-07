# er_master_to_migration
This program is a tool to create migration files from databases designed by "ERMaster", a plug-in for "Eclipse".<br/>
For more information on how to use "ERMaster," please refer to the following website.

 - ERMaster<br>
http://ermaster.sourceforge.net/

## How to use
The usage is as follows.

1. Design a database using "ERMaster".
2. Export to Excel file with "ERMaster" function
3. Execute the command with the option "-i" for the exported Excel file.
4. There are other required options, which are specified based on the following commands.

Example command:<br>
```commandline
python er_master_to_migration.py -i database.xls -project laravel -date "2022-07-20"
```

## Requirement
The environment in which this program operates is as follows.<br/>
It is possible that it will work even if the version is small.<br/>
But no guarantees.<br/>

 - python v3.9

The following libraries are used to read Excel files.
```commandline
pip install openpyxl pyexcel pyexcel-xls pyexcel-xlsx
```

## Options

| Option   | Description                                                                                                                   |
|----------|-------------------------------------------------------------------------------------------------------------------------------|
| -i       | Required.<br>Specify the path of the exel file to be read.                                                                    |
| -project | Required.<br>Set the project type.<br/>The following projects are currently supported<br/><br/> - laravel                     |
| -date    | Required.<br>Specifies the date of the migration file. <br/>The format is "yyyy-mm-dd".                                       |
| -o       | Optional.<br>Specify the path to which the source code will be written.                                                       |
| -sql    | Optional.<br>Set the database type. Default is "MySql". Supports the following databases.<br/><br/> - mysql<br/> - postgresql |

## Note
I have created a tool in Laravel that allows me to create a continuous flow of migration files from "ERMaster".<br>
Migration management in Laravel is very useful.<br>
Database management becomes difficult when SQL documents are created in DDL.<br>
If there are tools to manage migration in other frameworks, we would like to add support for this.<br>
Thank you!<br>

## Author
 
* Shinya Tomozumi
* Tomozumi System
* Twitter : https://twitter.com/hincoco27