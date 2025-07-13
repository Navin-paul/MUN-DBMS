
CREATE TABLE delegates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    school VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    experience TEXT,
    country1 VARCHAR(100),
    country2 VARCHAR(100),
    country3 VARCHAR(100),
    committee VARCHAR(100)
);