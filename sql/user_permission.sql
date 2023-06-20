create user ana_ro with password '';
alter role ana_ro with password '';
grant select on all tables in schema "public" to ana_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO ana_ro;

create user dash_ro with password '';
grant select on all tables in schema "public" to dash_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO dash_ro;

ALTER ROLE api_ingest WITH password '';

CREATE DATABASE airflow;
CREATE USER airflow_rw WITH PASSWORD '';
-- ALTER ROLE airflow_rw WITH PASSWORD '';
GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow_rw;
ALTER USER airflow_rw WITH SUPERUSER; 

SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'airflow';
SELECT * FROM pg_stat_activity WHERE pg_stat_activity.datname='airflow';
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'airflow';

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO airflow_rw;

create user go_rw with password '';
revoke all on all tables in schema "public" from go_rw;
grant update, select, delete, insert on "products"  to go_rw;
grant update, select, delete, insert on "reply_catch"  to go_rw;
grant create on database api_ingest to go_rw;
GRANT USAGE, SELECT ON SEQUENCE products_id_seq TO go_rw;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO go_rw;

select * from information_schema.role_table_grants where grantee='go_rw';
select * from pg_tables where tableowner = 'go_rw';
select r.usename as grantor, e.usename as grantee, nspname, privilege_type, is_grantable from pg_namespace
join lateral (  SELECT * from aclexplode(nspacl) as x ) a on true
join pg_user e on a.grantee = e.usesysid
join pg_user r on a.grantor = r.usesysid 
 where e.usename = 'go_ingest';

-- security user
ALTER DATABASE api_ingest SET anon.privacy_by_default = True;
ALTER DATABASE foo SET session_preload_libraries = 'anon';
CREATE EXTENSION anon CASCADE;
SELECT anon.init();


CREATE EXTENSION IF NOT EXISTS anon CASCADE;
SELECT anon.start_dynamic_masking();

CREATE ROLE skynet LOGIN;
SECURITY LABEL FOR anon ON ROLE skynet IS 'MASKED';

SECURITY LABEL FOR anon ON COLUMN people.lastname
IS 'MASKED WITH FUNCTION anon.fake_last_name()';
SECURITY LABEL FOR anon ON COLUMN people.phone
IS 'MASKED WITH FUNCTION anon.partial(phone,2,$$******$$,2)';


