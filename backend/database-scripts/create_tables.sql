-- Google Cloud Sales Analytics Database Schema for PostgreSQL
-- This script creates all tables with their constraints

-- Start fresh by dropping tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS OpportunityUpdateLog CASCADE;
DROP TABLE IF EXISTS UpdateEvent CASCADE;
DROP TABLE IF EXISTS QuarterlyTarget CASCADE;
DROP TABLE IF EXISTS YearlyTarget CASCADE;
DROP TABLE IF EXISTS Win CASCADE;
DROP TABLE IF EXISTS Revenue CASCADE;
DROP TABLE IF EXISTS Signing CASCADE;
DROP TABLE IF EXISTS Opportunity CASCADE;
DROP TABLE IF EXISTS Product CASCADE;
DROP TABLE IF EXISTS Client CASCADE;
DROP TABLE IF EXISTS DirectorAccountExecutive CASCADE;
DROP TABLE IF EXISTS "User" CASCADE; -- User is a reserved word in PostgreSQL, so using quotes
DROP TABLE IF EXISTS "user" CASCADE; -- user is a reserved word in PostgreSQL, so using quotes

-- 1. User Table (lowercase "user")
CREATE TABLE "user" (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    role VARCHAR(20) NOT NULL CHECK (role IN ('director', 'account-executive', 'admin')),
    hashed_password VARCHAR(500) NOT NULL
);

-- 2. DirectorAccountExecutive Table
-- Maps account executives to their directors
CREATE TABLE DirectorAccountExecutive (
    account_executive_id INTEGER PRIMARY KEY,
    director_id INTEGER NOT NULL,
    FOREIGN KEY (account_executive_id) REFERENCES "user"(user_id),
    FOREIGN KEY (director_id) REFERENCES "user"(user_id)
    -- Role checks enforced through triggers
);

-- 3. Client Table
-- Stores client information and associates clients with account executives
CREATE TABLE Client (
    client_id SERIAL PRIMARY KEY,
    client_name VARCHAR(100) NOT NULL,
    account_executive_id INTEGER NOT NULL,
    city VARCHAR(50),
    province VARCHAR(2) CHECK (province IN ('AB', 'BC', 'MB', 'NB', 'NL', 'NT', 'NS', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT')),
    industry VARCHAR(50),
    created_date DATE NOT NULL,
    FOREIGN KEY (account_executive_id) REFERENCES "user"(user_id)
    -- Role check enforced through trigger
);

-- 4. Product Table
-- Stores all Google Cloud products with their categories
CREATE TABLE Product (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) UNIQUE NOT NULL,
    product_category VARCHAR(50) NOT NULL CHECK (
        product_category IN ('gcp-core', 'data-analytics', 'cloud-security', 'mandiant', 
                           'looker', 'apigee', 'maps', 'marketplace', 'vertex-ai-platform')
    ),
    CONSTRAINT product_name_category_check CHECK (
        (product_category = 'gcp-core' AND product_name IN (
            'gcp-consumption-commit', 'gcp-consumption-non-commit', 'gcp-consumption-subscription', 
            'flex-committed-use-discounts', 'gcp-commit-contracts', 'enterprise-agreement', 'gcp-core-products'
        )) OR
        (product_category = 'data-analytics' AND product_name IN (
            'bq-enterprise-edition-1yr', 'bq-enterprise-edition-3yr', 'bq-enterprise-plus-edition-1yr', 
            'bq-enterprise-plus-edition-3yr', 'bq-mission-critical-edition-1yr', 'bq-slots-for-annual-subscription'
        )) OR
        (product_category = 'cloud-security' AND product_name IN ('chronicle', 'virustotal')) OR
        (product_category = 'mandiant' AND product_name IN ('mandiant-consulting', 'mandiant-saas')) OR
        (product_category = 'looker' AND product_name = 'looker') OR
        (product_category = 'apigee' AND product_name = 'apigee') OR
        (product_category = 'maps' AND product_name = 'maps') OR
        (product_category = 'marketplace' AND product_name = 'marketplace-products') OR
        (product_category = 'vertex-ai-platform' AND product_name = 'vertex-ai-platform-products')
    )
);

-- 5. Opportunity Table
-- Tracks sales opportunities with forecast categories, sales stages, and probabilities
CREATE TABLE Opportunity (
    opportunity_id SERIAL PRIMARY KEY,
    opportunity_name VARCHAR(100) NOT NULL,
    client_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    forecast_category VARCHAR(20) NOT NULL CHECK (
        forecast_category IN ('omit', 'pipeline', 'upside', 'commit', 'closed-won')
    ),
    sales_stage VARCHAR(50) NOT NULL CHECK (
        sales_stage IN ('qualify', 'refine', 'tech-eval/soln-dev', 'proposal/negotiation', 'migrate')
    ),
    close_date DATE NOT NULL,
    probability DECIMAL(5,2) NOT NULL,
    amount DECIMAL(15,2) NOT NULL CHECK (amount > 0),
    created_date TIMESTAMP NOT NULL,
    last_modified_date TIMESTAMP NOT NULL,
    FOREIGN KEY (client_id) REFERENCES Client(client_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id),
    CONSTRAINT forecast_sales_stage_check CHECK (
        (forecast_category = 'omit' AND sales_stage = 'qualify') OR
        (forecast_category = 'pipeline' AND sales_stage IN ('refine', 'tech-eval/soln-dev')) OR
        (forecast_category = 'upside' AND sales_stage = 'proposal/negotiation') OR
        (forecast_category = 'commit' AND sales_stage = 'proposal/negotiation') OR
        (forecast_category = 'closed-won' AND sales_stage = 'migrate')
    ),
    CONSTRAINT probability_forecast_check CHECK (
        (forecast_category = 'omit' AND probability BETWEEN 0 AND 100) OR
        (forecast_category = 'pipeline' AND probability BETWEEN 10 AND 50) OR
        (forecast_category = 'upside' AND probability BETWEEN 60 AND 80) OR
        (forecast_category = 'commit' AND probability BETWEEN 90 AND 100) OR
        (forecast_category = 'closed-won' AND probability = 100)
    ),
    CONSTRAINT close_date_check CHECK (close_date >= CAST(created_date AS DATE)),
    CONSTRAINT modified_date_check CHECK (last_modified_date >= created_date)
);

-- 6. Signing Table
-- Records contract signings with financial details and terms
CREATE TABLE Signing (
    signing_id SERIAL PRIMARY KEY,
    opportunity_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    total_contract_value DECIMAL(15,2) NOT NULL CHECK (total_contract_value > 0),
    incremental_acv DECIMAL(15,2) CHECK (incremental_acv >= 0 OR incremental_acv IS NULL),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    signing_date DATE NOT NULL,
    fiscal_year INTEGER NOT NULL,
    fiscal_quarter INTEGER NOT NULL CHECK (fiscal_quarter IN (1, 2, 3, 4)),
    FOREIGN KEY (opportunity_id) REFERENCES Opportunity(opportunity_id),
    FOREIGN KEY (client_id) REFERENCES Client(client_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id),
    CONSTRAINT end_date_check CHECK (end_date > start_date),
);

-- 7. Revenue Table
-- Tracks revenue amounts by fiscal periods
CREATE TABLE Revenue (
    revenue_id SERIAL PRIMARY KEY,
    opportunity_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    signing_id INTEGER,
    product_id INTEGER NOT NULL,
    fiscal_year INTEGER NOT NULL,
    fiscal_quarter INTEGER NOT NULL CHECK (fiscal_quarter IN (1, 2, 3, 4)),
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    amount DECIMAL(15,2) NOT NULL CHECK (amount > 0),
    FOREIGN KEY (opportunity_id) REFERENCES Opportunity(opportunity_id),
    FOREIGN KEY (client_id) REFERENCES Client(client_id),
    FOREIGN KEY (signing_id) REFERENCES Signing(signing_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id),
    CONSTRAINT fiscal_quarter_month_check CHECK (
        (fiscal_quarter = 1 AND month IN (1, 2, 3)) OR
        (fiscal_quarter = 2 AND month IN (4, 5, 6)) OR
        (fiscal_quarter = 3 AND month IN (7, 8, 9)) OR
        (fiscal_quarter = 4 AND month IN (10, 11, 12))
    )
);

-- 8. Win Table
-- Tracks GCP and DA (Data Analytics) wins per client

CREATE TABLE Win (
    win_id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    win_category VARCHAR(10) NOT NULL CHECK (win_category IN ('gcp', 'da')),
    win_level INTEGER NOT NULL,
    win_multiplier DECIMAL(3,1) NOT NULL CHECK (win_multiplier IN (0.5, 1.0)),
    fiscal_year INTEGER NOT NULL,
    fiscal_quarter INTEGER NOT NULL CHECK (fiscal_quarter IN (1, 2, 3, 4)),
    opportunity_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    FOREIGN KEY (client_id) REFERENCES Client(client_id),
    FOREIGN KEY (opportunity_id) REFERENCES Opportunity(opportunity_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id),
    CONSTRAINT win_level_check CHECK (
        (win_category = 'gcp' AND win_level IN (1, 2, 3)) OR
        (win_category = 'da' AND win_level IN (1, 2))
    ),
    CONSTRAINT unique_win_per_category_level_year UNIQUE (client_id, win_category, win_level, fiscal_year)
);

-- 9. YearlyTarget Table
-- Stores annual targets for account executives
CREATE TABLE YearlyTarget (
    target_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    fiscal_year INTEGER NOT NULL,
    target_type VARCHAR(20) NOT NULL CHECK (target_type IN ('revenue', 'signings', 'wins', 'pipeline')),
    amount DECIMAL(15,2) NOT NULL CHECK (amount > 0),
    FOREIGN KEY (user_id) REFERENCES "user"(user_id),
    CONSTRAINT unique_target_per_user_year_type UNIQUE (user_id, fiscal_year, target_type)
);

-- 10. QuarterlyTarget Table
-- Breaks down yearly targets into quarterly percentages
CREATE TABLE QuarterlyTarget (
    quarterly_target_id SERIAL PRIMARY KEY,
    target_id INTEGER NOT NULL,
    fiscal_quarter INTEGER NOT NULL CHECK (fiscal_quarter IN (1, 2, 3, 4)),
    user_id INTEGER NOT NULL,
    percentage DECIMAL(5,2) NOT NULL CHECK (percentage BETWEEN 0 AND 100),
    FOREIGN KEY (target_id) REFERENCES YearlyTarget(target_id),
    FOREIGN KEY (user_id) REFERENCES "user"(user_id),
    CONSTRAINT unique_quarterly_target UNIQUE (target_id, fiscal_quarter)
);

-- 11. UpdateEvent Table
-- Stores metadata about opportunity update events
CREATE TABLE UpdateEvent (
    change_batch_id SERIAL PRIMARY KEY,
    opportunity_id INTEGER NOT NULL,
    change_date TIMESTAMP NOT NULL,
    FOREIGN KEY (opportunity_id) REFERENCES Opportunity(opportunity_id)
);

-- 12. OpportunityUpdateLog Table
-- Detailed log of changes to opportunity fields
CREATE TABLE OpportunityUpdateLog (
    log_id SERIAL PRIMARY KEY,
    change_batch_id INTEGER NOT NULL,
    field_name VARCHAR(50) NOT NULL CHECK (
        field_name IN ('forecast_category', 'sales_stage', 'probability', 'close_date', 'amount')
    ),
    old_value TEXT NOT NULL,
    new_value TEXT NOT NULL,
    FOREIGN KEY (change_batch_id) REFERENCES UpdateEvent(change_batch_id),
    CONSTRAINT unique_field_per_batch UNIQUE (change_batch_id, field_name)
);