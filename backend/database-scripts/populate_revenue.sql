-- Revenue Population Script for Google Cloud Sales Analytics
-- This script creates revenue records for all signed contracts in the singing table
-- It includes enough revenue to potentially trigger Win 1, Win 2, and Win 3 for both GCP and DA categories
-- Revenue records are properly linked to opportunities, clients, and signings
-- Fiscal periods are consistent with signing dates


TRUNCATE TABLE revenue RESTART IDENTITY CASCADE;

-- ===============================================================================
-- ACCOUNT EXECUTIVE: John Smith (ID: 3)
-- ===============================================================================

-- Maple Leaf Industries (client_id=2) - Enterprise Agreement - Q1 2024 - GCP Win 1 Revenue
-- Signed in Q1 2024, revenue in Q1, Q2, Q3 2024 (3 consecutive months for Win 1)
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q1 2024
(4, 2, 1, 6, 2024, 1, 1, 10000.00),
(4, 2, 1, 6, 2024, 1, 2, 10000.00),
(4, 2, 1, 6, 2024, 1, 3, 10000.00),
-- Q2 2024
(4, 2, 1, 6, 2024, 2, 4, 25000.00),
(4, 2, 1, 6, 2024, 2, 5, 25000.00),
(4, 2, 1, 6, 2024, 2, 6, 25000.00),
-- Q3 2024
(4, 2, 1, 6, 2024, 3, 7, 25000.00),
(4, 2, 1, 6, 2024, 3, 8, 25000.00),
(4, 2, 1, 6, 2024, 3, 9, 25000.00);

-- Pacific Ventures (client_id=3) - GCP Core - Q2 2024 - GCP Win 2 Revenue
-- Large GCP Core revenues for 3 consecutive months to trigger Win 2
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q2 2024
(7, 3, 2, 1, 2024, 2, 4, 10000.00),
(7, 3, 2, 1, 2024, 2, 5, 10000.00),
(7, 3, 2, 1, 2024, 2, 6, 10000.00),
-- Q3 2024 - Higher amounts for Win 2 qualification
(7, 3, 2, 1, 2024, 3, 7, 15000.00),
(7, 3, 2, 1, 2024, 3, 8, 15000.00),
(7, 3, 2, 1, 2024, 3, 9, 15000.00),
-- Q4 2024
(7, 3, 2, 1, 2024, 4, 10, 20000.00),
(7, 3, 2, 1, 2024, 4, 11, 20000.00),
(7, 3, 2, 1, 2024, 4, 12, 20000.00);

-- Capital Partners (client_id=5) - Chronicle - Q3 2024 - DA Win 1 Revenue
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q3 2024
(15, 5, 3, 14, 2024, 3, 7, 5000.00),
(15, 5, 3, 14, 2024, 3, 8, 5000.00),
(15, 5, 3, 14, 2024, 3, 9, 5000.00),
-- Q4 2024
(15, 5, 3, 14, 2024, 4, 10, 8000.00),
(15, 5, 3, 14, 2024, 4, 11, 8000.00),
(15, 5, 3, 14, 2024, 4, 12, 8000.00);

-- Northern Lights Ltd (client_id=6) - GCP Consumption Subscription - Q4 2024 - GCP Win 3 potential
-- High revenue combined with previous Win 2 for potential Win 3
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q4 2024
(16, 6, 4, 3, 2024, 4, 10, 18000.00),
(16, 6, 4, 3, 2024, 4, 11, 18000.00),
(16, 6, 4, 3, 2024, 4, 12, 18000.00),
-- Q1 2025
(16, 6, 4, 3, 2025, 1, 1, 20000.00),
(16, 6, 4, 3, 2025, 1, 2, 20000.00),
(16, 6, 4, 3, 2025, 1, 3, 20000.00);

-- ===============================================================================
-- ACCOUNT EXECUTIVE: Michelle Chen (ID: 4)
-- ===============================================================================

-- Sapphire Solutions (client_id=7) - GCP Core - Q1 2024 - GCP Win 1 Revenue
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q1 2024
(19, 7, 5, 1, 2024, 1, 3, 6000.00),
-- Q2 2024 - Three consecutive months for Win 1
(19, 7, 5, 1, 2024, 2, 4, 6000.00),
(19, 7, 5, 1, 2024, 2, 5, 6000.00),
-- Q3 2024
(19, 7, 5, 1, 2024, 3, 7, 8000.00),
(19, 7, 5, 1, 2024, 3, 8, 8000.00),
(19, 7, 5, 1, 2024, 3, 9, 8000.00);

-- Crimson Innovations (client_id=8) - Data Analytics - Q1 2024 - DA Win 1 Revenue
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q2 2024 - Three consecutive months for Win 1
(23, 8, 6, 7, 2024, 2, 4, 5500.00),
(23, 8, 6, 7, 2024, 2, 5, 5500.00),
(23, 8, 6, 7, 2024, 2, 6, 5500.00),
-- Q3 2024
(23, 8, 6, 7, 2024, 3, 7, 5500.00),
(23, 8, 6, 7, 2024, 3, 8, 5500.00),
(23, 8, 6, 7, 2024, 3, 9, 5500.00);

-- Golden Gate Industries (client_id=9) - GCP Consumption Subscription - Q2 2024 - GCP Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q2 2024
(24, 9, 7, 3, 2024, 2, 6, 8000.00),
-- Q3 2024 - Three consecutive months for Win 1
(24, 9, 7, 3, 2024, 3, 7, 8000.00),
(24, 9, 7, 3, 2024, 3, 8, 8000.00),
(24, 9, 7, 3, 2024, 3, 9, 8000.00),
-- Q4 2024
(24, 9, 7, 3, 2024, 4, 10, 10000.00),
(24, 9, 7, 3, 2024, 4, 11, 10000.00),
(24, 9, 7, 3, 2024, 4, 12, 10000.00);

-- Silverline Logistics (client_id=10) - GCP Core - Q2 2024 - GCP Win 2 Revenue
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q3 2024 - Three consecutive months with higher amounts for Win 2
(27, 10, 8, 1, 2024, 3, 7, 14000.00),
(27, 10, 8, 1, 2024, 3, 8, 14000.00),
(27, 10, 8, 1, 2024, 3, 9, 14000.00),
-- Q4 2024
(27, 10, 8, 1, 2024, 4, 10, 14000.00),
(27, 10, 8, 1, 2024, 4, 11, 14000.00),
(27, 10, 8, 1, 2024, 4, 12, 14000.00);

-- Emerald Dynamics (client_id=11) - Enterprise Agreement - Q3 2024 - GCP Win 3 potential
-- Large revenue for a significant contract that can contribute to Win 3
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q3 2024
(29, 11, 9, 6, 2024, 3, 9, 20000.00),
-- Q4 2024 - Three consecutive months with high amounts
(29, 11, 9, 6, 2024, 4, 10, 20000.00),
(29, 11, 9, 6, 2024, 4, 11, 20000.00),
(29, 11, 9, 6, 2024, 4, 12, 20000.00),
-- Q1 2025
(29, 11, 9, 6, 2025, 1, 1, 25000.00),
(29, 11, 9, 6, 2025, 1, 2, 25000.00),
(29, 11, 9, 6, 2025, 1, 3, 25000.00);

-- Cobalt Systems (client_id=12) - Flex CUDs - Q3 2024 - GCP Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q4 2024 - Three consecutive months for Win 1
(33, 12, 10, 4, 2024, 4, 10, 6000.00),
(33, 12, 10, 4, 2024, 4, 11, 6000.00),
(33, 12, 10, 4, 2024, 4, 12, 6000.00),
-- Q1 2025
(33, 12, 10, 4, 2025, 1, 1, 8000.00),
(33, 12, 10, 4, 2025, 1, 2, 8000.00),
(33, 12, 10, 4, 2025, 1, 3, 8000.00);

-- Starlight Marketing (client_id=13) - BQ Enterprise Edition - Q4 2024 - DA Win 2 potential
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q4 2024
(34, 13, 11, 8, 2024, 4, 10, 4000.00),
(34, 13, 11, 8, 2024, 4, 11, 4000.00),
(34, 13, 11, 8, 2024, 4, 12, 4000.00),
-- Q1 2025 - Three consecutive months with high amounts for Win 2
(34, 13, 11, 8, 2025, 1, 1, 13000.00),
(34, 13, 11, 8, 2025, 1, 2, 13000.00),
(34, 13, 11, 8, 2025, 1, 3, 13000.00);

-- Blue Horizon Media (client_id=14) - Chronicle - Q4 2024 - GCP Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES
-- Q4 2024
(38, 14, 12, 14, 2024, 4, 10, 1500.00),
(38, 14, 12, 14, 2024, 4, 11, 2000.00),
(38, 14, 12, 14, 2024, 4, 12, 2500.00),
-- Q1 2025 - Three consecutive months for Win 1
(38, 14, 12, 14, 2025, 1, 1, 5000.00),
(38, 14, 12, 14, 2025, 1, 2, 5000.00),
(38, 14, 12, 14, 2025, 1, 3, 5000.00);

-- Redwood Financial (client_id=15) - BQ Enterprise Edition 3yr - Q1 2024 - DA Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q1 2024
(39, 15, 13, 9, 2024, 1, 3, 5000.00),
-- Q2 2024 - Three consecutive months for Win 1
(39, 15, 13, 9, 2024, 2, 4, 5000.00),
(39, 15, 13, 9, 2024, 2, 5, 5000.00),
(39, 15, 13, 9, 2024, 2, 6, 5000.00),
-- Q3 2024
(39, 15, 13, 9, 2024, 3, 7, 8000.00),
(39, 15, 13, 9, 2024, 3, 8, 8000.00),
(39, 15, 13, 9, 2024, 3, 9, 8000.00);

-- ===============================================================================
-- ACCOUNT EXECUTIVE: Amar Singh (ID: 5)
-- ===============================================================================

-- Arctic Innovations (client_id=16) - BQ Enterprise Edition - Q1 2024 - DA Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q1 2024
(42, 16, 14, 8, 2024, 1, 3, 5000.00),
-- Q2 2024 - Three consecutive months for Win 1
(42, 16, 14, 8, 2024, 2, 4, 5000.00),
(42, 16, 14, 8, 2024, 2, 5, 5000.00),
(42, 16, 14, 8, 2024, 2, 6, 5000.00),
-- Q3 2024
(42, 16, 14, 8, 2024, 3, 7, 8000.00);

-- Dune Capital (client_id=19) - Enterprise Agreement - Q1 2024 - GCP Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q1 2024
(43, 19, 15, 6, 2024, 1, 3, 8000.00),
-- Q2 2024 - Three consecutive months for Win 1
(43, 19, 15, 6, 2024, 2, 4, 6000.00),
(43, 19, 15, 6, 2024, 2, 5, 6000.00),
(43, 19, 15, 6, 2024, 2, 6, 6000.00),
-- Q3 2024
(43, 19, 15, 6, 2024, 3, 7, 10000.00),
(43, 19, 15, 6, 2024, 3, 8, 10000.00);

-- Keystone Energy (client_id=26) - GCP Core - Q2 2024 - GCP Win 2 potential
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q2 2024
(47, 26, 16, 1, 2024, 2, 6, 10000.00),
-- Q3 2024 - Three consecutive months with high amounts for Win 2
(47, 26, 16, 1, 2024, 3, 7, 12500.00),
(47, 26, 16, 1, 2024, 3, 8, 12500.00),
(47, 26, 16, 1, 2024, 3, 9, 12500.00),
-- Q4 2024
(47, 26, 16, 1, 2024, 4, 10, 15000.00),
(47, 26, 16, 1, 2024, 4, 11, 15000.00);

-- Lakeshore Industries (client_id=27) - Flex CUDs - Q2 2024 - GCP Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q2 2024
(48, 27, 17, 4, 2024, 2, 6, 4000.00),
-- Q3 2024 - Three consecutive months for Win 1
(48, 27, 17, 4, 2024, 3, 7, 5000.00),
(48, 27, 17, 4, 2024, 3, 8, 5000.00),
(48, 27, 17, 4, 2024, 3, 9, 5000.00),
-- Q4 2024
(48, 27, 17, 4, 2024, 4, 10, 7000.00),
(48, 27, 17, 4, 2024, 4, 11, 7000.00);

-- Northstar Holdings (client_id=29) - BQ Enterprise Edition - Q3 2024 - DA Win 2 potential
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q3 2024
(50, 29, 18, 9, 2024, 3, 9, 8000.00),
-- Q4 2024 - Three consecutive months with high amounts for Win 2
(50, 29, 18, 9, 2024, 4, 10, 13000.00),
(50, 29, 18, 9, 2024, 4, 11, 13000.00),
(50, 29, 18, 9, 2024, 4, 12, 13000.00),
-- Q1 2025
(50, 29, 18, 9, 2025, 1, 1, 15000.00),
(50, 29, 18, 9, 2025, 1, 2, 15000.00);

-- Quartz Financial (client_id=32) - Data Analytics - Q3 2024 - DA Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q3 2024
(52, 32, 19, 7, 2024, 3, 9, 4000.00),
-- Q4 2024 - Three consecutive months for Win 1
(52, 32, 19, 7, 2024, 4, 10, 5000.00),
(52, 32, 19, 7, 2024, 4, 11, 5000.00),
(52, 32, 19, 7, 2024, 4, 12, 5000.00),
-- Q1 2025
(52, 32, 19, 7, 2025, 1, 1, 7000.00),
(52, 32, 19, 7, 2025, 1, 2, 7000.00);

-- Ultraviolet Media (client_id=36) - GCP Consumption Subscription - Q4 2024 - GCP Win 3 potential
-- High revenue to complement the Win 2 and qualify for Win 3
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q4 2024
(55, 36, 20, 3, 2024, 4, 12, 10000.00),
-- Q1 2025 - Three consecutive months with high amounts
(55, 36, 20, 3, 2025, 1, 1, 16000.00),
(55, 36, 20, 3, 2025, 1, 2, 16000.00),
(55, 36, 20, 3, 2025, 1, 3, 16000.00);

-- ===============================================================================
-- ACCOUNT EXECUTIVE: Julia Rodriguez (ID: 6)
-- ===============================================================================

-- Apex Innovations (client_id=41) - GCP Core - Q1 2024 - GCP Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q1 2024
(57, 41, 21, 1, 2024, 1, 3, 4000.00),
-- Q2 2024 - Three consecutive months for Win 1
(57, 41, 21, 1, 2024, 2, 4, 5000.00),
(57, 41, 21, 1, 2024, 2, 5, 5000.00),
(57, 41, 21, 1, 2024, 2, 6, 5000.00),
-- Q3 2024
(57, 41, 21, 1, 2024, 3, 7, 8000.00),
(57, 41, 21, 1, 2024, 3, 8, 8000.00);

-- Frontier Analytics (client_id=46) - Data Analytics - Q1 2024 - DA Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q2 2024 - Three consecutive months for Win 1
(60, 46, 22, 7, 2024, 2, 4, 5000.00),
(60, 46, 22, 7, 2024, 2, 5, 5000.00),
(60, 46, 22, 7, 2024, 2, 6, 5000.00),
-- Q3 2024
(60, 46, 22, 7, 2024, 3, 7, 7000.00),
(60, 46, 22, 7, 2024, 3, 8, 7000.00),
(60, 46, 22, 7, 2024, 3, 9, 7000.00);

-- Highland Ventures (client_id=48) - Enterprise Agreement - Q2 2024 - GCP Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q2 2024
(61, 48, 23, 6, 2024, 2, 6, 6000.00),
-- Q3 2024 - Three consecutive months for Win 1
(61, 48, 23, 6, 2024, 3, 7, 6000.00),
(61, 48, 23, 6, 2024, 3, 8, 6000.00),
(61, 48, 23, 6, 2024, 3, 9, 6000.00),
-- Q4 2024
(61, 48, 23, 6, 2024, 4, 10, 10000.00),
(61, 48, 23, 6, 2024, 4, 11, 10000.00);

-- Monarch Systems (client_id=53) - GCP Core - Q2 2024 - GCP Win 2 potential
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q3 2024 - Three consecutive months with high amounts for Win 2
(63, 53, 24, 1, 2024, 3, 7, 13000.00),
(63, 53, 24, 1, 2024, 3, 8, 13000.00),
(63, 53, 24, 1, 2024, 3, 9, 13000.00),
-- Q4 2024
(63, 53, 24, 1, 2024, 4, 10, 15000.00),
(63, 53, 24, 1, 2024, 4, 11, 15000.00),
(63, 53, 24, 1, 2024, 4, 12, 15000.00);

-- Nexus Financial (client_id=54) - Chronicle - Q3 2024 - DA Win 2 potential
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q3 2024
(64, 54, 25, 14, 2024, 3, 9, 9000.00),
-- Q4 2024 - Three consecutive months with high amounts for Win 2
(64, 54, 25, 14, 2024, 4, 10, 13000.00),
(64, 54, 25, 14, 2024, 4, 11, 13000.00),
(64, 54, 25, 14, 2024, 4, 12, 13000.00),
-- Q1 2025
(64, 54, 25, 14, 2025, 1, 1, 14000.00),
(64, 54, 25, 14, 2025, 1, 2, 14000.00);

-- Unity Medical (client_id=61) - BQ Enterprise Edition - Q3 2024 - DA Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q3 2024
(68, 61, 26, 9, 2024, 3, 9, 4000.00),
-- Q4 2024 - Three consecutive months for Win 1
(68, 61, 26, 9, 2024, 4, 10, 5000.00),
(68, 61, 26, 9, 2024, 4, 11, 5000.00),
(68, 61, 26, 9, 2024, 4, 12, 5000.00),
-- Q1 2025
(68, 61, 26, 9, 2025, 1, 1, 7000.00),
(68, 61, 26, 9, 2025, 1, 2, 7000.00);

-- Xavier Innovations (client_id=64) - GCP Core - Q4 2024 - GCP Win 3 potential
-- High revenue to complement Win 2 and qualify for Win 3
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q4 2024
(71, 64, 27, 1, 2024, 4, 12, 9000.00),
-- Q1 2025 - Three consecutive months with high amounts
(71, 64, 27, 1, 2025, 1, 1, 14000.00),
(71, 64, 27, 1, 2025, 1, 2, 14000.00),
(71, 64, 27, 1, 2025, 1, 3, 14000.00);

-- ===============================================================================
-- ACCOUNT EXECUTIVE: Rachel Wilson (ID: 7)
-- ===============================================================================

-- Alpha Strategies (client_id=66) - Enterprise Agreement - Q1 2024 - GCP Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q1 2024
(72, 66, 28, 6, 2024, 1, 3, 5000.00),
-- Q2 2024 - Three consecutive months for Win 1
(72, 66, 28, 6, 2024, 2, 4, 5000.00),
(72, 66, 28, 6, 2024, 2, 5, 5000.00),
(72, 66, 28, 6, 2024, 2, 6, 5000.00),
-- Q3 2024
(72, 66, 28, 6, 2024, 3, 7, 8000.00),
(72, 66, 28, 6, 2024, 3, 8, 8000.00);

-- Cobalt Enterprises (client_id=68) - Flex CUDs - Q1 2024 - GCP Win 2 potential
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q2 2024 - Three consecutive months with high amounts for Win 2
(74, 68, 29, 4, 2024, 2, 4, 13000.00),
(74, 68, 29, 4, 2024, 2, 5, 13000.00),
(74, 68, 29, 4, 2024, 2, 6, 13000.00),
-- Q3 2024
(74, 68, 29, 4, 2024, 3, 7, 15000.00),
(74, 68, 29, 4, 2024, 3, 8, 15000.00),
(74, 68, 29, 4, 2024, 3, 9, 15000.00);

-- Gamma Investments (client_id=72) - Data Analytics - Q2 2024 - DA Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q2 2024
(76, 72, 30, 7, 2024, 2, 6, 4000.00),
-- Q3 2024 - Three consecutive months for Win 1
(76, 72, 30, 7, 2024, 3, 7, 5000.00),
(76, 72, 30, 7, 2024, 3, 8, 5000.00),
(76, 72, 30, 7, 2024, 3, 9, 5000.00),
-- Q4 2024
(76, 72, 30, 7, 2024, 4, 10, 7000.00),
(76, 72, 30, 7, 2024, 4, 11, 7000.00);

-- Lumina Ventures (client_id=77) - BQ Enterprise Edition - Q2 2024 - DA Win 2 potential
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q3 2024 - Three consecutive months with high amounts for Win 2
(79, 77, 31, 8, 2024, 3, 7, 12500.00),
(79, 77, 31, 8, 2024, 3, 8, 12500.00),
(79, 77, 31, 8, 2024, 3, 9, 12500.00),
-- Q4 2024
(79, 77, 31, 8, 2024, 4, 10, 14000.00),
(79, 77, 31, 8, 2024, 4, 11, 14000.00),
(79, 77, 31, 8, 2024, 4, 12, 14000.00);

-- Orbit Industries (client_id=80) - GCP Core - Q3 2024 - GCP Win 3 potential
-- Significant revenue to contribute to Win 3
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q3 2024
(81, 80, 32, 1, 2024, 3, 9, 10000.00),
-- Q4 2024 - Three consecutive months with high amounts
(81, 80, 32, 1, 2024, 4, 10, 15000.00),
(81, 80, 32, 1, 2024, 4, 11, 15000.00),
(81, 80, 32, 1, 2024, 4, 12, 15000.00),
-- Q1 2025
(81, 80, 32, 1, 2025, 1, 1, 18000.00),
(81, 80, 32, 1, 2025, 1, 2, 18000.00);

-- Pulse Analytics (client_id=81) - BQ Enterprise Edition - Q4 2024 - DA Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q4 2024
(82, 81, 33, 9, 2024, 4, 12, 4000.00),
-- Q1 2025 - Three consecutive months for Win 1
(82, 81, 33, 9, 2025, 1, 1, 5500.00),
(82, 81, 33, 9, 2025, 1, 2, 5500.00),
(82, 81, 33, 9, 2025, 1, 3, 5500.00);

-- ===============================================================================
-- ACCOUNT EXECUTIVE: David Kim (ID: 8)
-- ===============================================================================

-- Aegis Consulting (client_id=91) - GCP Core - Q1 2024 - GCP Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q1 2024
(87, 91, 34, 1, 2024, 1, 3, 4000.00),
-- Q2 2024 - Three consecutive months for Win 1
(87, 91, 34, 1, 2024, 2, 4, 5000.00),
(87, 91, 34, 1, 2024, 2, 5, 5000.00),
(87, 91, 34, 1, 2024, 2, 6, 5000.00),
-- Q3 2024
(87, 91, 34, 1, 2024, 3, 7, 8000.00),
(87, 91, 34, 1, 2024, 3, 8, 8000.00);

-- Dynasty Industries (client_id=94) - Enterprise Agreement - Q2 2024 - GCP Win 2 potential
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q2 2024
(90, 94, 35, 6, 2024, 2, 6, 9000.00),
-- Q3 2024 - Three consecutive months with high amounts for Win 2
(90, 94, 35, 6, 2024, 3, 7, 13000.00),
(90, 94, 35, 6, 2024, 3, 8, 13000.00),
(90, 94, 35, 6, 2024, 3, 9, 13000.00),
-- Q4 2024
(90, 94, 35, 6, 2024, 4, 10, 15000.00),
(90, 94, 35, 6, 2024, 4, 11, 15000.00),
(90, 94, 35, 6, 2024, 4, 12, 15000.00);

-- Fidelity Group (client_id=96) - BQ Enterprise Edition - Q3 2024 - DA Win 2 potential
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q3 2024
(91, 96, 36, 9, 2024, 3, 9, 8000.00),
-- Q4 2024 - Three consecutive months with high amounts for Win 2
(91, 96, 36, 9, 2024, 4, 10, 13000.00),
(91, 96, 36, 9, 2024, 4, 11, 13000.00),
(91, 96, 36, 9, 2024, 4, 12, 13000.00),
-- Q1 2025
(91, 96, 36, 9, 2025, 1, 1, 15000.00),
(91, 96, 36, 9, 2025, 1, 2, 15000.00);

-- InnovaTech (client_id=99) - GCP Core - Q4 2024 - GCP Win 3 potential
-- High revenue for Win 3 (complementing the Win 2)
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q4 2024
(94, 99, 37, 1, 2024, 4, 12, 10000.00),
-- Q1 2025 - Three consecutive months with high amounts
(94, 99, 37, 1, 2025, 1, 1, 15000.00),
(94, 99, 37, 1, 2025, 1, 2, 15000.00),
(94, 99, 37, 1, 2025, 1, 3, 15000.00);

-- Junction Capital (client_id=100) - Data Analytics - Q4 2024 - DA Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q4 2024
(95, 100, 38, 7, 2024, 4, 12, 4000.00),
-- Q1 2025 - Three consecutive months for Win 1
(95, 100, 38, 7, 2025, 1, 1, 5500.00),
(95, 100, 38, 7, 2025, 1, 2, 5500.00),
(95, 100, 38, 7, 2025, 1, 3, 5500.00);

-- ===============================================================================
-- ACCOUNT EXECUTIVE: Lisa Jackson (ID: 9)
-- ===============================================================================

-- Unity Systems (client_id=111) - BQ Enterprise Edition - Q1 2024 - DA Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q1 2024
(100, 111, 39, 8, 2024, 1, 3, 4000.00),
-- Q2 2024 - Three consecutive months for Win 1
(100, 111, 39, 8, 2024, 2, 4, 5000.00),
(100, 111, 39, 8, 2024, 2, 5, 5000.00),
(100, 111, 39, 8, 2024, 2, 6, 5000.00),
-- Q3 2024
(100, 111, 39, 8, 2024, 3, 7, 7000.00),
(100, 111, 39, 8, 2024, 3, 8, 7000.00);

-- Axiom Ventures (client_id=116) - Data Analytics - Q2 2024 - DA Win 2 potential
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q2 2024
(102, 116, 40, 7, 2024, 2, 6, 7000.00),
-- Q3 2024 - Three consecutive months with high amounts for Win 2
(102, 116, 40, 7, 2024, 3, 7, 13000.00),
(102, 116, 40, 7, 2024, 3, 8, 13000.00),
(102, 116, 40, 7, 2024, 3, 9, 13000.00),
-- Q4 2024
(102, 116, 40, 7, 2024, 4, 10, 15000.00),
(102, 116, 40, 7, 2024, 4, 11, 15000.00),
(102, 116, 40, 7, 2024, 4, 12, 15000.00);

-- Beacon Capital (client_id=117) - Enterprise Agreement - Q2 2024 - GCP Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q2 2024
(103, 117, 41, 6, 2024, 2, 6, 6000.00),
-- Q3 2024 - Three consecutive months for Win 1
(103, 117, 41, 6, 2024, 3, 7, 6000.00),
(103, 117, 41, 6, 2024, 3, 8, 6000.00),
(103, 117, 41, 6, 2024, 3, 9, 6000.00),
-- Q4 2024
(103, 117, 41, 6, 2024, 4, 10, 9000.00),
(103, 117, 41, 6, 2024, 4, 11, 9000.00),
(103, 117, 41, 6, 2024, 4, 12, 9000.00);

-- Helios Enterprises (client_id=123) - GCP Core - Q3 2024 - GCP Win 2 potential
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q3 2024
(108, 123, 42, 1, 2024, 3, 9, 9000.00),
-- Q4 2024 - Three consecutive months with high amounts for Win 2
(108, 123, 42, 1, 2024, 4, 10, 15000.00),
(108, 123, 42, 1, 2024, 4, 11, 15000.00),
(108, 123, 42, 1, 2024, 4, 12, 15000.00),
-- Q1 2025
(108, 123, 42, 1, 2025, 1, 1, 18000.00),
(108, 123, 42, 1, 2025, 1, 2, 18000.00),
(108, 123, 42, 1, 2025, 1, 3, 18000.00);

-- Jubilee Holdings (client_id=125) - GCP Consumption Subscription - Q3 2024 - GCP Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q3 2024
(109, 125, 43, 3, 2024, 3, 9, 4000.00),
-- Q4 2024 - Three consecutive months for Win 1
(109, 125, 43, 3, 2024, 4, 10, 5500.00),
(109, 125, 43, 3, 2024, 4, 11, 5500.00),
(109, 125, 43, 3, 2024, 4, 12, 5500.00),
-- Q1 2025
(109, 125, 43, 3, 2025, 1, 1, 7000.00),
(109, 125, 43, 3, 2025, 1, 2, 7000.00),
(109, 125, 43, 3, 2025, 1, 3, 7000.00);

-- Paragon Systems (client_id=131) - Chronicle - Q4 2024 - GCP Win 3 potential
-- High revenue to complement Win 2 and qualify for Win 3
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q4 2024
(113, 131, 44, 14, 2024, 4, 12, 9000.00),
-- Q1 2025 - Three consecutive months with high amounts
(113, 131, 44, 14, 2025, 1, 1, 14000.00),
(113, 131, 44, 14, 2025, 1, 2, 14000.00),
(113, 131, 44, 14, 2025, 1, 3, 14000.00);

-- Stellar Industries (client_id=134) - GCP Core - Q4 2024 - GCP Win 1
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q4 2024
(115, 134, 45, 1, 2024, 4, 12, 3000.00),
-- Q1 2025 - Three consecutive months for Win 1
(115, 134, 45, 1, 2025, 1, 1, 5500.00),
(115, 134, 45, 1, 2025, 1, 2, 5500.00),
(115, 134, 45, 1, 2025, 1, 3, 5500.00);

-- ===============================================================================
-- Additional revenue records for major opportunities to ensure triggering of wins
-- ===============================================================================

-- Extra GCP Win 3 revenue boost for John Smith (Q4 2024 - Q1 2025)
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q4 2024
(7, 3, 2, 1, 2024, 4, 10, 5000.00),
(7, 3, 2, 1, 2024, 4, 11, 5000.00),
(7, 3, 2, 1, 2024, 4, 12, 5000.00),
-- Q1 2025
(7, 3, 2, 1, 2025, 1, 1, 8000.00),
(7, 3, 2, 1, 2025, 1, 2, 8000.00),
(7, 3, 2, 1, 2025, 1, 3, 8000.00);

-- Extra DA Win 2 revenue boost for Michelle Chen (Q4 2024 - Q1 2025)
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q4 2024
(39, 15, 13, 9, 2024, 4, 10, 10000.00),
(39, 15, 13, 9, 2024, 4, 11, 10000.00),
(39, 15, 13, 9, 2024, 4, 12, 10000.00),
-- Q1 2025
(39, 15, 13, 9, 2025, 1, 1, 12500.00),
(39, 15, 13, 9, 2025, 1, 2, 12500.00),
(39, 15, 13, 9, 2025, 1, 3, 12500.00);

-- Extra GCP Win 2 revenue boost for Amar Singh (Q4 2024 - Q1 2025)
INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount)
VALUES 
-- Q4 2024
(47, 26, 16, 1, 2024, 4, 10, 15000.00),
(47, 26, 16, 1, 2024, 4, 11, 15000.00),
(47, 26, 16, 1, 2024, 4, 12, 15000.00),
-- Q1 2025
(47, 26, 16, 1, 2025, 1, 1, 20000.00),
(47, 26, 16, 1, 2025, 1, 2, 20000.00),
(47, 26, 16, 1, 2025, 1, 3, 20000.00);

-- Insert revenue records for 2024, balanced across fiscal quarters per account executive.
-- For each opportunity, we insert three rows (one per month in the quarter).
-- Win Level 1: $5,000 per month; Win Level 2: $12,500 per month.
-- signing_id is set to NULL since no contract was signed.

INSERT INTO Revenue (opportunity_id, client_id, signing_id, product_id, fiscal_year, fiscal_quarter, month, amount) VALUES

-- Account Executive 3 (John Smith)
-- Opportunity 8: Win Level 1, Q1 (months 1-3), client_id = 3, product_id = 7
(8, 3, NULL, 7, 2024, 1, 1, 5000.00),
(8, 3, NULL, 7, 2024, 1, 2, 5000.00),
(8, 3, NULL, 7, 2024, 1, 3, 5000.00),

-- Opportunity 13: Win Level 1, Q2 (months 4-6), client_id = 5, product_id = 7
(13, 5, NULL, 7, 2024, 2, 4, 5000.00),
(13, 5, NULL, 7, 2024, 2, 5, 5000.00),
(13, 5, NULL, 7, 2024, 2, 6, 5000.00),

-- Opportunity 14: Win Level 2, Q3 (months 7-9), client_id = 5, product_id = 7
(14, 5, NULL, 7, 2024, 3, 7, 12500.00),
(14, 5, NULL, 7, 2024, 3, 8, 12500.00),
(14, 5, NULL, 7, 2024, 3, 9, 12500.00),

-- Opportunity 18: Win Level 2, Q4 (months 10-12), client_id = 6, product_id = 22
(18, 6, NULL, 22, 2024, 4, 10, 12500.00),
(18, 6, NULL, 22, 2024, 4, 11, 12500.00),
(18, 6, NULL, 22, 2024, 4, 12, 12500.00),

-- Account Executive 4 (Michelle Chen)
-- Opportunity 30: Win Level 1, Q1 (months 1-3), client_id = 11, product_id = 7
(30, 11, NULL, 7, 2024, 1, 1, 5000.00),
(30, 11, NULL, 7, 2024, 1, 2, 5000.00),
(30, 11, NULL, 7, 2024, 1, 3, 5000.00),

-- Opportunity 22: Win Level 2, Q2 (months 4-6), client_id = 8, product_id = 22
(22, 8, NULL, 22, 2024, 2, 4, 12500.00),
(22, 8, NULL, 22, 2024, 2, 5, 12500.00),
(22, 8, NULL, 22, 2024, 2, 6, 12500.00),

-- Opportunity 40: Win Level 2, Q3 (months 7-9), client_id = 15, product_id = 7
(40, 15, NULL, 7, 2024, 3, 7, 12500.00),
(40, 15, NULL, 7, 2024, 3, 8, 12500.00),
(40, 15, NULL, 7, 2024, 3, 9, 12500.00),

-- Account Executive 5 (Amar Singh)
-- Opportunity 45: Win Level 1, Q1 (months 1-3), client_id = 22, product_id = 7
(45, 22, NULL, 7, 2024, 1, 1, 5000.00),
(45, 22, NULL, 7, 2024, 1, 2, 5000.00),
(45, 22, NULL, 7, 2024, 1, 3, 5000.00),

-- Opportunity 53: Win Level 2, Q2 (months 4-6), client_id = 33, product_id = 22
(53, 33, NULL, 22, 2024, 2, 4, 12500.00),
(53, 33, NULL, 22, 2024, 2, 5, 12500.00),
(53, 33, NULL, 22, 2024, 2, 6, 12500.00),

-- Account Executive 6 (Julia Rodriguez)
-- Opportunity 67: Win Level 1, Q1 (months 1-3), client_id = 60, product_id = 7
(67, 60, NULL, 7, 2024, 1, 1, 5000.00),
(67, 60, NULL, 7, 2024, 1, 2, 5000.00),
(67, 60, NULL, 7, 2024, 1, 3, 5000.00),

-- Opportunity 59: Win Level 2, Q2 (months 4-6), client_id = 44, product_id = 22
(59, 44, NULL, 22, 2024, 2, 4, 12500.00),
(59, 44, NULL, 22, 2024, 2, 5, 12500.00),
(59, 44, NULL, 22, 2024, 2, 6, 12500.00),

-- Opportunity 69: Win Level 2, Q3 (months 7-9), client_id = 62, product_id = 2
(69, 62, NULL, 2, 2024, 3, 7, 12500.00),
(69, 62, NULL, 2, 2024, 3, 8, 12500.00),
(69, 62, NULL, 2, 2024, 3, 9, 12500.00),

-- Account Executive 7 (Rachel Wilson)
-- Opportunity 85: Win Level 1, Q1 (months 1-3), client_id = 86, product_id = 7
(85, 86, NULL, 7, 2024, 1, 1, 5000.00),
(85, 86, NULL, 7, 2024, 1, 2, 5000.00),
(85, 86, NULL, 7, 2024, 1, 3, 5000.00),

-- Opportunity 80: Win Level 2, Q2 (months 4-6), client_id = 79, product_id = 22
(80, 79, NULL, 22, 2024, 2, 4, 12500.00),
(80, 79, NULL, 22, 2024, 2, 5, 12500.00),
(80, 79, NULL, 22, 2024, 2, 6, 12500.00),

-- Account Executive 8 (David Kim)
-- Opportunity 88: Win Level 1, Q1 (months 1-3), client_id = 92, product_id = 7
(88, 92, NULL, 7, 2024, 1, 1, 5000.00),
(88, 92, NULL, 7, 2024, 1, 2, 5000.00),
(88, 92, NULL, 7, 2024, 1, 3, 5000.00),

-- Opportunity 92: Win Level 2, Q2 (months 4-6), client_id = 97, product_id = 22
(92, 97, NULL, 22, 2024, 2, 4, 12500.00),
(92, 97, NULL, 22, 2024, 2, 5, 12500.00),
(92, 97, NULL, 22, 2024, 2, 6, 12500.00),

-- Account Executive 9 (Lisa Jackson)
-- Opportunity 112: Win Level 1, Q1 (months 1-3), client_id = 129, product_id = 7
(112, 129, NULL, 7, 2024, 1, 1, 5000.00),
(112, 129, NULL, 7, 2024, 1, 2, 5000.00),
(112, 129, NULL, 7, 2024, 1, 3, 5000.00),

-- Opportunity 107: Win Level 2, Q2 (months 4-6), client_id = 122, product_id = 22
(107, 122, NULL, 22, 2024, 2, 4, 12500.00),
(107, 122, NULL, 22, 2024, 2, 5, 12500.00),
(107, 122, NULL, 22, 2024, 2, 6, 12500.00);


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
