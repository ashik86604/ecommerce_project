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
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `shipping_address_id` int DEFAULT NULL,
  `order_status` enum('placed','payment_verified','processing','packed','shipped','out_for_delivery','delivered','cancelled') DEFAULT 'placed',
  `payment_method` enum('upi','card') NOT NULL,
  `payment_status` enum('pending','verified','failed','refunded') DEFAULT 'pending',
  `order_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `estimated_delivery` date DEFAULT NULL,
  `delivered_date` datetime DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `razorpay_order_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`order_id`),
  KEY `user_id` (`user_id`),
  KEY `shipping_address_id` (`shipping_address_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`shipping_address_id`) REFERENCES `addresses` (`address_id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,1,15800.00,1,'shipped','upi','refunded','2026-03-06 08:34:31','2026-03-11',NULL,'2026-03-06 08:34:31','2026-03-07 09:31:16',NULL),(2,2,47300.00,2,'delivered','upi','refunded','2026-03-06 09:57:37','2026-03-11',NULL,'2026-03-06 09:57:37','2026-03-07 09:32:04',NULL),(3,1,15800.00,1,'placed','upi','pending','2026-03-06 16:26:31','2026-03-11',NULL,'2026-03-06 16:26:31','2026-03-06 16:26:31',NULL),(4,1,51.05,1,'placed','card','pending','2026-03-06 16:31:05','2026-03-11',NULL,'2026-03-06 16:31:05','2026-03-06 16:31:05',NULL),(5,1,52.10,1,'placed','upi','pending','2026-03-06 16:44:43','2026-03-11',NULL,'2026-03-06 16:44:43','2026-03-06 16:44:43',NULL),(6,1,51.05,1,'processing','card','pending','2026-03-06 16:50:52','2026-03-11',NULL,'2026-03-06 16:50:52','2026-03-07 08:41:40',NULL),(7,1,52.10,1,'placed','upi','pending','2026-03-06 17:17:10','2026-03-11',NULL,'2026-03-06 17:17:10','2026-03-06 17:17:10',NULL),(8,1,52.10,1,'cancelled','card','refunded','2026-03-06 17:17:14','2026-03-11',NULL,'2026-03-06 17:17:14','2026-03-06 17:36:18',NULL),(9,1,52.10,1,'placed','card','pending','2026-03-06 17:44:58','2026-03-11',NULL,'2026-03-06 17:44:58','2026-03-06 17:44:58',NULL),(10,1,52.10,1,'placed','card','pending','2026-03-06 17:46:53','2026-03-11',NULL,'2026-03-06 17:46:53','2026-03-06 17:46:53',NULL),(11,1,52.10,1,'placed','upi','pending','2026-03-06 17:46:56','2026-03-11',NULL,'2026-03-06 17:46:56','2026-03-06 17:46:56',NULL),(12,1,52.10,1,'placed','card','pending','2026-03-06 17:49:16','2026-03-11',NULL,'2026-03-06 17:49:16','2026-03-06 17:49:16',NULL),(13,1,52.10,1,'placed','card','pending','2026-03-06 18:06:51','2026-03-11',NULL,'2026-03-06 18:06:51','2026-03-06 18:06:51',NULL),(14,1,52.10,1,'placed','upi','pending','2026-03-06 18:07:06','2026-03-11',NULL,'2026-03-06 18:07:06','2026-03-06 18:07:06',NULL),(15,1,52.10,1,'placed','upi','pending','2026-03-06 18:09:39','2026-03-11',NULL,'2026-03-06 18:09:39','2026-03-06 18:09:39',NULL),(16,1,52.10,1,'placed','card','pending','2026-03-06 18:09:51','2026-03-11',NULL,'2026-03-06 18:09:51','2026-03-06 18:09:51',NULL),(17,1,52.10,1,'processing','upi','pending','2026-03-06 18:10:03','2026-03-11',NULL,'2026-03-06 18:10:03','2026-03-07 09:04:57',NULL),(18,1,52.10,1,'cancelled','card','refunded','2026-03-06 18:48:39','2026-03-12',NULL,'2026-03-06 18:48:39','2026-03-06 18:53:35',NULL),(19,1,63050.00,1,'delivered','upi','pending','2026-03-06 18:54:05','2026-03-12',NULL,'2026-03-06 18:54:05','2026-03-07 09:55:24',NULL),(20,1,78800.00,1,'packed','upi','pending','2026-03-06 19:01:56','2026-03-12',NULL,'2026-03-06 19:01:56','2026-03-07 09:04:33',NULL),(21,1,15800.00,1,'shipped','upi','pending','2026-03-07 05:41:09','2026-03-12',NULL,'2026-03-07 05:41:09','2026-03-07 09:04:24',NULL),(22,1,15800.00,1,'delivered','upi','pending','2026-03-07 05:41:31','2026-03-12',NULL,'2026-03-07 05:41:31','2026-03-07 09:04:14',NULL),(23,1,15800.00,1,'delivered','upi','pending','2026-03-07 05:44:33','2026-03-12',NULL,'2026-03-07 05:44:33','2026-03-07 09:11:52',NULL),(24,1,15800.00,1,'out_for_delivery','upi','pending','2026-03-07 05:54:18','2026-03-12',NULL,'2026-03-07 05:54:18','2026-03-07 09:03:46',NULL),(25,1,51.05,1,'cancelled','upi','refunded','2026-03-07 09:56:43','2026-03-12',NULL,'2026-03-07 09:56:43','2026-03-07 09:57:03',NULL),(26,1,31550.00,1,'placed','upi','pending','2026-03-07 10:05:00','2026-03-12',NULL,'2026-03-07 10:05:00','2026-03-07 10:05:00',NULL),(27,1,31550.00,1,'payment_verified','upi','verified','2026-03-07 10:08:21','2026-03-12',NULL,'2026-03-07 10:08:21','2026-03-07 10:08:26',NULL),(28,1,51.05,1,'placed','card','pending','2026-03-09 05:17:45','2026-03-14',NULL,'2026-03-09 05:17:45','2026-03-09 05:17:45',NULL),(29,1,51.05,1,'payment_verified','upi','verified','2026-03-09 05:20:28','2026-03-14',NULL,'2026-03-09 05:20:28','2026-03-09 05:20:40',NULL),(30,1,51.05,1,'placed','card','pending','2026-03-09 05:21:43','2026-03-14',NULL,'2026-03-09 05:21:43','2026-03-09 05:21:43',NULL),(31,1,51.05,1,'placed','upi','pending','2026-03-09 05:21:54','2026-03-14',NULL,'2026-03-09 05:21:54','2026-03-09 05:21:54',NULL),(32,1,51.05,1,'placed','card','pending','2026-03-09 05:22:21','2026-03-14',NULL,'2026-03-09 05:22:21','2026-03-09 05:22:21',NULL),(33,1,51.05,1,'placed','card','pending','2026-03-09 05:24:02','2026-03-14',NULL,'2026-03-09 05:24:02','2026-03-09 05:24:02',NULL),(34,2,15800.00,2,'placed','upi','pending','2026-03-09 05:34:37','2026-03-14',NULL,'2026-03-09 05:34:37','2026-03-09 05:34:37',NULL),(35,2,52.10,2,'placed','upi','pending','2026-03-09 05:36:54','2026-03-14',NULL,'2026-03-09 05:36:54','2026-03-09 05:36:54',NULL),(36,1,51.05,1,'packed','upi','pending','2026-03-09 05:47:09','2026-03-14',NULL,'2026-03-09 05:47:09','2026-03-09 05:55:04',NULL),(37,1,51.05,1,'placed','upi','pending','2026-03-09 06:23:31','2026-03-14',NULL,'2026-03-09 06:23:31','2026-03-09 06:23:31',NULL),(38,1,51.05,1,'placed','upi','pending','2026-03-09 06:52:21','2026-03-14',NULL,'2026-03-09 06:52:21','2026-03-09 06:52:21',NULL),(39,1,51.05,1,'placed','upi','pending','2026-03-09 06:55:14','2026-03-14',NULL,'2026-03-09 06:55:14','2026-03-09 06:55:14',NULL),(40,1,51.05,1,'placed','card','pending','2026-03-09 06:55:22','2026-03-14',NULL,'2026-03-09 06:55:22','2026-03-09 06:55:22',NULL),(41,1,51.05,1,'placed','upi','pending','2026-03-09 07:03:07','2026-03-14',NULL,'2026-03-09 07:03:07','2026-03-09 07:03:07',NULL),(42,1,51.05,1,'placed','upi','pending','2026-03-09 07:18:42','2026-03-14',NULL,'2026-03-09 07:18:42','2026-03-09 07:18:42',NULL),(43,1,52.10,1,'placed','upi','pending','2026-03-09 07:21:39','2026-03-14',NULL,'2026-03-09 07:21:39','2026-03-09 07:21:39','order_SP2iWp4wFHD7pq'),(44,1,55.25,1,'placed','card','pending','2026-03-09 07:25:00','2026-03-14',NULL,'2026-03-09 07:25:00','2026-03-09 07:25:01','order_SP2m51CwZvdcwh'),(45,1,55.25,1,'payment_verified','upi','verified','2026-03-09 07:32:40','2026-03-14',NULL,'2026-03-09 07:32:40','2026-03-09 07:33:12','order_SP2uAJVSMVW0JB'),(46,1,51.05,1,'payment_verified','upi','verified','2026-03-09 07:34:26','2026-03-14',NULL,'2026-03-09 07:34:26','2026-03-09 07:34:54','order_SP2w2oTRJQhmEB'),(47,1,51.05,1,'placed','upi','pending','2026-03-09 07:44:37','2026-03-14',NULL,'2026-03-09 07:44:37','2026-03-09 07:44:38','order_SP36o31qLAvw2c'),(48,1,51.05,1,'placed','upi','pending','2026-03-09 07:45:53','2026-03-14',NULL,'2026-03-09 07:45:53','2026-03-09 07:46:02','order_SP38H7t9PO73TD'),(49,1,51.05,1,'payment_verified','upi','verified','2026-03-09 07:45:56','2026-03-14',NULL,'2026-03-09 07:45:56','2026-03-09 07:47:54','order_SP38N6iQxYlwZ9'),(50,8,52.10,3,'packed','upi','verified','2026-03-10 04:43:42','2026-03-15',NULL,'2026-03-10 04:43:42','2026-03-10 04:45:24','order_SPOYozgFSA6nrZ');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-10 20:31:49
