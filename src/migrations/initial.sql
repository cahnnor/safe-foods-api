-- sets up demo data for safe-foods DB.
USE food;
INSERT INTO `restaurants` (id, restaurant_name, proximity, delivery_time) VALUES (1, "Shawarma Palace", 1.5, 15), (2, "Ozzy\'s", 0.0, 0.0);
INSERT INTO `dishes` (id, dish_name, restaurant_name) VALUES (1, "Chicken Shawarma Wrap", "Shawarma Palace"), (2, "Chicken Shawarma Platter", "Ozzy\'s");
INSERT INTO `users` (id, user_name) VALUES (1, "Connor"), (2, "Not Connor");
INSERT INTO `likes` (id, user_name, dish_name, restaurant_name) VALUES (1, "Connor", "Chicken Shawarma Platter", "Ozzy\'s"), (2, "Not Connor", "Chicken Shawarma Wrap", "Shawarma Palace");
INSERT INTO `tags` (id, tag, dish_name, restaurant_name) VALUES (1, "Halal", "Chicken Shawarma Platter", "Ozzy\'s"), (2, "Halal", "Chicken Shawarma Wrap", "Shawarma Palace"), (3, "Lactose-Free", "Chicken Shawarma Platter", "Ozzy\'s");