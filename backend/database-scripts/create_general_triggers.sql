-- =======================================================================
-- Google Cloud Sales Analytics - Database General Triggers Script
-- =======================================================================
-- 
-- Description:
-- This script creates general-purpose triggers for the Google Cloud Sales Analytics
-- database that enforce various business rules, data integrity constraints, and
-- logging mechanisms. These triggers ensure the proper functioning of the application
-- by validating data, maintaining referential integrity, and tracking changes.
--
-- Categories of Triggers:
-- 1. ROLE VALIDATION TRIGGERS - Ensure users have appropriate roles for specific actions
-- 2. DATA CONSISTENCY TRIGGERS - Maintain referential integrity across related tables
-- 3. AUTOMATIC UPDATE TRIGGERS - Handle automatic field updates on record changes
-- 4. AUDIT LOGGING TRIGGERS - Track changes to business-critical data for audit purposes
--
-- Implementation Notes:
-- - All existing trigger functions are dropped before creation to ensure clean installation
-- - Each trigger function includes detailed documentation explaining its purpose
-- - Triggers are attached to specific tables with appropriate execution timing (BEFORE/AFTER)
-- - Error messages are provided to help identify validation issues
--
-- Usage:
-- Execute this script after creating database tables and before populating with data
-- to establish all general validation rules and automated processes.
-- =======================================================================

-- =======================================================================
-- First, drop all existing functions to ensure a clean slate
-- =======================================================================

-- Drop any other potentially related functions from original script
DROP FUNCTION IF EXISTS check_user_role() CASCADE;
DROP FUNCTION IF EXISTS check_client_ae_role() CASCADE;
DROP FUNCTION IF EXISTS check_yearly_target_ae_role() CASCADE;
DROP FUNCTION IF EXISTS check_quarterly_target_ae_role() CASCADE;
DROP FUNCTION IF EXISTS check_signing_opportunity_consistency() CASCADE;
DROP FUNCTION IF EXISTS check_revenue_opportunity_consistency() CASCADE;
DROP FUNCTION IF EXISTS check_quarterly_target_consistency() CASCADE;
DROP FUNCTION IF EXISTS update_opportunity_modified_date() CASCADE;
DROP FUNCTION IF EXISTS log_opportunity_changes() CASCADE;

-- ===================================================================
-- ROLE VALIDATION TRIGGERS
-- ===================================================================

-- ===================================================================
-- Trigger: check_user_role
-- Description: Ensures that users in the DirectorAccountExecutive table have the correct roles
--   - director_id must have the 'director' role
--   - account_executive_id must have the 'account-executive' role
-- When: Before INSERT or UPDATE on DirectorAccountExecutive
-- ===================================================================
CREATE OR REPLACE FUNCTION check_user_role()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if director has the correct role
    IF NOT EXISTS (SELECT 1 FROM "user" WHERE user_id = NEW.director_id AND role = 'director') THEN
        RAISE EXCEPTION 'User with ID % must have director role', NEW.director_id;
    END IF;
    
    -- Check if account executive has the correct role
    IF NOT EXISTS (SELECT 1 FROM "user" WHERE user_id = NEW.account_executive_id AND role = 'account-executive') THEN
        RAISE EXCEPTION 'User with ID % must have account-executive role', NEW.account_executive_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER director_role_check_trigger
BEFORE INSERT OR UPDATE ON DirectorAccountExecutive
FOR EACH ROW EXECUTE FUNCTION check_user_role();

-- ===================================================================
-- Trigger: check_client_ae_role
-- Description: Verifies that the account executive assigned to a client
--   has the 'account-executive' role in the user table
-- When: Before INSERT or UPDATE on Client
-- ===================================================================
CREATE OR REPLACE FUNCTION check_client_ae_role()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if the assigned account executive has the correct role
    IF NOT EXISTS (SELECT 1 FROM "user" WHERE user_id = NEW.account_executive_id AND role = 'account-executive') THEN
        RAISE EXCEPTION 'User with ID % must have account-executive role', NEW.account_executive_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER client_ae_role_check_trigger
BEFORE INSERT OR UPDATE ON Client
FOR EACH ROW EXECUTE FUNCTION check_client_ae_role();

-- ===================================================================
-- Trigger: check_yearly_target_ae_role
-- Description: Ensures that yearly targets are only assigned to users
--   with the 'account-executive' role
-- When: Before INSERT or UPDATE on YearlyTarget
-- ===================================================================
CREATE OR REPLACE FUNCTION check_yearly_target_ae_role()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if the user receiving a target has the account-executive role
    IF NOT EXISTS (SELECT 1 FROM "user" WHERE user_id = NEW.user_id AND role = 'account-executive') THEN
        RAISE EXCEPTION 'User with ID % must have account-executive role', NEW.user_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER yearly_target_ae_role_check_trigger
BEFORE INSERT OR UPDATE ON YearlyTarget
FOR EACH ROW EXECUTE FUNCTION check_yearly_target_ae_role();

-- ===================================================================
-- Trigger: check_quarterly_target_ae_role
-- Description: Ensures that quarterly targets are only assigned to
--   users with the 'account-executive' role
-- When: Before INSERT or UPDATE on QuarterlyTarget
-- ===================================================================
CREATE OR REPLACE FUNCTION check_quarterly_target_ae_role()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if the user receiving a quarterly target has the account-executive role
    IF NOT EXISTS (SELECT 1 FROM "user" WHERE user_id = NEW.user_id AND role = 'account-executive') THEN
        RAISE EXCEPTION 'User with ID % must have account-executive role', NEW.user_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER quarterly_target_ae_role_check_trigger
BEFORE INSERT OR UPDATE ON QuarterlyTarget
FOR EACH ROW EXECUTE FUNCTION check_quarterly_target_ae_role();

-- ===================================================================
-- DATA CONSISTENCY TRIGGERS
-- ===================================================================

-- ===================================================================
-- Trigger: check_signing_opportunity_consistency
-- Description: Ensures that when a Signing record is created or updated,
--   the client_id and product_id match those in the referenced opportunity
-- When: Before INSERT or UPDATE on Signing
-- Purpose: Maintains data integrity by preventing inconsistent relationships
-- ===================================================================
CREATE OR REPLACE FUNCTION check_signing_opportunity_consistency()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if the client_id and product_id match those in the referenced opportunity
    IF NOT EXISTS (
        SELECT 1 FROM Opportunity 
        WHERE opportunity_id = NEW.opportunity_id 
        AND client_id = NEW.client_id 
        AND product_id = NEW.product_id
    ) THEN
        RAISE EXCEPTION 'The client_id and product_id in Signing must match those in the referenced Opportunity';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER signing_opportunity_consistency_trigger
BEFORE INSERT OR UPDATE ON Signing
FOR EACH ROW EXECUTE FUNCTION check_signing_opportunity_consistency();

-- ===================================================================
-- Trigger: check_revenue_opportunity_consistency
-- Description: Ensures that when a Revenue record is created or updated,
--   both the client_id and product_id match those in the referenced opportunity
-- When: Before INSERT or UPDATE on Revenue
-- Purpose: Prevents revenue from being incorrectly attributed to clients or products
-- ===================================================================
CREATE OR REPLACE FUNCTION check_revenue_opportunity_consistency()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if both client_id and product_id match those in the referenced opportunity
    IF NOT EXISTS (
        SELECT 1 FROM Opportunity 
        WHERE opportunity_id = NEW.opportunity_id 
        AND client_id = NEW.client_id
        AND product_id = NEW.product_id
    ) THEN
        RAISE EXCEPTION 'The client_id and product_id in Revenue must match those in the referenced Opportunity';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER revenue_opportunity_consistency_trigger
BEFORE INSERT OR UPDATE ON Revenue
FOR EACH ROW EXECUTE FUNCTION check_revenue_opportunity_consistency();

-- ===================================================================
-- Trigger: check_quarterly_target_consistency
-- Description: Ensures that a quarterly target belongs to the same user
--   as the yearly target it's associated with
-- When: Before INSERT or UPDATE on QuarterlyTarget
-- Purpose: Prevents quarterly targets from being assigned to the wrong user
-- ===================================================================
CREATE OR REPLACE FUNCTION check_quarterly_target_consistency()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if the user_id matches the one in the referenced YearlyTarget
    IF NOT EXISTS (
        SELECT 1 FROM YearlyTarget 
        WHERE target_id = NEW.target_id 
        AND user_id = NEW.user_id
    ) THEN
        RAISE EXCEPTION 'The user_id in QuarterlyTarget must match the one in the referenced YearlyTarget';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER quarterly_target_consistency_trigger
BEFORE INSERT OR UPDATE ON QuarterlyTarget
FOR EACH ROW EXECUTE FUNCTION check_quarterly_target_consistency();

-- ===================================================================
-- AUTOMATIC UPDATE TRIGGERS
-- ===================================================================

-- ===================================================================
-- Trigger: update_opportunity_modified_date
-- Description: Automatically updates the last_modified_date field in the
--   Opportunity table whenever a record is updated
-- When: Before UPDATE on Opportunity
-- Purpose: Maintains accurate tracking of when opportunity records change
-- ===================================================================
CREATE OR REPLACE FUNCTION update_opportunity_modified_date()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_modified_date = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER opportunity_update_modified_date_trigger
BEFORE UPDATE ON Opportunity
FOR EACH ROW EXECUTE FUNCTION update_opportunity_modified_date();

-- ===================================================================
-- AUDIT LOGGING TRIGGERS
-- ===================================================================

-- ===================================================================
-- Trigger: log_opportunity_changes
-- Description: Records changes to important fields in the Opportunity table
--   by creating entries in the UpdateEvent and OpportunityUpdateLog tables
-- When: After UPDATE on Opportunity
-- Purpose: Maintains an audit trail of opportunity changes for reporting and analysis
-- Details: Tracks changes to forecast_category, sales_stage, probability, close_date, and amount
-- ===================================================================
CREATE OR REPLACE FUNCTION log_opportunity_changes()
RETURNS TRIGGER AS $$
DECLARE
    batch_id INTEGER;
    tracked_fields TEXT[] := ARRAY['forecast_category', 'sales_stage', 'probability', 'close_date', 'amount'];
    field_name TEXT;
    old_value TEXT;
    new_value TEXT;
    changed BOOLEAN := FALSE;
BEGIN
    -- Check if any tracked fields have changed
    FOREACH field_name IN ARRAY tracked_fields LOOP
        EXECUTE format('SELECT $1.%I::TEXT, $2.%I::TEXT', field_name, field_name) 
        INTO old_value, new_value
        USING OLD, NEW;
        
        IF old_value IS DISTINCT FROM new_value THEN
            changed := TRUE;
            EXIT;
        END IF;
    END LOOP;
    
    -- Only create a log entry if tracked fields have changed
    IF changed THEN
        -- Create a new entry in UpdateEvent
        INSERT INTO UpdateEvent (opportunity_id, change_date)
        VALUES (NEW.opportunity_id, CURRENT_TIMESTAMP)
        RETURNING change_batch_id INTO batch_id;
        
        -- Log changes for each tracked field that changed
        FOREACH field_name IN ARRAY tracked_fields LOOP
            EXECUTE format('SELECT $1.%I::TEXT, $2.%I::TEXT', field_name, field_name) 
            INTO old_value, new_value
            USING OLD, NEW;
            
            IF old_value IS DISTINCT FROM new_value THEN
                INSERT INTO OpportunityUpdateLog (change_batch_id, field_name, old_value, new_value)
                VALUES (batch_id, field_name, old_value, new_value);
            END IF;
        END LOOP;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER opportunity_log_changes_trigger
AFTER UPDATE ON Opportunity
FOR EACH ROW EXECUTE FUNCTION log_opportunity_changes();