#!/bin/bash

sleep 18s
echo ----------------------- CREATING DATABASE ... ------------------------------------------
/opt/mssql-tools/bin/sqlcmd -S localhost,1433 -i /usr/src/app/CreateDB.sql -U SA -P QwErTy123!