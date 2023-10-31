-- Path: app/create_roles.sql
-- Insert roles into the test database

USE motiquote_test;

INSERT INTO roles (role) VALUES ('admin');
INSERT INTO roles (role) VALUES ('user');

COMMIT;
