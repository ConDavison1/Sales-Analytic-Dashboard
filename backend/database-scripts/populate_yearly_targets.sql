-- SQL Script to populate yearlytarget table with revenue targets for account executives

-- First, clear the existing data from the table
TRUNCATE TABLE yearlytarget RESTART IDENTITY CASCADE;
-- Based on requirements:
-- First AE: $20 million for 2023, 2024, 2025
-- Second AE: $27 million for 2023, 2024, 2025
-- All other AEs: $2.5 million for 2023, 2024, 2025

-- User ID 3 (John Smith): First account executive - $20 million
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (3, 2023, 'revenue', 20000000.00),
  (3, 2024, 'revenue', 20000000.00),
  (3, 2025, 'revenue', 20000000.00);

-- User ID 4 (Michelle Chen): Second account executive - $27 million
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (4, 2023, 'revenue', 27000000.00),
  (4, 2024, 'revenue', 27000000.00),
  (4, 2025, 'revenue', 27000000.00);

-- All other account executives - $2.5 million each
-- User ID 5 (Amar Singh)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (5, 2023, 'revenue', 2500000.00),
  (5, 2024, 'revenue', 2500000.00),
  (5, 2025, 'revenue', 2500000.00);

-- User ID 6 (Julia Rodriguez)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (6, 2023, 'revenue', 2500000.00),
  (6, 2024, 'revenue', 2500000.00),
  (6, 2025, 'revenue', 2500000.00);

-- User ID 7 (Rachel Wilson)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (7, 2023, 'revenue', 2500000.00),
  (7, 2024, 'revenue', 2500000.00),
  (7, 2025, 'revenue', 2500000.00);

-- User ID 8 (David Kim)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (8, 2023, 'revenue', 2500000.00),
  (8, 2024, 'revenue', 2500000.00),
  (8, 2025, 'revenue', 2500000.00);

-- User ID 9 (Lisa Jackson)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (9, 2023, 'revenue', 2500000.00),
  (9, 2024, 'revenue', 2500000.00),
  (9, 2025, 'revenue', 2500000.00);

-- SIGNINGS TARGETS
-- Adding signing targets for all account executives

-- User ID 3 (John Smith): First account executive - $5 million
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (3, 2023, 'signings', 5000000.00),
  (3, 2024, 'signings', 5000000.00),
  (3, 2025, 'signings', 5000000.00);

-- User ID 4 (Michelle Chen): Second account executive - $5 million
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (4, 2023, 'signings', 5000000.00),
  (4, 2024, 'signings', 5000000.00),
  (4, 2025, 'signings', 5000000.00);

-- All other account executives - $1 million each
-- User ID 5 (Amar Singh)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (5, 2023, 'signings', 1000000.00),
  (5, 2024, 'signings', 1000000.00),
  (5, 2025, 'signings', 1000000.00);

-- User ID 6 (Julia Rodriguez)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (6, 2023, 'signings', 1000000.00),
  (6, 2024, 'signings', 1000000.00),
  (6, 2025, 'signings', 1000000.00);

-- User ID 7 (Rachel Wilson)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (7, 2023, 'signings', 1000000.00),
  (7, 2024, 'signings', 1000000.00),
  (7, 2025, 'signings', 1000000.00);

-- User ID 8 (David Kim)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (8, 2023, 'signings', 1000000.00),
  (8, 2024, 'signings', 1000000.00),
  (8, 2025, 'signings', 1000000.00);

-- User ID 9 (Lisa Jackson)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (9, 2023, 'signings', 1000000.00),
  (9, 2024, 'signings', 1000000.00),
  (9, 2025, 'signings', 1000000.00);

-- WINS TARGETS
-- Adding wins targets for the last 5 account executives (10 per year)

-- User ID 5 (Amar Singh)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (5, 2023, 'wins', 10.00),
  (5, 2024, 'wins', 10.00),
  (5, 2025, 'wins', 10.00);

-- User ID 6 (Julia Rodriguez)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (6, 2023, 'wins', 10.00),
  (6, 2024, 'wins', 10.00),
  (6, 2025, 'wins', 10.00);

-- User ID 7 (Rachel Wilson)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (7, 2023, 'wins', 10.00),
  (7, 2024, 'wins', 10.00),
  (7, 2025, 'wins', 10.00);

-- User ID 8 (David Kim)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (8, 2023, 'wins', 10.00),
  (8, 2024, 'wins', 10.00),
  (8, 2025, 'wins', 10.00);

-- User ID 9 (Lisa Jackson)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (9, 2023, 'wins', 10.00),
  (9, 2024, 'wins', 10.00),
  (9, 2025, 'wins', 10.00);

-- PIPELINE TARGETS
-- Adding pipeline targets for all account executives (same as revenue targets)

-- User ID 3 (John Smith): First account executive - $20 million
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (3, 2023, 'pipeline', 20000000.00),
  (3, 2024, 'pipeline', 20000000.00),
  (3, 2025, 'pipeline', 20000000.00);

-- User ID 4 (Michelle Chen): Second account executive - $27 million
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (4, 2023, 'pipeline', 27000000.00),
  (4, 2024, 'pipeline', 27000000.00),
  (4, 2025, 'pipeline', 27000000.00);

-- All other account executives - $2.5 million each
-- User ID 5 (Amar Singh)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (5, 2023, 'pipeline', 2500000.00),
  (5, 2024, 'pipeline', 2500000.00),
  (5, 2025, 'pipeline', 2500000.00);

-- User ID 6 (Julia Rodriguez)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (6, 2023, 'pipeline', 2500000.00),
  (6, 2024, 'pipeline', 2500000.00),
  (6, 2025, 'pipeline', 2500000.00);

-- User ID 7 (Rachel Wilson)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (7, 2023, 'pipeline', 2500000.00),
  (7, 2024, 'pipeline', 2500000.00),
  (7, 2025, 'pipeline', 2500000.00);

-- User ID 8 (David Kim)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (8, 2023, 'pipeline', 2500000.00),
  (8, 2024, 'pipeline', 2500000.00),
  (8, 2025, 'pipeline', 2500000.00);

-- User ID 9 (Lisa Jackson)
INSERT INTO yearlytarget (user_id, fiscal_year, target_type, amount)
VALUES
  (9, 2023, 'pipeline', 2500000.00),
  (9, 2024, 'pipeline', 2500000.00),
  (9, 2025, 'pipeline', 2500000.00);