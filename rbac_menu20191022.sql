-- MySQL dump 10.13  Distrib 5.7.27, for Linux (x86_64)
--
-- Host: localhost    Database: jumpserver
-- ------------------------------------------------------
-- Server version	5.7.27-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `rbac_menu`
--


LOCK TABLES `rbac_menu` WRITE;
/*!40000 ALTER TABLE `rbac_menu` DISABLE KEYS */;
INSERT INTO `rbac_menu` (`id`,`name`,`icon`,`html_class`,`url`,`parent_id`,`key`,`child_mark`,`assist_url`) VALUES
('165f4ce1e20046ba99e257d4d18546b8','资产列表',NULL,NULL,'/assets/asset/','2f7cda06da5d452bb01e65252013c971','9:0',0,'/assets/nodes/\r\n/assets/assets/'),
('297f7b5b97a94f51a4a08785db99d2d5','系统用户',NULL,NULL,'/assets/system-user/','2f7cda06da5d452bb01e65252013c971','9:3',0,''),
('2f7cda06da5d452bb01e65252013c971','资产管理',NULL,NULL,'#',NULL,'9',6,''),
('3018dee01745447d861f72c42ff87fd8','资产授权',NULL,NULL,'/perms/asset-permission/','b1bd0074b6924baaa2a1542becaa150c','10:0',0,'/assets/nodes/\r\n/assets/assets/\r\n/perms/asset-permissions/'),
('840cc6877f65485abe105ff00f4e2ca2','网域列表',NULL,NULL,'/assets/domain/','2f7cda06da5d452bb01e65252013c971','9:1',0,'/assets/assets/\r\n/assets/nodes/\r\n/assets/gateway/'),
('9e6c796213c54a4c89657f5b447b8848','命令过滤',NULL,NULL,'/assets/cmd-filter/','2f7cda06da5d452bb01e65252013c971','9:5',0,''),
('a4862242ea7b486083726f5accb8d690','管理用户',NULL,NULL,'/assets/admin-user/','2f7cda06da5d452bb01e65252013c971','9:2',0,''),
('b1bd0074b6924baaa2a1542becaa150c','权限管理',NULL,NULL,'#',NULL,'10',1,''),
('d2245c34ee9a4b26a2965891d5d7a2dc','标签管理',NULL,NULL,'/assets/label/','2f7cda06da5d452bb01e65252013c971','9:4',0,'/assets/labels/\r\n/assets/assets/\r\n/assets/nodes/');
/*!40000 ALTER TABLE `rbac_menu` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-10-09  3:49:35
