TRUNCATE TABLE signing RESTART IDENTITY CASCADE;

-- Create signing records distributed across all quarters of 2024
-- Ensuring each account executive has signings in different quarters

-- ACCOUNT EXECUTIVE: John Smith (ID: 3) - Q1
-- Maple Leaf Industries - Manufacturing Cloud Transformation (opportunity_id = 4, Enterprise Agreement)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (4, 2, 6, 1200000.00, 450000.00, '2024-03-01', '2027-01-28', '2024-02-15', 2024, 1);

-- ACCOUNT EXECUTIVE: John Smith (ID: 3) - Q2
-- Pacific Ventures - Investment Analytics Platform (opportunity_id = 7, GCP Core)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (7, 3, 1, 450000.00, 135000.00, '2024-06-01', '2026-12-15', '2024-05-18', 2024, 2);

-- ACCOUNT EXECUTIVE: John Smith (ID: 3) - Q3
-- Capital Partners - Financial Threat Detection Program (opportunity_id = 15, Mandiant Security)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (15, 5, 14, 230000.00, 92000.00, '2024-09-01', '2027-05-10', '2024-08-25', 2024, 3);

-- ACCOUNT EXECUTIVE: John Smith (ID: 3) - Q4
-- Northern Lights Ltd - Energy Operations Platform (opportunity_id = 16, GCP Consumption Subscription)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (16, 6, 3, 650000.00, 280000.00, '2024-12-01', '2027-12-20', '2024-11-25', 2024, 4);

-- ACCOUNT EXECUTIVE: Michelle Chen (ID: 4) - Q1
-- Sapphire Solutions - IT Infrastructure Modernization (opportunity_id = 19, GCP Core)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (19, 7, 1, 320000.00, 105000.00, '2024-03-01', '2026-08-30', '2024-02-20', 2024, 1);

-- ACCOUNT EXECUTIVE: Michelle Chen (ID: 4) - Q1
-- Crimson Innovations - Research Analytics Implementation (opportunity_id = 23, Data Analytics)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (23, 8, 7, 190000.00, 75000.00, '2024-03-01', '2026-12-05', '2024-02-22', 2024, 1);

-- ACCOUNT EXECUTIVE: Michelle Chen (ID: 4) - Q2
-- Golden Gate Industries - Manufacturing Operations Platform (opportunity_id = 24, GCP Consumption Subscription)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (24, 9, 3, 450000.00, 190000.00, '2024-06-01', '2027-07-25', '2024-05-18', 2024, 2);

-- ACCOUNT EXECUTIVE: Michelle Chen (ID: 4) - Q2
-- Silverline Logistics - Logistics Operations Platform (opportunity_id = 27, GCP Core)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (27, 10, 1, 380000.00, 128000.00, '2024-06-01', '2026-09-18', '2024-05-23', 2024, 2);

-- ACCOUNT EXECUTIVE: Michelle Chen (ID: 4) - Q3
-- Emerald Dynamics - Energy Cloud Transformation (opportunity_id = 29, Enterprise Agreement)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (29, 11, 6, 850000.00, 390000.00, '2024-09-01', '2027-09-01', '2024-08-21', 2024, 3);

-- ACCOUNT EXECUTIVE: Michelle Chen (ID: 4) - Q3
-- Cobalt Systems - Computing Resource Optimization (opportunity_id = 33, Flex Committed Use Discounts)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (33, 12, 4, 420000.00, 165000.00, '2024-09-01', '2027-01-25', '2024-08-24', 2024, 3);

-- ACCOUNT EXECUTIVE: Michelle Chen (ID: 4) - Q4
-- Starlight Marketing - Marketing Analytics Platform (opportunity_id = 34, BQ Enterprise Edition)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (34, 13, 8, 310000.00, 120000.00, '2024-12-01', '2027-08-08', '2024-11-19', 2024, 4);

-- ACCOUNT EXECUTIVE: Michelle Chen (ID: 4) - Q4
-- Blue Horizon Media - Media Security Services (opportunity_id = 38, Mandiant Security)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (38, 14, 14, 240000.00, 95000.00, '2024-12-01', '2027-12-18', '2024-11-25', 2024, 4);

-- ACCOUNT EXECUTIVE: Michelle Chen (ID: 4) - Q1
-- Redwood Financial - Financial Data Warehouse (opportunity_id = 39, BQ Enterprise Edition 3yr)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (39, 15, 9, 520000.00, 210000.00, '2024-03-01', '2026-12-28', '2024-02-17', 2024, 1);

-- ACCOUNT EXECUTIVE: Amar Singh (ID: 5) - Q1
-- Arctic Innovations - Data Analytics Platform Implementation (opportunity_id = 42, BQ Enterprise Edition)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (42, 16, 8, 375000.00, 140000.00, '2024-03-01', '2026-06-02', '2024-02-15', 2024, 1);

-- ACCOUNT EXECUTIVE: Amar Singh (ID: 5) - Q1
-- Dune Capital - Financial Cloud Transformation (opportunity_id = 43, Enterprise Agreement)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (43, 19, 6, 950000.00, 420000.00, '2024-03-01', '2027-05-15', '2024-02-20', 2024, 1);

-- ACCOUNT EXECUTIVE: Amar Singh (ID: 5) - Q2
-- Keystone Energy - Energy Management Platform (opportunity_id = 47, GCP Core)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (47, 26, 1, 530000.00, 200000.00, '2024-06-01', '2026-12-22', '2024-05-17', 2024, 2);

-- ACCOUNT EXECUTIVE: Amar Singh (ID: 5) - Q2
-- Lakeshore Industries - Manufacturing Infrastructure Optimization (opportunity_id = 48, Flex Committed Use Discounts)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (48, 27, 4, 410000.00, 155000.00, '2024-06-01', '2027-05-05', '2024-05-24', 2024, 2);

-- ACCOUNT EXECUTIVE: Amar Singh (ID: 5) - Q3
-- Northstar Holdings - Financial Data Analytics (opportunity_id = 50, BQ Enterprise Edition)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (50, 29, 9, 390000.00, 145000.00, '2024-09-01', '2027-06-10', '2024-08-21', 2024, 3);

-- ACCOUNT EXECUTIVE: Amar Singh (ID: 5) - Q3
-- Quartz Financial - Financial Analytics Implementation (opportunity_id = 52, Data Analytics)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (52, 32, 7, 295000.00, 110000.00, '2024-09-01', '2027-09-25', '2024-08-25', 2024, 3);

-- ACCOUNT EXECUTIVE: Amar Singh (ID: 5) - Q4
-- Ultraviolet Media - Content Delivery Platform (opportunity_id = 55, GCP Consumption Subscription)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (55, 36, 3, 380000.00, 150000.00, '2024-12-01', '2027-05-15', '2024-11-23', 2024, 4);

-- ACCOUNT EXECUTIVE: Julia Rodriguez (ID: 6) - Q1
-- Apex Innovations - Technology Platform Migration (opportunity_id = 57, GCP Core)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (57, 41, 1, 425000.00, 165000.00, '2024-03-01', '2026-11-12', '2024-02-18', 2024, 1);

-- ACCOUNT EXECUTIVE: Julia Rodriguez (ID: 6) - Q1
-- Frontier Analytics - Advanced Analytics Platform (opportunity_id = 60, Data Analytics)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (60, 46, 7, 380000.00, 140000.00, '2024-03-01', '2026-06-25', '2024-02-22', 2024, 1);

-- ACCOUNT EXECUTIVE: Julia Rodriguez (ID: 6) - Q2
-- Highland Ventures - Investment Cloud Transformation (opportunity_id = 61, Enterprise Agreement)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (61, 48, 6, 920000.00, 360000.00, '2024-06-01', '2027-07-10', '2024-05-24', 2024, 2);

-- ACCOUNT EXECUTIVE: Julia Rodriguez (ID: 6) - Q2
-- Monarch Systems - Cloud Infrastructure Implementation (opportunity_id = 63, GCP Core)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (63, 53, 1, 395000.00, 148000.00, '2024-06-01', '2026-12-10', '2024-05-25', 2024, 2);

-- ACCOUNT EXECUTIVE: Julia Rodriguez (ID: 6) - Q3
-- Nexus Financial - Financial Security Services (opportunity_id = 64, Mandiant Security)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (64, 54, 14, 260000.00, 105000.00, '2024-09-01', '2027-07-20', '2024-08-17', 2024, 3);

-- ACCOUNT EXECUTIVE: Julia Rodriguez (ID: 6) - Q3
-- Unity Medical - Healthcare Analytics Platform (opportunity_id = 68, BQ Enterprise Edition)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (68, 61, 9, 435000.00, 175000.00, '2024-09-01', '2027-01-30', '2024-08-16', 2024, 3);

-- ACCOUNT EXECUTIVE: Julia Rodriguez (ID: 6) - Q4
-- Xavier Innovations - Technology Platform Development (opportunity_id = 71, GCP Core)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (71, 64, 1, 360000.00, 130000.00, '2024-12-01', '2027-09-18', '2024-11-23', 2024, 4);

-- ACCOUNT EXECUTIVE: Rachel Wilson (ID: 7) - Q1
-- Alpha Strategies - Strategic Business Transformation (opportunity_id = 72, Enterprise Agreement)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (72, 66, 6, 780000.00, 320000.00, '2024-03-01', '2027-05-25', '2024-02-17', 2024, 1);

-- ACCOUNT EXECUTIVE: Rachel Wilson (ID: 7) - Q1
-- Cobalt Enterprises - Manufacturing Infrastructure Optimization (opportunity_id = 74, Flex Committed Use Discounts)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (74, 68, 4, 410000.00, 170000.00, '2024-03-01', '2026-07-20', '2024-02-19', 2024, 1);

-- ACCOUNT EXECUTIVE: Rachel Wilson (ID: 7) - Q2
-- Gamma Investments - Investment Analytics Platform (opportunity_id = 76, Data Analytics)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (76, 72, 7, 350000.00, 145000.00, '2024-06-01', '2027-05-28', '2024-05-24', 2024, 2);

-- ACCOUNT EXECUTIVE: Rachel Wilson (ID: 7) - Q2
-- Lumina Ventures - Venture Analytics Platform (opportunity_id = 79, BQ Enterprise Edition)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (79, 77, 8, 290000.00, 115000.00, '2024-06-01', '2027-03-01', '2024-05-25', 2024, 2);

-- ACCOUNT EXECUTIVE: Rachel Wilson (ID: 7) - Q3
-- Orbit Industries - Manufacturing Cloud Platform (opportunity_id = 81, GCP Core)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (81, 80, 1, 385000.00, 155000.00, '2024-09-01', '2027-03-15', '2024-08-23', 2024, 3);

-- ACCOUNT EXECUTIVE: Rachel Wilson (ID: 7) - Q4
-- Pulse Analytics - Advanced Analytics Data Warehouse (opportunity_id = 82, BQ Enterprise Edition)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (82, 81, 9, 360000.00, 135000.00, '2024-12-01', '2027-10-05', '2024-11-18', 2024, 4);

-- ACCOUNT EXECUTIVE: David Kim (ID: 8) - Q1
-- Aegis Consulting - Business Solutions Platform (opportunity_id = 87, GCP Core)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (87, 91, 1, 420000.00, 160000.00, '2024-03-01', '2026-09-01', '2024-02-22', 2024, 1);

-- ACCOUNT EXECUTIVE: David Kim (ID: 8) - Q2
-- Dynasty Industries - Industrial Cloud Transformation (opportunity_id = 90, Enterprise Agreement)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (90, 94, 6, 890000.00, 400000.00, '2024-06-01', '2027-09-10', '2024-05-25', 2024, 2);

-- ACCOUNT EXECUTIVE: David Kim (ID: 8) - Q3
-- Fidelity Group - Financial Data Warehouse (opportunity_id = 91, BQ Enterprise Edition)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (91, 96, 9, 495000.00, 195000.00, '2024-09-01', '2027-05-15', '2024-08-20', 2024, 3);

-- ACCOUNT EXECUTIVE: David Kim (ID: 8) - Q4
-- InnovaTech - Tech Innovation Platform (opportunity_id = 94, GCP Core)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (94, 99, 1, 380000.00, 142000.00, '2024-12-01', '2027-09-08', '2024-11-24', 2024, 4);

-- ACCOUNT EXECUTIVE: David Kim (ID: 8) - Q4
-- Junction Capital - Investment Analytics Dashboard (opportunity_id = 95, Data Analytics)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (95, 100, 7, 310000.00, 122000.00, '2024-12-01', '2027-09-22', '2024-11-21', 2024, 4);

-- ACCOUNT EXECUTIVE: Lisa Jackson (ID: 9) - Q1
-- Unity Systems - IT Analytics Platform (opportunity_id = 100, BQ Enterprise Edition)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (100, 111, 8, 320000.00, 125000.00, '2024-03-01', '2026-08-01', '2024-02-17', 2024, 1);

-- ACCOUNT EXECUTIVE: Lisa Jackson (ID: 9) - Q2
-- Axiom Ventures - Venture Analytics Platform (opportunity_id = 102, Data Analytics)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (102, 116, 7, 365000.00, 140000.00, '2024-06-01', '2026-12-18', '2024-05-18', 2024, 2);

-- ACCOUNT EXECUTIVE: Lisa Jackson (ID: 9) - Q2
-- Beacon Capital - Financial Cloud Transformation (opportunity_id = 103, Enterprise Agreement)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (103, 117, 6, 950000.00, 380000.00, '2024-06-01', '2027-06-15', '2024-05-24', 2024, 2);

-- ACCOUNT EXECUTIVE: Lisa Jackson (ID: 9) - Q3
-- Helios Enterprises - Enterprise Cloud Platform (opportunity_id = 108, GCP Core)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (108, 123, 1, 480000.00, 180000.00, '2024-09-01', '2027-06-25', '2024-08-23', 2024, 3);

-- ACCOUNT EXECUTIVE: Lisa Jackson (ID: 9) - Q3
-- Jubilee Holdings - Portfolio Management Platform (opportunity_id = 109, GCP Consumption Subscription)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (109, 125, 3, 395000.00, 155000.00, '2024-09-01', '2027-05-05', '2024-08-22', 2024, 3);

-- ACCOUNT EXECUTIVE: Lisa Jackson (ID: 9) - Q4
-- Paragon Systems - Advanced Security Services (opportunity_id = 113, Mandiant Security)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (113, 131, 14, 280000.00, 112000.00, '2024-12-01', '2028-01-05', '2024-11-17', 2024, 4);

-- ACCOUNT EXECUTIVE: Lisa Jackson (ID: 9) - Q4
-- Stellar Industries - Manufacturing Operations Platform (opportunity_id = 115, GCP Core)
INSERT INTO Signing (opportunity_id, client_id, product_id, total_contract_value, incremental_acv, start_date, end_date, signing_date, fiscal_year, fiscal_quarter)
VALUES (115, 134, 1, 410000.00, 160000.00, '2024-12-01', '2027-10-15', '2024-11-25', 2024, 4);