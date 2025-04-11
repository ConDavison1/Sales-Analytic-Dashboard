-- Insert opportunities for clients managed by Michelle Chen (user_id = 4)

-- Client 1: Sapphire Solutions (client_id = 7) - IT Services in Edmonton, AB
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: GCP Core (product_id = 1) - Can qualify for revenue-based wins
('Sapphire Solutions - IT Infrastructure Modernization', 7, 1, 'closed-won', 'migrate', '2026-12-31', 100.00, 320000.00, '2024-01-04 10:15:00', '2024-02-20 14:30:00'),
-- Product: Cloud Security (product_id = 11) - Contract-based
('Sapphire Solutions - Client Security Solutions', 7, 11, 'pipeline', 'tech-eval/soln-dev', '2026-12-31', 45.00, 150000.00, '2024-01-12 13:45:00', '2024-02-05 16:20:00');

-- Client 2: Crimson Innovations (client_id = 8) - Research in Halifax, NS
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: BigQuery Enterprise (product_id = 8) - Can qualify for signing-based wins
('Crimson Innovations - Research Data Warehouse', 8, 8, 'commit', 'proposal/negotiation', '2026-12-31', 90.00, 280000.00, '2024-01-07 09:30:00', '2024-02-15 11:45:00'),
-- Product: Vertex AI Platform (product_id = 22) - Can qualify for revenue-based wins (DA)
('Crimson Innovations - AI Research Platform', 8, 22, 'upside', 'proposal/negotiation', '2026-12-31', 70.00, 225000.00, '2024-01-15 14:20:00', '2024-02-10 09:15:00'),
-- Product: Data Analytics (product_id = 7) - Can qualify for revenue-based wins (DA)
('Crimson Innovations - Research Analytics Implementation', 8, 7, 'closed-won', 'migrate', '2026-12-31', 100.00, 190000.00, '2024-01-21 11:30:00', '2024-02-22 15:45:00');

-- Client 3: Golden Gate Industries (client_id = 9) - Manufacturing in Quebec City, QC
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: GCP Consumption Subscription (product_id = 3) - Can qualify for signing-based wins
('Golden Gate Industries - Manufacturing Operations Platform', 9, 3, 'closed-won', 'migrate', '2026-12-31', 100.00, 450000.00, '2024-01-03 10:45:00', '2024-02-18 14:10:00'),
-- Product: Maps Platform (product_id = 18) - Less relevant for win qualification
('Golden Gate Industries - Supply Chain Mapping System', 9, 18, 'pipeline', 'refine', '2026-12-31', 30.00, 95000.00, '2024-01-11 15:30:00', '2024-02-03 10:20:00'),
-- Product: Looker (product_id = 15) - Contract-based
('Golden Gate Industries - Manufacturing Performance Analytics', 9, 15, 'omit', 'qualify', '2026-12-31', 15.00, 120000.00, '2024-01-18 09:15:00', '2024-01-30 13:40:00');

-- Client 4: Silverline Logistics (client_id = 10) - Logistics in Vancouver, BC
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: GCP Core (product_id = 1) - Can qualify for revenue-based wins
('Silverline Logistics - Logistics Operations Platform', 10, 1, 'closed-won', 'migrate', '2026-12-31', 100.00, 380000.00, '2024-01-08 13:30:00', '2024-02-23 16:45:00'),
-- Product: Maps Platform (product_id = 18) - Less relevant for win qualification
('Silverline Logistics - Route Optimization System', 10, 18, 'upside', 'proposal/negotiation', '2026-12-31', 65.00, 135000.00, '2024-01-17 10:20:00', '2024-02-08 15:30:00');

-- Client 5: Emerald Dynamics (client_id = 11) - Energy in Calgary, AB
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: Enterprise Agreement (product_id = 6) - Can qualify for signing-based wins
('Emerald Dynamics - Energy Cloud Transformation', 11, 6, 'closed-won', 'migrate', '2026-12-31', 100.00, 850000.00, '2024-01-05 09:45:00', '2024-02-21 13:15:00'),
-- Product: Data Analytics (product_id = 7) - Can qualify for revenue-based wins (DA)
('Emerald Dynamics - Energy Production Analytics', 11, 7, 'commit', 'proposal/negotiation', '2026-12-31', 95.00, 320000.00, '2024-01-14 11:30:00', '2024-02-16 10:45:00'),
-- Product: Chronicle (product_id = 12) - Contract-based (security)
('Emerald Dynamics - Energy Security Operations', 11, 12, 'pipeline', 'tech-eval/soln-dev', '2026-12-31', 40.00, 175000.00, '2024-01-23 14:20:00', '2024-02-09 09:30:00');

-- Client 6: Cobalt Systems (client_id = 12) - Technology in Winnipeg, MB
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: GCP Core (product_id = 1) - Can qualify for revenue-based wins
('Cobalt Systems - Software Development Environment', 12, 1, 'upside', 'proposal/negotiation', '2026-12-31', 75.00, 280000.00, '2024-01-09 10:15:00', '2024-02-12 14:30:00'),
-- Product: Flex Committed Use Discounts (product_id = 4) - Can qualify for signing-based wins
('Cobalt Systems - Computing Resource Optimization', 12, 4, 'closed-won', 'migrate', '2026-12-31', 100.00, 420000.00, '2024-01-19 15:45:00', '2024-02-24 11:20:00');

-- Client 7: Starlight Marketing (client_id = 13) - Marketing in Ottawa, ON
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: BigQuery Enterprise (product_id = 8) - Can qualify for signing-based wins
('Starlight Marketing - Marketing Analytics Platform', 13, 8, 'closed-won', 'migrate', '2026-12-31', 100.00, 310000.00, '2024-01-06 13:40:00', '2024-02-19 15:30:00'),
-- Product: Looker (product_id = 15) - Contract-based
('Starlight Marketing - Campaign Performance Dashboard', 13, 15, 'omit', 'qualify', '2026-12-31', 10.00, 140000.00, '2024-01-16 09:30:00', '2024-01-28 11:15:00'),
-- Product: API Management (product_id = 16) - Contract-based
('Starlight Marketing - Marketing API Integration', 13, 16, 'pipeline', 'refine', '2026-12-31', 35.00, 95000.00, '2024-01-24 11:45:00', '2024-02-14 16:20:00');

-- Client 8: Blue Horizon Media (client_id = 14) - Media in Montreal, QC
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: GCP Core (product_id = 1) - Can qualify for revenue-based wins
('Blue Horizon Media - Media Content Platform', 14, 1, 'commit', 'proposal/negotiation', '2026-12-31', 90.00, 395000.00, '2024-01-10 14:30:00', '2024-02-13 10:15:00'),
-- Product: Mandiant Security (product_id = 14) - Can qualify for signing-based wins
('Blue Horizon Media - Media Security Services', 14, 14, 'closed-won', 'migrate', '2026-12-31', 100.00, 240000.00, '2024-01-20 09:10:00', '2024-02-25 13:45:00');

-- Client 9: Redwood Financial (client_id = 15) - Finance in Toronto, ON
INSERT INTO Opportunity (opportunity_name, client_id, product_id, forecast_category, sales_stage, close_date, probability, amount, created_date, last_modified_date)
VALUES
-- Product: BQ Enterprise Plus (product_id = 9) - Can qualify for signing-based wins
('Redwood Financial - Financial Data Warehouse', 15, 9, 'closed-won', 'migrate', '2026-12-31', 100.00, 520000.00, '2024-01-04 15:20:00', '2024-02-17 10:45:00'),
-- Product: Data Analytics (product_id = 7) - Can qualify for revenue-based wins (DA)
('Redwood Financial - Investment Analytics Platform', 15, 7, 'upside', 'proposal/negotiation', '2026-12-31', 70.00, 290000.00, '2024-01-13 09:45:00', '2024-02-11 14:30:00'),
-- Product: Cloud Security (product_id = 11) - Contract-based (security)
('Redwood Financial - Financial Security Framework', 15, 11, 'commit', 'proposal/negotiation', '2026-12-31', 90.00, 185000.00, '2024-01-22 11:10:00', '2024-02-21 16:20:00');