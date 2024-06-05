-- Stores all restaurants, referenced by name mostly.
USE food;
DROP TABLE IF EXISTS likes;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS dishes;
DROP TABLE IF EXISTS restaurants;

CREATE TABLE `restaurants` (
    id int NOT NULL AUTO_INCREMENT,
    restaurant_name VARCHAR(255) NOT NULL,
    proximity float NOT NULL DEFAULT 0.0,
    delivery_time float NOT NULL DEFAULT 0.0,
    PRIMARY KEY (id),
    UNIQUE KEY `restaurant_name`(`restaurant_name`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

-- Stores all dishes, referenced by restaurant.

CREATE TABLE `dishes` (
    id int NOT NULL AUTO_INCREMENT,
    dish_name VARCHAR(255) NOT NULL,
    restaurant_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    KEY `dish_name`(`dish_name`),
    CONSTRAINT `dishes_ibfk_1` FOREIGN KEY (`restaurant_name`) REFERENCES `restaurants`(`restaurant_name`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

-- Stores all Users.

CREATE TABLE `users` (
    id int NOT NULL AUTO_INCREMENT,
    user_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY `user_name`(`user_name`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

-- Stores all likes, Keys users.

CREATE TABLE `likes` (
    id int NOT NULL AUTO_INCREMENT,
    dish_name VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    restaurant_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (dish_name, user_name, restaurant_name),
    CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`dish_name`) REFERENCES `dishes`(`dish_name`),
    CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`user_name`) REFERENCES `users`(`user_name`),
    CONSTRAINT `likes_ibfk_3` FOREIGN KEY (`restaurant_name`) REFERENCES `restaurants`(`restaurant_name`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

-- Stores all Tags.

CREATE TABLE `tags` (
    id int NOT NULL AUTO_INCREMENT,
    tag VARCHAR(255) NOT NULL,
    dish_name VARCHAR(255) NOT NULL,
    restaurant_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (tag, dish_name, restaurant_name),
    CONSTRAINT `tags_ibfk_1` FOREIGN KEY (`dish_name`) REFERENCES `dishes`(`dish_name`),
    CONSTRAINT `tags_ibfk_2` FOREIGN KEY (`restaurant_name`) REFERENCES `restaurants`(`restaurant_name`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;