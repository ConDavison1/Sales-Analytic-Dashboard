-- =======================================================================
-- Google Cloud Sales Analytics - Win Calculation Triggers (UPDATED)
-- =======================================================================
-- 
-- Description:
-- This script implements a sophisticated, modular system of triggers and functions
-- that automatically calculate and record sales wins based on revenue and signing data.
-- It has been updated to include opportunity_id and product_id in the Win table.
--
-- Win Types and Criteria:
-- 1. GCP (Google Cloud Platform) Wins - Levels 1, 2, and 3
--    - Revenue-based pathways: Core products only or mixed products
--    - Contract-based pathways: Duet, Mandiant, Flex CUDs/BQ, and Commit/EA
--    - Combined pathway for Win 3: Revenue achievement plus qualifying contract
--
-- 2. DA (Data Analytics) Wins - Levels 1 and 2
--    - Revenue-based pathways: Data Analytics and Vertex AI products
--    - Contract-based pathway: BQ Editions bookings
--
-- Key Features:
-- - Modular design with separate functions for each win pathway
-- - Automated threshold checks for 3 consecutive months of revenue
-- - Business rules enforcement (e.g., previous year Win 1 restriction)
-- - Win multipliers (1.0x or 0.5x) assigned based on pathway
-- - Win progression tracking (Win 2 → Win 3 automatic evaluation)
--
-- Implementation Notes:
-- - Functions are organized into helper functions, pathway-specific functions, and main triggers
-- - All functions are dropped at script start to ensure clean installation
-- - Each function has a single responsibility with clear parameters and return values
-- - Triggers fire automatically after insertions to Revenue and Signing tables
--
-- Updates:
-- - Updated insert_win function to include opportunity_id and product_id
-- - Modified revenue-based functions to track the specific opportunities generating revenue
-- - Modified signing-based functions to include the opportunity linked to the signing
-- =======================================================================

-- Win Calculation Triggers for Google Cloud Sales Analytics
-- This script creates modular triggers to automatically calculate and record wins
-- based on revenue and signing data

-- =======================================================================
-- First, drop all existing functions to ensure a clean slate
-- =======================================================================

-- Drop all trigger functions
DROP FUNCTION IF EXISTS check_revenue_based_wins() CASCADE;
DROP FUNCTION IF EXISTS check_signing_based_wins() CASCADE;

-- Drop all helper functions
DROP FUNCTION IF EXISTS check_existing_win(INTEGER, VARCHAR, INTEGER, INTEGER) CASCADE;
DROP FUNCTION IF EXISTS check_previous_year_gcp_win1(INTEGER, INTEGER) CASCADE;
DROP FUNCTION IF EXISTS get_fiscal_quarter(INTEGER) CASCADE;
DROP FUNCTION IF EXISTS get_product_ids_by_category(VARCHAR[]) CASCADE;
DROP FUNCTION IF EXISTS insert_win(INTEGER, VARCHAR, INTEGER, DECIMAL, INTEGER, INTEGER, INTEGER, INTEGER) CASCADE;
DROP FUNCTION IF EXISTS check_consecutive_months_revenue(INTEGER, INTEGER, INTEGER[], DECIMAL) CASCADE;
DROP FUNCTION IF EXISTS get_opportunity_for_revenue(INTEGER, INTEGER, INTEGER[]) CASCADE;

-- Drop all win pathway functions
DROP FUNCTION IF EXISTS check_gcp_win1_core_pathway(INTEGER, INTEGER, INTEGER) CASCADE;
DROP FUNCTION IF EXISTS check_gcp_win1_mixed_pathway(INTEGER, INTEGER, INTEGER) CASCADE;
DROP FUNCTION IF EXISTS check_gcp_win2_revenue_pathway(INTEGER, INTEGER, INTEGER) CASCADE;
DROP FUNCTION IF EXISTS check_gcp_win3_combined_pathway(INTEGER, INTEGER, INTEGER) CASCADE;
DROP FUNCTION IF EXISTS check_da_win1_revenue_pathway(INTEGER, INTEGER, INTEGER) CASCADE;
DROP FUNCTION IF EXISTS check_da_win2_revenue_pathway(INTEGER, INTEGER, INTEGER) CASCADE;

-- Drop all signing pathway functions
DROP FUNCTION IF EXISTS check_gcp_win1_duet_pathway(INTEGER, INTEGER, INTEGER, VARCHAR, DECIMAL, INTEGER, INTEGER) CASCADE;
DROP FUNCTION IF EXISTS check_gcp_win1_mandiant_pathway(INTEGER, INTEGER, INTEGER, VARCHAR, DECIMAL, INTEGER, INTEGER) CASCADE;
DROP FUNCTION IF EXISTS check_gcp_win1_flex_cuds_bq_pathway(INTEGER, INTEGER, INTEGER, VARCHAR, DECIMAL, INTEGER, INTEGER) CASCADE;
DROP FUNCTION IF EXISTS check_gcp_win1_commit_ea_pathway(INTEGER, INTEGER, INTEGER, VARCHAR, DECIMAL, INTEGER, INTEGER) CASCADE;
DROP FUNCTION IF EXISTS check_da_win1_bq_editions_pathway(INTEGER, INTEGER, INTEGER, VARCHAR, DECIMAL, INTEGER, INTEGER) CASCADE;

-- =======================================================================
-- Helper Functions
-- =======================================================================

-- Enhanced check_existing_win function with debugging
CREATE OR REPLACE FUNCTION check_existing_win(
    p_client_id INTEGER, 
    p_win_category VARCHAR(10), 
    p_win_level INTEGER, 
    p_fiscal_year INTEGER
) RETURNS BOOLEAN AS $$
DECLARE
    exists_result BOOLEAN;
BEGIN
    -- Check if a win already exists for this client, category, level, and fiscal year
    SELECT EXISTS (
        SELECT 1 FROM Win 
        WHERE client_id = p_client_id
        AND win_category = p_win_category
        AND win_level = p_win_level
        AND fiscal_year = p_fiscal_year
    ) INTO exists_result;
    
    IF exists_result THEN
        RAISE NOTICE 'Client % already has a % Win % in fiscal year %',
                    p_client_id, p_win_category, p_win_level, p_fiscal_year;
    END IF;
    
    RETURN exists_result;
END;
$$ LANGUAGE plpgsql;

-- Function to check if a client had a GCP Win 1 in the previous fiscal year
CREATE OR REPLACE FUNCTION check_previous_year_gcp_win1(
    p_client_id INTEGER, 
    p_fiscal_year INTEGER
) RETURNS BOOLEAN AS $$
BEGIN
    -- Check if a GCP Win 1 exists for this client in the previous fiscal year
    RETURN EXISTS (
        SELECT 1 FROM Win 
        WHERE client_id = p_client_id
        AND win_category = 'gcp'
        AND win_level = 1
        AND fiscal_year = p_fiscal_year - 1
    );
END;
$$ LANGUAGE plpgsql;

-- Function to calculate current fiscal quarter based on month
CREATE OR REPLACE FUNCTION get_fiscal_quarter(p_month INTEGER) RETURNS INTEGER AS $$
BEGIN
    RETURN CASE
        WHEN p_month BETWEEN 1 AND 3 THEN 1
        WHEN p_month BETWEEN 4 AND 6 THEN 2
        WHEN p_month BETWEEN 7 AND 9 THEN 3
        WHEN p_month BETWEEN 10 AND 12 THEN 4
    END;
END;
$$ LANGUAGE plpgsql;

-- Function to get product IDs by category
CREATE OR REPLACE FUNCTION get_product_ids_by_category(
    p_categories VARCHAR[] 
) RETURNS INTEGER[] AS $$
DECLARE
    result_ids INTEGER[];
BEGIN
    SELECT array_agg(product_id) INTO result_ids
    FROM Product
    WHERE product_category = ANY(p_categories);
    
    RETURN result_ids;
END;
$$ LANGUAGE plpgsql;

-- Function to get a representative opportunity with better debugging
CREATE OR REPLACE FUNCTION get_opportunity_for_revenue(
    p_client_id INTEGER,
    p_fiscal_year INTEGER,
    p_product_ids INTEGER[]
) RETURNS TABLE(opportunity_id INTEGER, product_id INTEGER) AS $$
DECLARE
    opportunities_count INTEGER;
BEGIN
    -- First, check how many matching opportunities exist
    SELECT COUNT(*) INTO opportunities_count
    FROM Opportunity o
    WHERE o.client_id = p_client_id
    AND o.product_id = ANY(p_product_ids)
    AND o.forecast_category <> 'omit';
    
    RAISE NOTICE 'Client % has % eligible opportunities for products %', 
                 p_client_id, opportunities_count, p_product_ids;
    
    -- Then run the query
    RETURN QUERY
    SELECT o.opportunity_id, o.product_id
    FROM Opportunity o
    WHERE o.client_id = p_client_id
    AND o.product_id = ANY(p_product_ids)
    AND o.forecast_category <> 'omit'  -- Skip opportunities marked as 'omit'
    ORDER BY 
        -- Order by sales stage (most advanced first)
        CASE o.sales_stage
            WHEN 'migrate' THEN 1
            WHEN 'proposal/negotiation' THEN 2
            WHEN 'tech-eval/soln-dev' THEN 3
            WHEN 'refine' THEN 4
            WHEN 'qualify' THEN 5
        END,
        o.probability DESC  -- Higher probability opportunities first
    LIMIT 1;
    
    -- If no opportunities were returned, log a message
    GET DIAGNOSTICS opportunities_count = ROW_COUNT;
    IF opportunities_count = 0 THEN
        RAISE NOTICE 'No eligible opportunities found for client % with products %',
                    p_client_id, p_product_ids;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Updated function to insert a win record with opportunity_id and product_id
CREATE OR REPLACE FUNCTION insert_win(
    p_client_id INTEGER,
    p_win_category VARCHAR(10),
    p_win_level INTEGER,
    p_win_multiplier DECIMAL(3,1),
    p_fiscal_year INTEGER,
    p_fiscal_quarter INTEGER,
    p_opportunity_id INTEGER,
    p_product_id INTEGER
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Win (
        client_id, 
        win_category, 
        win_level, 
        win_multiplier, 
        fiscal_year, 
        fiscal_quarter,
        opportunity_id,
        product_id
    )
    VALUES (
        p_client_id, 
        p_win_category, 
        p_win_level, 
        p_win_multiplier, 
        p_fiscal_year, 
        p_fiscal_quarter,
        p_opportunity_id,
        p_product_id
    );
END;
$$ LANGUAGE plpgsql;

-- Function to check for consecutive months with sufficient revenue with enhanced debugging
CREATE OR REPLACE FUNCTION check_consecutive_months_revenue(
    p_client_id INTEGER,
    p_fiscal_year INTEGER,
    p_product_ids INTEGER[],
    p_revenue_threshold DECIMAL(15,2)
) RETURNS TABLE(found BOOLEAN, last_month INTEGER, revenue DECIMAL(15,2)) AS $$
DECLARE
    month_sequence INTEGER[];
    revenue_amount DECIMAL(15,2);
    temp_found BOOLEAN := FALSE;
    temp_last_month INTEGER := NULL;
    temp_revenue DECIMAL(15,2) := 0;
BEGIN
    -- Get the months where revenue exists for this client and fiscal year
    SELECT array_agg(month ORDER BY month) INTO month_sequence
    FROM (
        SELECT DISTINCT month
        FROM Revenue
        WHERE client_id = p_client_id
        AND fiscal_year = p_fiscal_year
        AND product_id = ANY(p_product_ids)
    ) AS distinct_months;
    
    RAISE NOTICE 'Client %, Year %, Months found: %, Product IDs: %', 
                 p_client_id, p_fiscal_year, month_sequence, p_product_ids;
    
    -- Check if we have enough months to evaluate
    IF month_sequence IS NOT NULL AND array_length(month_sequence, 1) >= 3 THEN
        -- Loop through possible 3-month sequences
        FOR i IN 1..(array_length(month_sequence, 1) - 2) LOOP
            -- Check if these are consecutive months
            IF month_sequence[i+1] = month_sequence[i] + 1 AND 
               month_sequence[i+2] = month_sequence[i] + 2 THEN
                
                RAISE NOTICE 'Examining consecutive months: %, %, %', 
                             month_sequence[i], month_sequence[i+1], month_sequence[i+2];
                
                -- Calculate total revenue for these 3 months
                SELECT COALESCE(SUM(amount), 0) INTO revenue_amount
                FROM Revenue
                WHERE client_id = p_client_id
                AND fiscal_year = p_fiscal_year
                AND month IN (month_sequence[i], month_sequence[i+1], month_sequence[i+2])
                AND product_id = ANY(p_product_ids);
                
                RAISE NOTICE 'Revenue for months %, %, %: $ %, Threshold: $ %', 
                             month_sequence[i], month_sequence[i+1], month_sequence[i+2],
                             revenue_amount, p_revenue_threshold;
                
                -- Check if revenue exceeds threshold over these 3 months
                IF revenue_amount >= p_revenue_threshold THEN
                    temp_found := TRUE;
                    temp_last_month := month_sequence[i+2];
                    temp_revenue := revenue_amount;
                    RAISE NOTICE 'THRESHOLD MET! Revenue: $ %, Threshold: $ %', 
                                 revenue_amount, p_revenue_threshold;
                    EXIT; -- Exit the loop once we find a qualifying sequence
                END IF;
            END IF;
        END LOOP;
    ELSE
        RAISE NOTICE 'Not enough months found to check for consecutive sequences. Month array: %', month_sequence;
    END IF;
    
    -- Explicitly return the results
    found := temp_found;
    last_month := temp_last_month;
    revenue := temp_revenue;
    
    RETURN NEXT;
    RETURN;
END;
$$ LANGUAGE plpgsql;

-- =======================================================================
-- GCP Win 1 - Revenue (Core) Pathway
-- =======================================================================

-- =======================================================================
-- FIXED check_gcp_win1_core_pathway Function
-- =======================================================================

CREATE OR REPLACE FUNCTION check_gcp_win1_core_pathway(
    p_client_id INTEGER,
    p_fiscal_year INTEGER,
    p_fiscal_quarter INTEGER
) RETURNS BOOLEAN AS $$
DECLARE
    win_recorded BOOLEAN := FALSE;
    result RECORD;
    gcp_core_product_ids INTEGER[];
    opp_record RECORD;
    existing_win BOOLEAN;
    previous_win BOOLEAN;
BEGIN
    RAISE NOTICE '=== Starting check_gcp_win1_core_pathway for client_id: %, fiscal_year: %, fiscal_quarter: % ===', 
                 p_client_id, p_fiscal_year, p_fiscal_quarter;
    
    -- Skip check if the client already has a GCP Win 1 in this fiscal year
    existing_win := check_existing_win(p_client_id, 'gcp', 1, p_fiscal_year);
    IF existing_win THEN
        RAISE NOTICE 'Client % already has a GCP Win 1 in fiscal year %. Skipping.', p_client_id, p_fiscal_year;
        RETURN FALSE;
    ELSE
        RAISE NOTICE 'Client % does not have an existing GCP Win 1 in fiscal year %. Continuing...', p_client_id, p_fiscal_year;
    END IF;
    
    -- Skip check if the client had a GCP Win 1 in the previous fiscal year (restriction)
    previous_win := check_previous_year_gcp_win1(p_client_id, p_fiscal_year);
    IF previous_win THEN
        RAISE NOTICE 'Client % had a GCP Win 1 in the previous fiscal year (%). Skipping.', p_client_id, p_fiscal_year - 1;
        RETURN FALSE;
    ELSE
        RAISE NOTICE 'Client % did not have a GCP Win 1 in fiscal year %. Continuing...', p_client_id, p_fiscal_year - 1;
    END IF;
    
    -- Get GCP Core product IDs
    gcp_core_product_ids := get_product_ids_by_category(ARRAY['gcp-core']);
    RAISE NOTICE 'GCP Core product IDs: %', gcp_core_product_ids;
    
    -- Check for 3 consecutive months with sufficient revenue
    RAISE NOTICE 'Checking for 3 consecutive months with at least $15,000 revenue for client % in fiscal year %', p_client_id, p_fiscal_year;
    
    -- Execute the check_consecutive_months_revenue function and capture the result
    SELECT * INTO result FROM check_consecutive_months_revenue(
        p_client_id, 
        p_fiscal_year, 
        gcp_core_product_ids, 
        15000 -- $15,000 threshold
    );
    
    -- Debug output to verify what we got from the function
    RAISE NOTICE 'Result from check_consecutive_months_revenue: found=%, last_month=%, revenue=%', 
                 result.found, result.last_month, result.revenue;
    
    IF result.found IS TRUE THEN  -- Explicitly check if found is TRUE
        RAISE NOTICE 'Found sufficient revenue for client %: $% in 3 consecutive months ending with month %', 
                     p_client_id, result.revenue, result.last_month;
        
        -- Get a representative opportunity for this win
        RAISE NOTICE 'Looking for a representative opportunity for client % with products %', p_client_id, gcp_core_product_ids;
        SELECT * INTO opp_record FROM get_opportunity_for_revenue(
            p_client_id, 
            p_fiscal_year, 
            gcp_core_product_ids
        );
        
        IF opp_record.opportunity_id IS NOT NULL THEN
            RAISE NOTICE 'Found opportunity id: % with product_id: %', opp_record.opportunity_id, opp_record.product_id;
            
            -- Create a new GCP Win 1 record
            RAISE NOTICE 'Inserting GCP Win 1 record for client % in fiscal year % quarter % (opportunity_id: %, product_id: %)',
                         p_client_id, p_fiscal_year, get_fiscal_quarter(result.last_month), opp_record.opportunity_id, opp_record.product_id;
            
            PERFORM insert_win(
                p_client_id,
                'gcp',
                1,
                1.0, -- Full multiplier for Core
                p_fiscal_year,
                get_fiscal_quarter(result.last_month),
                opp_record.opportunity_id,
                opp_record.product_id
            );
            win_recorded := TRUE;
            RAISE NOTICE 'Successfully recorded GCP Win 1 (Core) for client %', p_client_id;
        ELSE
            RAISE WARNING 'No suitable opportunity found for client % with GCP Core products', p_client_id;
        END IF;
    ELSE
        RAISE NOTICE 'Did NOT find sufficient revenue for client % in fiscal year %', p_client_id, p_fiscal_year;
    END IF;
    
    RAISE NOTICE '=== Finished check_gcp_win1_core_pathway for client %. Win recorded: % ===', p_client_id, win_recorded;
    RETURN win_recorded;
END;
$$ LANGUAGE plpgsql;


-- =======================================================================
-- GCP Win 1 - Revenue (Mixed) Pathway
-- =======================================================================

CREATE OR REPLACE FUNCTION check_gcp_win1_mixed_pathway(
    p_client_id INTEGER,
    p_fiscal_year INTEGER,
    p_fiscal_quarter INTEGER
) RETURNS BOOLEAN AS $$
DECLARE
    win_recorded BOOLEAN := FALSE;
    result RECORD;
    gcp_mixed_product_ids INTEGER[];
    opp_record RECORD;
    existing_win BOOLEAN;
    previous_win BOOLEAN;
BEGIN
    RAISE NOTICE '=== Starting check_gcp_win1_mixed_pathway for client_id: %, fiscal_year: %, fiscal_quarter: % ===', 
                 p_client_id, p_fiscal_year, p_fiscal_quarter;

    -- Skip check if the client already has a GCP Win 1 in this fiscal year
    existing_win := check_existing_win(p_client_id, 'gcp', 1, p_fiscal_year);
    IF existing_win THEN
        RAISE NOTICE 'Client % already has a GCP Win 1 in fiscal year %. Skipping.', p_client_id, p_fiscal_year;
        RETURN FALSE;
    ELSE
        RAISE NOTICE 'Client % does not have an existing GCP Win 1 in fiscal year %. Continuing...', p_client_id, p_fiscal_year;
    END IF;
    
    -- Skip check if the client had a GCP Win 1 in the previous fiscal year (restriction)
    previous_win := check_previous_year_gcp_win1(p_client_id, p_fiscal_year);
    IF previous_win THEN
        RAISE NOTICE 'Client % had a GCP Win 1 in the previous fiscal year (%). Skipping.', p_client_id, p_fiscal_year - 1;
        RETURN FALSE;
    ELSE
        RAISE NOTICE 'Client % did not have a GCP Win 1 in fiscal year %. Continuing...', p_client_id, p_fiscal_year - 1;
    END IF;
    
    -- Get Mixed product IDs
    gcp_mixed_product_ids := get_product_ids_by_category(
        ARRAY['gcp-core', 'cloud-security', 'looker', 'apigee', 'maps']
    );
    RAISE NOTICE 'GCP Mixed product IDs: %', gcp_mixed_product_ids;
    
    -- Check for 3 consecutive months with sufficient revenue
    RAISE NOTICE 'Checking for 3 consecutive months with at least $15,000 revenue for client % in fiscal year %', p_client_id, p_fiscal_year;
    
    -- Execute the check_consecutive_months_revenue function and capture the result
    SELECT * INTO result FROM check_consecutive_months_revenue(
        p_client_id, 
        p_fiscal_year, 
        gcp_mixed_product_ids, 
        15000 -- $15,000 threshold
    );
    
    -- Debug output to verify what we got from the function
    RAISE NOTICE 'Result from check_consecutive_months_revenue: found=%, last_month=%, revenue=%', 
                 result.found, result.last_month, result.revenue;
    
    IF result.found IS TRUE THEN  -- Explicitly check if found is TRUE
        RAISE NOTICE 'Found sufficient revenue for client %: $% in 3 consecutive months ending with month %', 
                     p_client_id, result.revenue, result.last_month;
        
        -- Get a representative opportunity for this win
        RAISE NOTICE 'Looking for a representative opportunity for client % with products %', p_client_id, gcp_mixed_product_ids;
        SELECT * INTO opp_record FROM get_opportunity_for_revenue(
            p_client_id, 
            p_fiscal_year, 
            gcp_mixed_product_ids
        );
        
        IF opp_record.opportunity_id IS NOT NULL THEN
            RAISE NOTICE 'Found opportunity id: % with product_id: %', opp_record.opportunity_id, opp_record.product_id;
            
            -- Create a new GCP Win 1 record
            RAISE NOTICE 'Inserting GCP Win 1 record for client % in fiscal year % quarter % (opportunity_id: %, product_id: %)',
                         p_client_id, p_fiscal_year, get_fiscal_quarter(result.last_month), opp_record.opportunity_id, opp_record.product_id;
            
            PERFORM insert_win(
                p_client_id,
                'gcp',
                1,
                0.5, -- Half multiplier for Mixed
                p_fiscal_year,
                get_fiscal_quarter(result.last_month),
                opp_record.opportunity_id,
                opp_record.product_id
            );
            win_recorded := TRUE;
            RAISE NOTICE 'Successfully recorded GCP Win 1 (Mixed) for client %', p_client_id;
        ELSE
            RAISE WARNING 'No suitable opportunity found for client % with GCP Mixed products', p_client_id;
        END IF;
    ELSE
        RAISE NOTICE 'Did NOT find sufficient revenue for client % in fiscal year %', p_client_id, p_fiscal_year;
    END IF;
    
    RAISE NOTICE '=== Finished check_gcp_win1_mixed_pathway for client %. Win recorded: % ===', p_client_id, win_recorded;
    RETURN win_recorded;
END;
$$ LANGUAGE plpgsql;


-- =======================================================================
-- GCP Win 2 - Revenue Pathway
-- =======================================================================

-- Enhanced GCP Win 2 function
CREATE OR REPLACE FUNCTION check_gcp_win2_revenue_pathway(
    p_client_id INTEGER,
    p_fiscal_year INTEGER,
    p_fiscal_quarter INTEGER
) RETURNS BOOLEAN AS $$
DECLARE
    win_recorded BOOLEAN := FALSE;
    result RECORD;
    gcp_core_product_ids INTEGER[];
    opp_record RECORD;
    existing_win BOOLEAN;
BEGIN
    RAISE NOTICE '=== Starting check_gcp_win2_revenue_pathway for client_id: %, fiscal_year: %, fiscal_quarter: % ===', 
                 p_client_id, p_fiscal_year, p_fiscal_quarter;
    
    -- Skip check if the client already has a GCP Win 2 in this fiscal year
    existing_win := check_existing_win(p_client_id, 'gcp', 2, p_fiscal_year);
    IF existing_win THEN
        RAISE NOTICE 'Client % already has a GCP Win 2 in fiscal year %. Skipping.', p_client_id, p_fiscal_year;
        RETURN FALSE;
    ELSE
        RAISE NOTICE 'Client % does not have an existing GCP Win 2 in fiscal year %. Continuing...', p_client_id, p_fiscal_year;
    END IF;
    
    -- Get GCP Core product IDs
    gcp_core_product_ids := get_product_ids_by_category(ARRAY['gcp-core']);
    RAISE NOTICE 'GCP Core product IDs: %', gcp_core_product_ids;
    
    -- Check for 3 consecutive months with sufficient revenue
    RAISE NOTICE 'Checking for 3 consecutive months with at least $37,500 revenue for client % in fiscal year %', p_client_id, p_fiscal_year;
    
    -- Execute the check_consecutive_months_revenue function and capture the result
    SELECT * INTO result FROM check_consecutive_months_revenue(
        p_client_id, 
        p_fiscal_year, 
        gcp_core_product_ids, 
        37500 -- $37,500 threshold
    );
    
    -- Debug output to verify what we got from the function
    RAISE NOTICE 'Result from check_consecutive_months_revenue: found=%, last_month=%, revenue=%', 
                 result.found, result.last_month, result.revenue;
    
    IF result.found IS TRUE THEN  -- Explicitly check if found is TRUE
        RAISE NOTICE 'Found sufficient revenue for client %: $% in 3 consecutive months ending with month %', 
                     p_client_id, result.revenue, result.last_month;
        
        -- Get a representative opportunity for this win
        RAISE NOTICE 'Looking for a representative opportunity for client % with products %', p_client_id, gcp_core_product_ids;
        SELECT * INTO opp_record FROM get_opportunity_for_revenue(
            p_client_id, 
            p_fiscal_year, 
            gcp_core_product_ids
        );
        
        IF opp_record.opportunity_id IS NOT NULL THEN
            RAISE NOTICE 'Found opportunity id: % with product_id: %', opp_record.opportunity_id, opp_record.product_id;
            
            -- Create a new GCP Win 2 record
            RAISE NOTICE 'Inserting GCP Win 2 record for client % in fiscal year % quarter % (opportunity_id: %, product_id: %)',
                         p_client_id, p_fiscal_year, get_fiscal_quarter(result.last_month), opp_record.opportunity_id, opp_record.product_id;
            
            PERFORM insert_win(
                p_client_id,
                'gcp',
                2,
                1.0, -- Full multiplier
                p_fiscal_year,
                get_fiscal_quarter(result.last_month),
                opp_record.opportunity_id,
                opp_record.product_id
            );
            win_recorded := TRUE;
            RAISE NOTICE 'Successfully recorded GCP Win 2 for client %', p_client_id;
            
            -- Check for Win 3 eligibility (if there's a qualifying contract)
            RAISE NOTICE 'Checking for GCP Win 3 eligibility for client %', p_client_id;
            PERFORM check_gcp_win3_combined_pathway(
                p_client_id,
                p_fiscal_year,
                get_fiscal_quarter(result.last_month)
            );
            RAISE NOTICE 'Completed GCP Win 3 eligibility check for client %', p_client_id;
        ELSE
            RAISE WARNING 'No suitable opportunity found for client % with GCP Core products', p_client_id;
        END IF;
    ELSE
        RAISE NOTICE 'Did NOT find sufficient revenue for client % in fiscal year %', p_client_id, p_fiscal_year;
    END IF;
    
    RAISE NOTICE '=== Finished check_gcp_win2_revenue_pathway for client %. Win recorded: % ===', p_client_id, win_recorded;
    RETURN win_recorded;
END;
$$ LANGUAGE plpgsql;

-- =======================================================================
-- GCP Win 3 - Combined Revenue and Contract Pathway
-- =======================================================================

CREATE OR REPLACE FUNCTION check_gcp_win3_combined_pathway(
   p_client_id INTEGER,
   p_fiscal_year INTEGER,
   p_fiscal_quarter INTEGER
) RETURNS BOOLEAN AS $$
DECLARE
   win_recorded BOOLEAN := FALSE;
   contract_opportunity_id INTEGER;
   contract_product_id INTEGER;
   existing_win BOOLEAN;
   has_win2 BOOLEAN;
BEGIN
   RAISE NOTICE '=== Starting check_gcp_win3_combined_pathway for client_id: %, fiscal_year: %, fiscal_quarter: % ===', 
                p_client_id, p_fiscal_year, p_fiscal_quarter;
   
   -- Skip check if the client already has a GCP Win 3 in this fiscal year
   existing_win := check_existing_win(p_client_id, 'gcp', 3, p_fiscal_year);
   IF existing_win THEN
       RAISE NOTICE 'Client % already has a GCP Win 3 in fiscal year %. Skipping.', p_client_id, p_fiscal_year;
       RETURN FALSE;
   ELSE
       RAISE NOTICE 'Client % does not have an existing GCP Win 3 in fiscal year %. Continuing...', p_client_id, p_fiscal_year;
   END IF;
   
   -- Check if client has Win 2
   has_win2 := check_existing_win(p_client_id, 'gcp', 2, p_fiscal_year);
   IF has_win2 THEN
       RAISE NOTICE 'Client % has a GCP Win 2 in fiscal year %. Checking for qualifying contract...', p_client_id, p_fiscal_year;
       
       -- Look for a qualifying contract
       RAISE NOTICE 'Looking for contracts with value >= $200,000 for client %', p_client_id;
       SELECT s.opportunity_id, s.product_id INTO contract_opportunity_id, contract_product_id
       FROM Signing s
       JOIN Product p ON s.product_id = p.product_id
       WHERE s.client_id = p_client_id
       AND p.product_name IN ('gcp-commit-contracts', 'enterprise-agreement')
       AND s.total_contract_value >= 200000
       LIMIT 1;
       
       IF contract_opportunity_id IS NOT NULL THEN
           RAISE NOTICE 'Found qualifying contract for client % (opportunity_id: %, product_id: %)', 
                        p_client_id, contract_opportunity_id, contract_product_id;
           
           -- Create a GCP Win 3 record
           RAISE NOTICE 'Inserting GCP Win 3 record for client % in fiscal year % quarter % (opportunity_id: %, product_id: %)',
                        p_client_id, p_fiscal_year, p_fiscal_quarter, contract_opportunity_id, contract_product_id;
           
           PERFORM insert_win(
               p_client_id,
               'gcp',
               3,
               1.0, -- Full multiplier
               p_fiscal_year,
               p_fiscal_quarter,
               contract_opportunity_id,
               contract_product_id
           );
           win_recorded := TRUE;
           RAISE NOTICE 'Successfully recorded GCP Win 3 for client %', p_client_id;
       ELSE
           RAISE NOTICE 'No qualifying contract found for client % with value >= $200,000', p_client_id;
       END IF;
   ELSE
       RAISE NOTICE 'Client % does not have a GCP Win 2 in fiscal year %. Win 3 not possible.', p_client_id, p_fiscal_year;
   END IF;
   
   RAISE NOTICE '=== Finished check_gcp_win3_combined_pathway for client %. Win recorded: % ===', p_client_id, win_recorded;
   RETURN win_recorded;
END;
$$ LANGUAGE plpgsql;

-- =======================================================================
-- DA Win 1 - Revenue Pathway
-- =======================================================================

CREATE OR REPLACE FUNCTION check_da_win1_revenue_pathway(
    p_client_id INTEGER,
    p_fiscal_year INTEGER,
    p_fiscal_quarter INTEGER
) RETURNS BOOLEAN AS $$
DECLARE
    win_recorded BOOLEAN := FALSE;
    result RECORD;
    da_product_ids INTEGER[];
    opp_record RECORD;
    existing_win BOOLEAN;
BEGIN
    RAISE NOTICE '=== Starting check_da_win1_revenue_pathway for client_id: %, fiscal_year: %, fiscal_quarter: % ===', 
                 p_client_id, p_fiscal_year, p_fiscal_quarter;
    
    -- Skip check if the client already has a DA Win 1 in this fiscal year
    existing_win := check_existing_win(p_client_id, 'da', 1, p_fiscal_year);
    IF existing_win THEN
        RAISE NOTICE 'Client % already has a DA Win 1 in fiscal year %. Skipping.', p_client_id, p_fiscal_year;
        RETURN FALSE;
    ELSE
        RAISE NOTICE 'Client % does not have an existing DA Win 1 in fiscal year %. Continuing...', p_client_id, p_fiscal_year;
    END IF;
    
    -- Get DA product IDs
    da_product_ids := get_product_ids_by_category(
        ARRAY['data-analytics', 'vertex-ai-platform']
    );
    RAISE NOTICE 'DA product IDs: %', da_product_ids;
    
    -- Check for 3 consecutive months with sufficient revenue
    RAISE NOTICE 'Checking for 3 consecutive months with at least $15,000 revenue for client % in fiscal year %', p_client_id, p_fiscal_year;
    
    -- Execute the check_consecutive_months_revenue function and capture the result
    SELECT * INTO result FROM check_consecutive_months_revenue(
        p_client_id, 
        p_fiscal_year, 
        da_product_ids, 
        15000 -- $15,000 threshold
    );
    
    -- Debug output to verify what we got from the function
    RAISE NOTICE 'Result from check_consecutive_months_revenue: found=%, last_month=%, revenue=%', 
                 result.found, result.last_month, result.revenue;
    
    IF result.found IS TRUE THEN  -- Explicitly check if found is TRUE
        RAISE NOTICE 'Found sufficient revenue for client %: $% in 3 consecutive months ending with month %', 
                     p_client_id, result.revenue, result.last_month;
        
        -- Get a representative opportunity for this win
        RAISE NOTICE 'Looking for a representative opportunity for client % with products %', p_client_id, da_product_ids;
        SELECT * INTO opp_record FROM get_opportunity_for_revenue(
            p_client_id, 
            p_fiscal_year, 
            da_product_ids
        );
        
        IF opp_record.opportunity_id IS NOT NULL THEN
            RAISE NOTICE 'Found opportunity id: % with product_id: %', opp_record.opportunity_id, opp_record.product_id;
            
            -- Create a new DA Win 1 record
            RAISE NOTICE 'Inserting DA Win 1 record for client % in fiscal year % quarter % (opportunity_id: %, product_id: %)',
                         p_client_id, p_fiscal_year, get_fiscal_quarter(result.last_month), opp_record.opportunity_id, opp_record.product_id;
            
            PERFORM insert_win(
                p_client_id,
                'da',
                1,
                1.0, -- Full multiplier
                p_fiscal_year,
                get_fiscal_quarter(result.last_month),
                opp_record.opportunity_id,
                opp_record.product_id
            );
            win_recorded := TRUE;
            RAISE NOTICE 'Successfully recorded DA Win 1 for client %', p_client_id;
        ELSE
            RAISE WARNING 'No suitable opportunity found for client % with DA products', p_client_id;
        END IF;
    ELSE
        RAISE NOTICE 'Did NOT find sufficient revenue for client % in fiscal year %', p_client_id, p_fiscal_year;
    END IF;
    
    RAISE NOTICE '=== Finished check_da_win1_revenue_pathway for client %. Win recorded: % ===', p_client_id, win_recorded;
    RETURN win_recorded;
END;
$$ LANGUAGE plpgsql;

-- =======================================================================
-- DA Win 2 - Revenue Pathway
-- =======================================================================
CREATE OR REPLACE FUNCTION check_da_win2_revenue_pathway(
    p_client_id INTEGER,
    p_fiscal_year INTEGER,
    p_fiscal_quarter INTEGER
) RETURNS BOOLEAN AS $$
DECLARE
    win_recorded BOOLEAN := FALSE;
    result RECORD;
    da_product_ids INTEGER[];
    opp_record RECORD;
    existing_win BOOLEAN;
BEGIN
    RAISE NOTICE '=== Starting check_da_win2_revenue_pathway for client_id: %, fiscal_year: %, fiscal_quarter: % ===', 
                 p_client_id, p_fiscal_year, p_fiscal_quarter;
    
    -- Skip check if the client already has a DA Win 2 in this fiscal year
    existing_win := check_existing_win(p_client_id, 'da', 2, p_fiscal_year);
    IF existing_win THEN
        RAISE NOTICE 'Client % already has a DA Win 2 in fiscal year %. Skipping.', p_client_id, p_fiscal_year;
        RETURN FALSE;
    ELSE
        RAISE NOTICE 'Client % does not have an existing DA Win 2 in fiscal year %. Continuing...', p_client_id, p_fiscal_year;
    END IF;
    
    -- Get DA product IDs
    da_product_ids := get_product_ids_by_category(
        ARRAY['data-analytics', 'vertex-ai-platform']
    );
    RAISE NOTICE 'DA product IDs: %', da_product_ids;
    
    -- Check for 3 consecutive months with sufficient revenue
    RAISE NOTICE 'Checking for 3 consecutive months with at least $37,500 revenue for client % in fiscal year %', p_client_id, p_fiscal_year;
    
    -- Execute the check_consecutive_months_revenue function and capture the result
    SELECT * INTO result FROM check_consecutive_months_revenue(
        p_client_id, 
        p_fiscal_year, 
        da_product_ids, 
        37500 -- $37,500 threshold
    );
    
    -- Debug output to verify what we got from the function
    RAISE NOTICE 'Result from check_consecutive_months_revenue: found=%, last_month=%, revenue=%', 
                 result.found, result.last_month, result.revenue;
    
    IF result.found IS TRUE THEN  -- Explicitly check if found is TRUE
        RAISE NOTICE 'Found sufficient revenue for client %: $% in 3 consecutive months ending with month %', 
                     p_client_id, result.revenue, result.last_month;
        
        -- Get a representative opportunity for this win
        RAISE NOTICE 'Looking for a representative opportunity for client % with products %', p_client_id, da_product_ids;
        SELECT * INTO opp_record FROM get_opportunity_for_revenue(
            p_client_id, 
            p_fiscal_year, 
            da_product_ids
        );
        
        IF opp_record.opportunity_id IS NOT NULL THEN
            RAISE NOTICE 'Found opportunity id: % with product_id: %', opp_record.opportunity_id, opp_record.product_id;
            
            -- Create a new DA Win 2 record
            RAISE NOTICE 'Inserting DA Win 2 record for client % in fiscal year % quarter % (opportunity_id: %, product_id: %)',
                         p_client_id, p_fiscal_year, get_fiscal_quarter(result.last_month), opp_record.opportunity_id, opp_record.product_id;
            
            PERFORM insert_win(
                p_client_id,
                'da',
                2,
                1.0, -- Full multiplier
                p_fiscal_year,
                get_fiscal_quarter(result.last_month),
                opp_record.opportunity_id,
                opp_record.product_id
            );
            win_recorded := TRUE;
            RAISE NOTICE 'Successfully recorded DA Win 2 for client %', p_client_id;
        ELSE
            RAISE WARNING 'No suitable opportunity found for client % with DA products', p_client_id;
        END IF;
    ELSE
        RAISE NOTICE 'Did NOT find sufficient revenue for client % in fiscal year %', p_client_id, p_fiscal_year;
    END IF;
    
    RAISE NOTICE '=== Finished check_da_win2_revenue_pathway for client %. Win recorded: % ===', p_client_id, win_recorded;
    RETURN win_recorded;
END;
$$ LANGUAGE plpgsql;

-- =======================================================================
-- Main Revenue Wins Check Function
-- =======================================================================

CREATE OR REPLACE FUNCTION check_revenue_based_wins() RETURNS TRIGGER AS $$
DECLARE
   curr_client_id INTEGER;
   curr_fiscal_year INTEGER;
   curr_fiscal_quarter INTEGER;
   gcp_win1_core BOOLEAN;
   gcp_win1_mixed BOOLEAN;
   gcp_win2 BOOLEAN;
   da_win1 BOOLEAN;
   da_win2 BOOLEAN;
BEGIN
   RAISE NOTICE '=== Starting check_revenue_based_wins trigger for new revenue record ===';
   
   -- Get client ID and fiscal information from the new revenue record
   curr_client_id := NEW.client_id;
   curr_fiscal_year := NEW.fiscal_year;
   curr_fiscal_quarter := NEW.fiscal_quarter;
   
   RAISE NOTICE 'Processing revenue record for client_id: %, fiscal_year: %, fiscal_quarter: %', 
                curr_client_id, curr_fiscal_year, curr_fiscal_quarter;
   
   -- Check each win pathway in sequence
   
   -- GCP Win 1 - Core Pathway
   RAISE NOTICE 'Checking GCP Win 1 - Core Pathway for client %', curr_client_id;
   gcp_win1_core := check_gcp_win1_core_pathway(curr_client_id, curr_fiscal_year, curr_fiscal_quarter);
   
   IF gcp_win1_core THEN
       RAISE NOTICE 'GCP Win 1 - Core Pathway recorded for client %. Skipping Mixed Pathway check.', curr_client_id;
       -- Skip other Win 1 checks if we recorded a win
       NULL;
   ELSE
       -- GCP Win 1 - Mixed Pathway (only check if Core pathway didn't record a win)
       RAISE NOTICE 'GCP Win 1 - Core Pathway not recorded. Checking Mixed Pathway for client %', curr_client_id;
       gcp_win1_mixed := check_gcp_win1_mixed_pathway(curr_client_id, curr_fiscal_year, curr_fiscal_quarter);
       
       IF gcp_win1_mixed THEN
           RAISE NOTICE 'GCP Win 1 - Mixed Pathway recorded for client %', curr_client_id;
       ELSE
           RAISE NOTICE 'GCP Win 1 - Mixed Pathway not recorded for client %', curr_client_id;
       END IF;
   END IF;
   
   -- GCP Win 2 - Revenue Pathway (independent of Win 1)
   RAISE NOTICE 'Checking GCP Win 2 - Revenue Pathway for client % (independent of Win 1)', curr_client_id;
   gcp_win2 := check_gcp_win2_revenue_pathway(curr_client_id, curr_fiscal_year, curr_fiscal_quarter);
   
   IF gcp_win2 THEN
       RAISE NOTICE 'GCP Win 2 - Revenue Pathway recorded for client %', curr_client_id;
   ELSE
       RAISE NOTICE 'GCP Win 2 - Revenue Pathway not recorded for client %', curr_client_id;
   END IF;
   
   -- DA Win 1 - Revenue Pathway (independent of GCP wins)
   RAISE NOTICE 'Checking DA Win 1 - Revenue Pathway for client % (independent of GCP wins)', curr_client_id;
   da_win1 := check_da_win1_revenue_pathway(curr_client_id, curr_fiscal_year, curr_fiscal_quarter);
   
   IF da_win1 THEN
       RAISE NOTICE 'DA Win 1 - Revenue Pathway recorded for client %', curr_client_id;
   ELSE
       RAISE NOTICE 'DA Win 1 - Revenue Pathway not recorded for client %', curr_client_id;
   END IF;
   
   -- DA Win 2 - Revenue Pathway (independent of DA Win 1)
   RAISE NOTICE 'Checking DA Win 2 - Revenue Pathway for client % (independent of DA Win 1)', curr_client_id;
   da_win2 := check_da_win2_revenue_pathway(curr_client_id, curr_fiscal_year, curr_fiscal_quarter);
   
   IF da_win2 THEN
       RAISE NOTICE 'DA Win 2 - Revenue Pathway recorded for client %', curr_client_id;
   ELSE
       RAISE NOTICE 'DA Win 2 - Revenue Pathway not recorded for client %', curr_client_id;
   END IF;
   
   RAISE NOTICE '=== Finished check_revenue_based_wins trigger for client % ===', curr_client_id;
   RAISE NOTICE 'Results: GCP Win 1 Core: %, GCP Win 1 Mixed: %, GCP Win 2: %, DA Win 1: %, DA Win 2: %',
                gcp_win1_core, gcp_win1_mixed, gcp_win2, da_win1, da_win2;
   
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a trigger to check for revenue-based wins after a new revenue record is inserted
CREATE TRIGGER check_revenue_wins_trigger
AFTER INSERT ON Revenue
FOR EACH ROW EXECUTE FUNCTION check_revenue_based_wins();

-- =======================================================================
-- Signing-based Win Pathways
-- =======================================================================

-- Function to check for GCP Win 1 - Duet Pathway
CREATE OR REPLACE FUNCTION check_gcp_win1_duet_pathway(
    p_client_id INTEGER,
    p_fiscal_year INTEGER,
    p_fiscal_quarter INTEGER,
    p_product_name VARCHAR(100),
    p_annual_contract_value DECIMAL(15,2),
    p_opportunity_id INTEGER,
    p_product_id INTEGER
) RETURNS BOOLEAN AS $$
DECLARE
    win_recorded BOOLEAN := FALSE;
BEGIN
    -- Skip check if the client already has a GCP Win 1 in this fiscal year or had one in the previous year
    IF check_existing_win(p_client_id, 'gcp', 1, p_fiscal_year) OR
       check_previous_year_gcp_win1(p_client_id, p_fiscal_year) THEN
        RETURN FALSE;
    END IF;
    
    -- Check if this is a Duet for Workspace contract with ACV >= $60,000
    IF p_product_name = 'duet-for-workspace' AND p_annual_contract_value >= 60000 THEN
        -- Create a new GCP Win 1 record
        PERFORM insert_win(
            p_client_id,
            'gcp',
            1,
            1.0, -- Full multiplier
            p_fiscal_year,
            p_fiscal_quarter,
            p_opportunity_id,
            p_product_id
        );
        win_recorded := TRUE;
    END IF;
    
    RETURN win_recorded;
END;
$$ LANGUAGE plpgsql;

-- Function to check for GCP Win 1 - Mandiant Pathway
CREATE OR REPLACE FUNCTION check_gcp_win1_mandiant_pathway(
    p_client_id INTEGER,
    p_fiscal_year INTEGER,
    p_fiscal_quarter INTEGER,
    p_product_category VARCHAR(50),
    p_annual_contract_value DECIMAL(15,2),
    p_opportunity_id INTEGER,
    p_product_id INTEGER
) RETURNS BOOLEAN AS $$
DECLARE
    win_recorded BOOLEAN := FALSE;
BEGIN
    -- Skip check if the client already has a GCP Win 1 in this fiscal year or had one in the previous year
    IF check_existing_win(p_client_id, 'gcp', 1, p_fiscal_year) OR
       check_previous_year_gcp_win1(p_client_id, p_fiscal_year) THEN
        RETURN FALSE;
    END IF;
    
    -- Check if this is a Mandiant contract with ACV >= $60,000
    IF p_product_category = 'mandiant' AND p_annual_contract_value >= 60000 THEN
        -- Create a new GCP Win 1 record
        PERFORM insert_win(
            p_client_id,
            'gcp',
            1,
            0.5, -- Half multiplier for Mandiant
            p_fiscal_year,
            p_fiscal_quarter,
            p_opportunity_id,
            p_product_id
        );
        win_recorded := TRUE;
    END IF;
    
    RETURN win_recorded;
END;
$$ LANGUAGE plpgsql;

-- Function to check for GCP Win 1 - Flex CUDs/BQ Editions Pathway
CREATE OR REPLACE FUNCTION check_gcp_win1_flex_cuds_bq_pathway(
    p_client_id INTEGER,
    p_fiscal_year INTEGER,
    p_fiscal_quarter INTEGER,
    p_product_name VARCHAR(100),
    p_annual_contract_value DECIMAL(15,2),
    p_opportunity_id INTEGER,
    p_product_id INTEGER
) RETURNS BOOLEAN AS $$
DECLARE
    win_recorded BOOLEAN := FALSE;
BEGIN
    -- Skip check if the client already has a GCP Win 1 in this fiscal year or had one in the previous year
    IF check_existing_win(p_client_id, 'gcp', 1, p_fiscal_year) OR
       check_previous_year_gcp_win1(p_client_id, p_fiscal_year) THEN
        RETURN FALSE;
    END IF;
    
    -- Check if this is a qualifying Flex CUDs or BQ Edition with ACV >= $60,000
    IF (p_product_name = 'flex-committed-use-discounts' OR 
        p_product_name IN ('bq-enterprise-edition-1yr', 'bq-mission-critical-edition-1yr', 'bq-slots-for-annual-subscription')) 
        AND p_annual_contract_value >= 60000 THEN
        -- Create a new GCP Win 1 record
        PERFORM insert_win(
            p_client_id,
            'gcp',
            1,
            1.0, -- Full multiplier
            p_fiscal_year,
            p_fiscal_quarter,
            p_opportunity_id,
            p_product_id
        );
        win_recorded := TRUE;
    END IF;
    
    RETURN win_recorded;
END;
$$ LANGUAGE plpgsql;

-- Function to check for GCP Win 1 - Commit/EA Pathway
CREATE OR REPLACE FUNCTION check_gcp_win1_commit_ea_pathway(
    p_client_id INTEGER,
    p_fiscal_year INTEGER,
    p_fiscal_quarter INTEGER,
    p_product_name VARCHAR(100),
    p_annual_contract_value DECIMAL(15,2),
    p_opportunity_id INTEGER,
    p_product_id INTEGER
) RETURNS BOOLEAN AS $$
DECLARE
    win_recorded BOOLEAN := FALSE;
BEGIN
    -- Skip check if the client already has a GCP Win 1 in this fiscal year or had one in the previous year
    IF check_existing_win(p_client_id, 'gcp', 1, p_fiscal_year) OR
       check_previous_year_gcp_win1(p_client_id, p_fiscal_year) THEN
        RETURN FALSE;
    END IF;
    
    -- Check if this is a Commit Contract or EA with ACV >= $200,000
    IF p_product_name IN ('gcp-commit-contracts', 'enterprise-agreement') AND 
       p_annual_contract_value >= 200000 THEN
        -- Create a new GCP Win 1 record
        PERFORM insert_win(
            p_client_id,
            'gcp',
            1,
            1.0, -- Full multiplier
            p_fiscal_year,
            p_fiscal_quarter,
            p_opportunity_id,
            p_product_id
        );
        win_recorded := TRUE;
    END IF;
    
    RETURN win_recorded;
END;
$$ LANGUAGE plpgsql;

-- Function to check for DA Win 1 - BQ Editions Bookings Pathway
CREATE OR REPLACE FUNCTION check_da_win1_bq_editions_pathway(
    p_client_id INTEGER,
    p_fiscal_year INTEGER,
    p_fiscal_quarter INTEGER,
    p_product_name VARCHAR(100),
    p_annual_contract_value DECIMAL(15,2),
    p_opportunity_id INTEGER,
    p_product_id INTEGER
) RETURNS BOOLEAN AS $$
DECLARE
    win_recorded BOOLEAN := FALSE;
BEGIN
    -- Skip check if the client already has a DA Win 1 in this fiscal year
    IF check_existing_win(p_client_id, 'da', 1, p_fiscal_year) THEN
        RETURN FALSE;
    END IF;
    
    -- Check if this is a qualifying BQ Edition contract with ACV >= $60,000
    IF p_product_name IN (
        'bq-enterprise-edition-1yr', 'bq-enterprise-edition-3yr',
        'bq-enterprise-plus-edition-1yr', 'bq-enterprise-plus-edition-3yr'
    ) AND p_annual_contract_value >= 60000 THEN
        -- Create a new DA Win 1 record
        PERFORM insert_win(
            p_client_id,
            'da',
            1,
            1.0, -- Full multiplier
            p_fiscal_year,
            p_fiscal_quarter,
            p_opportunity_id,
            p_product_id
        );
        win_recorded := TRUE;
    END IF;
    
    RETURN win_recorded;
END;
$$ LANGUAGE plpgsql;

-- Main function for checking signing-based wins
CREATE OR REPLACE FUNCTION check_signing_based_wins() RETURNS TRIGGER AS $$
DECLARE
    curr_client_id INTEGER;
    curr_fiscal_year INTEGER;
    curr_fiscal_quarter INTEGER;
    product_category VARCHAR(50);
    product_name VARCHAR(100);
    annual_contract_value DECIMAL(15,2);
    calculated_term_in_years DECIMAL(5,2);
    curr_opportunity_id INTEGER;
    curr_product_id INTEGER;
BEGIN
    -- Get client ID, opportunity ID, product ID and signing information from the new signing record
    curr_client_id := NEW.client_id;
    curr_fiscal_year := NEW.fiscal_year;
    curr_fiscal_quarter := NEW.fiscal_quarter;
    curr_opportunity_id := NEW.opportunity_id;
    curr_product_id := NEW.product_id;
    
    -- Get product information
    SELECT p.product_category, p.product_name INTO product_category, product_name
    FROM Product p
    WHERE p.product_id = NEW.product_id;
    
    -- Calculate term_in_years using the AGE function
    calculated_term_in_years := 
        EXTRACT(YEAR FROM AGE(NEW.end_date, NEW.start_date)) + 
        EXTRACT(MONTH FROM AGE(NEW.end_date, NEW.start_date)) / 12.0 + 
        EXTRACT(DAY FROM AGE(NEW.end_date, NEW.start_date)) / 365.25;
    
    -- Calculate annual contract value based on total contract value and calculated term in years
    annual_contract_value := NEW.total_contract_value / calculated_term_in_years;
    
    -- Check each signing-based win pathway
    PERFORM check_gcp_win1_duet_pathway(
        curr_client_id, 
        curr_fiscal_year, 
        curr_fiscal_quarter, 
        product_name, 
        annual_contract_value,
        curr_opportunity_id,
        curr_product_id
    );
    
    PERFORM check_gcp_win1_mandiant_pathway(
        curr_client_id, 
        curr_fiscal_year, 
        curr_fiscal_quarter, 
        product_category, 
        annual_contract_value,
        curr_opportunity_id,
        curr_product_id
    );
    
    PERFORM check_gcp_win1_flex_cuds_bq_pathway(
        curr_client_id, 
        curr_fiscal_year, 
        curr_fiscal_quarter, 
        product_name, 
        annual_contract_value,
        curr_opportunity_id,
        curr_product_id
    );
    
    PERFORM check_gcp_win1_commit_ea_pathway(
        curr_client_id, 
        curr_fiscal_year, 
        curr_fiscal_quarter, 
        product_name, 
        annual_contract_value,
        curr_opportunity_id,
        curr_product_id
    );
    
    PERFORM check_da_win1_bq_editions_pathway(
        curr_client_id, 
        curr_fiscal_year, 
        curr_fiscal_quarter, 
        product_name, 
        annual_contract_value,
        curr_opportunity_id,
        curr_product_id
    );
    
    -- Check for GCP Win 3 if client already has Win 2
    IF check_existing_win(curr_client_id, 'gcp', 2, curr_fiscal_year) AND 
       product_name IN ('gcp-commit-contracts', 'enterprise-agreement') AND 
       annual_contract_value >= 200000 THEN
        
        PERFORM check_gcp_win3_combined_pathway(curr_client_id, curr_fiscal_year, curr_fiscal_quarter);
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a trigger to check for signing-based wins after a new signing record is inserted
CREATE TRIGGER check_signing_wins_trigger
AFTER INSERT ON Signing
FOR EACH ROW EXECUTE FUNCTION check_signing_based_wins();