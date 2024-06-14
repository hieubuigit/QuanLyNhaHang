CREATE TABLE bill
(
    id             int UNSIGNED AUTO_INCREMENT
        PRIMARY KEY,
    id_user        int                                      NOT NULL,
    reciever       varchar(255) DEFAULT 'Không tên'         NULL,
    coupon         double       DEFAULT 0                   NULL,
    ship_cost      double       DEFAULT 0                   NULL,
    total_bill     double       DEFAULT 0                   NOT NULL,
    recive_address varchar(255)                             NULL,
    phone          varchar(255)                             NULL,
    email          varchar(255)                             NULL,
    status_order   int          DEFAULT 1                   NULL,
    payment_method varchar(45)                              NULL,
    date_order     timestamp    DEFAULT CURRENT_TIMESTAMP() NULL,
    date_finish    date                                     NULL,
    date_cancel    date                                     NULL,
    cancel_reason  varchar(255)                             NULL,
    created_at     timestamp    DEFAULT CURRENT_TIMESTAMP() NULL,
    updated_at     timestamp    DEFAULT CURRENT_TIMESTAMP() NULL ON UPDATE CURRENT_TIMESTAMP()
)
    COLLATE = utf8mb4_unicode_ci;

CREATE TABLE bill_detail
(
    id         int AUTO_INCREMENT
        PRIMARY KEY,
    id_bill    char(10)                              NOT NULL,
    id_product char(10)                              NOT NULL,
    price      double                                NOT NULL,
    quantity   int                                   NOT NULL,
    total      double                                NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP() NULL,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP() NULL ON UPDATE CURRENT_TIMESTAMP()
)
    COLLATE = utf8mb4_unicode_ci;

CREATE TABLE cart
(
    id         int AUTO_INCREMENT
        PRIMARY KEY,
    id_user    int                                   NOT NULL,
    id_code    int                                   NULL,
    total_cart double    DEFAULT 0                   NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP() NULL,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP() NULL ON UPDATE CURRENT_TIMESTAMP()
)
    COLLATE = utf8mb4_unicode_ci;

CREATE TABLE cart_detail
(
    id         int UNSIGNED AUTO_INCREMENT
        PRIMARY KEY,
    id_cart    int                                   NOT NULL,
    id_product char(10)                              NOT NULL,
    size       varchar(255)                          NULL,
    price      double                                NULL,
    quantity   int                                   NULL,
    total      double                                NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP() NULL,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP() NULL ON UPDATE CURRENT_TIMESTAMP()
)
    COLLATE = utf8mb4_unicode_ci;

CREATE DEFINER = root@localhost TRIGGER `add_cart_detail-update-total-cart`
    AFTER INSERT
    ON cart_detail
    FOR EACH ROW
    UPDATE cart SET total_cart = (SELECT SUM(total) FROM cart_detail WHERE cart_detail.id_cart = NEW.id_cart)
                                                                                                                                                        WHERE cart.id = NEW.id_cart;

CREATE DEFINER = root@localhost TRIGGER remove_cart_detail
    AFTER DELETE
    ON cart_detail
    FOR EACH ROW
    UPDATE cart
                                                                                                                                         SET total_cart = (SELECT SUM(total)
                                                                                                                                                           FROM cart_detail
                                                                                                                                                           WHERE cart_detail.id_cart = 						old.id_cart)
                                                                                                                                         WHERE id = old.id_cart;

CREATE DEFINER = root@localhost TRIGGER `update_cart_detail-Cart`
    AFTER UPDATE
    ON cart_detail
    FOR EACH ROW
    UPDATE cart
                                                                                                                                              SET total_cart = (SELECT SUM(total)
                                                                                                                                                                FROM cart_detail
                                                                                                                                                                WHERE cart_detail.id_cart = 						NEW.id_cart)
                                                                                                                                              WHERE id = NEW.id_cart;

CREATE TABLE category
(
    id          int AUTO_INCREMENT
        PRIMARY KEY,
    title       varchar(45)                           NOT NULL,
    description varchar(45)                           NULL,
    created_at  timestamp DEFAULT CURRENT_TIMESTAMP() NULL,
    updated_at  timestamp                             NULL ON UPDATE CURRENT_TIMESTAMP()
)
    COLLATE = utf8mb4_unicode_ci;

CREATE TABLE color
(
    id         int AUTO_INCREMENT
        PRIMARY KEY,
    color_name varchar(255)                          NOT NULL,
    code       varchar(255)                          NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP() NULL,
    updated_at timestamp                             NULL ON UPDATE CURRENT_TIMESTAMP()
)
    COLLATE = utf8mb4_unicode_ci;

CREATE TABLE customer
(
    id           int AUTO_INCREMENT
        PRIMARY KEY,
    full_name    varchar(45)                           NULL,
    email        varchar(45)                           NULL,
    phone_number varchar(45)                           NULL,
    address      varchar(45)                           NULL,
    birthday     date                                  NULL,
    sex          char                                  NULL,
    created_at   timestamp DEFAULT CURRENT_TIMESTAMP() NULL,
    updated_at   timestamp                             NULL ON UPDATE CURRENT_TIMESTAMP()
)
    COLLATE = utf8mb4_unicode_ci;

CREATE TABLE employee
(
    id             int AUTO_INCREMENT
        PRIMARY KEY,
    full_name      varchar(45)                           NULL,
    phone_number   varchar(45)                           NULL,
    birthday       date                                  NULL,
    sex            char                                  NULL,
    roles_group_id int                                   NULL,
    created_at     timestamp DEFAULT CURRENT_TIMESTAMP() NULL,
    updated_at     timestamp                             NULL ON UPDATE CURRENT_TIMESTAMP()
)
    COLLATE = utf8mb4_unicode_ci;

CREATE TABLE feedback
(
    id           int UNSIGNED NOT NULL,
    id_user      int          NOT NULL,
    virtual_name varchar(50)  NULL,
    id_product   char(10)     NOT NULL,
    content      varchar(255) NULL,
    star         int          NOT NULL,
    created_at   timestamp    NULL,
    updated_at   timestamp    NULL
)
    COLLATE = utf8mb4_unicode_ci;

CREATE TABLE gender
(
    id   int                                    NOT NULL,
    name varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL
)
    CHARSET = latin1;

CREATE TABLE my_product
(
    id         int AUTO_INCREMENT
        PRIMARY KEY,
    id_product char(10)                              NOT NULL,
    id_user    int                                   NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP() NULL,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP() NULL ON UPDATE CURRENT_TIMESTAMP()
)
    COLLATE = utf8mb4_unicode_ci;

CREATE DEFINER = root@localhost TRIGGER `can't add product already exists`
    BEFORE INSERT
    ON my_product
    FOR EACH ROW
    IF EXISTS(SELECT *
                                                                                                                                                                 FROM my_product
                                                                                                                                                                 WHERE id_product =NEW.id_product
                                                                                                                                                                   AND id_user = NEW.id_user)
THEN
    SIGNAL SQLSTATE VALUE '45000' SET MESSAGE_TEXT = 'INSERT failed due to duplicate wish item';
END IF;

CREATE TABLE product_detail
(
    id         int UNSIGNED NOT NULL,
    id_product char(10)     NOT NULL,
    id_store   int          NOT NULL,
    id_color   int          NOT NULL,
    id_size    int          NOT NULL,
    quantity   int          NOT NULL,
    created_at timestamp    NULL,
    updated_at timestamp    NULL
)
    COLLATE = utf8mb4_unicode_ci;

CREATE TABLE product_images
(
    id         int AUTO_INCREMENT
        PRIMARY KEY,
    id_product char(10)                              NOT NULL,
    image      varchar(255)                          NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP() NULL,
    updated_at timestamp                             NULL ON UPDATE CURRENT_TIMESTAMP()
)
    COLLATE = utf8mb4_unicode_ci;

CREATE TABLE product_store
(
    id           int UNSIGNED  NOT NULL,
    id_product   char(10)      NOT NULL,
    id_store     int           NOT NULL,
    number       int DEFAULT 0 NOT NULL,
    number_tranf int DEFAULT 0 NOT NULL,
    status       int DEFAULT 0 NOT NULL,
    number_error int DEFAULT 0 NOT NULL,
    created_at   timestamp     NULL,
    updated_at   timestamp     NULL
)
    COLLATE = utf8mb4_unicode_ci;

CREATE TABLE products
(
    id              int UNSIGNED AUTO_INCREMENT
        PRIMARY KEY,
    id_product      char(10)                                 NOT NULL,
    name            varchar(255)                             NULL,
    id_type         int                                      NULL,
    id_color        int                                      NULL,
    quantity        int          DEFAULT 100                 NULL,
    gender          int                                      NULL,
    description     text                                     NULL,
    import_price    double       DEFAULT 0                   NULL,
    price           double       DEFAULT 0                   NULL,
    promotion_price double       DEFAULT -1                  NULL,
    image           varchar(255) DEFAULT ''                  NULL,
    new             int          DEFAULT 0                   NULL,
    hot             int          DEFAULT 0                   NULL,
    created_at      timestamp    DEFAULT CURRENT_TIMESTAMP() NULL,
    updated_at      timestamp    DEFAULT CURRENT_TIMESTAMP() NULL
)
    COLLATE = utf8mb4_unicode_ci;

CREATE TABLE status_order
(
    id         int UNSIGNED AUTO_INCREMENT
        PRIMARY KEY,
    name       varchar(255) NOT NULL,
    created_at timestamp    NULL,
    updated_at timestamp    NULL
)
    COLLATE = utf8mb4_unicode_ci;

CREATE TABLE type_product
(
    id         int UNSIGNED AUTO_INCREMENT
        PRIMARY KEY,
    name       varchar(255)                          NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP() NULL,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP() NULL
)
    COLLATE = utf8mb4_unicode_ci;

CREATE TABLE users
(
    id           int AUTO_INCREMENT
        PRIMARY KEY,
    username     varchar(255)                          NOT NULL,
    password     varchar(255)                          NOT NULL,
    email        varchar(255)                          NULL,
    full_name    varchar(255)                          NULL,
    phone_number varchar(255)                          NULL,
    address      varchar(255)                          NULL,
    create_at    timestamp DEFAULT CURRENT_TIMESTAMP() NULL,
    activation   varchar(255)                          NULL
)
    COLLATE = utf8mb4_unicode_ci;


