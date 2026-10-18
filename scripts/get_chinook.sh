#!/usr/bin/env bash
set -e
mkdir -p data
curl -L -o data/Chinook_Sqlite.sqlite \
  https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite
echo "Saved data/Chinook_Sqlite.sqlite"
