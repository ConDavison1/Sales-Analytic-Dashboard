-- Clear all data and reset identity sequences
TRUNCATE TABLE "user" RESTART IDENTITY CASCADE;

-- Populate "user" table with initial data
-- 1 director (Steve Hogg), 1 admin, and 7 account executives

-- Placeholder password value for demonstration
-- In a real application, use proper password hashing
INSERT INTO "user" (username, email, first_name, last_name, role, hashed_password)
VALUES
    -- Director
    ('shogg', 'steve.hogg@gmail.com', 'Steve', 'Hogg', 'director', 'password'),

    -- Admin
    ('admin1', 'admin@gmail.com', 'Admin', 'User', 'admin', 'password'),

    -- Account Executives
    ('jsmith', 'john.smith@gmail.com', 'John', 'Smith', 'account-executive', 'password'),

    ('mchen', 'michelle.chen@gmail.com', 'Michelle', 'Chen', 'account-executive', 'password'),

    ('asingh', 'amar.singh@gmail.com', 'Amar', 'Singh', 'account-executive', 'password'),

    ('jrodriguez', 'julia.rodriguez@gmail.com', 'Julia', 'Rodriguez', 'account-executive', 'password'),

    ('rwilson', 'rachel.wilson@gmail.com', 'Rachel', 'Wilson', 'account-executive', 'password'),

    ('dkim', 'david.kim@gmail.com', 'David', 'Kim', 'account-executive', 'password'),

    ('ljackson', 'lisa.jackson@gmail.com', 'Lisa', 'Jackson', 'account-executive', 'password');

-- Verify the inserted users
SELECT user_id, username, first_name, last_name, role FROM "user" ORDER BY user_id;

-- Set up the DirectorAccountExecutive relationships
-- Assign all AEs to Steve Hogg (user_id = 1)
INSERT INTO DirectorAccountExecutive (account_executive_id, director_id)
VALUES
    (3, 1),  -- John Smith -> Steve Hogg
    (4, 1),  -- Michelle Chen -> Steve Hogg
    (5, 1),  -- Amar Singh -> Steve Hogg
    (6, 1),  -- Julia Rodriguez -> Steve Hogg
    (7, 1),  -- Rachel Wilson -> Steve Hogg
    (8, 1),  -- David Kim -> Steve Hogg
    (9, 1);  -- Lisa Jackson -> Steve Hogg

-- Verify the director-account executive relationships
SELECT d.first_name || ' ' || d.last_name AS director_name,
       a.first_name || ' ' || a.last_name AS account_executive_name
FROM DirectorAccountExecutive dae
JOIN "user" d ON dae.director_id = d.user_id
JOIN "user" a ON dae.account_executive_id = a.user_id
ORDER BY account_executive_name;
