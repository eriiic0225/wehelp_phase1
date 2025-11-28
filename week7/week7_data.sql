-- MySQL dump 10.13  Distrib 8.4.7, for macos15 (arm64)
--
-- Host: localhost    Database: website
-- ------------------------------------------------------
-- Server version	8.4.7

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `follower_count` int unsigned NOT NULL DEFAULT '0',
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member`
--

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
INSERT INTO `member` VALUES (1,'test2','test@test.com','test',100,'2025-11-11 13:47:03'),(2,'test2','test2@test.com','test2',80,'2025-11-11 13:48:21'),(3,'test3','test3@test.com','test3',120,'2025-11-11 13:48:21'),(4,'test4','test4@test.com','test4',110,'2025-11-11 13:48:21'),(5,'test5','test5@test.com','test5',90,'2025-11-11 13:48:23'),(10,'try','try@try.com','try',0,'2025-11-19 02:53:36'),(11,'阿寶','finn@gmail.com','finn',0,'2025-11-19 20:39:56'),(12,'老皮','jake@gmail.com','jake',0,'2025-11-19 20:41:23'),(13,'Ryan','Ryan@sushi.com','sushi',0,'2025-11-19 20:43:34'),(14,'BMO','bmo@bmo.com','bmo',0,'2025-11-20 02:18:08'),(15,'hihi','hi@hi.com','hi',0,'2025-11-20 02:22:13'),(16,'Buddy','buddy@gmail.com','buddy',0,'2025-11-20 22:22:32'),(17,'阿寶v2','fff@fff.com','$2b$12$Slxt245vs2UFqW9Ubncb5e6r4mu1gG8h1/7gy9hTRRrzLYfruulrO',0,'2025-11-25 16:11:58'),(18,'老皮v2','jjjj@jjj.com','$2b$12$nlK/sN7mPfCeKSDDdHUExe3j/j.BmtdCiOw.h44QJ2Cz20eQoAla.',0,'2025-11-27 19:43:23'),(19,'BMO v2','bbb@bbb.com','$2b$12$1.ImYIcEx5q4VJBefw9ZquzXX8tB73talVCO2WT5raO3y.9nw93Qm',0,'2025-11-27 21:20:12'),(20,'阿極','ppp@ppp.com','$2b$12$d/L9A0DO2FKNiwlhXvZv0.URE/1GM3S3OMli9tfcsKr0nct0dyVJq',0,'2025-11-27 23:14:22'),(21,'泰瑞','ttt@ttt.com','$2b$12$l7FPnxxsWcDK1t04SyID5u6IQnFEuE3Bb2JYK0pXa6bgvcXqcPvNy',0,'2025-11-27 23:19:36');
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `member_id` int NOT NULL,
  `content` text NOT NULL,
  `like_count` int unsigned NOT NULL DEFAULT '0',
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `message_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
INSERT INTO `message` VALUES (1,1,'hello!',80,'2025-11-11 21:35:44'),(3,3,'Hello World!',120,'2025-11-11 21:36:31'),(5,1,'你好!',110,'2025-11-11 21:37:34'),(6,5,'Bonjour!',100,'2025-11-11 21:38:30'),(7,11,'測試測試',0,'2025-11-20 17:29:10'),(8,11,'新增一筆',0,'2025-11-20 18:24:50'),(9,12,'哈囉阿寶',0,'2025-11-20 18:45:50'),(10,12,'測試again',0,'2025-11-20 18:49:32'),(11,13,'QQ',0,'2025-11-20 19:02:19'),(14,14,'哈囉大家',0,'2025-11-20 22:11:42'),(16,15,'Hihi',0,'2025-11-20 22:19:59'),(18,16,'不知道要說些什麼',0,'2025-11-20 22:23:20');
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `search_history`
--

DROP TABLE IF EXISTS `search_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `search_history` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `executor` int NOT NULL,
  `target` int NOT NULL,
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `executor` (`executor`),
  KEY `idx_target_time` (`target`,`time`),
  CONSTRAINT `search_history_ibfk_1` FOREIGN KEY (`executor`) REFERENCES `member` (`id`),
  CONSTRAINT `search_history_ibfk_2` FOREIGN KEY (`target`) REFERENCES `member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search_history`
--

LOCK TABLES `search_history` WRITE;
/*!40000 ALTER TABLE `search_history` DISABLE KEYS */;
INSERT INTO `search_history` VALUES (6,17,14,'2025-11-26 22:53:14'),(7,17,14,'2025-11-26 22:54:01'),(8,17,14,'2025-11-26 22:55:05'),(9,17,18,'2025-11-27 21:15:22'),(10,18,17,'2025-11-27 21:18:50'),(11,19,17,'2025-11-27 21:20:33'),(12,19,18,'2025-11-27 21:20:37'),(13,19,17,'2025-11-27 23:11:40'),(14,19,18,'2025-11-27 23:11:43'),(15,17,18,'2025-11-27 23:11:57'),(16,17,19,'2025-11-27 23:12:00'),(17,17,18,'2025-11-27 23:12:22'),(18,19,18,'2025-11-27 23:12:24'),(19,17,18,'2025-11-27 23:12:25'),(20,19,18,'2025-11-27 23:12:25'),(21,17,18,'2025-11-27 23:12:27'),(22,19,18,'2025-11-27 23:12:28'),(23,17,18,'2025-11-27 23:12:28'),(24,19,18,'2025-11-27 23:12:30'),(25,18,19,'2025-11-27 23:13:06'),(26,17,19,'2025-11-27 23:13:10'),(27,18,19,'2025-11-27 23:13:11'),(28,17,19,'2025-11-27 23:13:12'),(29,18,19,'2025-11-27 23:13:13'),(30,17,19,'2025-11-27 23:13:14'),(31,18,19,'2025-11-27 23:13:15'),(32,20,17,'2025-11-27 23:14:53'),(33,20,18,'2025-11-27 23:14:58'),(34,20,19,'2025-11-27 23:15:02'),(35,18,20,'2025-11-27 23:15:07'),(36,18,17,'2025-11-27 23:15:28'),(37,20,17,'2025-11-27 23:15:33'),(38,18,17,'2025-11-27 23:15:34'),(39,21,18,'2025-11-27 23:22:02'),(40,21,18,'2025-11-27 23:29:44'),(41,21,18,'2025-11-27 23:30:24'),(42,21,20,'2025-11-27 23:30:37'),(43,21,12,'2025-11-27 23:31:12'),(44,21,12,'2025-11-27 23:36:53');
/*!40000 ALTER TABLE `search_history` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-28 14:43:25
