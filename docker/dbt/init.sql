create schema source;
CREATE TABLE source.users (
 id bpchar(36) NULL,
 user_name varchar(60) null,
 email varchar(60) null
);
INSERT INTO "source".users (id, user_name, email) VALUES('1', 'jon', 'jon@acme.com');
INSERT INTO "source".users (id, user_name, email) VALUES('1', 'jane', 'jane@acme.com');

