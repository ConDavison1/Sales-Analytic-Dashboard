-- Populate Product table with all Google Cloud products
-- Based on the provided product documentation

-- Clear any existing data in the Product table and reset identity sequence

TRUNCATE TABLE product RESTART IDENTITY CASCADE;

-- Insert product data: product_name, product_category
INSERT INTO product (product_name, product_category)
VALUES
    -- 1. GCP Core (gcp-core) products
    ('gcp-consumption-commit', 'gcp-core'),
    ('gcp-consumption-non-commit', 'gcp-core'),
    ('gcp-consumption-subscription', 'gcp-core'),
    ('flex-committed-use-discounts', 'gcp-core'),
    ('gcp-commit-contracts', 'gcp-core'),
    ('enterprise-agreement', 'gcp-core'),
    ('gcp-core-products', 'gcp-core'),

    -- 2. Data Analytics (data-analytics) products
    ('bq-enterprise-edition-1yr', 'data-analytics'),
    ('bq-enterprise-edition-3yr', 'data-analytics'),
    ('bq-enterprise-plus-edition-1yr', 'data-analytics'),
    ('bq-enterprise-plus-edition-3yr', 'data-analytics'),
    ('bq-mission-critical-edition-1yr', 'data-analytics'),
    ('bq-slots-for-annual-subscription', 'data-analytics'),

    -- 3. Cloud Security (cloud-security) products
    ('chronicle', 'cloud-security'),
    ('virustotal', 'cloud-security'),

    -- 4. Mandiant (mandiant) products
    ('mandiant-consulting', 'mandiant'),
    ('mandiant-saas', 'mandiant'),

    -- 5. Looker (looker) product
    ('looker', 'looker'),

    -- 6. Apigee (apigee) product
    ('apigee', 'apigee'),

    -- 7. Maps (maps) product
    ('maps', 'maps'),

    -- 8. Marketplace (marketplace) products
    ('marketplace-products', 'marketplace'),

    -- 9. Vertex AI Platform (vertex-ai-platform) products
    ('vertex-ai-platform-products', 'vertex-ai-platform');

-- Verify the inserted products
SELECT product_id, product_name, product_category 
FROM product 
ORDER BY product_category, product_name;

-- Count products by category
SELECT product_category, COUNT(*) as product_count
FROM product
GROUP BY product_category
ORDER BY product_category;