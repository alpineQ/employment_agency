#!/bin/bash

sleep 30s
echo -----------------------I AM RUNNING ------------------------------------------
/opt/mssql-tools/bin/sqlcmd -S localhost,1433 -i CreateDB.sql -U SA -P QwErTy123!