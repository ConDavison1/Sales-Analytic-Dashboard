-- Insert opportunities for clients managed by David Kim (user_id = 8)
-- Random selection of 15 clients out of the 25 he manages

-- Client: Aegis Consulting (client_id = 91) - Consulting in Calgary, AB
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: GCP Core (product_id = 1) - Can qualify for revenue-based wins
('Aegis Consulting - Business Solutions Platform', 91, 1, 'closed-won', 'migrate', '2026-12-31', 100.00, 420000.00, '2024-01-10 13:30:00', '2024-02-22 10:15:00');

-- Client: Borealis Ventures (client_id = 92) - Ventures in Edmonton, AB
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: Data Analytics (product_id = 7) - Can qualify for revenue-based wins (DA)
('Borealis Ventures - Startup Analytics Platform', 92, 7, 'commit', 'proposal/negotiation', '2026-12-31', 95.00, 280000.00, '2024-01-15 09:45:00', '2024-02-18 14:30:00');

-- Client: Celestial Systems (client_id = 93) - Systems in Regina, SK
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: Cloud Security (product_id = 11) - Contract-based (security)
('Celestial Systems - Integrated Security Framework', 93, 11, 'pipeline', 'tech-eval/soln-dev', '2026-12-31', 40.00, 175000.00, '2024-01-05 11:20:00', '2024-02-10 15:25:00');

-- Client: Dynasty Industries (client_id = 94) - Industries in Saskatoon, SK
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: Enterprise Agreement (product_id = 6) - Can qualify for signing-based wins
('Dynasty Industries - Industrial Cloud Transformation', 94, 6, 'closed-won', 'migrate', '2026-12-31', 100.00, 890000.00, '2024-01-18 14:50:00', '2024-02-25 11:40:00');

-- Client: Fidelity Group (client_id = 96) - Finance in Toronto, ON
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: BQ Enterprise Plus (product_id = 9) - Can qualify for signing-based wins
('Fidelity Group - Financial Data Warehouse', 96, 9, 'closed-won', 'migrate', '2026-12-31', 100.00, 495000.00, '2024-01-08 10:15:00', '2024-02-20 13:35:00');

-- Client: Genesis Innovations (client_id = 97) - Innovations in Ottawa, ON
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: Vertex AI Platform (product_id = 22) - Can qualify for revenue-based wins (DA)
('Genesis Innovations - AI Innovation Platform', 97, 22, 'upside', 'proposal/negotiation', '2026-12-31', 70.00, 340000.00, '2024-01-22 15:40:00', '2024-02-15 09:20:00');

-- Client: Harbinger Solutions (client_id = 98) - Solutions in Montreal, QC
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: Flex Committed Use Discounts (product_id = 4) - Can qualify for signing-based wins
('Harbinger Solutions - Cloud Infrastructure Optimization', 98, 4, 'commit', 'proposal/negotiation', '2026-12-31', 90.00, 360000.00, '2024-01-12 13:10:00', '2024-02-16 11:45:00');

-- Client: InnovaTech (client_id = 99) - Technology in Quebec City, QC
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: GCP Core (product_id = 1) - Can qualify for revenue-based wins
('InnovaTech - Tech Innovation Platform', 99, 1, 'closed-won', 'migrate', '2026-12-31', 100.00, 380000.00, '2024-01-25 09:30:00', '2024-02-24 16:20:00');

-- Client: Junction Capital (client_id = 100) - Finance in Vancouver, BC
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: Data Analytics (product_id = 7) - Can qualify for revenue-based wins (DA)
('Junction Capital - Investment Analytics Dashboard', 100, 7, 'closed-won', 'migrate', '2026-12-31', 100.00, 310000.00, '2024-01-16 11:25:00', '2024-02-21 14:50:00');

-- Client: Legacy Logistics (client_id = 102) - Logistics in Halifax, NS
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: Maps Platform (product_id = 18) - Less relevant for win qualification
('Legacy Logistics - Route Optimization System', 102, 18, 'upside', 'proposal/negotiation', '2026-12-31', 65.00, 155000.00, '2024-01-20 13:40:00', '2024-02-12 10:15:00');

-- Client: Monument Enterprises (client_id = 103) - Manufacturing in St. John's, NL
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: GCP Consumption Subscription (product_id = 3) - Can qualify for signing-based wins
('Monument Enterprises - Manufacturing Operations Platform', 103, 3, 'commit', 'proposal/negotiation', '2026-12-31', 90.00, 425000.00, '2024-01-09 14:15:00', '2024-02-19 11:30:00');

-- Client: Pioneer Partners (client_id = 106) - Partnerships in Whitehorse, YT
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: API Management (product_id = 16) - Contract-based
('Pioneer Partners - Partnership API Integration', 106, 16, 'omit', 'qualify', '2026-12-31', 15.00, 130000.00, '2024-01-04 10:20:00', '2024-01-19 15:45:00');

-- Client: Trilogy Technologies (client_id = 110) - Technology in Abbotsford, BC
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: GCP Core (product_id = 1) - Can qualify for revenue-based wins
('Trilogy Technologies - Technology Development Platform', 110, 1, 'upside', 'proposal/negotiation', '2026-12-31', 75.00, 295000.00, '2024-01-14 16:30:00', '2024-02-11 09:45:00');

-- Client: Unity Systems (client_id = 111) - IT Services in London, ON
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: BQ Enterprise Edition (product_id = 8) - Can qualify for signing-based wins
('Unity Systems - IT Analytics Platform', 111, 8, 'closed-won', 'migrate', '2026-12-31', 100.00, 320000.00, '2024-01-07 12:40:00', '2024-02-17 15:10:00');

-- Client: Windsor Analytics (client_id = 113) - Analytics in Kitchener, ON
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: Looker (product_id = 15) - Contract-based
('Windsor Analytics - Analytics Visualization Platform', 113, 15, 'pipeline', 'refine', '2026-12-31', 30.00, 160000.00, '2024-01-11 09:50:00', '2024-02-08 13:25:00');