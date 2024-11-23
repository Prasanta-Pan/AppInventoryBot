
CREATE TABLE application_inventory (
    Name TEXT,
    Description TEXT,
    Division TEXT,
    Sites TEXT,
    Owner TEXT,
    Components TEXT,
    Technology TEXT,
    Version TEXT,
    Effective_Date TEXT,
    EOL TEXT,
    Interface TEXT,
    Medium TEXT
);


    INSERT INTO application_inventory (
        Name, Description, Division, Sites, Owner, Components,
        Technology, Version, Effective_Date, EOL, Interface, Medium
    ) VALUES (
        'VMS', 'An order execution and management system', 
        'Product & Execution', 'CH,EUROPE,ASIA', 
        'Prasanta', 'Batch: Batch 1, Batch 2, Batch 3 | 
Online: Online 1, Online 2, Online 3', 
        'Java 8, spring batch, API, IBM MQ, CFT, Postgres', '2.6.3', 
        'Q2-2001', 'Q4-2028', 
        'Predator, SVE, AAA', 'Predator:IBM MQ, SVE:IBM MQ, AAA:IBM MQ'
    );
    
    INSERT INTO application_inventory (
        Name, Description, Division, Sites, Owner, Components,
        Technology, Version, Effective_Date, EOL, Interface, Medium
    ) VALUES (
        'Predator', 'Execute order in market', 
        'Product & Execution', 'CH,EUROPE', 
        'Prasanta', 'Batch: Batch 1, Batch 2, Batch 3 | 
Online: Online 1, Online 2, Online 3', 
        'Java 11, API, DB2', '1.6.3', 
        'Q1-2015', 'Q1-2028', 
        'VMS, SVE', 'VMS:IBM MQ, SVE:IBM MQ'
    );
    

    INSERT INTO application_inventory (
        Name, Description, Division, Sites, Owner, Components,
        Technology, Version, Effective_Date, EOL, Interface, Medium
    ) VALUES (
        'SVE', 'Instrument referential system', 
        'Product & Execution', 'ASIA', 
        'Rajesh', 'Batch: Batch 1, Batch 2, Batch 3 | 
Online: Online 1, Online 2, Online 3', 
        'COBOL, IBM MQ, DB2', '2.2.1', 
        'Q1-2001', 'Q1-2028', 
        'VMS, Predator, My Wealth', 'VMS:IBM MQ, Predator:IBM MQ, My Wealth:IBM MQ'
    );
    

    INSERT INTO application_inventory (
        Name, Description, Division, Sites, Owner, Components,
        Technology, Version, Effective_Date, EOL, Interface, Medium
    ) VALUES (
        'AAA', 'Client portfolio management', 
        'Product & Execution', 'ASIA, EUROPE', 
        'Prasanta', 'Batch: Batch 1, Batch 2, Batch 3 | 
Online: Online 1, Online 2, Online 3', 
        'Java, C++, ActiveMQ, CFT, API, Spring Batch', '3.2.0', 
        'Q1-2015', 'Q2-2030', 
        'VMS, My Wealth,IAM', 'VMS:IBM MQ, My Wealth:API, IAM:SSO'
    );
    

    INSERT INTO application_inventory (
        Name, Description, Division, Sites, Owner, Components,
        Technology, Version, Effective_Date, EOL, Interface, Medium
    ) VALUES (
        'My Wealth', 'Wealth Banking for customer', 
        'Customer Experince (CX)', 'Europe', 
        'Prasanta', 'Batch: Batch 1, Batch 2, Batch 3 | 
Online: Online 1, Online 2, Online 3', 
        'Java 8, spring batch, API, IBM MQ, CFT, Postgres', '4.2.0', 
        'Q-2001', 'Q3-2030', 
        'AAA,SVE, IAM', 'VMS:IBM MQ, AAA:API, SVE:IBM MQ,IAM:OAuth 2.0'
    );
    

    INSERT INTO application_inventory (
        Name, Description, Division, Sites, Owner, Components,
        Technology, Version, Effective_Date, EOL, Interface, Medium
    ) VALUES (
        'IAM', 'Auth platform to support customer authentication and Authorization', 
        'Engineering', 'Europe, ASIA, CH', 
        'Prasanta', 'Batch: Batch 1, Batch 2, Batch 3 | 
Online: Online 1, Online 2, Online 3', 
        'Java 18, Spring, API, Postgress, OAuth2.0, SSO', '3.6.0', 
        'Q1-2015', 'Q4-2030', 
        'AAA, My Wealth', 'AAA:SSO, My Wealth:OAuth 2.0'
    );
    