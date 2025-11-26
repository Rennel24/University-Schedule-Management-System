-- Insert colleges first
INSERT INTO colleges (college_id, college_name) VALUES
(1, 'COE'),
(2, 'CET'),
(3, 'CAFAD'),
(4, 'CICS');

-- Then insert admins
INSERT INTO admins (admin_name, username, password, college_id) VALUES
('John Santos', 'coeadmin', 'admin123', 1),
('Maria Reyes', 'cetadmin', 'admin123', 2),
('Anna Cruz', 'cafadadmin', 'admin123', 3),
('Mark Delos', 'cicsadmin', 'admin123', 4);
