CREATE TABLE IF NOT EXISTS delegates (
    ID INT PRIMARY KEY,
    Name VARCHAR(100),
    School VARCHAR(100),
    Age INT,
    MUNs INT,
    Committee VARCHAR(50),
    Portfolio1 VARCHAR(100),
    Portfolio2 VARCHAR(100),
    BD INT,
    HC INT,
    SM INT,
    HM INT,
    VM INT
);

CREATE TABLE IF NOT EXISTS AIPPM (
    ID INT PRIMARY KEY,
    Portfolio VARCHAR(255) NOT NULL,
    Status ENUM('Available', 'Reserved', 'Alloted') NOT NULL DEFAULT 'Available',
    Delegate VARCHAR(255) DEFAULT NULL
);


CREATE TABLE IF NOT EXISTS UNGA (
    ID INT PRIMARY KEY,
    Portfolio VARCHAR(255) NOT NULL,
    Status ENUM('Available', 'Reserved', 'Alloted') NOT NULL DEFAULT 'Available',
    Delegate VARCHAR(255) DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS UNHRC (
    ID INT PRIMARY KEY,
    Portfolio VARCHAR(255) NOT NULL,
    Status ENUM('Available', 'Reserved', 'Alloted') NOT NULL DEFAULT 'Available',
    Delegate VARCHAR(255) DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS CRISIS (
    ID INT PRIMARY KEY,
    Portfolio VARCHAR(255) NOT NULL,
    Status ENUM('Available', 'Reserved', 'Alloted') NOT NULL DEFAULT 'Available',
    Delegate VARCHAR(255) DEFAULT NULL
);

