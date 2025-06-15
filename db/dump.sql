-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: lojacoverde
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Utilizador',6,'add_utilizador'),(22,'Can change Utilizador',6,'change_utilizador'),(23,'Can delete Utilizador',6,'delete_utilizador'),(24,'Can view Utilizador',6,'view_utilizador'),(25,'Can add Carrinho',7,'add_carrinho'),(26,'Can change Carrinho',7,'change_carrinho'),(27,'Can delete Carrinho',7,'delete_carrinho'),(28,'Can view Carrinho',7,'view_carrinho'),(29,'Can add Categoria',8,'add_categoria'),(30,'Can change Categoria',8,'change_categoria'),(31,'Can delete Categoria',8,'delete_categoria'),(32,'Can view Categoria',8,'view_categoria'),(33,'Can add Encomenda',9,'add_encomenda'),(34,'Can change Encomenda',9,'change_encomenda'),(35,'Can delete Encomenda',9,'delete_encomenda'),(36,'Can view Encomenda',9,'view_encomenda'),(37,'Pode alterar estado da encomenda',9,'mudar_estado_encomenda'),(38,'Can add Pedido',10,'add_pedido'),(39,'Can change Pedido',10,'change_pedido'),(40,'Can delete Pedido',10,'delete_pedido'),(41,'Can view Pedido',10,'view_pedido'),(42,'Can add Produto',11,'add_produto'),(43,'Can change Produto',11,'change_produto'),(44,'Can delete Produto',11,'delete_produto'),(45,'Can view Produto',11,'view_produto'),(46,'Can add Item de Encomenda',12,'add_itemencomenda'),(47,'Can change Item de Encomenda',12,'change_itemencomenda'),(48,'Can delete Item de Encomenda',12,'delete_itemencomenda'),(49,'Can view Item de Encomenda',12,'view_itemencomenda'),(50,'Can add Item no Carrinho',13,'add_itemcarrinho'),(51,'Can change Item no Carrinho',13,'change_itemcarrinho'),(52,'Can delete Item no Carrinho',13,'delete_itemcarrinho'),(53,'Can view Item no Carrinho',13,'view_itemcarrinho'),(54,'Can add Favorito',14,'add_favorito'),(55,'Can change Favorito',14,'change_favorito'),(56,'Can delete Favorito',14,'delete_favorito'),(57,'Can view Favorito',14,'view_favorito'),(58,'Can add contact message',15,'add_contactmessage'),(59,'Can change contact message',15,'change_contactmessage'),(60,'Can delete contact message',15,'delete_contactmessage'),(61,'Can view contact message',15,'view_contactmessage'),(62,'Can add item pedido',16,'add_itempedido'),(63,'Can change item pedido',16,'change_itempedido'),(64,'Can delete item pedido',16,'delete_itempedido'),(65,'Can view item pedido',16,'view_itempedido');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_ecommerce` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_ecommerce` FOREIGN KEY (`user_id`) REFERENCES `ecommerce_coverde_utilizadores` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-06-09 21:04:37.410542','3','Akeellah Antonia Cuambe Guerra (adcgfdddd@gmail.com)',1,'[{\"added\": {}}]',6,2),(2,'2025-06-10 07:45:35.675422','4','Akeellah Antonia Cuambe Guerra (a2023110951@alumni.iscac.pt)',1,'[{\"added\": {}}]',6,2),(3,'2025-06-10 07:46:54.063861','1','Frutas e Vegetais',1,'[{\"added\": {}}]',8,2),(4,'2025-06-10 07:49:12.927545','1','Abacate (Quilograma) - Akeellah Antonia',1,'[{\"added\": {}}]',11,2),(5,'2025-06-10 08:59:33.884072','5','João Martins (joao.martins@email.com)',1,'[{\"added\": {}}]',6,2),(6,'2025-06-10 09:05:30.479334','6','Maria Silva (maria.silva@email.com)',1,'[{\"added\": {}}]',6,2),(7,'2025-06-11 01:11:19.866700','2','coco (Unidade) - João',1,'[{\"added\": {}}]',11,2),(8,'2025-06-11 08:26:05.441906','5','João Martins (joao.martins@email.com)',2,'[{\"changed\": {\"fields\": [\"User permissions\"]}}]',6,2),(9,'2025-06-11 19:25:42.986544','2','Frutas e Vegetais Frescos',1,'[{\"added\": {}}]',8,2),(10,'2025-06-11 19:27:25.543647','3','Vegetais Tradicionais',1,'[{\"added\": {}}]',8,2),(11,'2025-06-11 19:28:32.716004','4','Produtos Biológicos',1,'[{\"added\": {}}]',8,2),(12,'2025-06-11 19:30:17.512631','5','Frutos Secos e Desidratados',1,'[{\"added\": {}}]',8,2),(13,'2025-06-11 19:39:12.518057','3','Couve Tronchuda Portuguesa (Quilograma) - João',1,'[{\"added\": {}}]',11,2),(14,'2025-06-11 19:44:07.193745','4','Maçã Biológica (Caixa) - João',1,'[{\"added\": {}}]',11,2),(15,'2025-06-11 19:47:40.894533','5','Alface Biológica Fresca (Caixa) - João',1,'[{\"added\": {}}]',11,2),(16,'2025-06-11 19:54:29.754549','6','Feijão Manteiga Biológico (Quilograma) - João',1,'[{\"added\": {}}]',11,2),(17,'2025-06-11 19:59:41.173168','7','Pimentão Biológico (Unidade) - João',1,'[{\"added\": {}}]',11,2),(18,'2025-06-11 20:04:56.841979','8','Bananas Biológica (Unidade) - João',1,'[{\"added\": {}}]',11,2),(19,'2025-06-11 20:15:00.837631','9','Cenoura Biológica (Quilograma) - João',1,'[{\"added\": {}}]',11,2),(20,'2025-06-11 20:21:06.871276','10','Caju de Moçambique (Quilograma) - João',1,'[{\"added\": {}}]',11,2),(21,'2025-06-11 20:24:52.418034','11','Caju (Quilograma) - Akeellah Antonia',1,'[{\"added\": {}}]',11,2),(22,'2025-06-11 20:39:51.846830','12','Coco Natural (Unidade) - Akeellah Antonia',1,'[{\"added\": {}}]',11,2),(23,'2025-06-12 07:15:47.159095','6','Maria Silva (maria.silva@email.com)',3,'',6,2),(24,'2025-06-14 23:52:00.858718','1','Carrinho de Bezura vamos',1,'[{\"added\": {}}]',7,2),(25,'2025-06-14 23:52:55.773176','2','Carrinho de Camila Cristina',1,'[{\"added\": {}}]',7,2);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(7,'ecommerce_coverde','carrinho'),(8,'ecommerce_coverde','categoria'),(15,'ecommerce_coverde','contactmessage'),(9,'ecommerce_coverde','encomenda'),(14,'ecommerce_coverde','favorito'),(13,'ecommerce_coverde','itemcarrinho'),(12,'ecommerce_coverde','itemencomenda'),(16,'ecommerce_coverde','itempedido'),(10,'ecommerce_coverde','pedido'),(11,'ecommerce_coverde','produto'),(6,'ecommerce_coverde','utilizador'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-06-09 16:45:32.965802'),(2,'contenttypes','0002_remove_content_type_name','2025-06-09 16:45:33.034565'),(3,'auth','0001_initial','2025-06-09 16:45:33.299527'),(4,'auth','0002_alter_permission_name_max_length','2025-06-09 16:45:33.368738'),(5,'auth','0003_alter_user_email_max_length','2025-06-09 16:45:33.376872'),(6,'auth','0004_alter_user_username_opts','2025-06-09 16:45:33.382736'),(7,'auth','0005_alter_user_last_login_null','2025-06-09 16:45:33.390298'),(8,'auth','0006_require_contenttypes_0002','2025-06-09 16:45:33.392858'),(9,'auth','0007_alter_validators_add_error_messages','2025-06-09 16:45:33.401172'),(10,'auth','0008_alter_user_username_max_length','2025-06-09 16:45:33.407522'),(11,'auth','0009_alter_user_last_name_max_length','2025-06-09 16:45:33.411855'),(12,'auth','0010_alter_group_name_max_length','2025-06-09 16:45:33.427692'),(13,'auth','0011_update_proxy_permissions','2025-06-09 16:45:33.437921'),(14,'auth','0012_alter_user_first_name_max_length','2025-06-09 16:45:33.444207'),(15,'ecommerce_coverde','0001_initial','2025-06-09 16:45:35.292124'),(16,'admin','0001_initial','2025-06-09 16:45:35.440621'),(17,'admin','0002_logentry_remove_auto_add','2025-06-09 16:45:35.449618'),(18,'admin','0003_logentry_add_action_flag_choices','2025-06-09 16:45:35.459307'),(19,'sessions','0001_initial','2025-06-09 16:45:35.499819'),(20,'ecommerce_coverde','0002_produto_data_atualizacao_alter_produto_categoria_and_more','2025-06-09 21:35:52.403865'),(22,'ecommerce_coverde','0004_remove_itemencomenda_encomenda_and_more','2025-06-10 19:15:38.437721'),(23,'ecommerce_coverde','0002_produto_data_atualizacao','2025-06-14 00:53:34.000000'),(24,'ecommerce_coverde','0003_contactmessage','2025-06-14 00:54:09.000000');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('4ceuzc5p2um3kr2ar6obx1qbb6hdhuvf','.eJxVjE0OwiAUhO_C2jRFChR3NvEc5PF-QqO1CVg3xruLSRe6mMXMNzMvFWF75LhVLnEmdVJHdfjNEuCV71_AuC4LF-SI65MLcbez2l0WmG_ntpn29t9FhprbfmCy3kDQYsFbcalP5Lj5waCwAbFNqL0ZCcWNRJ6CaBcogCXpnXp_AKxiOhk:1uQtKL:NOsa27hac9iKcaRe6jYkE1HedyTSMllOM3gOodLfKL0','2025-06-29 19:47:37.482249'),('cobiix9yupmtlykxd9sokiog2zfrqpkt','.eJxVjEsKAjEQRO-StQzGTufjTsFzhE7SIYPGgcRxI97dCLNQqFW9evUSntZH8Wvn5uckjsKK3W8XKF75_gUcl1q5RfZxeXJLPG2sT5dK8-00nPO2_rso1MvwHbkRjdJRjooSBq0PhIgqmZwzABKDTUmyCWgkB7AgM1gHWRHtpXh_AJZtOSY:1uQSIn:odvjg6a-kvFytjMMuQfO0YK6duat2sJnhBCMK-E5khA','2025-06-28 14:56:13.427270');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecommerce_coverde_carrinho`
--

DROP TABLE IF EXISTS `ecommerce_coverde_carrinho`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecommerce_coverde_carrinho` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `atualizado_em` datetime(6) NOT NULL,
  `utilizador_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ecommerce_coverde_carrinho_utilizador_id_4bb865ff_uniq` (`utilizador_id`),
  CONSTRAINT `ecommerce_coverde_ca_utilizador_id_4bb865ff_fk_ecommerce` FOREIGN KEY (`utilizador_id`) REFERENCES `ecommerce_coverde_utilizadores` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecommerce_coverde_carrinho`
--

LOCK TABLES `ecommerce_coverde_carrinho` WRITE;
/*!40000 ALTER TABLE `ecommerce_coverde_carrinho` DISABLE KEYS */;
INSERT INTO `ecommerce_coverde_carrinho` VALUES (1,'2025-06-14 23:52:00.858718',7),(2,'2025-06-14 23:52:55.772179',1);
/*!40000 ALTER TABLE `ecommerce_coverde_carrinho` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecommerce_coverde_categoria`
--

DROP TABLE IF EXISTS `ecommerce_coverde_categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecommerce_coverde_categoria` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) NOT NULL,
  `slug` varchar(60) NOT NULL,
  `descricao` longtext NOT NULL,
  `icone` varchar(30) NOT NULL,
  `ordem_menu` smallint unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nome` (`nome`),
  UNIQUE KEY `slug` (`slug`),
  KEY `categoria_slug_idx` (`slug`),
  KEY `categoria_ordem_idx` (`ordem_menu`),
  CONSTRAINT `ecommerce_coverde_categoria_chk_1` CHECK ((`ordem_menu` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecommerce_coverde_categoria`
--

LOCK TABLES `ecommerce_coverde_categoria` WRITE;
/*!40000 ALTER TABLE `ecommerce_coverde_categoria` DISABLE KEYS */;
INSERT INTO `ecommerce_coverde_categoria` VALUES (1,'Frutas e Vegetais','frutas-e-vegetais','vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv','fa-leaf',0),(2,'Frutas e Vegetais Frescos','frutas-e-vegetais-frescos','Descrição Geral:\r\nNa nossa secção de Frutas e Vegetais, oferecemos os melhores produtos da horta portuguesa, cultivados com técnicas sustentáveis e tradicionais. Desde os campos do Alentejo aos pomares do Ribatejo, cada peça é selecionada para garantir frescura, sabor autêntico e qualidade superior.','fa-leaf',20),(3,'Vegetais Tradicionais','vegetais-tradicionais','Legumes frescos, desde as couves portuguesas aos tomates coração de boi, ideais para sopas, cozidos e grelhados.','fa-leaf',8),(4,'Produtos Biológicos','produtos-biologicos','Cultivados sem pesticidas ou aditivos químicos, respeitando o ritmo da natureza.','fa-leaf',4),(5,'Frutos Secos e Desidratados','frutos-secos-e-desidratados','Nozes, amêndoas e figos secos, perfeitos para snacks saudáveis ou receitas tradicionais.','fa-leaf',5);
/*!40000 ALTER TABLE `ecommerce_coverde_categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecommerce_coverde_contactmessage`
--

DROP TABLE IF EXISTS `ecommerce_coverde_contactmessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecommerce_coverde_contactmessage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `assunto` varchar(200) NOT NULL,
  `mensagem` longtext NOT NULL,
  `data_envio` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecommerce_coverde_contactmessage`
--

LOCK TABLES `ecommerce_coverde_contactmessage` WRITE;
/*!40000 ALTER TABLE `ecommerce_coverde_contactmessage` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecommerce_coverde_contactmessage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecommerce_coverde_favorito`
--

DROP TABLE IF EXISTS `ecommerce_coverde_favorito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecommerce_coverde_favorito` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `criado_em` datetime(6) NOT NULL,
  `utilizador_id` bigint NOT NULL,
  `produto_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ecommerce_coverde_favori_utilizador_id_produto_id_70c1d9dc_uniq` (`utilizador_id`,`produto_id`),
  KEY `ecommerce_coverde_fa_produto_id_ff3552ea_fk_ecommerce` (`produto_id`),
  CONSTRAINT `ecommerce_coverde_fa_produto_id_ff3552ea_fk_ecommerce` FOREIGN KEY (`produto_id`) REFERENCES `ecommerce_coverde_produto` (`id`),
  CONSTRAINT `ecommerce_coverde_fa_utilizador_id_97b880f1_fk_ecommerce` FOREIGN KEY (`utilizador_id`) REFERENCES `ecommerce_coverde_utilizadores` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecommerce_coverde_favorito`
--

LOCK TABLES `ecommerce_coverde_favorito` WRITE;
/*!40000 ALTER TABLE `ecommerce_coverde_favorito` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecommerce_coverde_favorito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecommerce_coverde_itemcarrinho`
--

DROP TABLE IF EXISTS `ecommerce_coverde_itemcarrinho`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecommerce_coverde_itemcarrinho` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantidade` int unsigned NOT NULL,
  `carrinho_id` bigint NOT NULL,
  `produto_id` bigint NOT NULL,
  `preco` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ecommerce_coverde_item_c_carrinho_id_produto_id_bdc61239_uniq` (`carrinho_id`,`produto_id`),
  KEY `ecommerce_coverde_it_produto_id_24b842b4_fk_ecommerce` (`produto_id`),
  CONSTRAINT `ecommerce_coverde_it_carrinho_id_158f2e11_fk_ecommerce` FOREIGN KEY (`carrinho_id`) REFERENCES `ecommerce_coverde_carrinho` (`id`),
  CONSTRAINT `ecommerce_coverde_it_produto_id_24b842b4_fk_ecommerce` FOREIGN KEY (`produto_id`) REFERENCES `ecommerce_coverde_produto` (`id`),
  CONSTRAINT `ecommerce_coverde_itemcarrinho_chk_1` CHECK ((`quantidade` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecommerce_coverde_itemcarrinho`
--

LOCK TABLES `ecommerce_coverde_itemcarrinho` WRITE;
/*!40000 ALTER TABLE `ecommerce_coverde_itemcarrinho` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecommerce_coverde_itemcarrinho` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecommerce_coverde_itempedido`
--

DROP TABLE IF EXISTS `ecommerce_coverde_itempedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecommerce_coverde_itempedido` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantidade` int unsigned NOT NULL,
  `preco` decimal(10,2) NOT NULL,
  `pedido_id` bigint NOT NULL,
  `produto_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ecommerce_coverde_it_pedido_id_3208b8b7_fk_ecommerce` (`pedido_id`),
  KEY `ecommerce_coverde_it_produto_id_d21730e2_fk_ecommerce` (`produto_id`),
  CONSTRAINT `ecommerce_coverde_it_pedido_id_3208b8b7_fk_ecommerce` FOREIGN KEY (`pedido_id`) REFERENCES `ecommerce_coverde_pedido` (`id`),
  CONSTRAINT `ecommerce_coverde_it_produto_id_d21730e2_fk_ecommerce` FOREIGN KEY (`produto_id`) REFERENCES `ecommerce_coverde_produto` (`id`),
  CONSTRAINT `ecommerce_coverde_itempedido_chk_1` CHECK ((`quantidade` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecommerce_coverde_itempedido`
--

LOCK TABLES `ecommerce_coverde_itempedido` WRITE;
/*!40000 ALTER TABLE `ecommerce_coverde_itempedido` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecommerce_coverde_itempedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecommerce_coverde_pedido`
--

DROP TABLE IF EXISTS `ecommerce_coverde_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecommerce_coverde_pedido` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `total` decimal(10,2) NOT NULL,
  `status` varchar(20) NOT NULL,
  `metodo_pagamento` varchar(50) NOT NULL,
  `codigo` char(32) NOT NULL,
  `data_criacao` datetime(6) NOT NULL,
  `endereco_entrega` longtext NOT NULL DEFAULT (_utf8mb4'Desconhecido'),
  `utilizador_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo` (`codigo`),
  KEY `ecommerce_coverde_pe_utilizador_id_b5c18bb0_fk_ecommerce` (`utilizador_id`),
  CONSTRAINT `ecommerce_coverde_pe_utilizador_id_b5c18bb0_fk_ecommerce` FOREIGN KEY (`utilizador_id`) REFERENCES `ecommerce_coverde_utilizadores` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecommerce_coverde_pedido`
--

LOCK TABLES `ecommerce_coverde_pedido` WRITE;
/*!40000 ALTER TABLE `ecommerce_coverde_pedido` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecommerce_coverde_pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecommerce_coverde_produto`
--

DROP TABLE IF EXISTS `ecommerce_coverde_produto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecommerce_coverde_produto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `slug` varchar(120) NOT NULL,
  `descricao` longtext NOT NULL,
  `preco` decimal(10,2) NOT NULL,
  `unidade` varchar(2) NOT NULL,
  `stock` int unsigned NOT NULL,
  `imagem` varchar(100) DEFAULT NULL,
  `data_colheita` date DEFAULT NULL,
  `certificado_biologico` tinyint(1) NOT NULL,
  `disponivel` tinyint(1) NOT NULL,
  `destaque` tinyint(1) NOT NULL,
  `data_criacao` datetime(6) NOT NULL,
  `categoria_id` bigint DEFAULT NULL,
  `produtor_id` bigint NOT NULL,
  `data_atualizacao` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  UNIQUE KEY `unique_produto_slug` (`slug`),
  KEY `ecommerce_c_disponi_375ee7_idx` (`disponivel`,`destaque`),
  KEY `ecommerce_c_categor_5ac4fa_idx` (`categoria_id`,`disponivel`),
  KEY `ecommerce_c_slug_96bf70_idx` (`slug`),
  KEY `ecommerce_coverde_pr_produtor_id_fdd3f461_fk_ecommerce` (`produtor_id`),
  KEY `ecommerce_c_preco_7e3cc0_idx` (`preco`),
  CONSTRAINT `ecommerce_coverde_pr_categoria_id_baacbdea_fk_ecommerce` FOREIGN KEY (`categoria_id`) REFERENCES `ecommerce_coverde_categoria` (`id`),
  CONSTRAINT `ecommerce_coverde_pr_produtor_id_fdd3f461_fk_ecommerce` FOREIGN KEY (`produtor_id`) REFERENCES `ecommerce_coverde_utilizadores` (`id`),
  CONSTRAINT `ecommerce_coverde_produto_chk_1` CHECK ((`stock` >= 0)),
  CONSTRAINT `preco_positivo` CHECK ((`preco` >= 0.01000000000))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecommerce_coverde_produto`
--

LOCK TABLES `ecommerce_coverde_produto` WRITE;
/*!40000 ALTER TABLE `ecommerce_coverde_produto` DISABLE KEYS */;
INSERT INTO `ecommerce_coverde_produto` VALUES (1,'Abacate','abacate','vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',0.29,'kg',13,'produtos/abacate/446999377b9d4b879ac13aba9c3997f5.webp','2025-06-10',1,1,0,'2025-06-10 07:49:12.927545',1,4,'2025-06-10 07:49:12.927545'),(2,'coco','coco','doce e sululento',5.00,'un',26,'','2025-06-11',0,1,0,'2025-06-11 01:11:19.866268',1,5,'2025-06-11 01:11:19.866268'),(3,'Couve Tronchuda Portuguesa','couve-tronchuda-portuguesa','Aspecto: Folhas grandes, verde-escuras e frisadas, com nervura central carnuda e tronco robusto.\r\n\r\nSabor: Mais suave e delicado que outras couves, com ligeiro adocicado.\r\n\r\nTextura: Folhas tenras (quando jovens) e talos crocantes, ideais para cozinhar.',2.00,'kg',12,'produtos/couve-tronchuda-portuguesa/d15de256b1f44b84a46affb39ce2dc71.png','2025-06-11',1,1,0,'2025-06-11 19:39:12.515042',3,5,'2025-06-11 19:39:12.515042'),(4,'Maçã Biológica','maca-biologica','Descubra o verdadeiro sabor da natureza com as nossas maçãs biológicas, cultivadas com dedicação e respeito pela terra por pequenos agricultores locais.\r\nSem pesticidas nem químicos sintéticos, cada maçã é colhida à mão no ponto ideal de maturação, garantindo frescura, sabor autêntico e um valor nutricional superior.\r\n\r\n🌱 Produção biológica certificada\r\n👨‍🌾 Venda direta dos trabalhadores – sem intermediários\r\n📦 Colhidas no dia do envio para máxima frescura\r\n♻️ Sustentável e justa – apoia a agricultura local e o comércio justo',3.00,'cx',7,'produtos/maca-biologica/7ad8b9c4c2bd4702a5c576df713e68bb.jpg','2025-06-11',1,1,0,'2025-06-11 19:44:07.191786',2,5,'2025-06-11 19:44:07.191786'),(5,'Alface Biológica Fresca','alface-biologica-fresca','A nossa alface biológica é cultivada com cuidado em solos saudáveis, sem químicos ou pesticidas, respeitando os ritmos da natureza e os princípios da agricultura sustentável.\r\n\r\nColhida à mão no dia do envio, chega até si fresca, crocante e cheia de sabor. Ideal para saladas leves, sandes ou como base de pratos saudáveis.\r\n\r\n🌿 100% biológica e certificada\r\n👩‍🌾 Produção local e responsável\r\n📦 Colhida por quem a cultiva – sem intermediários\r\n💧 Naturalmente rica em água e fibras',5.00,'cx',12,'produtos/alface-biologica-fresca/f74a159928d04767918e26f88ec6e177.png','2025-06-11',1,1,0,'2025-06-11 19:47:40.894533',4,5,'2025-06-11 19:47:40.894533'),(6,'Feijão Manteiga Biológico','feijao-manteiga-biologico','O nosso feijão manteiga biológico é cultivado com métodos tradicionais e sustentáveis, sem recurso a pesticidas nem fertilizantes químicos. Rico em sabor, textura cremosa e altamente nutritivo, é uma excelente fonte de proteína vegetal e fibras.\r\n\r\n🌱 Produção biológica certificada\r\n👨‍🌾 Colhido e seco por quem o cultiva – venda direta dos trabalhadores\r\n🥣 Ideal para feijoadas, sopas, saladas e pratos tradicionais\r\n♻️ Sustentável, local e justo – apoia a agricultura familiar\r\n\r\nDo campo à sua mesa, com o sabor genuíno da terra e o cuidado de quem a trabalha.',1.50,'kg',20,'produtos/feijao-manteiga-biologico/7d43410d96c74135bbd9a364cbac0d4d.jpg','2025-06-11',1,1,0,'2025-06-11 19:54:29.739236',4,5,'2025-06-11 19:54:29.739236'),(7,'Pimentão Biológico','pimentao-biologico','Os nossos pimentões biológicos são cultivados de forma sustentável, sem químicos nem pesticidas, respeitando o ritmo da natureza e valorizando o trabalho manual dos agricultores.\r\n\r\nDe cores vivas e sabor suave e adocicado, são perfeitos para saladas, assados, refogados e pratos mediterrânicos. Cada pimentão é colhido no ponto certo de maturação, garantindo frescura, textura crocante e valor nutricional.\r\n\r\n🌱 100% biológico e certificado\r\n👩‍🌾 Colhido à mão por quem o cultiva – venda direta dos trabalhadores\r\n🌈 Disponível em vermelho, verde e amarelo (conforme a época)\r\n♻️ Sabor autêntico, produção local e sustentável\r\n\r\nEscolha alimentos com rosto, sabor e respeito pela terra.',2.50,'un',10,'produtos/pimentao-biologico/5046c3dd4903457f99a16755d703788c.png','2025-06-11',1,1,0,'2025-06-11 19:59:41.173168',2,5,'2025-06-11 19:59:41.173168'),(8,'Bananas Biológica','bananas-biologica','As nossas bananas biológicas são cultivadas com práticas sustentáveis, sem recurso a químicos nem pesticidas, respeitando o meio ambiente e o bem-estar de quem as produz.\r\n\r\nCom sabor doce, textura macia e aroma intenso, são ideais para comer ao natural, em batidos, bolos ou sobremesas.\r\n\r\n🌱 Agricultura biológica certificada\r\n👨‍🌾 Colhidas por quem as cultiva – venda direta dos trabalhadores\r\n🍯 Naturalmente doces, sem aditivos nem maturação artificial\r\n🌍 Produção ética, sustentável e de comércio justo\r\n\r\nUma escolha saborosa e consciente – boa para si, boa para o planeta.',3.00,'un',23,'produtos/bananas-biologica/67c041066bb7484fb4fb428c30ee8562.webp','2025-06-11',1,1,0,'2025-06-11 20:04:56.841979',2,5,'2025-06-11 20:04:56.841979'),(9,'Cenoura Biológica','cenoura-biologica','A nossa cenoura biológica é cultivada em solo vivo, sem recurso a químicos ou pesticidas, respeitando os ciclos naturais da terra. Crocante, saborosa e rica em nutrientes, é perfeita para consumir crua, cozinhada ou em sumos.\r\n\r\n🌱 100% biológica e certificada\r\n👩‍🌾 Colhida por quem a cultiva – venda direta dos trabalhadores\r\n🥕 Fonte natural de vitamina A, fibras e antioxidantes\r\n📦 Fresca, saborosa e de origem local\r\n\r\nDo campo à sua mesa com sabor autêntico, cuidado e responsabilidade.',1.00,'kg',15,'produtos/cenoura-biologica/7f6b69a7379c431fae5b253d078b840a.png','2025-06-11',1,1,0,'2025-06-11 20:15:00.833618',4,5,'2025-06-11 20:15:00.833618'),(10,'Caju de Moçambique','caju-de-mocambique','Diretamente de Moçambique, o nosso caju é colhido e processado com cuidado por comunidades locais, em práticas que valorizam o saber tradicional e o comércio justo.\r\n\r\nCom textura crocante e sabor rico, é um snack nutritivo, 100% natural e cheio de personalidade – perfeito para consumir ao natural, em saladas, granolas ou pratos exóticos.\r\n\r\n🌱 Produção artesanal e sustentável\r\n👩‍🌾 Colhido, descascado e embalado localmente – apoio direto aos produtores\r\n🥜 Sem aditivos nem conservantes – puro e biológico\r\n🌍 Origem: Moçambique – comércio justo e impacto social positivo\r\n\r\nAo escolher este caju, está a saborear qualidade e a apoiar o desenvolvimento de comunidades locais.',2.50,'kg',10000,'','2025-06-11',1,1,0,'2025-06-11 20:21:06.869704',5,5,'2025-06-11 20:21:06.869704'),(11,'Caju','caju','',4.00,'kg',30,'produtos/caju/be2073c151fa4afab1aabbfe90352bc4.webp','2025-06-11',0,1,0,'2025-06-11 20:24:52.418034',5,4,'2025-06-11 20:24:52.418034'),(12,'Coco Natural','coco-natural','O nosso coco natural é colhido com cuidado, diretamente por pequenos produtores que respeitam os métodos tradicionais e o equilíbrio da natureza. Com polpa firme e sabor delicadamente adocicado, é ideal para consumir fresco, ralado, em sobremesas, batidos ou receitas exóticas.\r\n\r\n🌴 100% natural, sem aditivos nem conservantes\r\n👨‍🌾 Colhido por quem o cultiva – venda direta dos trabalhadores\r\n💧 Rico em fibras, minerais e gorduras saudáveis\r\n♻️ Produção sustentável e responsável\r\n\r\nUma fruta tropical cheia de benefícios, sabor e compromisso com quem a produz.',1.00,'un',30,'produtos/coco-natural/aee2e93fc17e463589a967dc504a4de7.webp','2025-06-11',1,1,0,'2025-06-11 20:39:51.846830',4,4,'2025-06-11 20:39:51.846830');
/*!40000 ALTER TABLE `ecommerce_coverde_produto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecommerce_coverde_utilizadores`
--

DROP TABLE IF EXISTS `ecommerce_coverde_utilizadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecommerce_coverde_utilizadores` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `tipo` varchar(1) NOT NULL,
  `telefone` varchar(15) DEFAULT NULL,
  `nif` varchar(9) DEFAULT NULL,
  `morada` longtext,
  `codigo_postal` varchar(8) DEFAULT NULL,
  `localidade` varchar(100) DEFAULT NULL,
  `imagem_perfil` varchar(100) DEFAULT NULL,
  `data_registo` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `nif` (`nif`),
  KEY `email_idx` (`email`),
  KEY `tipo_utilizador_idx` (`tipo`),
  KEY `nif_idx` (`nif`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecommerce_coverde_utilizadores`
--

LOCK TABLES `ecommerce_coverde_utilizadores` WRITE;
/*!40000 ALTER TABLE `ecommerce_coverde_utilizadores` DISABLE KEYS */;
INSERT INTO `ecommerce_coverde_utilizadores` VALUES (1,'pbkdf2_sha256$1000000$uhxOR3bdtJ4lHF7fUD6OMk$sHmT6bttoFaXCxjCVq8sLcKqD8cZTxY9N9X/pRi28Io=',NULL,1,'Camila','Cristina',1,1,'2025-06-09 20:48:39.186692','prmonyllo@gmail.com','A',NULL,NULL,NULL,NULL,NULL,'','2025-06-09 20:48:39.546997'),(2,'pbkdf2_sha256$1000000$XPRySlQH2l0R7pFZDEB5Uz$QEqUUy/DHB1TZpEHoznLU7tTqqWDyKlRWYfYM7kjdYc=','2025-06-15 19:45:05.034592',1,'Camila','Cristina',1,1,'2025-06-09 20:59:17.526864','camila.cuambe@ecoplus.co.mz','A','239102421',NULL,NULL,NULL,NULL,'','2025-06-09 20:59:17.878362'),(3,'12345678',NULL,0,'Akeellah Antonia','Cuambe Guerra',0,1,'2025-06-09 21:04:37.403435','adcgfdddd@gmail.com','C',NULL,'233456674','','1234-234','COIMBRA','','2025-06-09 21:04:37.404664'),(4,'12345678',NULL,0,'Akeellah Antonia','Cuambe Guerra',0,1,'2025-06-10 07:45:35.665528','a2023110951@alumni.iscac.pt','P','936274286','233456673','','1234-234','COIMBRA','utilizadores/None/2e93f8f079b14e6c8383161f8ff0bdce.PNG','2025-06-10 07:45:35.671881'),(5,'Abc@1234',NULL,0,'João','Martins',0,1,'2025-06-10 08:59:33.852371','joao.martins@email.com','P','936274286',NULL,'Rua do Mercado, 45','1234-234','coimbra','','2025-06-10 08:59:33.875872'),(7,'pbkdf2_sha256$1000000$PN3Ssc0dm9G5VsqsNxF0fH$vquzjzE4CBpX3+qjzLSMuBshUjmT5O2ldmgs5NLauPY=','2025-06-11 18:13:28.653275',0,'Bezura','vamos',0,1,'2025-06-11 18:13:27.610360','ecopul@gmail.com','C','+35146554323','123456789','dom 12','1234-456','coimbra','','2025-06-11 18:13:28.578841'),(8,'pbkdf2_sha256$1000000$xGvVUWNxRloLuXmlqGiyPE$iliazCZoxh9h0fLCN15xbmD+BtORmM7ysiA9HHu5Y4Y=','2025-06-14 14:56:14.165175',0,'Maria','Silva',0,1,'2025-06-12 07:19:34.953416','maria.silva@email.com','C','+351911234567','234567891','Av. Principal, 89','4000-234','Porto','','2025-06-12 07:19:36.055668');
/*!40000 ALTER TABLE `ecommerce_coverde_utilizadores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecommerce_coverde_utilizadores_groups`
--

DROP TABLE IF EXISTS `ecommerce_coverde_utilizadores_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecommerce_coverde_utilizadores_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `utilizador_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ecommerce_coverde_utiliz_utilizador_id_group_id_dd11ed83_uniq` (`utilizador_id`,`group_id`),
  KEY `ecommerce_coverde_ut_group_id_19ae0b91_fk_auth_grou` (`group_id`),
  CONSTRAINT `ecommerce_coverde_ut_group_id_19ae0b91_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `ecommerce_coverde_ut_utilizador_id_1483f40b_fk_ecommerce` FOREIGN KEY (`utilizador_id`) REFERENCES `ecommerce_coverde_utilizadores` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecommerce_coverde_utilizadores_groups`
--

LOCK TABLES `ecommerce_coverde_utilizadores_groups` WRITE;
/*!40000 ALTER TABLE `ecommerce_coverde_utilizadores_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `ecommerce_coverde_utilizadores_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecommerce_coverde_utilizadores_user_permissions`
--

DROP TABLE IF EXISTS `ecommerce_coverde_utilizadores_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecommerce_coverde_utilizadores_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `utilizador_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ecommerce_coverde_utiliz_utilizador_id_permission_7d67b209_uniq` (`utilizador_id`,`permission_id`),
  KEY `ecommerce_coverde_ut_permission_id_f605d29f_fk_auth_perm` (`permission_id`),
  CONSTRAINT `ecommerce_coverde_ut_permission_id_f605d29f_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `ecommerce_coverde_ut_utilizador_id_330cbf01_fk_ecommerce` FOREIGN KEY (`utilizador_id`) REFERENCES `ecommerce_coverde_utilizadores` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecommerce_coverde_utilizadores_user_permissions`
--

LOCK TABLES `ecommerce_coverde_utilizadores_user_permissions` WRITE;
/*!40000 ALTER TABLE `ecommerce_coverde_utilizadores_user_permissions` DISABLE KEYS */;
INSERT INTO `ecommerce_coverde_utilizadores_user_permissions` VALUES (1,5,1),(37,5,2),(38,5,3),(2,5,4),(39,5,5),(40,5,6),(41,5,7),(42,5,8),(3,5,9),(4,5,10),(5,5,11),(43,5,12),(6,5,13),(7,5,14),(8,5,15),(44,5,16),(45,5,17),(46,5,18),(47,5,19),(9,5,20),(10,5,21),(11,5,22),(12,5,23),(13,5,24),(48,5,25),(49,5,26),(50,5,27),(14,5,28),(15,5,29),(16,5,30),(17,5,31),(18,5,32),(19,5,33),(51,5,34),(52,5,35),(20,5,36),(21,5,37),(53,5,38),(54,5,39),(55,5,40),(22,5,41),(56,5,42),(57,5,43),(58,5,44),(59,5,45),(60,5,46),(61,5,47),(62,5,48),(63,5,49),(64,5,50),(65,5,51),(66,5,52),(23,5,53),(67,5,54),(68,5,55),(69,5,56),(70,5,57),(71,5,58),(72,5,59),(73,5,60),(74,5,61),(75,5,62),(76,5,63),(77,5,64),(78,5,65);
/*!40000 ALTER TABLE `ecommerce_coverde_utilizadores_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-15 22:06:45
