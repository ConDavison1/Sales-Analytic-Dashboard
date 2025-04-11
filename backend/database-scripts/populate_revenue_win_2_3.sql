-- SQL Script to Insert Revenue Entries for Level 2 and Level 3 Wins
-- This script creates revenue entries that trigger GCP Win 2, GCP Win 3, and DA Win 2
-- according to criteria from the win calculation triggers.

-- IMPORTANT NOTE: Revenue amounts have been increased to $13,000 per month 
-- (total $39,000 over 3 months) to clearly exceed the $37,500 threshold
-- required for level 2 wins. This ensures the triggers activate properly.

-- =====================================================
-- Criteria for Revenue-Based Wins
-- =====================================================
-- GCP Win 2:
--   - $37,500 over 3 consecutive months from GCP Core products
--   - Products: IDs 1-7 (gcp-core category)
--
-- GCP Win 3:
--   - Client must have GCP Win 2 first
--   - Client must have a qualifying contract (enterprise-agreement or gcp-commit-contracts)
--   - Contract value ≥ $200,000
--
-- DA Win 2:
--   - $37,500 over 3 consecutive months from Data Analytics or Vertex AI products
--   - Products: IDs 8-13 (data-analytics) or ID 22 (vertex-ai-platform)



-- =====================================================
-- John Smith (user_id 3) - DA Win 2 for Client 4 (Prairie Tech)
-- =====================================================
-- Client has opportunity 10 with product_id 8 (bq-enterprise-edition-1yr)
-- We use consecutive months (4,5,6) in Q2 2024

INSERT INTO Revenue (
    opportunity_id, client_id, signing_id, fiscal_year, 
    fiscal_quarter, month, amount, product_id
) VALUES
    -- April 2024
    (10, 4, NULL, 2024, 2, 4, 13000.00, 8),
    -- May 2024
    (10, 4, NULL, 2024, 2, 5, 13000.00, 8),
    -- June 2024
    (10, 4, NULL, 2024, 2, 6, 13000.00, 8);

-- =====================================================
-- Michelle Chen (user_id 4) - GCP Win 2 and Win 3 for Client 9 (Golden Gate Industries)
-- =====================================================
-- Client has opportunity 24 with product_id 3 (gcp-consumption-subscription)
-- Existing signing_id 7 for this opportunity
-- We use consecutive months (7,8,9) in Q3 2024

INSERT INTO Revenue (
    opportunity_id, client_id, signing_id, fiscal_year, 
    fiscal_quarter, month, amount, product_id
) VALUES
    -- July 2024
    (24, 9, 7, 2024, 3, 7, 13000.00, 3),
    -- August 2024
    (24, 9, 7, 2024, 3, 8, 13000.00, 3),
    -- September 2024
    (24, 9, 7, 2024, 3, 9, 13000.00, 3);

-- =====================================================
-- Michelle Chen (user_id 4) - DA Win 2 for Client 15 (Redwood Financial)
-- =====================================================
-- Client has opportunity 39 with product_id 9 (bq-enterprise-edition-3yr)
-- Existing signing_id 13 for this opportunity
-- We use consecutive months (10,11,12) in Q4 2024

INSERT INTO Revenue (
    opportunity_id, client_id, signing_id, fiscal_year, 
    fiscal_quarter, month, amount, product_id
) VALUES
    -- October 2024
    (39, 15, 13, 2024, 4, 10, 13000.00, 9),
    -- November 2024
    (39, 15, 13, 2024, 4, 11, 13000.00, 9),
    -- December 2024
    (39, 15, 13, 2024, 4, 12, 13000.00, 9);

-- =====================================================
-- Amar Singh (user_id 5) - GCP Win 2 and Win 3 for Client 6 (Northern Lights Ltd)
-- =====================================================
-- Client has opportunity 16 with product_id 3 (gcp-consumption-subscription)
-- Existing signing_id 4 for this opportunity
-- We use consecutive months (1,2,3) in Q1 2025

INSERT INTO Revenue (
    opportunity_id, client_id, signing_id, fiscal_year, 
    fiscal_quarter, month, amount, product_id
) VALUES
    -- January 2025
    (16, 6, 4, 2025, 1, 1, 13000.00, 3),
    -- February 2025
    (16, 6, 4, 2025, 1, 2, 13000.00, 3),
    -- March 2025
    (16, 6, 4, 2025, 1, 3, 13000.00, 3);


-- =====================================================
-- Julia Rodriguez (user_id 6) - GCP Win 2 and Win 3 for Client 48 (Highland Ventures)
-- =====================================================
-- Client has opportunity 61 with product_id 6 (enterprise-agreement)
-- Existing signing_id 23 for this opportunity
-- We use consecutive months (7,8,9) in Q3 2024

INSERT INTO Revenue (
    opportunity_id, client_id, signing_id, fiscal_year, 
    fiscal_quarter, month, amount, product_id
) VALUES
    -- July 2024
    (61, 48, 23, 2024, 3, 7, 13000.00, 6),
    -- August 2024
    (61, 48, 23, 2024, 3, 8, 13000.00, 6),
    -- September 2024
    (61, 48, 23, 2024, 3, 9, 13000.00, 6);

-- =====================================================
-- Julia Rodriguez (user_id 6) - DA Win 2 for Client 42 (Brighton Capital)
-- =====================================================
-- Client has opportunity 58 with product_id 8 (bq-enterprise-edition-1yr)
-- We use consecutive months (10,11,12) in Q4 2024

INSERT INTO Revenue (
    opportunity_id, client_id, signing_id, fiscal_year, 
    fiscal_quarter, month, amount, product_id
) VALUES
    -- October 2024
    (58, 42, NULL, 2024, 4, 10, 13000.00, 8),
    -- November 2024
    (58, 42, NULL, 2024, 4, 11, 13000.00, 8),
    -- December 2024
    (58, 42, NULL, 2024, 4, 12, 13000.00, 8);

-- =====================================================
-- Rachel Wilson (user_id 7) - GCP Win 2 and Win 3 for Client 66 (Alpha Strategies)
-- =====================================================
-- Client has opportunity 72 with product_id 6 (enterprise-agreement)
-- Existing signing_id 28 for this opportunity
-- We use consecutive months (1,2,3) in Q1 2024

INSERT INTO Revenue (
    opportunity_id, client_id, signing_id, fiscal_year, 
    fiscal_quarter, month, amount, product_id
) VALUES
    -- January 2024
    (72, 66, 28, 2024, 1, 1, 13000.00, 6),
    -- February 2024
    (72, 66, 28, 2024, 1, 2, 13000.00, 6),
    -- March 2024
    (72, 66, 28, 2024, 1, 3, 13000.00, 6);

-- =====================================================
-- Rachel Wilson (user_id 7) - DA Win 2 for Client 77 (Lumina Ventures)
-- =====================================================
-- Client has opportunity 79 with product_id 8 (bq-enterprise-edition-1yr)
-- Existing signing_id 31 for this opportunity
-- We use consecutive months (4,5,6) in Q2 2024

INSERT INTO Revenue (
    opportunity_id, client_id, signing_id, fiscal_year, 
    fiscal_quarter, month, amount, product_id
) VALUES
    -- April 2024
    (79, 77, 31, 2024, 2, 4, 13000.00, 8),
    -- May 2024
    (79, 77, 31, 2024, 2, 5, 13000.00, 8),
    -- June 2024
    (79, 77, 31, 2024, 2, 6, 13000.00, 8);

-- =====================================================
-- David Kim (user_id 8) - GCP Win 2 and Win 3 for Client 94 (Dynasty Industries)
-- =====================================================
-- Client has opportunity 90 with product_id 6 (enterprise-agreement)
-- Existing signing_id 35 for this opportunity
-- We use consecutive months (7,8,9) in Q3 2024

INSERT INTO Revenue (
    opportunity_id, client_id, signing_id, fiscal_year, 
    fiscal_quarter, month, amount, product_id
) VALUES
    -- July 2024
    (90, 94, 35, 2024, 3, 7, 13000.00, 6),
    -- August 2024
    (90, 94, 35, 2024, 3, 8, 13000.00, 6),
    -- September 2024
    (90, 94, 35, 2024, 3, 9, 13000.00, 6);

-- =====================================================
-- David Kim (user_id 8) - DA Win 2 for Client 81 (Pulse Analytics)
-- =====================================================
-- Client has opportunity 82 with product_id 9 (bq-enterprise-edition-3yr)
-- Existing signing_id 33 for this opportunity
-- We use consecutive months (10,11,12) in Q4 2024

INSERT INTO Revenue (
    opportunity_id, client_id, signing_id, fiscal_year, 
    fiscal_quarter, month, amount, product_id
) VALUES
    -- October 2024
    (82, 81, 33, 2024, 4, 10, 13000.00, 9),
    -- November 2024
    (82, 81, 33, 2024, 4, 11, 13000.00, 9),
    -- December 2024
    (82, 81, 33, 2024, 4, 12, 13000.00, 9);

-- =====================================================
-- Lisa Jackson (user_id 9) - GCP Win 2 and Win 3 for Client 117 (Beacon Capital)
-- =====================================================
-- Client has opportunity 103 with product_id 6 (enterprise-agreement)
-- Existing signing_id 41 for this opportunity
-- We use consecutive months (1,2,3) in Q1 2025

INSERT INTO Revenue (
    opportunity_id, client_id, signing_id, fiscal_year, 
    fiscal_quarter, month, amount, product_id
) VALUES
    -- January 2025
    (103, 117, 41, 2025, 1, 1, 13000.00, 6),
    -- February 2025
    (103, 117, 41, 2025, 1, 2, 13000.00, 6),
    -- March 2025
    (103, 117, 41, 2025, 1, 3, 13000.00, 6);

-- =====================================================
-- Lisa Jackson (user_id 9) - DA Win 2 for Client 121 (Fortress Financial)
-- =====================================================
-- Client has opportunity 106 with product_id 9 (bq-enterprise-edition-3yr)
-- We use consecutive months (4,5,6) in Q2 2024

INSERT INTO Revenue (
    opportunity_id, client_id, signing_id, fiscal_year, 
    fiscal_quarter, month, amount, product_id
) VALUES
    -- April 2024
    (106, 121, NULL, 2024, 2, 4, 13000.00, 9),
    -- May 2024
    (106, 121, NULL, 2024, 2, 5, 13000.00, 9),
    -- June 2024
    (106, 121, NULL, 2024, 2, 6, 13000.00, 9);

COMMIT;