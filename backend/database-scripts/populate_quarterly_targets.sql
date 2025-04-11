-- SQL Script to populate quarterlytarget table based on yearly targets
-- Quarterly distribution:
-- Q1 - 10% 
-- Q2 - 20%
-- Q3 - 25%
-- Q4 - 45%

-- First, clear the existing data from the table
TRUNCATE TABLE quarterlytarget RESTART IDENTITY CASCADE;

-- Use a procedural approach to populate quarterly targets for all yearly targets
DO $$
DECLARE
    yearly_target RECORD;
BEGIN
    -- Loop through all yearly targets
    FOR yearly_target IN 
        SELECT target_id, user_id, fiscal_year, target_type, amount 
        FROM yearlytarget
        ORDER BY target_id
    LOOP
        -- Insert Q1 (10%)
        INSERT INTO quarterlytarget (target_id, fiscal_quarter, user_id, percentage)
        VALUES (yearly_target.target_id, 1, yearly_target.user_id, 10.00);
        
        -- Insert Q2 (20%)
        INSERT INTO quarterlytarget (target_id, fiscal_quarter, user_id, percentage)
        VALUES (yearly_target.target_id, 2, yearly_target.user_id, 20.00);
        
        -- Insert Q3 (25%)
        INSERT INTO quarterlytarget (target_id, fiscal_quarter, user_id, percentage)
        VALUES (yearly_target.target_id, 3, yearly_target.user_id, 25.00);
        
        -- Insert Q4 (45%)
        INSERT INTO quarterlytarget (target_id, fiscal_quarter, user_id, percentage)
        VALUES (yearly_target.target_id, 4, yearly_target.user_id, 45.00);
    END LOOP;
END $$;

-- Verification query (commented out - uncomment to check results)
-- SELECT 
--     qt.quarterly_target_id,
--     qt.target_id,
--     qt.fiscal_quarter,
--     qt.user_id,
--     qt.percentage,
--     yt.fiscal_year,
--     yt.target_type,
--     yt.amount,
--     ROUND(yt.amount * (qt.percentage / 100), 2) AS quarterly_amount
-- FROM 
--     quarterlytarget qt
-- JOIN 
--     yearlytarget yt ON qt.target_id = yt.target_id
-- ORDER BY 
--     qt.target_id, 
--     qt.fiscal_quarter;