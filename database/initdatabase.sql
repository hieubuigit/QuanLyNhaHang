create database QuanLyBanHang;

create table Employee (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(20),
    LastName VARCHAR(20),
    BirthDate DATE,
    Gender BOOL,
    PhoneNumber VARCHAR(12),
    Email VARCHAR(100),
    BasicSalary DECIMAL,
    Address VARCHAR(255),
    MaterialStatus INT,
    AvatarUrl VARCHAR(255),
    CreatedDate DATETIME,
    UpdatedDate DATETIME
);