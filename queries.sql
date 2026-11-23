-- Requirement 1: Filtering and Sorting
-- This query shows all projects that are currently in progress, sorted by their total cost in descending order.
SELECT 
    project_name, status, total_cost
FROM Projects
WHERE status = 'In Progress'
ORDER BY total_cost DESC;

-- Requirement 2: INNER JOIN
-- This query shows each client, their project, and the status of that project

SELECT
    c.business_name, p.project_name, p.status
FROM Projects p
INNER JOIN Clients c
    ON c.client_id = p.client_id
ORDER BY c.business_name;

-- Requirement 3: LEFT JOIN
-- This query shows all invoices that have not been paid

SELECT 
    i.invoice_id, i.total_amount, i.status, p.payment_id
FROM Invoices i
LEFT JOIN Payments p
    ON i.invoice_id = p.invoice_id
WHERE p.payment_id IS NULL
ORDER BY i.invoice_id;

-- Requirement 4: Three-Table Join
-- This query shows each client, their project, and the amount of their invoice
SELECT
    c.business_name, p.project_name, i.invoice_id, i.total_amount,
    i.status AS invoice_status
FROM Clients c
INNER JOIN Projects p
    ON c.client_id = p.client_id
INNER JOIN Invoices i
    ON p.project_id = i.project_id
ORDER BY c.business_name, i.invoice_id;

-- Requirement 5: Aggregate Query
-- This query calculates the total payments received across all invoices
SELECT
    SUM(amount) AS total_payments_received
FROM Payments;

-- Requirement 6: GROUP BY and HAVING
-- This query shows the services that are used by more than one client

SELECT
    s.service_name,
    COUNT(ps.project_service_id) AS number_of_projects
FROM Services s
INNER JOIN ProjectServices ps
    ON s.service_id = ps.service_id
GROUP BY s.service_name
HAVING COUNT(ps.project_service_id) > 1
ORDER BY number_of_projects DESC;

-- Requirement 7: Subquery
-- This query shows projects that cost more than the average total cost of all projects
SELECT
    project_name, total_cost
FROM Projects
WHERE total_cost > (
    SELECT AVG(total_cost)
    FROM Projects
)

ORDER BY total_cost DESC;

-- Requirement 8: Set Operation
-- This query shows clients who have either pending projects or overdue invoices
SELECT
    c.business_name
FROM Clients c
INNER JOIN Projects p
    ON c.client_id = p.client_id
WHERE p.status = 'Pending'
UNION
SELECT
    c.business_name
FROM Clients c
INNER JOIN Projects p
    ON c.client_id = p.client_id
INNER JOIN Invoices i
    ON p.project_id = i.project_id
WHERE i.status = 'Overdue'

ORDER BY business_name;

-- Requirement 9: View
-- This query shows invoices with outstanding balance, and amount owed
SELECT
    business_name, project_name, invoice_id, total_amount, amount_paid, balance_due
FROM InvoiceBalances
WHERE balance_due > 0
ORDER BY balance_due DESC;

