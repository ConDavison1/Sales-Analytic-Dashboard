-- Clear existing client data and reset identity sequences
TRUNCATE TABLE client RESTART IDENTITY CASCADE;

---------------------------------------------------
-- Insert 6 client accounts for John Smith (user_id = 3)
---------------------------------------------------
INSERT INTO client (client_name, account_executive_id, city, province, industry, created_date) VALUES
  ('Aurora Consulting', 3, 'Toronto', 'ON', 'Consulting', '2023-01-01'),
  ('Maple Leaf Industries', 3, 'Montreal', 'QC', 'Manufacturing', '2023-01-01'),
  ('Pacific Ventures', 3, 'Vancouver', 'BC', 'Investments', '2023-01-01'),
  ('Prairie Tech', 3, 'Winnipeg', 'MB', 'Technology', '2023-01-01'),
  ('Capital Partners', 3, 'Ottawa', 'ON', 'Finance', '2023-01-01'),
  ('Northern Lights Ltd', 3, 'Calgary', 'AB', 'Energy', '2023-01-01');

---------------------------------------------------
-- Insert 9 client accounts for Michelle Chen (user_id = 4)
---------------------------------------------------
INSERT INTO client (client_name, account_executive_id, city, province, industry, created_date) VALUES
  ('Sapphire Solutions', 4, 'Edmonton', 'AB', 'IT Services', '2023-01-01'),
  ('Crimson Innovations', 4, 'Halifax', 'NS', 'Research', '2023-01-01'),
  ('Golden Gate Industries', 4, 'Quebec City', 'QC', 'Manufacturing', '2023-01-01'),
  ('Silverline Logistics', 4, 'Vancouver', 'BC', 'Logistics', '2023-01-01'),
  ('Emerald Dynamics', 4, 'Calgary', 'AB', 'Energy', '2023-01-01'),
  ('Cobalt Systems', 4, 'Winnipeg', 'MB', 'Technology', '2023-01-01'),
  ('Starlight Marketing', 4, 'Ottawa', 'ON', 'Marketing', '2023-01-01'),
  ('Blue Horizon Media', 4, 'Montreal', 'QC', 'Media', '2023-01-01'),
  ('Redwood Financial', 4, 'Toronto', 'ON', 'Finance', '2023-01-01');

---------------------------------------------------
-- Insert 25 client accounts for Amar Singh (user_id = 5)
---------------------------------------------------
INSERT INTO client (client_name, account_executive_id, city, province, industry, created_date) VALUES
  ('Arctic Innovations', 5, 'Calgary', 'AB', 'Technology', '2023-01-01'),
  ('Boreal Technologies', 5, 'Edmonton', 'AB', 'Software', '2023-01-01'),
  ('Cedarwood Analytics', 5, 'Regina', 'SK', 'Analytics', '2023-01-01'),
  ('Dune Capital', 5, 'Saskatoon', 'SK', 'Finance', '2023-01-01'),
  ('Everest Solutions', 5, 'Winnipeg', 'MB', 'Consulting', '2023-01-01'),
  ('Falcon Dynamics', 5, 'Toronto', 'ON', 'Engineering', '2023-01-01'),
  ('Glacier Ventures', 5, 'Ottawa', 'ON', 'Investments', '2023-01-01'),
  ('Harbor Investments', 5, 'Montreal', 'QC', 'Finance', '2023-01-01'),
  ('Ironwood Enterprises', 5, 'Quebec City', 'QC', 'Manufacturing', '2023-01-01'),
  ('Jasper Logistics', 5, 'Vancouver', 'BC', 'Logistics', '2023-01-01'),
  ('Keystone Energy', 5, 'Victoria', 'BC', 'Energy', '2023-01-01'),
  ('Lakeshore Industries', 5, 'Halifax', 'NS', 'Manufacturing', '2023-01-01'),
  ('Maplewood Systems', 5, 'St. John''s', 'NL', 'IT Services', '2023-01-01'),
  ('Northstar Holdings', 5, 'Fredericton', 'NB', 'Finance', '2023-01-01'),
  ('Oakridge Consulting', 5, 'Charlottetown', 'PE', 'Consulting', '2023-01-01'),
  ('Pinnacle Resources', 5, 'Whitehorse', 'YT', 'Natural Resources', '2023-01-01'),
  ('Quartz Financial', 5, 'Yellowknife', 'NT', 'Finance', '2023-01-01'),
  ('Redwood Manufacturing', 5, 'Iqaluit', 'NU', 'Manufacturing', '2023-01-01'),
  ('Summit Data Group', 5, 'Kelowna', 'BC', 'Data Services', '2023-01-01'),
  ('Timberline Securities', 5, 'Abbotsford', 'BC', 'Securities', '2023-01-01'),
  ('Ultraviolet Media', 5, 'London', 'ON', 'Media', '2023-01-01'),
  ('Valiant Medical', 5, 'Hamilton', 'ON', 'Healthcare', '2023-01-01'),
  ('Windward Solutions', 5, 'Kitchener', 'ON', 'Consulting', '2023-01-01'),
  ('Xenon Biotech', 5, 'Windsor', 'ON', 'Biotechnology', '2023-01-01'),
  ('Yukon Analytics', 5, 'Oshawa', 'ON', 'Analytics', '2023-01-01');

---------------------------------------------------
-- Insert 25 client accounts for Julia Rodriguez (user_id = 6)
---------------------------------------------------
INSERT INTO client (client_name, account_executive_id, city, province, industry, created_date) VALUES
  ('Apex Innovations', 6, 'Calgary', 'AB', 'Technology', '2023-01-01'),
  ('Brighton Capital', 6, 'Edmonton', 'AB', 'Finance', '2023-01-01'),
  ('Cascade Solutions', 6, 'Regina', 'SK', 'Consulting', '2023-01-01'),
  ('Delta Dynamics', 6, 'Saskatoon', 'SK', 'Engineering', '2023-01-01'),
  ('Edgewater Technologies', 6, 'Winnipeg', 'MB', 'IT Services', '2023-01-01'),
  ('Frontier Analytics', 6, 'Toronto', 'ON', 'Analytics', '2023-01-01'),
  ('Glenwood Industries', 6, 'Ottawa', 'ON', 'Manufacturing', '2023-01-01'),
  ('Highland Ventures', 6, 'Montreal', 'QC', 'Investments', '2023-01-01'),
  ('Imperial Consulting', 6, 'Quebec City', 'QC', 'Consulting', '2023-01-01'),
  ('Jubilee Enterprises', 6, 'Vancouver', 'BC', 'Business Services', '2023-01-01'),
  ('Kingston Logistics', 6, 'Victoria', 'BC', 'Logistics', '2023-01-01'),
  ('Lunar Biotech', 6, 'Halifax', 'NS', 'Biotechnology', '2023-01-01'),
  ('Monarch Systems', 6, 'St. John''s', 'NL', 'IT Solutions', '2023-01-01'),
  ('Nexus Financial', 6, 'Fredericton', 'NB', 'Finance', '2023-01-01'),
  ('Optimum Energy', 6, 'Charlottetown', 'PE', 'Energy', '2023-01-01'),
  ('Paramount Services', 6, 'Whitehorse', 'YT', 'Consulting', '2023-01-01'),
  ('Quantum Industries', 6, 'Yellowknife', 'NT', 'Manufacturing', '2023-01-01'),
  ('Riverside Consulting', 6, 'Iqaluit', 'NU', 'Consulting', '2023-01-01'),
  ('Summit Strategies', 6, 'Kelowna', 'BC', 'Strategy', '2023-01-01'),
  ('Trinity Manufacturing', 6, 'Abbotsford', 'BC', 'Manufacturing', '2023-01-01'),
  ('Unity Medical', 6, 'London', 'ON', 'Healthcare', '2023-01-01'),
  ('Vertex Ventures', 6, 'Hamilton', 'ON', 'Investments', '2023-01-01'),
  ('Westport Holdings', 6, 'Kitchener', 'ON', 'Holdings', '2023-01-01'),
  ('Xavier Innovations', 6, 'Windsor', 'ON', 'Technology', '2023-01-01'),
  ('Zenith Resources', 6, 'Oshawa', 'ON', 'Natural Resources', '2023-01-01');

---------------------------------------------------
-- Insert 25 client accounts for Rachel Wilson (user_id = 7)
---------------------------------------------------
INSERT INTO client (client_name, account_executive_id, city, province, industry, created_date) VALUES
  ('Alpha Strategies', 7, 'Calgary', 'AB', 'Strategy', '2023-01-01'),
  ('Bravo Consulting', 7, 'Edmonton', 'AB', 'Consulting', '2023-01-01'),
  ('Cobalt Enterprises', 7, 'Regina', 'SK', 'Manufacturing', '2023-01-01'),
  ('Delta Advisors', 7, 'Saskatoon', 'SK', 'Advisory', '2023-01-01'),
  ('Echo Solutions', 7, 'Winnipeg', 'MB', 'Solutions', '2023-01-01'),
  ('Foxtrot Technologies', 7, 'Toronto', 'ON', 'Technology', '2023-01-01'),
  ('Gamma Investments', 7, 'Ottawa', 'ON', 'Investments', '2023-01-01'),
  ('Helix Systems', 7, 'Montreal', 'QC', 'Systems', '2023-01-01'),
  ('Ionix Industries', 7, 'Quebec City', 'QC', 'Industries', '2023-01-01'),
  ('Jolt Energy', 7, 'Vancouver', 'BC', 'Energy', '2023-01-01'),
  ('Kinetic Partners', 7, 'Victoria', 'BC', 'Consulting', '2023-01-01'),
  ('Lumina Ventures', 7, 'Halifax', 'NS', 'Ventures', '2023-01-01'),
  ('Momentum Group', 7, 'St. John''s', 'NL', 'Group', '2023-01-01'),
  ('Nova Consulting', 7, 'Fredericton', 'NB', 'Consulting', '2023-01-01'),
  ('Orbit Industries', 7, 'Charlottetown', 'PE', 'Manufacturing', '2023-01-01'),
  ('Pulse Analytics', 7, 'Whitehorse', 'YT', 'Analytics', '2023-01-01'),
  ('Quantum Leap', 7, 'Yellowknife', 'NT', 'Technology', '2023-01-01'),
  ('Radiant Innovations', 7, 'Iqaluit', 'NU', 'Innovations', '2023-01-01'),
  ('Synergy Solutions', 7, 'Kelowna', 'BC', 'Solutions', '2023-01-01'),
  ('Titan Technologies', 7, 'Abbotsford', 'BC', 'Technology', '2023-01-01'),
  ('Uprise Holdings', 7, 'London', 'ON', 'Finance', '2023-01-01'),
  ('Vortex Media', 7, 'Hamilton', 'ON', 'Media', '2023-01-01'),
  ('Wavelength Systems', 7, 'Kitchener', 'ON', 'Systems', '2023-01-01'),
  ('Xplore Ventures', 7, 'Windsor', 'ON', 'Ventures', '2023-01-01'),
  ('Zenith Analytics', 7, 'Oshawa', 'ON', 'Analytics', '2023-01-01');

---------------------------------------------------
-- Insert 25 client accounts for David Kim (user_id = 8)
---------------------------------------------------
INSERT INTO client (client_name, account_executive_id, city, province, industry, created_date) VALUES
  ('Aegis Consulting', 8, 'Calgary', 'AB', 'Consulting', '2023-01-01'),
  ('Borealis Ventures', 8, 'Edmonton', 'AB', 'Ventures', '2023-01-01'),
  ('Celestial Systems', 8, 'Regina', 'SK', 'Systems', '2023-01-01'),
  ('Dynasty Industries', 8, 'Saskatoon', 'SK', 'Industries', '2023-01-01'),
  ('Echelon Partners', 8, 'Winnipeg', 'MB', 'Partnerships', '2023-01-01'),
  ('Fidelity Group', 8, 'Toronto', 'ON', 'Finance', '2023-01-01'),
  ('Genesis Innovations', 8, 'Ottawa', 'ON', 'Innovations', '2023-01-01'),
  ('Harbinger Solutions', 8, 'Montreal', 'QC', 'Solutions', '2023-01-01'),
  ('InnovaTech', 8, 'Quebec City', 'QC', 'Technology', '2023-01-01'),
  ('Junction Capital', 8, 'Vancouver', 'BC', 'Finance', '2023-01-01'),
  ('Keystone Advisors', 8, 'Victoria', 'BC', 'Advisory', '2023-01-01'),
  ('Legacy Logistics', 8, 'Halifax', 'NS', 'Logistics', '2023-01-01'),
  ('Monument Enterprises', 8, 'St. John''s', 'NL', 'Manufacturing', '2023-01-01'),
  ('Noble Strategies', 8, 'Fredericton', 'NB', 'Consulting', '2023-01-01'),
  ('Oracle Consulting', 8, 'Charlottetown', 'PE', 'Consulting', '2023-01-01'),
  ('Pioneer Partners', 8, 'Whitehorse', 'YT', 'Partnerships', '2023-01-01'),
  ('Quantum Designs', 8, 'Yellowknife', 'NT', 'Design', '2023-01-01'),
  ('Renaissance Analytics', 8, 'Iqaluit', 'NU', 'Analytics', '2023-01-01'),
  ('Summit Advisors', 8, 'Kelowna', 'BC', 'Advisory', '2023-01-01'),
  ('Trilogy Technologies', 8, 'Abbotsford', 'BC', 'Technology', '2023-01-01'),
  ('Unity Systems', 8, 'London', 'ON', 'IT Services', '2023-01-01'),
  ('Vertex Solutions', 8, 'Hamilton', 'ON', 'Solutions', '2023-01-01'),
  ('Windsor Analytics', 8, 'Kitchener', 'ON', 'Analytics', '2023-01-01'),
  ('Xcel Industries', 8, 'Windsor', 'ON', 'Manufacturing', '2023-01-01'),
  ('Yield Partners', 8, 'Oshawa', 'ON', 'Consulting', '2023-01-01');

---------------------------------------------------
-- Insert 25 client accounts for Lisa Jackson (user_id = 9)
---------------------------------------------------
INSERT INTO client (client_name, account_executive_id, city, province, industry, created_date) VALUES
  ('Axiom Ventures', 9, 'Calgary', 'AB', 'Ventures', '2023-01-01'),
  ('Beacon Capital', 9, 'Edmonton', 'AB', 'Finance', '2023-01-01'),
  ('Catalyst Systems', 9, 'Regina', 'SK', 'Technology', '2023-01-01'),
  ('Delta Force Industries', 9, 'Saskatoon', 'SK', 'Manufacturing', '2023-01-01'),
  ('Eminence Solutions', 9, 'Winnipeg', 'MB', 'Consulting', '2023-01-01'),
  ('Fortress Financial', 9, 'Toronto', 'ON', 'Finance', '2023-01-01'),
  ('Galaxy Innovations', 9, 'Ottawa', 'ON', 'Innovations', '2023-01-01'),
  ('Helios Enterprises', 9, 'Montreal', 'QC', 'Enterprises', '2023-01-01'),
  ('Infinity Consulting', 9, 'Quebec City', 'QC', 'Consulting', '2023-01-01'),
  ('Jubilee Holdings', 9, 'Vancouver', 'BC', 'Holdings', '2023-01-01'),
  ('Kinetic Dynamics', 9, 'Victoria', 'BC', 'Technology', '2023-01-01'),
  ('Luminary Tech', 9, 'Halifax', 'NS', 'Technology', '2023-01-01'),
  ('Momentum Advisors', 9, 'St. John''s', 'NL', 'Advisory', '2023-01-01'),
  ('Nexus Global', 9, 'Fredericton', 'NB', 'Global Business', '2023-01-01'),
  ('Optimum Strategies', 9, 'Charlottetown', 'PE', 'Strategy', '2023-01-01'),
  ('Paragon Systems', 9, 'Whitehorse', 'YT', 'Systems', '2023-01-01'),
  ('Quantum Edge', 9, 'Yellowknife', 'NT', 'Technology', '2023-01-01'),
  ('Resonance Partners', 9, 'Iqaluit', 'NU', 'Consulting', '2023-01-01'),
  ('Stellar Industries', 9, 'Kelowna', 'BC', 'Manufacturing', '2023-01-01'),
  ('Titan Advisors', 9, 'Abbotsford', 'BC', 'Advisory', '2023-01-01'),
  ('Umbra Solutions', 9, 'London', 'ON', 'IT Services', '2023-01-01'),
  ('Vanguard Analytics', 9, 'Hamilton', 'ON', 'Analytics', '2023-01-01'),
  ('Windward Enterprises', 9, 'Kitchener', 'ON', 'Manufacturing', '2023-01-01'),
  ('Xenith Group', 9, 'Windsor', 'ON', 'Group', '2023-01-01'),
  ('Zenith Global', 9, 'Oshawa', 'ON', 'Global Business', '2023-01-01');

---------------------------------------------------
-- Verify the inserted clients
---------------------------------------------------
SELECT * FROM client ORDER BY client_id;