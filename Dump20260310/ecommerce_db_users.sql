-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: ecommerce_db
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('customer','super_admin','product_manager','order_manager','payment_manager','delivery_manager') DEFAULT 'customer',
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `profile_image` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'ashik','ashik@gmail.com','pbkdf2:sha256:600000$3b4rs4tSz9SbdhcY$dce074b96839c31a39a44849d0b2c176e8a67bee62127a5f76c84e73b8e91f3a','customer','ashik','s','8660479735',NULL,1,'2026-03-06 05:44:18','2026-03-06 08:33:33'),(2,'varshitha','varshitha@gmail.com','pbkdf2:sha256:600000$CJEPV0BmA5jtUy4i$784c2546a8dc5abf99bca18354940156b523c30e22cb16ca0bf6b41a3722e3e3','customer','varshu','n',NULL,NULL,1,'2026-03-06 06:05:08','2026-03-06 06:05:08'),(3,'admin','admin@ecommerce.com','pbkdf2:sha256:600000$ecY9HWWRZekCzm0a$c83fbb6a6eecf53396373aaf49d7dfaf3799c72c676b7f098789e16995b6df19','super_admin','Admin','User',NULL,NULL,1,'2026-03-06 06:40:19','2026-03-06 06:40:19'),(4,'order_mgr','order_mgr@ecommerce.com','pbkdf2:sha256:600000$mdhkOSlaoyvp4B8s$66752aa0b8231ac632cf1c46cf2f945a63496c9b0135c2e4b2b762a556502c72','order_manager','order_mgr','Admin',NULL,NULL,1,'2026-03-06 09:11:15','2026-03-06 09:11:15'),(5,'delivery_mgr','delivery_mgr@ecommerce.com','pbkdf2:sha256:600000$RvEcRn5QA1766YnH$48035b524884fba2ee3189c394051a68388d131098bb8ff41657c65932b82f2f','delivery_manager','delivery_mgr','Admin',NULL,NULL,1,'2026-03-06 09:19:24','2026-03-06 09:19:24'),(6,'product_mgr','product_mgr@ecommerce.com','pbkdf2:sha256:600000$anwo2eUzPdMmLCYc$21effc4882fb4e22444757fd65c0e8ae64980e42e242b4c533ef000be6b461fe','product_manager','product_mgr','Admin',NULL,NULL,1,'2026-03-06 09:19:54','2026-03-06 09:19:54'),(7,'payment_mgr','payment_mgr@ecommerce.com','pbkdf2:sha256:600000$ORd3JkazGYdJKeor$f54fb79efb6f9974680aaf422b9cd8e685440c148341b6605eb8bf7ac76a336f','payment_manager','payment_mgr','Admin',NULL,NULL,1,'2026-03-06 09:49:15','2026-03-06 09:49:15'),(8,'lakshmi','lakshmi@gmail.com','pbkdf2:sha256:600000$mzm5QSyPS80hz4lv$09dccb7d7c4c7d98ca55d491fbdb356761ce990c75bae711c998fc32e57ac240','customer','lakshmi','h k',NULL,NULL,1,'2026-03-10 04:42:30','2026-03-10 04:42:30'),(9,'ashiks','aasshhiikk9972@gmail.com','pbkdf2:sha256:600000$Cz4SNo3IVTUZ3SVU$6d2469ba8a961c90dc17b8a956622384160e29ed00b0e8197534ebc1d9f5fd28','customer','ashik','s',NULL,NULL,1,'2026-03-10 06:09:26','2026-03-10 06:14:35');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-10 20:31:50
