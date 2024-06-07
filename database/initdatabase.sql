-- noinspection SqlNoDataSourceInspectionForFile

-- noinspection SqlDialectInspectionForFile

create
database QuanLyNhaHang;

-- User table include information of employee and account login into system
create table User
(
    Id          INT not null AUTO_INCREMENT PRIMARY KEY,
    UserCode    VARCHAR(25),
    FirstName   VARCHAR(20),
    LastName    VARCHAR(20),
    BirthDate   DATE,
    Identity    varchar(13),
    Gender      int,
    IncomeDate  DATE,
    PhoneNumber VARCHAR(12),
    `Email`     VARCHAR(100),
    Address     VARCHAR(255),
    UserName    VARCHAR(255),
    Password    VARCHAR(255),
    Status      int comment 'Active/Inactive',
    Type        int not null comment 'Admin, or Normal User',
    CreatedDate DATETIME,
    UpdatedDate DATETIME
);

create table Payslip
(
    Id          INT not null AUTO_INCREMENT PRIMARY KEY,
    UserId      INT not null,
    TotalSalary decimal(15, 2),
    Hours       float,
    PayOnMonth  VARCHAR(255),
    CreatedDate DATETIME,
    UpdatedDate DATETIME,
    constraint FK_USER_PAY_SLIP foreign key (UserId) references User (Id)
);

create table PayGrade
(
    Id          INT not null AUTO_INCREMENT PRIMARY KEY,
    Type        int not null comment 'User type on User table',
    Allowance   float,
    PayPerHours float,
    CreatedDate DATETIME,
    UpdatedDate DATETIME
);

create table `Table`
(
    Id          INT not null AUTO_INCREMENT PRIMARY KEY,
    TableNum    varchar(255)  not null,
    SeatNum     int not null,
    Status      int comment 'Available or Empty',
    CreatedDate DATETIME,
    UpdatedDate DATETIME
);

create table Product
(
    Id          INT            not null AUTO_INCREMENT PRIMARY KEY,
    Name        varchar(255)   not null,
    Price       decimal(15, 2) not null,
    Unit        int            not null,
    Quantity    float          not null,
    Capacity    float          not null,
    Alcohol     float          not null comment 'tinh thue tieu thu dac biet',
    ProductType int            not null comment 'Food/Drink',
    Image       BLOB   comment 'Image of food/drink',
    CreatedDate DATETIME       not null,
    UpdatedDate DATETIME
);

create table Billing
(
    Id                  INT            not null AUTO_INCREMENT PRIMARY KEY,
    TableId             int,
    UserId              int            not null,
    DiscountId          int,
    CustomerName        varchar(50)    not null,
    CustomerPhoneNumber varchar(12)    not null,
    TotalMoney          decimal(15, 2) not null,
    Type                int            not null,
    Status              int            not null,
    CreatedDate         DATETIME,
    UpdatedDate         DATETIME
);

create table OrderList
(
    Id          INT            not null AUTO_INCREMENT PRIMARY KEY,
    BillingId   int            not null,
    ProductId   int            not null,
    CurPrice    decimal(15, 2) not null,
    Quantity    int            not null,
    CreatedDate DATETIME,
    UpdatedDate DATETIME,

    constraint FK_BILLING_ORDERlIST foreign key (BillingId) references Billing (Id),
    constraint FK_PRODUCT_ORDERLIST foreign key (ProductId) references Product (Id)
);

create table Discount
(
    Id          INT          not null AUTO_INCREMENT PRIMARY KEY,
    Percent     float        not null,
    StartDate   date         not null,
    EndDate     date         not null,
    Quantity    int          not null,
    Description varchar(200) not null,
    CreatedDate DATETIME     not null,
    UpdatedDate DATETIME
);



--- Insert template database
-- User name = admin, Password = Abc@123
INSERT INTO user(UserCode, FirstName, LastName, BirthDate, Identity, Gender, IncomeDate, PhoneNumber, Email, Address, UserName, Password, Status, Type, CreatedDate, UpdatedDate)
VALUES ('NV1', 'Admin', 'Admin', '1999-01-01', '123456789', 1, curdate(), '09876543211', 'abc@gmail.com', 'Sai Gon', 'admin', '$2b$12$5b69Fb94hoY08JdHjqV4IOscwNrCvn.vYEu0TyYcQi82x4lW0xbJm', 1, 0, curdate(), NULL)
