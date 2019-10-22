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
('02616106a26b47e181f82db79d5951e8','采购云主机',NULL,NULL,'/cmis/chost/','4231d7d83245484294bf84507c120c2c','6:1',0,''),
('06640b645d4642bea61be3afaeef411b','批量采购云主机',NULL,NULL,'/cmis/chost/bulk/','4231d7d83245484294bf84507c120c2c','6:2',0,'/cmis/chost/'),
('1017bc94a30a477fb99289d76afa210c','Web终端',NULL,NULL,'/terminal/web-terminal/',NULL,'4',0,'/perms/user/'),
('4231d7d83245484294bf84507c120c2c','云管中心',NULL,NULL,'#',NULL,'6',3,''),
('5818f5b5e18d434d9cae163559ef626a','域名管理',NULL,NULL,'#',NULL,'7',0,''),
('5d4abbbc141d4398961f622983e6a2f7','配置管理',NULL,NULL,'#',NULL,'8',2,''),
('6028eb6fd9f84af4b3c5afa2304d6c42','我的资产',NULL,NULL,'/assets/user-asset/',NULL,'1',0,'/perms/user/\r\n/assets/user-asset/'),
('8534de02217c4861afedb10395e3fe73','WEB配置',NULL,NULL,'/config/web-config/','e304cdb0cca641b782c7c4ffa266cd5b','8:0:0',1,''),
('86c120acc1ca44478558055cbd960a85','应用配置',NULL,NULL,'/config/app/','5d4abbbc141d4398961f622983e6a2f7','8:1',0,''),
('8eb0f529e5cd413ab373c30257bc313b','CDN',NULL,NULL,'/cmis/cdn/','4231d7d83245484294bf84507c120c2c','6:0',1,'/api/cmis/v1/cdn/'),
('974c3dbc476d482494e73882eb594c2b','批量WEB配置',NULL,NULL,'/config/web-config/bulk/','8534de02217c4861afedb10395e3fe73','8:0:0:0',0,''),
('9a571e2221694530b50c7e46ba25a036','CDN刷新',NULL,NULL,'/cmis/cdn/fresh/','8eb0f529e5cd413ab373c30257bc313b','6:0:0',0,'/api/cmis/v1/cdn/fresh/'),
('d38f6c9e862341b090a5bde0a6a4f02b','域名列表',NULL,NULL,'/domain-name/domain-name/','5818f5b5e18d434d9cae163559ef626a','7:0',0,''),
('dc796bade62445aaa94d57e388179dbc','个人信息',NULL,NULL,'/users/profile/',NULL,'3',0,'/users/profile/otp/enable/authentication/\r\n/users/profile/pubkey/generate/'),
('e304cdb0cca641b782c7c4ffa266cd5b','节点配置',NULL,NULL,'/config/node-config/','5d4abbbc141d4398961f622983e6a2f7','8:0',1,''),
('ef1005100d214995ad84c654253081d4','文件管理',NULL,NULL,'/terminal/web-sftp/',NULL,'5',0,'/api/perms/v1/user/nodes-assets/tree/'),
('faecad6273a8418295ed7497056b2194','命令执行',NULL,NULL,'/ops/command-execution/start/',NULL,'2',0,'/api/ops/v1/command-executions/\r\n/perms/user/\r\n/ops/celery/');
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
