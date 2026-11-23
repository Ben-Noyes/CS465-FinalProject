-- SAMPLE RECORDS
-- These were created with AI

INSERT INTO Clients (client_id, business_name, contact_name, email, phone, address)
VALUES
(1, 'Snow removal', 'John Doe', 'john.doe@snowremoval.com', '555-1234', '123 Main St'),
(2, 'Web Solutions', 'Jane Smith', 'jane.smith@websolutions.com', '555-5678', '456 Oak Ave'),
(3, 'Lawn Care', 'Mike Johnson', 'mike.johnson@lawncare.com', '555-9012', '789 Pine Rd'),
(4, 'roofing', 'Sarah Lee', 'sarah.lee@roofing.com', '555-3456', '101 Cedar Dr'),
(5, 'Plumbing Pros', 'Tom Brown', 'tom.brown@plumbingpros.com', '555-7890', '202 Elm St'),
(6, 'Construction', 'David Wilson', 'david.wilson@construction.com', '555-1111', '303 Maple Ln'),
(7, 'Electrical Experts', 'Emily Davis', 'emily.davis@electricalexperts.com', '555-2222', '404 Birch St'),
(8, 'Landscaping', 'Chris Martin', 'chris.martin@landscaping.com', '555-3333', '505 Spruce Ave');

INSERT INTO Projects (project_id, client_id, project_name, start_date, complete_date, status, total_cost)
VALUES
(1, 1, 'Winter Cleanup', '2024-01-15', NULL, 'In Progress', 1500.00),
(2, 2, 'Website Redesign', '2024-02-01', NULL, 'Pending', 3000.00),
(3, 3, 'Lawn Maintenance', '2024-03-10', NULL, 'In Progress', 800.00),
(4, 4, 'Roof Replacement', '2024-04-05', NULL, 'Pending', 5000.00),
(5, 5, 'Pipe Installation', '2024-05-20', NULL, 'Pending', 1200.00),
(6, 6, 'Home Renovation', '2024-06-15', NULL, 'In Progress', 10000.00),
(7, 7, 'Electrical Wiring Upgrade', '2024-07-01', NULL, 'Pending', 2500.00),
(8, 8, 'Garden Landscaping', '2024-08-10', NULL, 'In Progress', 2000.00),
(9, 1, 'Snow Plowing', '2024-09-01', NULL, 'Pending', 1800.00),
(10, 2, 'E-commerce Integration', '2024-10-15', NULL, 'Pending', 4000.00);


INSERT INTO Services (service_id, service_name, description, base_price)
VALUES
(1, 'Website Development', 'Design and development of a new website', 2500.00),
(2, 'Website Redesign', 'Modernization of an existing website', 2000.00),
(3, 'SEO Optimization', 'Improving website visibility in search engines', 300.00),
(4, 'Website Maintenance', 'Ongoing website updates and support', 150.00),
(5, 'Google Ads Management', 'Managing Google Ads campaigns', 250.00),
(6, 'Google Business Profile Setup', 'Creating and optimizing a Google Business Profile', 200.00),
(7, 'Analytics Setup', 'Setting up Google Analytics and tracking', 150.00),
(8, 'Content Updates', 'Updating website text and images', 100.00);


INSERT INTO ProjectServices (project_service_id, project_id, service_id, agreed_price, date_added)
VALUES
(1, 1, 1, 2500.00, '2026-06-01'),
(2, 1, 3, 300.00, '2026-06-05'),
(3, 1, 7, 150.00, '2026-06-10'),
(4, 2, 1, 3000.00, '2026-07-01'),
(5, 2, 3, 300.00, '2026-07-05'),
(6, 3, 2, 2800.00, '2026-08-01'),
(7, 3, 7, 150.00, '2026-08-05'),
(8, 4, 1, 3200.00, '2026-09-01'),
(9, 4, 6, 200.00, '2026-09-05'),
(10, 5, 1, 2200.00, '2026-09-15'),
(11, 6, 1, 1800.00, '2026-10-01'),
(12, 7, 1, 2000.00, '2026-10-01'),
(13, 8, 1, 2600.00, '2026-10-05'),
(14, 9, 3, 600.00, '2026-08-01'),
(15, 9, 5, 250.00, '2026-08-10'),
(16, 10, 3, 450.00, '2026-09-01');

INSERT INTO Invoices (invoice_id, project_id, invoice_date, due_date, total_amount, status)
VALUES
(1, 1, '2024-01-15', '2024-02-15', 1500.00, 'Paid'),
(2, 2, '2024-02-01', '2024-03-01', 3000.00, 'Paid'),
(3, 3, '2024-03-10', '2024-04-10', 800.00, 'Paid'),
(4, 4, '2024-04-05', '2024-05-05', 5000.00, 'Overdue'),
(5, 5, '2024-05-20', '2024-06-20', 1200.00, 'Paid'),
(6, 6, '2024-06-15', '2024-07-15', 10000.00, 'Overdue'),
(7, 7, '2024-07-01', '2024-08-01', 2500.00, 'Paid'),
(8, 8, '2024-08-10', '2024-09-10', 2000.00, 'Overdue'),
(9, 9, '2024-09-01', '2024-10-01', 1800.00, 'Paid'),
(10, 10, '2024-10-15', '2024-11-15', 4000.00, 'Overdue'),
(11, 1, '2024-02-15', '2024-03-15', 300.00, 'Paid'),
(12, 2, '2024-03-01', '2024-04-01', 150.00, 'Paid'),
(13, 3, '2024-04-10', '2024-05-10', 200.00, 'Overdue'),
(14, 4, '2024-05-05', '2024-06-05', 250.00, 'Paid'),
(15, 5, '2024-06-20', '2024-07-20', 100.00, 'Overdue');


-- Insert payments received for client invoices
INSERT INTO Payments (payment_id, invoice_id, payment_date, amount, payment_method)
VALUES
(1, 1, '2024-02-01', 1500.00, 'Credit Card'),
(2, 2, '2024-02-20', 3000.00, 'Bank Transfer'),
(3, 3, '2024-04-01', 800.00, 'Check'),
(4, 5, '2024-06-01', 1200.00, 'Credit Card'),
(5, 7, '2024-07-20', 2500.00, 'Bank Transfer'),
(6, 9, '2024-09-20', 1800.00, 'Check'),
(7, 11, '2024-03-01', 300.00, 'Credit Card'),
(8, 12, '2024-03-15', 150.00, 'Bank Transfer'),
(9, 14, '2024-05-20', 250.00, 'Cash'),
(10, 4, '2024-05-01', 1000.00, 'Bank Transfer'),
(11, 6, '2024-07-01', 2000.00, 'Check'),
(12, 8, '2024-09-01', 500.00, 'Credit Card');
