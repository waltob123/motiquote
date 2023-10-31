-- Path: app/create_roles.sql
-- Insert roles into the database

USE motiquote;

INSERT INTO roles (role) VALUES ('admin');
INSERT INTO roles (role) VALUES ('user');

COMMIT;
