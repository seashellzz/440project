CREATE DATABASE IF NOT EXISTS Comp440;
USE Comp440;
CREATE TABLE users (
  username VARCHAR(255) PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  firstName VARCHAR(255) NOT NULL,
  lastName VARCHAR(255) NOT NULL
); 
CREATE TABLE items (
  item_id INT PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  description VARCHAR(255),
  post_date VARCHAR(255) NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  username VARCHAR(255),
  FOREIGN KEY (username) REFERENCES users(username)
);
CREATE TABLE item_categories (
  item_id INT,
  category_name VARCHAR(255) NOT NULL,
  FOREIGN KEY (item_id) REFERENCES items(item_id)
);
CREATE TABLE reviews (
  review_id INT PRIMARY KEY AUTO_INCREMENT,
  item_id INT,
  username VARCHAR(255),
  rating ENUM('excellent', 'good', 'fair', 'poor') NOT NULL,
  description VARCHAR(255) NOT NULL,
  review_date VARCHAR(255) NOT NULL,
  FOREIGN KEY (item_id) REFERENCES items(item_id),
  FOREIGN KEY (username) REFERENCES users(username)
);
exit




-- INSERT INTO users (username, email, password, firstName, lastName)
-- VALUES
--   ('user1', 'user1@example.com', 'password1', 'John', 'Doe'),
--   ('user2', 'user2@example.com', 'password2', 'Jane', 'Smith'),
--   ('user3', 'user3@example.com', 'password3', 'Robert', 'Johnson'),
--   ('user4', 'user4@example.com', 'password4', 'Emily', 'Williams'),
--   ('user5', 'user5@example.com', 'password5', 'Michael', 'Brown'),
--   ('user6', 'user6@example.com', 'password6', 'Emma', 'Jones'),
--   ('user7', 'user7@example.com', 'password7', 'William', 'Garcia'),
--   ('user8', 'user8@example.com', 'password8', 'Olivia', 'Miller'),
--   ('user9', 'user9@example.com', 'password9', 'Liam', 'Davis'),
--   ('user10', 'user10@example.com', 'password10', 'Sophia', 'Martinez'),
--   ('user11', 'user11@example.com', 'password11', 'Noah', 'Rodriguez'),
--   ('user12', 'user12@example.com', 'password12', 'Ava', 'Lopez');
-- INSERT INTO items (title, description, post_date, price, username)
-- VALUES
--   ('Item 1', 'Description for item 1', '2023-08-08', 19.99, 'user1'),
--   ('Item 2', 'Description for item 2', '2023-08-08', 29.99, 'user2'),
--   ('Item 3', 'Description for item 3', '2023-08-08', 39.99, 'user3'),
--   ('Item 4', 'Description for item 4', '2023-08-08', 49.99, 'user4'),
--   ('Item 5', 'Description for item 5', '2023-08-08', 59.99, 'user5'),
--   ('Item 6', 'Description for item 6', '2023-08-08', 69.99, 'user6'),
--   ('Item 7', 'Description for item 7', '2023-08-08', 79.99, 'user7'),
--   ('Item 8', 'Description for item 8', '2023-08-08', 89.99, 'user8'),
--   ('Item 9', 'Description for item 9', '2023-08-08', 99.99, 'user9'),
--   ('Item 10', 'Description for item 10', '2023-08-08', 109.99, 'user10'),
--   ('Item 11', 'Description for item 11', '2023-08-08', 119.99, 'user11'),
--   ('Item 12', 'Description for item 12', '2023-08-08', 129.99, 'user12');
-- INSERT INTO item_categories (item_id, category_name)
-- VALUES
--   (1, 'Category 1'),
--   (2, 'Category 2'),
--   (3, 'Category 3'),
--   (4, 'Category 1'),
--   (5, 'Category 2'),
--   (6, 'Category 3'),
--   (7, 'Category 1'),
--   (8, 'Category 2'),
--   (9, 'Category 3'),
--   (10, 'Category 1'),
--   (11, 'Category 2'),
--   (12, 'Category 3');
-- INSERT INTO reviews (item_id, username, rating, description, review_date)
-- VALUES
--   (1, 'user1', 'excellent', 'Great item!', '2023-08-08'),
--   (2, 'user2', 'good', 'Nice product.', '2023-08-08'),
--   (3, 'user3', 'fair', 'Okay item.', '2023-08-08'),
--   (4, 'user4', 'poor', 'Not satisfied.', '2023-08-08'),
--   (5, 'user5', 'excellent', 'Highly recommended.', '2023-08-08'),
--   (6, 'user6', 'good', 'Satisfied with the purchase.', '2023-08-08'),
--   (7, 'user7', 'fair', 'Average quality.', '2023-08-08'),
--   (8, 'user8', 'excellent', 'Fantastic item!', '2023-08-08'),
--   (9, 'user9', 'good', 'Good value for money.', '2023-08-08'),
--   (10, 'user10', 'fair', 'Decent product.', '2023-08-08'),
--   (11, 'user11', 'poor', 'Disappointed.', '2023-08-08'),
--   (12, 'user12', 'excellent', 'Very satisfied!', '2023-08-08');
-- exit
