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
-- Table structure for table `delivery_tracking`
--

DROP TABLE IF EXISTS `delivery_tracking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `delivery_tracking` (
  `tracking_id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `status` enum('processing','packed','shipped','out_for_delivery','delivered','cancelled') NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  `status_update_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `notes` text,
  `updated_by` int DEFAULT NULL,
  PRIMARY KEY (`tracking_id`),
  KEY `order_id` (`order_id`),
  KEY `updated_by` (`updated_by`),
  CONSTRAINT `delivery_tracking_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE,
  CONSTRAINT `delivery_tracking_ibfk_2` FOREIGN KEY (`updated_by`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `delivery_tracking`
--

LOCK TABLES `delivery_tracking` WRITE;
/*!40000 ALTER TABLE `delivery_tracking` DISABLE KEYS */;
INSERT INTO `delivery_tracking` VALUES (1,1,'processing','Order Placed','2026-03-06 08:34:31',NULL,1),(2,1,'processing','Payment Verified','2026-03-06 08:35:20',NULL,1),(3,1,'processing','Order Updated','2026-03-06 09:05:51',NULL,3),(4,1,'shipped','Order Updated','2026-03-06 09:05:57',NULL,3),(5,2,'processing','Order Placed','2026-03-06 09:57:37',NULL,2),(6,2,'processing','Payment Verified','2026-03-06 09:57:46',NULL,2),(7,2,'processing','Order Updated','2026-03-06 09:58:46',NULL,4),(8,2,'delivered','home','2026-03-06 09:59:48','done verywell',5),(9,3,'processing','Order Placed','2026-03-06 16:26:31',NULL,1),(10,4,'processing','Order Placed','2026-03-06 16:31:05',NULL,1),(11,5,'processing','Order Placed','2026-03-06 16:44:43',NULL,1),(12,6,'processing','Order Placed','2026-03-06 16:50:52',NULL,1),(13,7,'processing','Order Placed','2026-03-06 17:17:10',NULL,1),(14,8,'processing','Order Placed','2026-03-06 17:17:14',NULL,1),(15,8,'cancelled','Order Cancelled','2026-03-06 17:36:18','Customer requested cancellation',NULL),(16,18,'cancelled','Order Cancelled','2026-03-06 18:53:35','Customer requested cancellation',NULL),(17,24,'processing','Order Placed','2026-03-07 05:54:18',NULL,1),(18,24,'processing','Order Updated','2026-03-07 06:07:29',NULL,4),(19,24,'shipped','Order Updated','2026-03-07 06:07:34',NULL,4),(20,24,'delivered','Order Updated','2026-03-07 06:07:36',NULL,4),(21,24,'cancelled','Order Updated','2026-03-07 06:07:39',NULL,4),(22,24,'shipped','Order Updated','2026-03-07 06:07:44',NULL,4),(23,6,'processing','Order Updated','2026-03-07 08:41:30',NULL,4),(24,6,'shipped','Order Updated','2026-03-07 08:41:33',NULL,4),(25,6,'delivered','Order Updated','2026-03-07 08:41:35',NULL,4),(26,6,'cancelled','Order Updated','2026-03-07 08:41:37',NULL,4),(27,6,'processing','Order Updated','2026-03-07 08:41:40',NULL,4),(28,24,'processing','Order Updated','2026-03-07 08:49:35',NULL,4),(29,24,'shipped','Order Updated','2026-03-07 08:49:42',NULL,4),(30,24,'delivered','Order Updated','2026-03-07 08:49:47',NULL,4),(31,24,'cancelled','Order Updated','2026-03-07 08:49:49',NULL,4),(32,24,'shipped','Order Updated','2026-03-07 08:50:10',NULL,4),(33,24,'processing','Order Updated','2026-03-07 09:01:56',NULL,4),(34,24,'packed','Order Updated','2026-03-07 09:01:59',NULL,4),(35,24,'shipped','Order Updated','2026-03-07 09:02:02',NULL,4),(36,24,'out_for_delivery','Order Updated','2026-03-07 09:02:05',NULL,4),(37,24,'delivered','Order Updated','2026-03-07 09:02:07',NULL,4),(38,24,'cancelled','Order Updated','2026-03-07 09:02:10',NULL,4),(39,24,'packed','Order Updated','2026-03-07 09:02:13',NULL,4),(40,24,'shipped','Order Updated','2026-03-07 09:03:37',NULL,4),(41,24,'out_for_delivery','Order Updated','2026-03-07 09:03:46',NULL,4),(42,23,'cancelled','Order Updated','2026-03-07 09:04:05',NULL,4),(43,22,'delivered','Order Updated','2026-03-07 09:04:14',NULL,4),(44,21,'shipped','Order Updated','2026-03-07 09:04:24',NULL,4),(45,20,'packed','Order Updated','2026-03-07 09:04:33',NULL,4),(46,19,'processing','Order Updated','2026-03-07 09:04:42',NULL,4),(47,17,'processing','Order Updated','2026-03-07 09:04:57',NULL,4),(48,23,'delivered','Order Updated','2026-03-07 09:11:52',NULL,4),(49,1,'cancelled','Order Cancelled','2026-03-07 09:31:16',NULL,7),(50,2,'cancelled','Order Cancelled','2026-03-07 09:32:04',NULL,7),(51,19,'packed','banglore','2026-03-07 09:54:50','sdfsd',5),(52,19,'shipped','goa','2026-03-07 09:55:02','',5),(53,19,'out_for_delivery','america','2026-03-07 09:55:11','',5),(54,19,'delivered','los angeles','2026-03-07 09:55:24','',5),(55,25,'processing','Order Placed','2026-03-07 09:56:43',NULL,1),(56,25,'cancelled','Order Cancelled','2026-03-07 09:57:03','Customer requested cancellation',NULL),(57,26,'processing','Order Placed','2026-03-07 10:05:00',NULL,1),(58,27,'processing','Order Placed','2026-03-07 10:08:21',NULL,1),(59,27,'processing','Payment Verified','2026-03-07 10:08:26',NULL,1),(60,28,'processing','Order Placed','2026-03-09 05:17:45',NULL,1),(61,29,'processing','Order Placed','2026-03-09 05:20:28',NULL,1),(62,29,'processing','Payment Verified','2026-03-09 05:20:40',NULL,1),(63,30,'processing','Order Placed','2026-03-09 05:21:43',NULL,1),(64,31,'processing','Order Placed','2026-03-09 05:21:54',NULL,1),(65,32,'processing','Order Placed','2026-03-09 05:22:21',NULL,1),(66,33,'processing','Order Placed','2026-03-09 05:24:02',NULL,1),(67,34,'processing','Order Placed','2026-03-09 05:34:37',NULL,2),(68,35,'processing','Order Placed','2026-03-09 05:36:54',NULL,2),(69,36,'processing','Order Placed','2026-03-09 05:47:09',NULL,1),(70,36,'processing','Order Updated','2026-03-09 05:54:59',NULL,3),(71,36,'packed','Order Updated','2026-03-09 05:55:04',NULL,3),(72,37,'processing','Order Placed','2026-03-09 06:23:31',NULL,1),(73,38,'processing','Order Placed','2026-03-09 06:52:21',NULL,1),(74,39,'processing','Order Placed','2026-03-09 06:55:14',NULL,1),(75,40,'processing','Order Placed','2026-03-09 06:55:22',NULL,1),(76,41,'processing','Order Placed','2026-03-09 07:03:07',NULL,1),(77,42,'processing','Order Placed','2026-03-09 07:18:42',NULL,1),(78,43,'processing','Order Placed','2026-03-09 07:21:39',NULL,1),(79,44,'processing','Order Placed','2026-03-09 07:25:00',NULL,1),(80,45,'processing','Order Placed','2026-03-09 07:32:40',NULL,1),(81,45,'processing','Payment Verified','2026-03-09 07:33:12',NULL,1),(82,46,'processing','Order Placed','2026-03-09 07:34:26',NULL,1),(83,46,'processing','Payment Verified','2026-03-09 07:34:54',NULL,1),(84,47,'processing','Order Placed','2026-03-09 07:44:37',NULL,1),(85,48,'processing','Order Placed','2026-03-09 07:45:53',NULL,1),(86,49,'processing','Order Placed','2026-03-09 07:45:56',NULL,1),(87,49,'processing','Payment Verified','2026-03-09 07:47:54',NULL,1),(88,50,'processing','Order Placed','2026-03-10 04:43:42',NULL,8),(89,50,'processing','Payment Verified','2026-03-10 04:44:19',NULL,8),(90,50,'processing','Order Updated','2026-03-10 04:45:20',NULL,4),(91,50,'packed','Order Updated','2026-03-10 04:45:24',NULL,4),(92,50,'shipped','','2026-03-10 04:46:52','',5),(93,50,'out_for_delivery','','2026-03-10 04:46:58','',5);
/*!40000 ALTER TABLE `delivery_tracking` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-10 20:31:51
