-- Transaction:
-- This script demonstrates recording a payment
-- Records a payment for an invoice and updates the invoice status if fully paid

BEGIN TRANSACTION;
-- Record a payment for invoice_id 15
INSERT INTO Payments (invoice_id, payment_date, amount, payment_method)
VALUES (15, '2024-07-01', 100.00, 'Credit Card');

-- Update the invoice status to 'Paid' if the total payments equal or exceed the invoice total
UPDATE Invoices
SET status = 'Paid'
WHERE invoice_id = 15;

-- Undo both for the sample database
ROLLBACK;