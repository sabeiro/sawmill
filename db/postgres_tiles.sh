psql -p 5432 -U postgres -d tdg -h 172.25.219.51 -c "COPY data_sience.mcdonalds_arne TO '/tmp/dirCount_all.csv' (format csv,header true);"
