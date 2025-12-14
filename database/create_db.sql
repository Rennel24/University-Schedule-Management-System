INSERT INTO sections (section_name, program_id) VALUES
('BSCS 1101', (SELECT program_id FROM programs WHERE program_name='BSCS')),
('BSCS 2101', (SELECT program_id FROM programs WHERE program_name='BSCS')),
('BSIT 3101', (SELECT program_id FROM programs WHERE program_name='BSIT')),
('BSCS 3101', (SELECT program_id FROM programs WHERE program_name='BSCS')),
('BSIT 4101', (SELECT program_id FROM programs WHERE program_name='BSIT')),
('BSCS 4101', (SELECT program_id FROM programs WHERE program_name='BSCS'));
