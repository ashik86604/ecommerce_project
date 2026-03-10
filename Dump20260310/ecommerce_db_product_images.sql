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
-- Table structure for table `product_images`
--

DROP TABLE IF EXISTS `product_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_images` (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `image_url` varchar(255) NOT NULL,
  `is_primary` tinyint(1) DEFAULT '0',
  `uploaded_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`image_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `product_images_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_images`
--

LOCK TABLES `product_images` WRITE;
/*!40000 ALTER TABLE `product_images` DISABLE KEYS */;
INSERT INTO `product_images` VALUES (1,2,'/static/uploads/products/2_1772780249_watch1.jpg',1,'2026-03-06 06:57:29'),(2,2,'/static/uploads/products/2_1772780249_watch2.jpg',0,'2026-03-06 06:57:29'),(3,3,'/static/uploads/products/3_1772814629_watch2.jpg',1,'2026-03-06 16:30:29'),(4,4,'/static/uploads/products/4_1773127421_IMG1.jpg',1,'2026-03-10 07:23:41'),(5,5,'/static/uploads/products/5_1773127544_IMG2.jpg',1,'2026-03-10 07:25:44'),(6,6,'/static/uploads/products/6_1773127649_IMG3.jpg',1,'2026-03-10 07:27:29'),(7,8,'/static/uploads/products/8_1773127850_IMG5.jpg',1,'2026-03-10 07:30:50'),(8,9,'/static/uploads/products/9_1773127948_IMG7.jpg',1,'2026-03-10 07:32:28'),(9,10,'/static/uploads/products/10_1773128142_IMG1.jpg',1,'2026-03-10 07:35:42'),(10,11,'/static/uploads/products/11_1773128207_IMG2.jpg',1,'2026-03-10 07:36:47'),(11,12,'/static/uploads/products/12_1773128270_IMG4.jpg',1,'2026-03-10 07:37:50'),(12,13,'/static/uploads/products/13_1773128323_IMG5.jpg',1,'2026-03-10 07:38:43'),(13,14,'/static/uploads/products/14_1773128423_IMG7.jpg',1,'2026-03-10 07:40:23'),(14,15,'/static/uploads/products/15_1773133180_Cetaphil_Face_Wash_Daily_Facial_Cleanser_for_Sensitive_Combination_to_Oily_Skin_NEW_16_oz_Fragrance_Free_Gentle_Foaming_Soap_Free_Hypoallergenic.jpeg',1,'2026-03-10 08:59:40'),(15,16,'/static/uploads/products/16_1773133266_15_Top_Mac_Lipstick_Shades___Kinda_Soar-Ta.jpeg',1,'2026-03-10 09:01:06'),(16,17,'/static/uploads/products/17_1773133421_Balck_charcoal_mask.jpeg',1,'2026-03-10 09:03:41'),(17,18,'/static/uploads/products/18_1773133481_Clean__Clear_Essentials_Lip_Care_Natural_Rosy_Gloss_Review__Swatches_-_Musings_of_a_Muse.jpeg',1,'2026-03-10 09:04:41'),(18,19,'/static/uploads/products/19_1773133599_Lakme_Eyeconic_Pro_Brush_Black_Matte_Liner_Pencil.jpeg',1,'2026-03-10 09:06:39'),(19,20,'/static/uploads/products/20_1773133677_RENEE_Kohl_Pen_Hard_Black_24Hr_Smudge__Waterproof_Kajal_with_Sharpener.jpeg',1,'2026-03-10 09:07:57'),(20,21,'/static/uploads/products/21_1773134071_1pc_Alloy_Faux_Diamond_Nose_Hoop_Ring_No_Piercing_Nose_Stud_Body_Piercing_Jewelry.jpeg',1,'2026-03-10 09:14:31'),(21,22,'/static/uploads/products/22_1773134131_814abc3f-7c81-4bbd-9c72-fed296a71810.jpg',1,'2026-03-10 09:15:31'),(22,23,'/static/uploads/products/23_1773134177_10378805.png',1,'2026-03-10 09:16:17'),(23,24,'/static/uploads/products/24_1773134235_Brass_Lotus_Flower_Toe_Ring_-_Adjustable_Indian_Foot_Jewelry.jpeg',1,'2026-03-10 09:17:15'),(24,25,'/static/uploads/products/25_1773134284_ce51cfcf-8b2b-4c1f-b7fb-8b84435fb75f.jpg',1,'2026-03-10 09:18:04'),(25,26,'/static/uploads/products/26_1773134347_download_1.jpeg',1,'2026-03-10 09:19:07'),(26,27,'/static/uploads/products/27_1773134496_100_coupon_bundle.jpeg',1,'2026-03-10 09:21:36'),(27,28,'/static/uploads/products/28_1773134632_2017_Fashion_Charm_Jewelry_ring_men_stainless_steel_Black_Rings_For_Women_-_7___Silver.jpeg',0,'2026-03-10 09:23:52'),(28,29,'/static/uploads/products/29_1773134743_BKE_Jute_Slider_Bracelet_-_Mens_Jewelry_in_Tan___Buckle.jpeg',1,'2026-03-10 09:25:43'),(29,30,'/static/uploads/products/30_1773134838_Bracelet_wallpaper.jpeg',1,'2026-03-10 09:27:18'),(30,31,'/static/uploads/products/31_1773135134_Boult_Bluetooth_TWS_Earbuds_with_Deep_Bass_Long_Battery__Fast_Charging_Support_.jpeg',1,'2026-03-10 09:32:14'),(31,32,'/static/uploads/products/32_1773135190_Buds_T110_RMA2306_with_AI_ENC_for_calls_38_hours_of_Playback_and_Deep_Bass.jpeg',1,'2026-03-10 09:33:10'),(32,33,'/static/uploads/products/33_1773135289_Celular_Sm315_Para_idosos_com_teclado_tecla_grande_volume_alto_radio_3g.jpeg',1,'2026-03-10 09:34:49'),(33,34,'/static/uploads/products/34_1773135334_download_1.jpeg',1,'2026-03-10 09:35:34'),(34,35,'/static/uploads/products/35_1773135404_download_2.jpeg',1,'2026-03-10 09:36:44'),(35,36,'/static/uploads/products/36_1773135483_download_3.jpeg',1,'2026-03-10 09:38:03'),(36,37,'/static/uploads/products/37_1773135546_download_4.jpeg',1,'2026-03-10 09:39:06'),(37,38,'/static/uploads/products/38_1773135638_download_5.jpeg',1,'2026-03-10 09:40:38'),(40,41,'/static/uploads/products/41_1773137114_15_Best_Keto_Fruits_That_Wont_Kick_You_Out_Of_Ketosis.jpeg',1,'2026-03-10 10:05:14'),(41,42,'/static/uploads/products/42_1773137168_Apple_Kimchi.jpeg',1,'2026-03-10 10:06:08'),(42,43,'/static/uploads/products/43_1773137244_Burro_Banana___Uber_Eats.jpeg',1,'2026-03-10 10:07:24'),(43,44,'/static/uploads/products/44_1773137324_download_1.jpeg',1,'2026-03-10 10:08:44'),(44,45,'/static/uploads/products/45_1773137390_download_2.jpeg',1,'2026-03-10 10:09:50'),(45,46,'/static/uploads/products/46_1773137500_Bitter_Gourd.jpeg',1,'2026-03-10 10:11:40'),(46,47,'/static/uploads/products/47_1773137590_Bunga_ng_Malunggay.jpeg',1,'2026-03-10 10:13:10'),(47,48,'/static/uploads/products/48_1773137681_download_2.jpeg',1,'2026-03-10 10:14:41'),(50,50,'/static/uploads/products/50_1773137840_download_4.jpeg',1,'2026-03-10 10:17:20'),(51,51,'/static/uploads/products/51_1773137939_download_3.jpeg',1,'2026-03-10 10:18:59'),(52,52,'/static/uploads/products/52_1773138132_IMG1.jpg',1,'2026-03-10 10:22:12'),(53,53,'/static/uploads/products/53_1773138186_IMG2.jpg',1,'2026-03-10 10:23:06'),(54,54,'/static/uploads/products/54_1773138236_IMG3.jpg',1,'2026-03-10 10:23:56'),(55,55,'/static/uploads/products/55_1773138280_IMG4.jpg',1,'2026-03-10 10:24:40'),(56,56,'/static/uploads/products/56_1773138340_IMG7.jpg',1,'2026-03-10 10:25:40'),(57,57,'/static/uploads/products/57_1773138669_IMG1.jpg',1,'2026-03-10 10:31:09'),(58,58,'/static/uploads/products/58_1773138718_IMG2.jpg',1,'2026-03-10 10:31:58'),(59,59,'/static/uploads/products/59_1773138762_IMG3.jpg',1,'2026-03-10 10:32:42'),(60,60,'/static/uploads/products/60_1773138808_IMG4.jpg',1,'2026-03-10 10:33:28');
/*!40000 ALTER TABLE `product_images` ENABLE KEYS */;
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
