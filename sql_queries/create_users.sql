CREATE TABLE users(
    ID INT AUTO_INCREMENT,
    UserName VARCHAR(20),
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Password VARCHAR(100),
    Email VARCHAR(100),
    SignUpDate DATETIME,
    PRIMARY KEY(ID)
);