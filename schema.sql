PRAGMA foreign_keys = ON;
.mode box

DROP TABLE IF EXISTS Payments;
DROP TABLE IF EXISTS Invoices;
DROP TABLE IF EXISTS ProjectServices;
DROP TABLE IF EXISTS Services;
DROP TABLE IF EXISTS Projects;
DROP TABLE IF EXISTS Clients;

-- Stores the client business information and contact details
CREATE TABLE Clients (
    client_id INTEGER PRIMARY KEY,
    business_name TEXT NOT NULL,
    contact_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    address TEXT
);

-- Stores website projects and tracks their status, cost, and associated client
CREATE TABLE Projects (
    project_id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    project_name TEXT NOT NULL,
    start_date TEXT NOT NULL,
    complete_date TEXT,
    status TEXT NOT NULL DEFAULT 'Pending',
    total_cost REAL CHECK (total_cost >= 0),

    FOREIGN KEY (client_id) REFERENCES Clients(client_id),
    CHECK (status IN ('Pending', 'In Progress', 'Completed', 'On Hold'))
);

-- Stores the services offered
CREATE TABLE Services (
    service_id INTEGER PRIMARY KEY,
    service_name TEXT NOT NULL UNIQUE,
    description TEXT,
    base_price REAL NOT NULL CHECK (base_price >= 0)
);

-- Connects projects tot their services and tracks the price
CREATE TABLE ProjectServices (
    project_service_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    agreed_price REAL NOT NULL CHECK (agreed_price >= 0),
    date_added TEXT,

    FOREIGN KEY (project_id) REFERENCES Projects(project_id),
    FOREIGN KEY (service_id) REFERENCES Services(service_id),
    UNIQUE (project_id, service_id)
);

-- Stores invoices for projects, including the total amount and payment status
CREATE TABLE Invoices (
    invoice_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL,
    invoice_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    total_amount REAL NOT NULL CHECK (total_amount >= 0),
    status TEXT NOT NULL DEFAULT 'Unpaid',

    FOREIGN KEY (project_id) REFERENCES Projects(project_id),
    CHECK (status IN ('Unpaid', 'Paid', 'Overdue')),
    CHECK (due_date >= invoice_date)
);

-- Stores payments made
CREATE TABLE Payments (
    payment_id INTEGER PRIMARY KEY,
    invoice_id INTEGER NOT NULL,
    payment_date TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount >= 0),
    payment_method TEXT NOT NULL,

    FOREIGN KEY (invoice_id) REFERENCES Invoices(invoice_id),
    CHECK (payment_method IN ('Credit Card', 'Bank Transfer', 'Cash', 'Check'))
);

-- View to calculate the balance due for each invoice, including the total amount, amount paid, and balance due
DROP VIEW IF EXISTS InvoiceBalances;

CREATE VIEW InvoiceBalances AS
SELECT
    i.invoice_id,
    p.project_name,
    c.business_name,
    i.total_amount,
    COALESCE(SUM(pay.amount), 0) AS amount_paid,
    i.total_amount - COALESCE(SUM(pay.amount), 0) AS balance_due
FROM Invoices i
JOIN Projects p ON i.project_id = p.project_id
JOIN Clients c ON p.client_id = c.client_id
LEFT JOIN Payments pay ON i.invoice_id = pay.invoice_id
GROUP BY 
    i.invoice_id,
    p.project_name,
    c.business_name,
    i.total_amount;

-- Index used to improve searches for projects based on their status
CREATE INDEX idx_project_status
ON Projects(status);