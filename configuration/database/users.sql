CREATE TABLE IF NOT EXISTS users (
   user_id CHAR(32) PRIMARY KEY NOT NULL,
   create_date INTEGER NOT NULL,
   last_action_date INTEGER NOT NULL
);