-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 01, 2026 at 04:14 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ecommerce_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts_user`
--

CREATE TABLE `accounts_user` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(10) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `shipping_address` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `accounts_user`
--

INSERT INTO `accounts_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `role`, `phone_number`, `shipping_address`) VALUES
(1, 'pbkdf2_sha256$1000000$7ZeNFADMqRtWCMIc7NpUi1$DRY+6iPI2acxUBdV1GY4WMcPP9XGVZtOW+qibf6xlXI=', '2026-09-04 12:40:23.920145', 1, 'Isha', '', '', '', 1, 1, '2026-08-11 11:39:44.635119', 'CUSTOMER', NULL, NULL),
(2, 'pbkdf2_sha256$1000000$kkQgiXCiIekTMIN0lGOlfQ$Pja3YMgs9vugo4zjLhsI5tJTuz2qqww2eXcHEkzEYd8=', '2026-08-20 14:57:29.327649', 0, 'Ishat', '', '', 'isha@gmail.com', 0, 1, '2026-08-19 12:00:45.188327', 'CUSTOMER', '03000000000', ''),
(3, 'pbkdf2_sha256$1000000$STPOnF8mYn48vtHr6TjCSh$fU9WNLAFi2ieNS+4eplhvHJztvV2V+gT5B/ywNvaxKs=', '2026-09-04 09:24:33.816292', 0, 'Ishap', '', '', 'ishh@gmail.com', 0, 1, '2026-08-20 14:45:33.243374', 'CUSTOMER', '03000000001', 'chichawatni'),
(4, 'pbkdf2_sha256$600000$2O1hGj89gGJ3g6JfdeXVup$LAKFDy88xvnqo/F85Vbl2u+Y7HvaLg7sW+R3pFr9+Lk=', '2026-09-04 13:52:02.100753', 1, 'Hassan', '', '', 'H@gmail.com', 1, 1, '2026-09-04 13:48:47.382957', 'CUSTOMER', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `accounts_user_groups`
--

CREATE TABLE `accounts_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `accounts_user_user_permissions`
--

CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add user', 6, 'add_user'),
(22, 'Can change user', 6, 'change_user'),
(23, 'Can delete user', 6, 'delete_user'),
(24, 'Can view user', 6, 'view_user'),
(25, 'Can add category', 7, 'add_category'),
(26, 'Can change category', 7, 'change_category'),
(27, 'Can delete category', 7, 'delete_category'),
(28, 'Can view category', 7, 'view_category'),
(29, 'Can add product', 8, 'add_product'),
(30, 'Can change product', 8, 'change_product'),
(31, 'Can delete product', 8, 'delete_product'),
(32, 'Can view product', 8, 'view_product'),
(33, 'Can add product image', 9, 'add_productimage'),
(34, 'Can change product image', 9, 'change_productimage'),
(35, 'Can delete product image', 9, 'delete_productimage'),
(36, 'Can view product image', 9, 'view_productimage'),
(37, 'Can add order', 10, 'add_order'),
(38, 'Can change order', 10, 'change_order'),
(39, 'Can delete order', 10, 'delete_order'),
(40, 'Can view order', 10, 'view_order'),
(41, 'Can add order item', 11, 'add_orderitem'),
(42, 'Can change order item', 11, 'change_orderitem'),
(43, 'Can delete order item', 11, 'delete_orderitem'),
(44, 'Can view order item', 11, 'view_orderitem'),
(45, 'Can add intent', 12, 'add_intent'),
(46, 'Can change intent', 12, 'change_intent'),
(47, 'Can delete intent', 12, 'delete_intent'),
(48, 'Can view intent', 12, 'view_intent'),
(49, 'Can add search log', 13, 'add_searchlog'),
(50, 'Can change search log', 13, 'change_searchlog'),
(51, 'Can delete search log', 13, 'delete_searchlog'),
(52, 'Can view search log', 13, 'view_searchlog'),
(53, 'Can add product csv import', 14, 'add_productcsvimport'),
(54, 'Can change product csv import', 14, 'change_productcsvimport'),
(55, 'Can delete product csv import', 14, 'delete_productcsvimport'),
(56, 'Can view product csv import', 14, 'view_productcsvimport'),
(57, 'Can add user interaction', 15, 'add_userinteraction'),
(58, 'Can change user interaction', 15, 'change_userinteraction'),
(59, 'Can delete user interaction', 15, 'delete_userinteraction'),
(60, 'Can view user interaction', 15, 'view_userinteraction'),
(61, 'Can add user preference profile', 16, 'add_userpreferenceprofile'),
(62, 'Can change user preference profile', 16, 'change_userpreferenceprofile'),
(63, 'Can delete user preference profile', 16, 'delete_userpreferenceprofile'),
(64, 'Can view user preference profile', 16, 'view_userpreferenceprofile'),
(65, 'Can add cached recommendation', 17, 'add_cachedrecommendation'),
(66, 'Can change cached recommendation', 17, 'change_cachedrecommendation'),
(67, 'Can delete cached recommendation', 17, 'delete_cachedrecommendation'),
(68, 'Can view cached recommendation', 17, 'view_cachedrecommendation');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2026-08-11 12:41:01.520466', '61', 'Dimmable Monitor Light Bar', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}, {\"added\": {\"name\": \"product image\", \"object\": \"Image for Dimmable Monitor Light Bar\"}}, {\"added\": {\"name\": \"product image\", \"object\": \"Image for Dimmable Monitor Light Bar\"}}]', 8, 1),
(2, '2026-08-11 12:42:52.987927', '60', 'Vegan Leather Desk Pad', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}, {\"added\": {\"name\": \"product image\", \"object\": \"Image for Vegan Leather Desk Pad\"}}, {\"added\": {\"name\": \"product image\", \"object\": \"Image for Vegan Leather Desk Pad\"}}]', 8, 1),
(3, '2026-08-11 12:43:13.672229', '61', 'Dimmable Monitor Light Bar', 2, '[]', 8, 1),
(4, '2026-08-12 09:09:45.031803', '1050', 'Smart Health & Sleep Ring', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(5, '2026-08-12 09:11:24.328756', '1066', 'Vegan Leather Desk Pad', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(6, '2026-08-12 09:12:06.724856', '1065', 'HD 1080p Web Camera', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(7, '2026-08-12 09:12:49.505134', '1064', 'Vertical Ergonomic Mouse', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(8, '2026-08-12 09:13:44.959059', '1063', 'Aluminum Laptop Stand', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(9, '2026-08-12 09:14:28.234525', '1062', 'Smart Video Doorbell', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(10, '2026-08-12 09:15:13.964190', '1061', 'Wi-Fi Smart Plug 4-Pack', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(11, '2026-08-12 09:22:21.977803', '1041', 'USB-C Dual Monitor Dock', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(12, '2026-08-12 09:23:08.307257', '1051', 'Heart Rate Chest Strap', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(13, '2026-08-12 09:23:34.482784', '1052', 'GPS Running Companion', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(14, '2026-08-12 09:23:52.837317', '1055', 'Ergonomic Gaming Chair', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(15, '2026-08-12 09:24:08.870433', '1057', 'Speed Cloth XL Desk Mat', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(16, '2026-08-12 09:24:22.786397', '1060', 'Smart LED Light Strip 5M', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(17, '2026-08-12 09:24:35.467844', '1059', 'Voice Assistant Smart Speaker', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(18, '2026-08-12 09:24:48.821918', '1058', 'Smart Outdoor Security Camera', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(19, '2026-08-17 11:55:15.940899', '1', 'product_imports/products.csv', 1, '[{\"added\": {}}]', 14, 1),
(20, '2026-08-17 13:29:45.174552', '1', 'product_imports/products.csv', 3, '', 14, 1),
(21, '2026-08-17 13:30:01.611426', '1070', 'Sony WH-1000XM5', 3, '', 8, 1),
(22, '2026-08-17 13:30:01.611426', '1069', 'HP Pavilion 15', 3, '', 8, 1),
(23, '2026-08-17 13:30:01.611426', '1068', 'Dell Inspiron 15', 3, '', 8, 1),
(24, '2026-08-17 13:30:15.103274', '2', 'product_imports/products_kn3nNAg.csv', 1, '[{\"added\": {}}]', 14, 1),
(25, '2026-08-17 13:40:52.308083', '2', 'product_imports/products_kn3nNAg.csv', 3, '', 14, 1),
(26, '2026-08-17 13:41:06.157788', '1073', 'Sony WH-1000XM5', 3, '', 8, 1),
(27, '2026-08-17 13:41:06.157788', '1072', 'HP Pavilion 15', 3, '', 8, 1),
(28, '2026-08-17 13:41:06.157788', '1071', 'Dell Inspiron 15', 3, '', 8, 1),
(29, '2026-08-17 13:41:20.208713', '71', 'Headphones', 3, '', 7, 1),
(30, '2026-08-17 13:41:20.208713', '70', 'Laptops', 3, '', 7, 1),
(31, '2026-08-17 13:41:31.676600', '3', 'product_imports/products_Og0wGGD.csv', 1, '[{\"added\": {}}]', 14, 1),
(32, '2026-08-17 13:43:15.216790', '73', 'Headphones', 3, '', 7, 1),
(33, '2026-08-17 13:43:15.216790', '72', 'Laptops', 3, '', 7, 1),
(34, '2026-08-17 13:43:27.398914', '3', 'product_imports/products_Og0wGGD.csv', 3, '', 14, 1),
(35, '2026-08-17 13:44:27.820611', '4', 'product_imports/products_0XD3MxX.csv', 1, '[{\"added\": {}}]', 14, 1),
(36, '2026-08-17 13:58:32.221207', '75', 'Headphones', 3, '', 7, 1),
(37, '2026-08-17 13:58:32.222207', '74', 'Laptops', 3, '', 7, 1),
(38, '2026-08-17 13:58:40.418099', '4', 'product_imports/products_0XD3MxX.csv', 3, '', 14, 1),
(39, '2026-08-17 14:01:12.654548', '5', 'product_imports/products_xUMoXWx.csv', 1, '[{\"added\": {}}]', 14, 1),
(40, '2026-08-17 14:10:12.928278', '77', 'Headphones', 3, '', 7, 1),
(41, '2026-08-17 14:10:12.928278', '76', 'Laptops', 3, '', 7, 1),
(42, '2026-08-17 14:10:21.457850', '5', 'product_imports/products_xUMoXWx.csv', 3, '', 14, 1),
(43, '2026-08-17 14:10:29.221460', '6', 'product_imports/products_F8fHk1C.csv', 1, '[{\"added\": {}}]', 14, 1),
(44, '2026-08-20 11:38:35.959043', '7', 'product_imports/test.csv', 1, '[{\"added\": {}}]', 14, 1),
(45, '2026-08-20 14:43:02.307369', '1086', 'Test Wireless Mouse', 3, '', 8, 1),
(46, '2026-08-20 14:58:32.578460', '33', 'Isha -  - None', 3, '', 15, 1),
(47, '2026-08-21 10:50:10.982346', '80', 'Computer Accessories', 3, '', 7, 1),
(48, '2026-08-21 10:51:00.504141', '1039', 'OLED Curved Monitor 34', 2, '[{\"changed\": {\"fields\": [\"Category\"]}}]', 8, 1),
(49, '2026-08-21 10:51:14.548252', '1038', 'UltraBook Pro 15', 2, '[{\"changed\": {\"fields\": [\"Category\"]}}]', 8, 1),
(50, '2026-08-21 10:51:41.725530', '64', 'Electronics', 2, '[{\"changed\": {\"fields\": [\"Name\", \"Slug\", \"Description\"]}}]', 7, 1),
(51, '2026-08-21 10:54:31.800177', '1066', 'Vegan Leather Desk Pad', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(52, '2026-08-21 10:59:19.124158', '1054', '7.1 Surround Gaming Headset', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(53, '2026-08-21 11:00:21.642018', '1053', 'Pro RGB Gaming Mouse', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(54, '2026-08-21 11:01:31.517955', '1043', 'Wireless ANC Headphones', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(55, '2026-08-21 11:02:25.700131', '1067', 'Dimmable Monitor Light Bar', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(56, '2026-08-21 11:03:08.760056', '1056', 'Wireless Gamepad Controller', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(57, '2026-08-21 11:04:09.590525', '1049', 'Fitness Tracker Smart Band', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(58, '2026-08-21 11:04:59.006580', '1048', 'SmartWatch Ultra GPS', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(59, '2026-08-21 11:05:48.238673', '1047', 'Waterproof Outdoor Speaker', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(60, '2026-08-21 11:07:02.163941', '1046', 'USB Condenser Microphone', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(61, '2026-08-21 11:07:53.764439', '1044', 'True Wireless Studio Earbuds', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(62, '2026-08-21 11:09:00.686340', '1045', 'Hi-Fi Desktop Speakers', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(63, '2026-08-21 11:22:33.767194', '1042', 'Mechanical Wireless Keyboard', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(64, '2026-08-21 11:23:24.885765', '1038', 'UltraBook Pro 15', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(65, '2026-08-24 12:57:00.091313', '1087', 'Test Wireless Mouse', 3, '', 8, 1),
(66, '2026-08-24 12:57:12.539448', '7', 'product_imports/test.csv', 3, '', 14, 1),
(67, '2026-08-24 12:57:36.628103', '8', 'product_imports/test_aZXMDUA.csv', 1, '[{\"added\": {}}]', 14, 1),
(68, '2026-08-24 13:05:40.025600', '1088', 'Test Wireless Mouse', 3, '', 8, 1),
(69, '2026-08-24 13:13:20.834858', '8', 'product_imports/test_aZXMDUA.csv', 3, '', 14, 1),
(70, '2026-08-24 13:13:44.044178', '9', 'product_imports/test_VNttdjZ.csv', 1, '[{\"added\": {}}]', 14, 1),
(71, '2026-08-24 13:14:34.860447', '9', 'product_imports/test_VNttdjZ.csv', 3, '', 14, 1),
(72, '2026-08-24 13:14:45.089135', '1089', 'Test Wireless Mouse', 3, '', 8, 1),
(73, '2026-08-24 13:17:40.035250', '10', 'product_imports/test_1BmI48u.csv', 1, '[{\"added\": {}}]', 14, 1),
(74, '2026-08-24 13:18:05.536964', '10', 'product_imports/test_1BmI48u.csv', 3, '', 14, 1),
(75, '2026-08-24 13:18:15.908450', '1090', 'Test Wireless Mouse', 3, '', 8, 1),
(76, '2026-09-02 11:01:14.114400', '20', 'product_imports/django_laptops_only.csv', 1, '[{\"added\": {}}]', 14, 1),
(77, '2026-09-02 11:03:19.834375', '1416', 'Acer EliteBook Ultra Model 20', 3, '', 8, 1),
(78, '2026-09-02 11:03:19.834375', '1415', 'ASUS EliteBook Ultra Model 19', 3, '', 8, 1),
(79, '2026-09-02 11:03:19.834375', '1414', 'Lenovo EliteBook Ultra Model 18', 3, '', 8, 1),
(80, '2026-09-02 11:03:19.834375', '1413', 'Dell EliteBook Ultra Model 17', 3, '', 8, 1),
(81, '2026-09-02 11:03:19.834375', '1412', 'HP EliteBook Ultra Model 16', 3, '', 8, 1),
(82, '2026-09-02 11:03:19.834375', '1411', 'Acer EliteBook Ultra Model 15', 3, '', 8, 1),
(83, '2026-09-02 11:03:19.834375', '1410', 'ASUS EliteBook Ultra Model 14', 3, '', 8, 1),
(84, '2026-09-02 11:03:19.834375', '1409', 'Lenovo EliteBook Ultra Model 13', 3, '', 8, 1),
(85, '2026-09-02 11:03:19.834375', '1408', 'Dell EliteBook Ultra Model 12', 3, '', 8, 1),
(86, '2026-09-02 11:03:19.834375', '1407', 'HP EliteBook Ultra Model 11', 3, '', 8, 1),
(87, '2026-09-02 11:03:19.834375', '1406', 'Acer EliteBook Ultra Model 10', 3, '', 8, 1),
(88, '2026-09-02 11:03:19.834375', '1405', 'ASUS EliteBook Ultra Model 9', 3, '', 8, 1),
(89, '2026-09-02 11:03:19.834375', '1404', 'Lenovo EliteBook Ultra Model 8', 3, '', 8, 1),
(90, '2026-09-02 11:03:19.834375', '1403', 'Dell EliteBook Ultra Model 7', 3, '', 8, 1),
(91, '2026-09-02 11:03:19.834375', '1402', 'HP EliteBook Ultra Model 6', 3, '', 8, 1),
(92, '2026-09-02 11:03:19.834375', '1401', 'Acer EliteBook Ultra Model 5', 3, '', 8, 1),
(93, '2026-09-02 11:03:19.834375', '1400', 'ASUS EliteBook Ultra Model 4', 3, '', 8, 1),
(94, '2026-09-02 11:03:19.834375', '1399', 'Lenovo EliteBook Ultra Model 3', 3, '', 8, 1),
(95, '2026-09-02 11:03:19.834375', '1398', 'Dell EliteBook Ultra Model 2', 3, '', 8, 1),
(96, '2026-09-02 11:03:19.834375', '1397', 'HP EliteBook Ultra Model 1', 3, '', 8, 1),
(97, '2026-09-02 11:12:42.240549', '20', 'product_imports/django_laptops_only.csv', 3, '', 14, 1),
(98, '2026-09-02 11:15:33.007352', '22', 'product_imports/django_laptops_only_ubNJw3m.csv', 1, '[{\"added\": {}}]', 14, 1),
(99, '2026-09-02 11:19:11.040458', '1449', 'Acer EliteBook Ultra Model 20', 3, '', 8, 1),
(100, '2026-09-02 11:19:11.040458', '1448', 'ASUS EliteBook Ultra Model 19', 3, '', 8, 1),
(101, '2026-09-02 11:19:11.040458', '1447', 'Lenovo EliteBook Ultra Model 18', 3, '', 8, 1),
(102, '2026-09-02 11:19:11.040458', '1446', 'Dell EliteBook Ultra Model 17', 3, '', 8, 1),
(103, '2026-09-02 11:19:11.040458', '1445', 'HP EliteBook Ultra Model 16', 3, '', 8, 1),
(104, '2026-09-02 11:19:11.041460', '1444', 'Acer EliteBook Ultra Model 15', 3, '', 8, 1),
(105, '2026-09-02 11:19:11.041460', '1443', 'ASUS EliteBook Ultra Model 14', 3, '', 8, 1),
(106, '2026-09-02 11:19:11.041460', '1442', 'Lenovo EliteBook Ultra Model 13', 3, '', 8, 1),
(107, '2026-09-02 11:19:11.041460', '1441', 'Dell EliteBook Ultra Model 12', 3, '', 8, 1),
(108, '2026-09-02 11:19:11.041460', '1440', 'HP EliteBook Ultra Model 11', 3, '', 8, 1),
(109, '2026-09-02 11:19:11.041460', '1439', 'Acer EliteBook Ultra Model 10', 3, '', 8, 1),
(110, '2026-09-02 11:19:11.041460', '1438', 'ASUS EliteBook Ultra Model 9', 3, '', 8, 1),
(111, '2026-09-02 11:19:11.041460', '1437', 'Lenovo EliteBook Ultra Model 8', 3, '', 8, 1),
(112, '2026-09-02 11:19:11.041460', '1436', 'Dell EliteBook Ultra Model 7', 3, '', 8, 1),
(113, '2026-09-02 11:19:11.041460', '1435', 'HP EliteBook Ultra Model 6', 3, '', 8, 1),
(114, '2026-09-02 11:19:11.041460', '1434', 'Acer EliteBook Ultra Model 5', 3, '', 8, 1),
(115, '2026-09-02 11:19:11.041460', '1433', 'ASUS EliteBook Ultra Model 4', 3, '', 8, 1),
(116, '2026-09-02 11:19:11.041460', '1432', 'Lenovo EliteBook Ultra Model 3', 3, '', 8, 1),
(117, '2026-09-02 11:19:11.041460', '1431', 'Dell EliteBook Ultra Model 2', 3, '', 8, 1),
(118, '2026-09-02 11:19:11.041460', '1430', 'HP EliteBook Ultra Model 1', 3, '', 8, 1),
(119, '2026-09-02 11:19:23.851975', '22', 'product_imports/django_laptops_only_ubNJw3m.csv', 3, '', 14, 1),
(120, '2026-09-02 11:21:37.380189', '23', 'product_imports/django_laptops_only_fLO2YLN.csv', 1, '[{\"added\": {}}]', 14, 1),
(121, '2026-09-02 11:22:26.034139', '1458', 'ASUS EliteBook Ultra Model 9', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(122, '2026-09-02 11:22:36.684739', '1457', 'Lenovo EliteBook Ultra Model 8', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(123, '2026-09-02 11:22:46.052031', '1456', 'Dell EliteBook Ultra Model 7', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(124, '2026-09-02 11:22:56.652416', '1455', 'HP EliteBook Ultra Model 6', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(125, '2026-09-02 11:23:06.686485', '1454', 'Acer EliteBook Ultra Model 5', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(126, '2026-09-02 11:23:16.620173', '1453', 'ASUS EliteBook Ultra Model 4', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(127, '2026-09-02 11:23:32.654784', '1452', 'Lenovo EliteBook Ultra Model 3', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(128, '2026-09-02 11:23:43.421846', '1450', 'HP EliteBook Ultra Model 1', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(129, '2026-09-02 11:30:09.881980', '1063', 'Aluminum  Stand', 2, '[{\"changed\": {\"fields\": [\"Name\", \"Slug\"]}}]', 8, 1),
(130, '2026-09-02 11:32:29.609103', '1043', 'Wireless ANC Headphones', 2, '[{\"changed\": {\"fields\": [\"Category\"]}}]', 8, 1),
(131, '2026-09-02 11:32:42.616441', '1044', 'True Wireless Studio Earbuds', 2, '[{\"changed\": {\"fields\": [\"Category\"]}}]', 8, 1),
(132, '2026-09-02 11:33:40.039063', '65', 'Audio & Speaker', 2, '[{\"changed\": {\"fields\": [\"Name\", \"Slug\", \"Description\"]}}]', 7, 1),
(133, '2026-09-03 13:39:26.616659', '1055', 'Ergonomic Gaming Chair', 2, '[{\"changed\": {\"fields\": [\"Stock count\"]}}]', 8, 1),
(134, '2026-09-04 12:42:37.961603', '1468', 'ASUS EliteBook Ultra Model 19', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(135, '2026-09-04 12:44:34.163142', '1467', 'Lenovo EliteBook Ultra Model 18', 2, '[{\"changed\": {\"fields\": [\"Image\"]}}]', 8, 1),
(136, '2026-09-08 13:30:34.584175', '7', 'Order #7', 3, '', 10, 4),
(137, '2026-09-08 14:31:10.617305', '1468', 'ASUS EliteBook Ultra Model 19', 3, '', 8, 4),
(138, '2026-09-08 14:31:10.620295', '1467', 'Lenovo EliteBook Ultra Model 18', 3, '', 8, 4);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(6, 'accounts', 'user'),
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(12, 'intents', 'intent'),
(10, 'orders', 'order'),
(11, 'orders', 'orderitem'),
(14, 'product_agent', 'productcsvimport'),
(7, 'products', 'category'),
(8, 'products', 'product'),
(9, 'products', 'productimage'),
(17, 'recommendations', 'cachedrecommendation'),
(15, 'recommendations', 'userinteraction'),
(16, 'recommendations', 'userpreferenceprofile'),
(13, 'search', 'searchlog'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-08-10 12:11:54.693072'),
(2, 'contenttypes', '0002_remove_content_type_name', '2026-08-10 12:11:54.799390'),
(3, 'auth', '0001_initial', '2026-08-10 12:11:55.086902'),
(4, 'auth', '0002_alter_permission_name_max_length', '2026-08-10 12:11:55.176712'),
(5, 'auth', '0003_alter_user_email_max_length', '2026-08-10 12:11:55.184305'),
(6, 'auth', '0004_alter_user_username_opts', '2026-08-10 12:11:55.192044'),
(7, 'auth', '0005_alter_user_last_login_null', '2026-08-10 12:11:55.201134'),
(8, 'auth', '0006_require_contenttypes_0002', '2026-08-10 12:11:55.209451'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2026-08-10 12:11:55.220317'),
(10, 'auth', '0008_alter_user_username_max_length', '2026-08-10 12:11:55.231427'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2026-08-10 12:11:55.243420'),
(12, 'auth', '0010_alter_group_name_max_length', '2026-08-10 12:11:55.271701'),
(13, 'auth', '0011_update_proxy_permissions', '2026-08-10 12:11:55.281147'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2026-08-10 12:11:55.297667'),
(15, 'accounts', '0001_initial', '2026-08-10 12:11:55.651804'),
(16, 'admin', '0001_initial', '2026-08-10 12:11:55.822010'),
(17, 'admin', '0002_logentry_remove_auto_add', '2026-08-10 12:11:55.837635'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2026-08-10 12:11:55.845648'),
(19, 'products', '0001_initial', '2026-08-10 12:11:56.047440'),
(20, 'orders', '0001_initial', '2026-08-10 12:11:56.284509'),
(21, 'sessions', '0001_initial', '2026-08-10 12:11:56.327997'),
(22, 'intents', '0001_initial', '2026-08-10 13:54:11.980599'),
(23, 'search', '0001_initial', '2026-08-10 13:54:12.077433'),
(24, 'search', '0002_searchlog_matched_product_and_more', '2026-08-10 13:54:12.167104'),
(25, 'products', '0002_product_sku', '2026-08-17 11:36:21.702517'),
(26, 'product_agent', '0001_initial', '2026-08-17 11:50:01.156404'),
(27, 'recommendations', '0001_initial', '2026-08-19 12:05:36.111153'),
(28, 'recommendations', '0002_userpreferenceprofile', '2026-08-19 13:08:11.969854'),
(29, 'recommendations', '0003_delete_userpreferenceprofile', '2026-08-19 13:10:40.531636'),
(30, 'recommendations', '0004_userpreferenceprofile', '2026-08-19 13:13:41.682112'),
(31, 'recommendations', '0005_cachedrecommendation', '2026-08-19 13:40:33.585141'),
(32, 'products', '0003_product_brand_alter_product_is_active_and_more', '2026-08-21 10:09:36.525682'),
(33, 'orders', '0002_order_estimated_delivery_date', '2026-09-02 12:49:27.037257');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('0yonq20on2505rcgpze3foslw21f1zei', '.eJxVjEEOgyAQRe8y64ZQQEZcdu8ZyMDQYttoAroy3r0lcePqJ_-9vB0ilRWG_biBp23Nfqup-IlhAAWXL1D8pLkBftP8WkRc5rVMQTRFnLSKceH0fZzuJZCp5pZl2WMvpVXaMEql6b-UNJELjjsVCPGOsYvoHKpg2BnrbKeDfmLU1sDxAwVoOjg:1wwgKt:MH6ZJm-JcPIBUJaaxlZmDwx23j74bqewagckiZuUzhY', '2026-09-02 13:28:07.333774'),
('2x3iysnzgxy8m7ovg38jzc188y7hlszv', '.eJxVjrsOgzAUQ__lzijKm4Sxe78B3TxU0lahDWGoEP9eIrEwWfKxbG_gsVQYNmBU2qbfFXNN9QcD6-BTko8wgLTEWtj3DkZc6zSuSyxjCgcRcPEc-lfMDYQn5sdM_JxrSY60CDnpQu5ziO_bmb0UTLhMbVDHKJlSqIMLqNBQqxzlx0ctFOcWBXdGMs96arwPhnHutNDUUOVdxB72P1glRMc:1wx41w:hYCQoIoVaJ98KQNylzYSE4SUiYEO16An-h-AGLCx1Ls', '2026-09-03 14:46:08.661980'),
('636lgiovw5sk8pb3wrudle4wh73jm37q', '.eJxVjEEOgyAQRe_CuiFFmQFcdu8ZCDJDsW0wUVwZ715NXLTb_95_m_BhrdmvC89-JNEJJW6_2xDim8sJ6BXKc5JxKnUeB3kq8qKL7Cfiz-Ny_wI5LPl4B2ssNNS4RNQqk2LLCdEiEvCd0SgARkcIyjqjtY5Dsk4hsFMu2TYe0RjmKrpt378P-jqe:1wzcWz:NTkFTRmxICuymiT4Shw-Ppch3YsWBSSxGgaPb-t4KJY', '2026-09-10 16:00:45.843783'),
('9hozyga7cadieaoqehjp9fyfl7mbv8rr', '.eJxVjDsOgzAQBe-ydWT5j02ZnjOg3bUVSCIjYVMh7p4g0dC-mXk7MK4N-v14wIhbm8at5nWcE_Rg4LYR8ieXE6Q3ltcieCltnUmcirhoFcOS8vd5ubeDCev0r63P2Srn0CdK6DDI6EhqaaM3TuuIRlOwilUnA3MKSmvyxssgHVPGDo4fDZQ6Rw:1wzYGq:uhdN0HLP28Jjh5iDS_ldfi12XwTvnWYjbkZgbsEwhWw', '2026-09-10 11:27:48.666357'),
('all6your1neke56n2hiqd5tgyr2dbd0e', '.eJxVjDsOgzAQBe-ydWT5j02ZnjOg3bUVSCIjYVMh7p4g0dC-mXk7MK4N-v14wIhbm8at5nWcE_Rg4LYR8ieXE6Q3ltcieCltnUmcirhoFcOS8vd5ubeDCev0r63P2Srn0CdK6DDI6EhqaaM3TuuIRlOwilUnA3MKSmvyxssgHVPGDo4fDZQ6Rw:1x1hbm:YgtRMy61CB_jzFIYhhyDlnar_6CjDcS4zXNV9gCwNOI', '2026-09-16 09:50:18.350719'),
('ayv5ei7977id84p14qgpvk7wffa9wth9', '.eJxVjDsOgzAQBe-ydWT5j02ZnjOg3bUVSCIjYVMh7p4g0dC-mXk7MK4N-v14wIhbm8at5nWcE_Rg4LYR8ieXE6Q3ltcieCltnUmcirhoFcOS8vd5ubeDCev0r63P2Srn0CdK6DDI6EhqaaM3TuuIRlOwilUnA3MKSmvyxssgHVPGDo4fDZQ6Rw:1wzXHl:jqNArgDI_iD6nRMKwiGqCOZtZPGV3W6hTlUoJljC3M0', '2026-09-10 10:24:41.464939'),
('bddg43tme3s5wexqzr5ghkznbserzp4o', '.eJxVjDsOgzAQBe-ydWT5j02ZnjOg3bUVSCIjYVMh7p4g0dC-mXk7MK4N-v14wIhbm8at5nWcE_Rg4LYR8ieXE6Q3ltcieCltnUmcirhoFcOS8vd5ubeDCev0r63P2Srn0CdK6DDI6EhqaaM3TuuIRlOwilUnA3MKSmvyxssgHVPGDo4fDZQ6Rw:1x0zmV:aP3yjXBhDfxQ8ZAfs0vhmm28kY6VIiiGx6HTslMz8A0', '2026-09-14 11:02:27.924607'),
('d8bq2wkb2okmabu5dqc15qb6pimwmnrc', '.eJxVjEsOgzAMRO_idRXFhfBbds8ZIsd2Cm0VpAArxN0LEhukWc28Nxsw5QW6bX-Ap3UZ_Dpr9qNAByXcukD81XQO8qH0ngxPacljMCdirnU2_ST6e13s7WCgeTjs6NSVKLbFELGx1krtgojTZyVMTKStLSLyEUEp6spZag-Dy0ANBob9D0IVO-0:1x3xw7:GJKhHAu3qUV8CEAXYRX-iO_XjGh9v_bJYd_Z8CeUEh0', '2026-09-22 15:40:39.338878'),
('df5tzsju0vcqhyn7im1p44qdpe9c992u', '.eJxVjEEOgyAQRe8y64ZQQEZcdu8ZyMDQYttoAroy3r0lcePqJ_-9vB0ilRWG_biBp23Nfqup-IlhAAWXL1D8pLkBftP8WkRc5rVMQTRFnLSKceH0fZzuJZCp5pZl2WMvpVXaMEql6b-UNJELjjsVCPGOsYvoHKpg2BnrbKeDfmLU1sDxAwVoOjg:1wwhTX:KVURlA5HqRgVqYdul7oQwLaXLZr2Viowx8Vi4OaBRU4', '2026-09-02 14:41:07.097490'),
('dzl98vylyrybarlvbyq82xkuvbpqhg3u', '.eJxVj8sKgzAURP_lriXEvG7jsvt-g9w8WtMWbWNcFPHfa8CNq4E5h4FZwVMu0K3QcqNqfhcaSyo_6NoGPjn5CB0ozTiHbWugp6UM_TLH3KewEwGnzpF_xbGC8KTxMTE_jSUnx6rCDjqz2xTi-3q4p4GB5qHOBn7BC-dGSBWQC0l7UpRE1tmghSPEFr32aC0Kp4JVxhotnbyjl_uT7Q8-dUSf:1wx5TI:YTjKrwZwR98wbpbNljirdLr8Ely-WMnzWGvkmdmIVhs', '2026-09-03 16:18:28.205962'),
('ew9v10bj7e87c2jrjrqrbxmnjyb7uuib', '.eJxVjDsOgzAQBe-ydWT5j02ZnjOg3bUVSCIjYVMh7p4g0dC-mXk7MK4N-v14wIhbm8at5nWcE_Rg4LYR8ieXE6Q3ltcieCltnUmcirhoFcOS8vd5ubeDCev0r63P2Srn0CdK6DDI6EhqaaM3TuuIRlOwilUnA3MKSmvyxssgHVPGDo4fDZQ6Rw:1x0y4t:3qwo1wlLamNrFLJUPzCs9fec1uBZq5ko9ZmEuexN2u8', '2026-09-14 09:13:19.024300'),
('fn3jig7qfgzdwbb8e846vg9xa2b2f58n', '.eJxVjDsOgzAQBe-ydWT5j02ZnjOg3bUVSCIjYVMh7p4g0dC-mXk7MK4N-v14wIhbm8at5nWcE_Rg4LYR8ieXE6Q3ltcieCltnUmcirhoFcOS8vd5ubeDCev0r63P2Srn0CdK6DDI6EhqaaM3TuuIRlOwilUnA3MKSmvyxssgHVPGDo4fDZQ6Rw:1x10Ru:TGjchTeqCELjCEr2HYJLr-HU-eNnG9ZPt-2LAe-iMfo', '2026-09-14 11:45:14.265049'),
('fnhlknabcxp463sg3xao6ph5uwqhaehp', '.eJxVjEEOgyAURO_y14YAAoLL7nsG8_mQSttgi7hojHevJm5cTTLvzaxAWCr0Kwhu1ZHfBXNN9Qe9aOBTEkXooXOOOQfb1sCASx2HZY5lSGFHLVw6j_SK-QDhifkxMZpyLcmzQ2Enndl9CvF9O93LwYjzuK-ViVEJrdEEH1Cj5U57LrlyptVSOmylt0qQ6LglClZI6U1ruOWafMQOtj-NeUUC:1x1Of9:o8SdzoAvaHjsRwMlUtrjpH7sw4Fxo1SDIls6n8SewyE', '2026-09-15 13:36:31.365560'),
('fuxvpcduzl9kja9knj6wsmrolk6zo4c0', '.eJxVjDsOgzAQBe-ydWT5j02ZnjOg3bUVSCIjYVMh7p4g0dC-mXk7MK4N-v14wIhbm8at5nWcE_Rg4LYR8ieXE6Q3ltcieCltnUmcirhoFcOS8vd5ubeDCev0r63P2Srn0CdK6DDI6EhqaaM3TuuIRlOwilUnA3MKSmvyxssgHVPGDo4fDZQ6Rw:1x11qy:sKlRJ8igOc4yqdKhY2HQfb8HSIf0wmLbtIwax_cnT2U', '2026-09-14 13:15:12.600624'),
('guj9cyvptje5kunk5fiddplj75lqqs48', 'eyJjYXJ0Ijp7fX0:1x0xt2:kpAJzW5zFyePGRERmew-Zi4k8EtrH96lqwWSWqMRDsQ', '2026-09-14 09:01:04.222330'),
('i1ppryxx6tl9s6vx3rn2yuj1o0jurnn6', '.eJxVjDsOgzAQBe-ydWT5j02ZnjOg3bUVSCIjYVMh7p4g0dC-mXk7MK4N-v14wIhbm8at5nWcE_Rg4LYR8ieXE6Q3ltcieCltnUmcirhoFcOS8vd5ubeDCev0r63P2Srn0CdK6DDI6EhqaaM3TuuIRlOwilUnA3MKSmvyxssgHVPGDo4fDZQ6Rw:1x134G:31zsqaUTqGHFNIFuuJnrDRLpfxJdE98MN0hKbPqD74Y', '2026-09-14 14:33:00.100310'),
('jos7g9m3fi2dqdw7k7tmqhcqmwftxmkw', '.eJxVjDsOgzAQBe-ydWT5j02ZnjOg3bUVSCIjYVMh7p4g0dC-mXk7MK4N-v14wIhbm8at5nWcE_Rg4LYR8ieXE6Q3ltcieCltnUmcirhoFcOS8vd5ubeDCev0r63P2Srn0CdK6DDI6EhqaaM3TuuIRlOwilUnA3MKSmvyxssgHVPGDo4fDZQ6Rw:1x0zx6:CBINe5hlxOSuPkEmU-bkx4XRpb0xaVEgiy1LOfGsp9U', '2026-09-14 11:13:24.044168'),
('k2m89lkfh1dbj7966uey01oompusyuc1', '.eJxVjDsOgzAQBe-ydWT5j02ZnjOg3bUVSCIjYVMh7p4g0dC-mXk7MK4N-v14wIhbm8at5nWcE_Rg4LYR8ieXE6Q3ltcieCltnUmcirhoFcOS8vd5ubeDCev0r63P2Srn0CdK6DDI6EhqaaM3TuuIRlOwilUnA3MKSmvyxssgHVPGDo4fDZQ6Rw:1x1n73:_xi2kjv8yUhjYE664Up8YPdhQiXTH5mL3zMjJp7r_-I', '2026-09-16 15:42:57.660116'),
('kcasnqfwczr2noi9rthmofkbf8evvjfr', '.eJxVjEEOgyAQRe8y64ZQQEZcdu8ZyMDQYttoAroy3r0lcePqJ_-9vB0ilRWG_biBp23Nfqup-IlhAAWXL1D8pLkBftP8WkRc5rVMQTRFnLSKceH0fZzuJZCp5pZl2WMvpVXaMEql6b-UNJELjjsVCPGOsYvoHKpg2BnrbKeDfmLU1sDxAwVoOjg:1wweyM:_xBdI09SuKitXghUY_4A9NMmO3rCOfQx6BzL59NylUI', '2026-09-02 12:00:46.211847'),
('kq053nb5tubu49mkdvpv9qz0tzm2zi18', '.eJxVjDsOgzAQBe-ydWT5j02ZnjOg3bUVSCIjYVMh7p4g0dC-mXk7MK4N-v14wIhbm8at5nWcE_Rg4LYR8ieXE6Q3ltcieCltnUmcirhoFcOS8vd5ubeDCev0r63P2Srn0CdK6DDI6EhqaaM3TuuIRlOwilUnA3MKSmvyxssgHVPGDo4fDZQ6Rw:1x1iUa:km43_RU5CtymoF058KIsCl1Odkis8nYOr_WqCMPeCYo', '2026-09-16 10:46:56.769335'),
('l90rc8nd8vjcvqyaku4trohwi5szhwgi', '.eJxVjEEOgyAQRe8y64YUgQFcdt8zGGSGYttoArgy3r01ceP2v_f-BjGUBv2232AIa8vDWrkME0EPEi7bGOKH5wPQO8yvRcRlbmUaxaGIk1bxXIi_j9O9HORQ878OzjrTUecTkZI2RcUJ0SGS4TujlcYwekIjnbda6zgm5yUa9tInpyLsPx9AOp4:1wyrdt:EIFkT9ur3IAJIN3CRE23oLPRBUu_Av1B9nIXBB2motM', '2026-09-08 13:56:45.722388'),
('m4xyoovc1uqudhuvkjzztx4tojj9vawr', '.eJxVjDsOgzAQBe-ydWT5j02ZnjOg3bUVSCIjYVMh7p4g0dC-mXk7MK4N-v14wIhbm8at5nWcE_Rg4LYR8ieXE6Q3ltcieCltnUmcirhoFcOS8vd5ubeDCev0r63P2Srn0CdK6DDI6EhqaaM3TuuIRlOwilUnA3MKSmvyxssgHVPGDo4fDZQ6Rw:1x11GQ:hUpwCDh3YtFs8HZQlTeidsv3nDqg4pMGhNcHsX6dSPQ', '2026-09-14 12:37:26.891161'),
('mpru9rhxkiykj5nqnj9hfbe5lmjf4kq9', '.eJx1zM0OgjAQBOB32TNpSltal6N3n4Fsf5SqAS3lYAjvLo1cOHiaZObLLOAoZWgXqLmWJd8zDTnmD7R1Ba8UXYAWJDJEWKtNNeqvwp_aWEdz7rt5CqmLflsEHDpL7hGGMvg7DbeRuXHIKVpWCNvXiV1GH57n3R4Oepr6cuv5yZw410Iqb7iQtCUFSYQWfSMsGVMb1ziDaIRVHpVG3Ugrr8ZJrWD9AkyIT2A:1wwgEa:w0WMdt27WKn5bf64-HVvGjoyYZSZhiUgYqKsUP16gZk', '2026-09-02 13:21:36.831740'),
('p08wqpqdobyrtv1mw7f0vkemupxxxhce', '.eJxVjDsOgzAQBe-ydWT5j02ZnjOg3bUVSCIjYVMh7p4g0dC-mXk7MK4N-v14wIhbm8at5nWcE_Rg4LYR8ieXE6Q3ltcieCltnUmcirhoFcOS8vd5ubeDCev0r63P2Srn0CdK6DDI6EhqaaM3TuuIRlOwilUnA3MKSmvyxssgHVPGDo4fDZQ6Rw:1x0xtY:I1J4olHgNzcLgovbSZoT7wbIVQeQm4nJ98OpxPSfh-E', '2026-09-14 09:01:36.902262'),
('q3rzp56z27brjpfjwu4wui8lmqdn5mls', '.eJxVjDsOgzAQBe-ydWT5j02ZnjOg3bUVSCIjYVMh7p4g0dC-mXk7MK4N-v14wIhbm8at5nWcE_Rg4LYR8ieXE6Q3ltcieCltnUmcirhoFcOS8vd5ubeDCev0r63P2Srn0CdK6DDI6EhqaaM3TuuIRlOwilUnA3MKSmvyxssgHVPGDo4fDZQ6Rw:1x1hFd:Sdx41FmUo8dT3MjBqYJ6alGYMSa8JZ5wpimdDQK0vnA', '2026-09-16 09:27:25.151371'),
('qg9wcbcxjwn8blco33w6ytd6hewqoh0l', '.eJxVzM0KgzAMwPF3yVlKW9Paetx9zyDpB7Pb0K3WwxDffTqE4SmQ_y9ZwFMu0C4gUPF9vmcaSiofaGUFr5x8hBYMIrMW1goERzwz8WdC2h_bXEdz6bt5irlLYUs1nHaO_CMOewh3Gm4j8-NQcnJsJ-yoE7uOIT4vhz096Gnqt2vUMaJQinRwgRQZbpXjkqPVtZLSUi2dQeFFw433wQgpna41N1x5F6mB9QvBa0_N:1x1knG:HpcTmVg20inqSW6s7gR6D2ucYy8VGWybE6aYHAS1Z7o', '2026-09-16 13:14:22.497599'),
('syop2n19hh55kj7mka5hzbvydvdo662y', '.eJx1zjsOgzAQBNC7bI0s_7Ep0-cMaP1RcBJBYkwRIe4eLFGEItVKM0-jXcFjLtCtwKiy9b4XHEsqH-hYA6-cfIQOpCXWwtbsSpq_Svwy8Zfxg-2ux6UM_TLH3KdQF-CUOfSPONYi3HG8TcRPY8nJkUrI0c7kOoX4vBz2NDDgPNT3dYySKYU6uIAKDbXKUU6l1UJxblFwZyTzrKXG-2AY504LTQ1V3kVsYfsCcZ1afg:1x1LxR:n9PvDERllROgH6PnNavN27WUO1sZHowMBk2QT-oa9E0', '2026-09-15 10:43:13.155618'),
('tpl2fvuljshk5gkjy8b8t4w4w9a3s66m', '.eJxVjEEOgyAQRe_CuiFFmQFcdu8ZCDJDsW0wUVwZ715NXLTb_95_m_BhrdmvC89-JNEJJW6_2xDim8sJ6BXKc5JxKnUeB3kq8qKL7Cfiz-Ny_wI5LPl4B2ssNNS4RNQqk2LLCdEiEvCd0SgARkcIyjqjtY5Dsk4hsFMu2TYe0RjmKrpt378P-jqe:1x2TDT:TgvtZnQj-AjVHJIJDm5btYjrN6d0Ak_FV8CvDKT-otQ', '2026-09-18 12:40:23.971796'),
('ulk3k4j7n6i7omw1mibankvf5mgotnsd', '.eJxVjDsOgzAQBe-ydWT5j02ZnjOg3bUVSCIjYVMh7p4g0dC-mXk7MK4N-v14wIhbm8at5nWcE_Rg4LYR8ieXE6Q3ltcieCltnUmcirhoFcOS8vd5ubeDCev0r63P2Srn0CdK6DDI6EhqaaM3TuuIRlOwilUnA3MKSmvyxssgHVPGDo4fDZQ6Rw:1x29cD:CO6WusgIkyOHRC3MuZOX5bpq1rHpLGCVUBpUU8pLoO8', '2026-09-17 15:44:37.593545'),
('uumbecl8wzs9urc6iwxd7osf6zne1xxi', '.eJxVjEEOgyAQRe8y64YUgQFcdt8zGGSGYttoArgy3r01ceP2v_f-BjGUBv2232AIa8vDWrkME0EPEi7bGOKH5wPQO8yvRcRlbmUaxaGIk1bxXIi_j9O9HORQ878OzjrTUecTkZI2RcUJ0SGS4TujlcYwekIjnbda6zgm5yUa9tInpyLsPx9AOp4:1x2739:JsXahWleaBz3L-XpEtjSOf1Ac4w4fMbh0aypb4jMw68', '2026-09-17 13:00:15.087205'),
('zicw2j26xh2r18sw6df4tnbespyi83mz', '.eJxVjEEOgyAQRe8y64ZQQEZcdu8ZyMDQYttoAroy3r0lcePqJ_-9vB0ilRWG_biBp23Nfqup-IlhAAWXL1D8pLkBftP8WkRc5rVMQTRFnLSKceH0fZzuJZCp5pZl2WMvpVXaMEql6b-UNJELjjsVCPGOsYvoHKpg2BnrbKeDfmLU1sDxAwVoOjg:1wwzLJ:a9fnhkY5kscvAI_pachrMU75kRgldBhN1bwAm9lKFus', '2026-09-03 09:45:49.289294');

-- --------------------------------------------------------

--
-- Table structure for table `intents_intent`
--

CREATE TABLE `intents_intent` (
  `id` bigint(20) NOT NULL,
  `intent_name` varchar(100) NOT NULL,
  `trigger_phrase` longtext NOT NULL,
  `response` longtext NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `orders_order`
--

CREATE TABLE `orders_order` (
  `id` bigint(20) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(254) NOT NULL,
  `address` varchar(250) NOT NULL,
  `postal_code` varchar(20) NOT NULL,
  `city` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `payment_status` varchar(20) NOT NULL,
  `order_status` varchar(20) NOT NULL,
  `transaction_id` varchar(100) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `estimated_delivery_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `orders_order`
--

INSERT INTO `orders_order` (`id`, `first_name`, `last_name`, `email`, `address`, `postal_code`, `city`, `created_at`, `updated_at`, `total_price`, `payment_status`, `order_status`, `transaction_id`, `user_id`, `estimated_delivery_date`) VALUES
(1, 'Isha', 'Tariq', 'ishatariq777@gmail.com', 'street 5 house no 4 block 10', '40000', 'Sargodha', '2026-08-12 10:26:11.990443', '2026-08-12 10:26:12.004311', 799.50, 'FAILED', 'CANCELLED', 'TXN-A7BB1F1780', 1, NULL),
(6, 'Isha', 'Tariq', 'ishatariq111@gmail.com', 'rdfjg hfg6', '6jgyu6', 'ryjgfd4ej', '2026-09-04 10:16:10.378651', '2026-09-04 10:16:10.411493', 844.99, 'COMPLETED', 'SHIPPED', 'TXN-FD965E333D', 3, '2026-09-09'),
(8, 'Hassan', 'M', 'abc@gmail.com', '##########', '#######', '####', '2026-09-08 13:33:08.098459', '2026-09-08 13:33:08.112449', 59.99, 'FAILED', 'DELIVERED', 'TXN-F34AA08B12', 4, '2026-09-13'),
(9, 'ali', 'h', 'abc@gmail.com', '##########', '$$$$', '$$$$', '2026-09-08 15:40:39.315894', '2026-09-08 15:40:39.332888', 1474.99, 'COMPLETED', 'PROCESSING', 'TXN-8970B2CC33', 4, '2026-09-13');

-- --------------------------------------------------------

--
-- Table structure for table `orders_orderitem`
--

CREATE TABLE `orders_orderitem` (
  `id` bigint(20) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `quantity` int(10) UNSIGNED NOT NULL,
  `order_id` bigint(20) NOT NULL,
  `product_id` bigint(20) NOT NULL
) ;

--
-- Dumping data for table `orders_orderitem`
--

INSERT INTO `orders_orderitem` (`id`, `price`, `quantity`, `order_id`, `product_id`) VALUES
(1, 799.50, 1, 1, 1039),
(6, 844.99, 1, 6, 1450),
(8, 59.99, 1, 8, 1065),
(9, 1474.99, 1, 9, 1464);

-- --------------------------------------------------------

--
-- Table structure for table `products_category`
--

CREATE TABLE `products_category` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `slug` varchar(100) NOT NULL,
  `description` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `products_category`
--

INSERT INTO `products_category` (`id`, `name`, `slug`, `description`) VALUES
(64, 'Electronics', 'electronics', 'High-performance computing hardware.'),
(65, 'Audio & Speaker', 'audio-speaker', 'Studio-grade sound equipment, and speakers.'),
(66, 'Wearables & Fitness', 'wearables-fitness', 'Smartwatches, health trackers, and wearable sensors.'),
(67, 'Gaming Gear', 'gaming-gear', 'Precision controllers, headsets, and gaming peripherals.'),
(68, 'Smart Home', 'smart-home', 'Automation tools, security cameras, and ambient lighting.'),
(69, 'Office & Workspace', 'office-workspace', 'Ergonomic accessories and modern desk setup gear.'),
(78, 'Laptops', 'laptops', ''),
(79, 'Headphones', 'headphones', ''),
(81, 'Computer Accessories', 'computer-accessories', '');

-- --------------------------------------------------------

--
-- Table structure for table `products_product`
--

CREATE TABLE `products_product` (
  `id` bigint(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `slug` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock_count` int(10) UNSIGNED NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `category_id` bigint(20) NOT NULL,
  `sku` varchar(100) DEFAULT NULL,
  `brand` varchar(100) DEFAULT NULL
) ;

--
-- Dumping data for table `products_product`
--

INSERT INTO `products_product` (`id`, `name`, `slug`, `description`, `price`, `stock_count`, `image`, `is_active`, `created_at`, `updated_at`, `category_id`, `sku`, `brand`) VALUES
(1038, 'UltraBook Pro 15', 'ultrabook-pro-15', 'Sleek aluminum laptop with 16GB RAM and M-series performance.', 1299.99, 15, 'products/2026/08/21/ultrabook-pro-15_lQbl19s-removebg-preview.png', 1, '2026-08-11 14:27:09.866610', '2026-08-21 11:23:24.882762', 78, NULL, NULL),
(1039, 'OLED Curved Monitor 34', 'oled-curved-monitor-34', 'Immersive 175Hz curved display for extreme productivity.', 799.50, 7, 'products/2026/08/11/oled-curved-monitor-34_wmPbwS3.jpg', 1, '2026-08-11 14:27:10.876462', '2026-08-21 10:51:00.502127', 78, NULL, NULL),
(1040, 'Portable NVMe SSD 2TB', 'portable-nvme-ssd-2tb', 'Ultra-fast external storage with up to 2000MB/s read speed.', 189.99, 45, 'products/2026/08/11/portable-nvme-ssd-2tb_eHwcREH.jpg', 1, '2026-08-11 14:27:13.427866', '2026-08-11 14:27:14.718181', 64, NULL, NULL),
(1041, 'USB-C Dual Monitor Dock', 'usb-c-dual-monitor-dock', '11-in-1 hub supporting 4K dual displays and 100W passthrough.', 129.00, 20, 'products/2026/08/12/18.jfif', 1, '2026-08-11 14:27:14.727712', '2026-08-12 09:22:21.977803', 64, NULL, NULL),
(1042, 'Mechanical Wireless Keyboard', 'mechanical-wireless-keyboard', 'Tactile hot-swappable mechanical switches with RGB lighting.', 110.00, 30, 'products/2026/08/21/mechanical-wireless-keyboard_kLxy5un-removebg-preview.png', 1, '2026-08-11 14:27:15.947539', '2026-08-21 11:22:33.766127', 64, NULL, NULL),
(1043, 'Wireless ANC Headphones', 'wireless-anc-headphones', 'Active Noise Cancellation with 40-hour battery life.', 249.99, 25, 'products/2026/08/21/wireless-anc-headphones_ZFqTAyJ-removebg-preview.png', 1, '2026-08-11 14:27:17.045006', '2026-09-02 11:32:29.607106', 79, NULL, NULL),
(1044, 'True Wireless Studio Earbuds', 'true-wireless-studio-earbuds', 'Water-resistant fit with deep bass and clear microphone.', 129.99, 50, 'products/2026/08/21/true-wireless-studio-earbuds_euwGrml-removebg-preview.png', 1, '2026-08-11 14:27:18.202213', '2026-09-02 11:32:42.616441', 79, NULL, NULL),
(1045, 'Hi-Fi Desktop Speakers', 'hi-fi-desktop-speakers', 'Wooden enclosure bookshelf speakers with Bluetooth 5.0.', 199.00, 12, 'products/2026/08/21/hi-fi-desktop-speakers_t4tGlZg-removebg-preview.png', 1, '2026-08-11 14:27:19.264366', '2026-08-21 11:09:00.686340', 65, NULL, NULL),
(1046, 'USB Condenser Microphone', 'usb-condenser-microphone', 'Cardioid pickup pattern for streaming, podcasts, and calls.', 89.95, 18, 'products/2026/08/21/usb-condenser-microphone_EUTJkmu-removebg-preview.png', 1, '2026-08-11 14:27:20.367652', '2026-08-21 11:07:02.163941', 65, NULL, NULL),
(1047, 'Waterproof Outdoor Speaker', 'waterproof-outdoor-speaker', 'IPX7 rated rugged portable speaker with 12-hour playtime.', 69.99, 40, 'products/2026/08/21/waterproof-outdoor-speaker_V4yVBnv-removebg-preview.png', 1, '2026-08-11 14:27:21.547654', '2026-08-21 11:05:48.222289', 65, NULL, NULL),
(1048, 'SmartWatch Ultra GPS', 'smartwatch-ultra-gps', 'Titanium case with heart rate sensor and multi-sport tracking.', 349.99, 10, 'products/2026/08/21/smartwatch-ultra-gps_UWziYJs-removebg-preview.png', 1, '2026-08-11 14:27:22.652795', '2026-08-21 11:04:58.989813', 66, NULL, NULL),
(1049, 'Fitness Tracker Smart Band', 'fitness-tracker-smart-band', 'Lightweight OLED band tracking sleep, steps, and SpO2.', 49.99, 60, 'products/2026/08/21/fitness-tracker-smart-band_Cqw7bh2-removebg-preview.png', 1, '2026-08-11 14:27:23.501104', '2026-08-21 11:04:09.590525', 66, NULL, NULL),
(1050, 'Smart Health & Sleep Ring', 'smart-health-sleep-ring', 'Discreet ceramic ring providing round-the-clock biometrics.', 299.00, 14, 'products/2026/08/12/3.jpg', 1, '2026-08-11 14:27:24.520826', '2026-08-12 09:09:45.031803', 66, NULL, NULL),
(1051, 'Heart Rate Chest Strap', 'heart-rate-chest-strap', 'ANT+ and Bluetooth dual-band precision workout sensor.', 59.99, 22, 'products/2026/08/12/16.jpg', 1, '2026-08-11 14:27:25.654798', '2026-08-12 09:23:08.307257', 66, NULL, NULL),
(1052, 'GPS Running Companion', 'gps-running-companion', 'Dedicated fitness watch with offline map routing.', 179.50, 19, 'products/2026/08/12/15.jpg', 1, '2026-08-11 14:27:26.748668', '2026-08-12 09:23:34.482784', 66, NULL, NULL),
(1053, 'Pro RGB Gaming Mouse', 'pro-rgb-gaming-mouse', '26k DPI optical sensor with sub-60g ultra-light design.', 79.99, 35, 'products/2026/08/21/pro-rgb-gaming-mouse_cYlR7HU-removebg-preview.png', 1, '2026-08-11 14:27:27.775264', '2026-08-21 11:00:21.640019', 67, NULL, NULL),
(1054, '7.1 Surround Gaming Headset', '71-surround-gaming-headset', 'Detachable noise-canceling mic with memory foam pads.', 99.99, 28, 'products/2026/08/21/71-surround-gaming-headset_cZZKRBi-removebg-preview.png', 1, '2026-08-11 14:27:28.755111', '2026-08-21 10:59:19.121159', 67, NULL, NULL),
(1055, 'Ergonomic Gaming Chair', 'ergonomic-gaming-chair', 'High-density foam with 4D armrests and lumbar support.', 289.00, 2, 'products/2026/08/12/14.jfif', 1, '2026-08-11 14:27:29.772080', '2026-09-03 13:39:26.614657', 67, NULL, NULL),
(1056, 'Wireless Gamepad Controller', 'wireless-gamepad-controller', 'Low latency wireless controller compatible with PC and Mobile.', 64.99, 40, 'products/2026/08/21/wireless-gamepad-controller_Dwcxzr3-removebg-preview.png', 1, '2026-08-11 14:27:30.949447', '2026-08-21 11:03:08.758011', 67, NULL, NULL),
(1057, 'Speed Cloth XL Desk Mat', 'speed-cloth-xl-desk-mat', 'Stitching-reinforced oversized mousepad surface.', 29.99, 100, 'products/2026/08/12/13.jfif', 1, '2026-08-11 14:27:32.070077', '2026-08-12 09:24:08.868433', 67, NULL, NULL),
(1058, 'Smart Outdoor Security Camera', 'smart-outdoor-security-camera', '2K color night vision camera with motion spotlight.', 119.99, 16, 'products/2026/08/12/12.jfif', 1, '2026-08-11 14:27:33.259326', '2026-08-12 09:24:48.821918', 68, NULL, NULL),
(1059, 'Voice Assistant Smart Speaker', 'voice-assistant-smart-speaker', 'Compact smart speaker with integrated home hub capabilities.', 49.99, 45, 'products/2026/08/12/11.jfif', 1, '2026-08-11 14:27:34.362562', '2026-08-12 09:24:35.451457', 68, NULL, NULL),
(1060, 'Smart LED Light Strip 5M', 'smart-led-light-strip-5m', 'Wi-Fi app controlled addressable RGB color modes.', 34.99, 50, 'products/2026/08/12/10.jpg', 1, '2026-08-11 14:27:35.508813', '2026-08-12 09:24:22.785184', 68, NULL, NULL),
(1061, 'Wi-Fi Smart Plug 4-Pack', 'wi-fi-smart-plug-4-pack', 'Schedule energy usage and turn off appliances remotely.', 29.99, 70, 'products/2026/08/12/9.jpg', 1, '2026-08-11 14:27:36.780965', '2026-08-12 09:15:13.964190', 68, NULL, NULL),
(1062, 'Smart Video Doorbell', 'smart-video-doorbell', 'Two-way audio chime with instant phone alerts.', 139.00, 11, 'products/2026/08/12/8.jpg', 1, '2026-08-11 14:27:37.750792', '2026-09-03 15:44:58.332384', 68, NULL, NULL),
(1063, 'Aluminum  Stand', 'aluminum-stand', 'Vented heat-dissipating riser for improved posture.', 39.99, 30, 'products/2026/08/12/7.jpg', 1, '2026-08-11 14:27:38.867268', '2026-09-02 11:30:09.881980', 69, NULL, NULL),
(1064, 'Vertical Ergonomic Mouse', 'vertical-ergonomic-mouse', 'Reduces wrist strain with natural handshake posture.', 45.00, 22, 'products/2026/08/12/6.jpg', 1, '2026-08-11 14:27:40.167449', '2026-08-12 09:12:49.502135', 69, NULL, NULL),
(1065, 'HD 1080p Web Camera', 'hd-1080p-web-camera', 'Auto-focus lens with dual privacy shutter microphones.', 59.99, 26, 'products/2026/08/12/5.jpg', 1, '2026-08-11 14:27:41.160918', '2026-09-08 13:33:08.108452', 69, NULL, NULL),
(1066, 'Vegan Leather Desk Pad', 'vegan-leather-desk-pad', 'Waterproof desk mat providing smooth cursor movement.', 24.99, 80, 'products/2026/08/21/test.jpg-removebg-preview.png', 1, '2026-08-11 14:27:42.459505', '2026-08-21 10:54:31.798178', 69, NULL, NULL),
(1067, 'Dimmable Monitor Light Bar', 'dimmable-monitor-light-bar', 'Space-saving screen glare reduction desk lamp.', 49.90, 18, 'products/2026/08/21/dimmable-monitor-light-bar_aG5SoLq-removebg-preview.png', 1, '2026-08-11 14:27:43.648827', '2026-08-21 11:02:25.699132', 69, NULL, NULL),
(1083, 'Dell Inspiron 15', 'dell-inspiron-15', 'Dell laptop', 899.99, 10, 'products/2026/08/17/LAP-001.png', 1, '2026-08-17 14:10:34.622892', '2026-08-17 14:10:36.665116', 78, 'LAP-001', NULL),
(1084, 'HP Pavilion 15', 'hp-pavilion-15', 'HP laptop', 799.99, 15, 'products/2026/08/17/LAP-002.png', 1, '2026-08-17 14:10:36.673112', '2026-09-03 15:44:09.237303', 78, 'LAP-002', NULL),
(1085, 'Sony WH-1000XM5', 'sony-wh-1000xm5', 'Wireless headphones', 349.99, 8, 'products/2026/08/17/HEAD-001_DFyX5NB.png', 1, '2026-08-17 14:10:39.289155', '2026-08-17 14:10:42.292735', 79, 'HEAD-001', NULL),
(1450, 'HP EliteBook Ultra Model 1', 'hp-elitebook-ultra-model-1', 'Processor: Intel Core i5-13420HRAM: 16GB DDR5Storage: 512GB NVMe SSDDisplay: 15.6-inch Full HD IPS, 144HzGraphics: NVIDIA GeForce RTX 4050 6GBOperating System: Windows 11 HomeBattery: 4-cell lithium-ion (up to 10 hours battery life)Connectivity: Wi-Fi 6E, Bluetooth 5.3, Thunderbolt 4, USB-C, HDMI 2.1Engineered by HP, this professional-grade laptop delivers supreme processing power, stunning visual fidelity, and robust build quality for power users and creators.', 844.99, 45, 'products/2026/09/02/images_zB7U5xj.jfif', 1, '2026-09-02 11:19:30.140555', '2026-09-04 10:16:10.395475', 78, 'LAP-SKU-2001', NULL),
(1451, 'Dell EliteBook Ultra Model 2', 'dell-elitebook-ultra-model-2', 'Processor: Intel Core i7-13700HRAM: 32GB DDR5Storage: 1TB NVMe SSDDisplay: 16-inch WQXGA IPS, 165HzGraphics: NVIDIA GeForce RTX 4060 8GBOperating System: Windows 11 HomeBattery: 4-cell lithium-ion (up to 10 hours battery life)Connectivity: Wi-Fi 6E, Bluetooth 5.3, Thunderbolt 4, USB-C, HDMI 2.1Engineered by Dell, this professional-grade laptop delivers supreme processing power, stunning visual fidelity, and robust build quality for power users and creators.', 889.99, 45, 'products/2026/09/02/LAP-SKU-2002_orYE9Gs.png', 1, '2026-09-02 11:19:41.218478', '2026-09-02 11:19:53.858128', 78, 'LAP-SKU-2002', NULL),
(1452, 'Lenovo EliteBook Ultra Model 3', 'lenovo-elitebook-ultra-model-3', 'Processor: AMD Ryzen 7 7840HSRAM: 8GB DDR5Storage: 2TB NVMe SSDDisplay: 14-inch OLED 90HzGraphics: NVIDIA GeForce RTX 4070 8GBOperating System: Windows 11 HomeBattery: 4-cell lithium-ion (up to 10 hours battery life)Connectivity: Wi-Fi 6E, Bluetooth 5.3, Thunderbolt 4, USB-C, HDMI 2.1Engineered by Lenovo, this professional-grade laptop delivers supreme processing power, stunning visual fidelity, and robust build quality for power users and creators.', 934.99, 61, 'products/2026/09/02/images_YzBImgA.jfif', 1, '2026-09-02 11:19:53.863968', '2026-09-02 11:23:32.637828', 78, 'LAP-SKU-2003', NULL),
(1453, 'ASUS EliteBook Ultra Model 4', 'asus-elitebook-ultra-model-4', 'Processor: AMD Ryzen 5 7640HSRAM: 16GB DDR5Storage: 512GB NVMe SSDDisplay: 17.3-inch Full HD 240HzGraphics: Intel Iris Xe GraphicsOperating System: Windows 11 HomeBattery: 4-cell lithium-ion (up to 10 hours battery life)Connectivity: Wi-Fi 6E, Bluetooth 5.3, Thunderbolt 4, USB-C, HDMI 2.1Engineered by ASUS, this professional-grade laptop delivers supreme processing power, stunning visual fidelity, and robust build quality for power users and creators.', 979.99, 49, 'products/2026/09/02/images_NCFQGPN.jfif', 1, '2026-09-02 11:20:04.958946', '2026-09-02 11:23:16.620173', 78, 'LAP-SKU-2004', NULL),
(1454, 'Acer EliteBook Ultra Model 5', 'acer-elitebook-ultra-model-5', 'Processor: Intel Core i9-13900HRAM: 32GB DDR5Storage: 1TB NVMe SSDDisplay: 15.6-inch Full HD IPS, 144HzGraphics: NVIDIA GeForce RTX 4050 6GBOperating System: Windows 11 HomeBattery: 4-cell lithium-ion (up to 10 hours battery life)Connectivity: Wi-Fi 6E, Bluetooth 5.3, Thunderbolt 4, USB-C, HDMI 2.1Engineered by Acer, this professional-grade laptop delivers supreme processing power, stunning visual fidelity, and robust build quality for power users and creators.', 1024.99, 64, 'products/2026/09/02/images_n8qbOGl.jfif', 1, '2026-09-02 11:20:16.033765', '2026-09-02 11:23:06.686485', 78, 'LAP-SKU-2005', NULL),
(1455, 'HP EliteBook Ultra Model 6', 'hp-elitebook-ultra-model-6', 'Processor: Intel Core i5-13420HRAM: 8GB DDR5Storage: 2TB NVMe SSDDisplay: 16-inch WQXGA IPS, 165HzGraphics: NVIDIA GeForce RTX 4060 8GBOperating System: Windows 11 HomeBattery: 4-cell lithium-ion (up to 10 hours battery life)Connectivity: Wi-Fi 6E, Bluetooth 5.3, Thunderbolt 4, USB-C, HDMI 2.1Engineered by HP, this professional-grade laptop delivers supreme processing power, stunning visual fidelity, and robust build quality for power users and creators.', 1069.99, 54, 'products/2026/09/02/images_gH8Zdiu.jfif', 1, '2026-09-02 11:20:27.107088', '2026-09-02 11:22:56.652416', 78, 'LAP-SKU-2006', NULL),
(1456, 'Dell EliteBook Ultra Model 7', 'dell-elitebook-ultra-model-7', 'Processor: Intel Core i7-13700HRAM: 16GB DDR5Storage: 512GB NVMe SSDDisplay: 14-inch OLED 90HzGraphics: NVIDIA GeForce RTX 4070 8GBOperating System: Windows 11 HomeBattery: 4-cell lithium-ion (up to 10 hours battery life)Connectivity: Wi-Fi 6E, Bluetooth 5.3, Thunderbolt 4, USB-C, HDMI 2.1Engineered by Dell, this professional-grade laptop delivers supreme processing power, stunning visual fidelity, and robust build quality for power users and creators.', 1114.99, 61, 'products/2026/09/02/images_aAmYjCg.jfif', 1, '2026-09-02 11:20:38.193785', '2026-09-02 11:22:46.052031', 78, 'LAP-SKU-2007', NULL),
(1457, 'Lenovo EliteBook Ultra Model 8', 'lenovo-elitebook-ultra-model-8', 'Processor: AMD Ryzen 7 7840HSRAM: 32GB DDR5Storage: 1TB NVMe SSDDisplay: 17.3-inch Full HD 240HzGraphics: Intel Iris Xe GraphicsOperating System: Windows 11 HomeBattery: 4-cell lithium-ion (up to 10 hours battery life)Connectivity: Wi-Fi 6E, Bluetooth 5.3, Thunderbolt 4, USB-C, HDMI 2.1Engineered by Lenovo, this professional-grade laptop delivers supreme processing power, stunning visual fidelity, and robust build quality for power users and creators.', 1159.99, 39, 'products/2026/09/02/images_ksIdOv7.jfif', 1, '2026-09-02 11:20:49.261594', '2026-09-02 11:22:36.684739', 78, 'LAP-SKU-2008', NULL),
(1458, 'ASUS EliteBook Ultra Model 9', 'asus-elitebook-ultra-model-9', 'Processor: AMD Ryzen 5 7640HSRAM: 8GB DDR5Storage: 2TB NVMe SSDDisplay: 15.6-inch Full HD IPS, 144HzGraphics: NVIDIA GeForce RTX 4050 6GBOperating System: Windows 11 HomeBattery: 4-cell lithium-ion (up to 10 hours battery life)Connectivity: Wi-Fi 6E, Bluetooth 5.3, Thunderbolt 4, USB-C, HDMI 2.1Engineered by ASUS, this professional-grade laptop delivers supreme processing power, stunning visual fidelity, and robust build quality for power users and creators.', 1204.99, 27, 'products/2026/09/02/images.jfif', 1, '2026-09-02 11:21:00.329515', '2026-09-02 11:22:26.034139', 78, 'LAP-SKU-2009', NULL),
(1459, 'Acer EliteBook Ultra Model 10', 'acer-elitebook-ultra-model-10', 'Processor: Intel Core i9-13900HRAM: 16GB DDR5Storage: 512GB NVMe SSDDisplay: 16-inch WQXGA IPS, 165HzGraphics: NVIDIA GeForce RTX 4060 8GBOperating System: Windows 11 HomeBattery: 4-cell lithium-ion (up to 10 hours battery life)Connectivity: Wi-Fi 6E, Bluetooth 5.3, Thunderbolt 4, USB-C, HDMI 2.1Engineered by Acer, this professional-grade laptop delivers supreme processing power, stunning visual fidelity, and robust build quality for power users and creators.', 1249.99, 24, 'products/2026/09/02/LAP-SKU-2010.png', 1, '2026-09-02 11:21:11.397339', '2026-09-02 11:21:20.329533', 78, 'LAP-SKU-2010', NULL),
(1460, 'HP EliteBook Ultra Model 11', 'hp-elitebook-ultra-model-11', 'Processor: Intel Core i5-13420HRAM: 32GB DDR5Storage: 1TB NVMe SSDDisplay: 14-inch OLED 90HzGraphics: NVIDIA GeForce RTX 4070 8GBOperating System: Windows 11 HomeBattery: 4-cell lithium-ion (up to 10 hours battery life)Connectivity: Wi-Fi 6E, Bluetooth 5.3, Thunderbolt 4, USB-C, HDMI 2.1Engineered by HP, this professional-grade laptop delivers supreme processing power, stunning visual fidelity, and robust build quality for power users and creators.', 1294.99, 46, 'products/2026/09/02/LAP-SKU-2011.png', 1, '2026-09-02 11:21:20.329533', '2026-09-02 11:21:22.179642', 78, 'LAP-SKU-2011', NULL),
(1461, 'Dell EliteBook Ultra Model 12', 'dell-elitebook-ultra-model-12', 'Processor: Intel Core i7-13700HRAM: 8GB DDR5Storage: 2TB NVMe SSDDisplay: 17.3-inch Full HD 240HzGraphics: Intel Iris Xe GraphicsOperating System: Windows 11 HomeBattery: 4-cell lithium-ion (up to 10 hours battery life)Connectivity: Wi-Fi 6E, Bluetooth 5.3, Thunderbolt 4, USB-C, HDMI 2.1Engineered by Dell, this professional-grade laptop delivers supreme processing power, stunning visual fidelity, and robust build quality for power users and creators.', 1339.99, 72, 'products/2026/09/02/LAP-SKU-2012.png', 1, '2026-09-02 11:21:22.179642', '2026-09-02 11:21:23.847326', 78, 'LAP-SKU-2012', NULL),
(1462, 'Lenovo EliteBook Ultra Model 13', 'lenovo-elitebook-ultra-model-13', 'Processor: AMD Ryzen 7 7840HSRAM: 16GB DDR5Storage: 512GB NVMe SSDDisplay: 15.6-inch Full HD IPS, 144HzGraphics: NVIDIA GeForce RTX 4050 6GBOperating System: Windows 11 HomeBattery: 4-cell lithium-ion (up to 10 hours battery life)Connectivity: Wi-Fi 6E, Bluetooth 5.3, Thunderbolt 4, USB-C, HDMI 2.1Engineered by Lenovo, this professional-grade laptop delivers supreme processing power, stunning visual fidelity, and robust build quality for power users and creators.', 1384.99, 34, 'products/2026/09/02/LAP-SKU-2013.png', 1, '2026-09-02 11:21:23.864670', '2026-09-02 11:21:25.463920', 78, 'LAP-SKU-2013', NULL),
(1463, 'ASUS EliteBook Ultra Model 14', 'asus-elitebook-ultra-model-14', 'Processor: AMD Ryzen 5 7640HSRAM: 32GB DDR5Storage: 1TB NVMe SSDDisplay: 16-inch WQXGA IPS, 165HzGraphics: NVIDIA GeForce RTX 4060 8GBOperating System: Windows 11 HomeBattery: 4-cell lithium-ion (up to 10 hours battery life)Connectivity: Wi-Fi 6E, Bluetooth 5.3, Thunderbolt 4, USB-C, HDMI 2.1Engineered by ASUS, this professional-grade laptop delivers supreme processing power, stunning visual fidelity, and robust build quality for power users and creators.', 1429.99, 76, 'products/2026/09/02/LAP-SKU-2014_sLvv7fo.png', 1, '2026-09-02 11:21:25.480144', '2026-09-02 11:21:27.213318', 78, 'LAP-SKU-2014', NULL),
(1464, 'Acer EliteBook Ultra Model 15', 'acer-elitebook-ultra-model-15', 'Processor: Intel Core i9-13900HRAM: 8GB DDR5Storage: 2TB NVMe SSDDisplay: 14-inch OLED 90HzGraphics: NVIDIA GeForce RTX 4070 8GBOperating System: Windows 11 HomeBattery: 4-cell lithium-ion (up to 10 hours battery life)Connectivity: Wi-Fi 6E, Bluetooth 5.3, Thunderbolt 4, USB-C, HDMI 2.1Engineered by Acer, this professional-grade laptop delivers supreme processing power, stunning visual fidelity, and robust build quality for power users and creators.', 1474.99, 37, 'products/2026/09/02/LAP-SKU-2015.png', 1, '2026-09-02 11:21:27.213318', '2026-09-08 15:40:39.326886', 78, 'LAP-SKU-2015', NULL),
(1465, 'HP EliteBook Ultra Model 16', 'hp-elitebook-ultra-model-16', 'Processor: Intel Core i5-13420HRAM: 16GB DDR5Storage: 512GB NVMe SSDDisplay: 17.3-inch Full HD 240HzGraphics: Intel Iris Xe GraphicsOperating System: Windows 11 HomeBattery: 4-cell lithium-ion (up to 10 hours battery life)Connectivity: Wi-Fi 6E, Bluetooth 5.3, Thunderbolt 4, USB-C, HDMI 2.1Engineered by HP, this professional-grade laptop delivers supreme processing power, stunning visual fidelity, and robust build quality for power users and creators.', 1519.99, 70, 'products/2026/09/02/LAP-SKU-2016.png', 1, '2026-09-02 11:21:28.861653', '2026-09-02 11:21:30.595653', 78, 'LAP-SKU-2016', NULL),
(1466, 'Dell EliteBook Ultra Model 17', 'dell-elitebook-ultra-model-17', 'Processor: Intel Core i7-13700HRAM: 32GB DDR5Storage: 1TB NVMe SSDDisplay: 15.6-inch Full HD IPS, 144HzGraphics: NVIDIA GeForce RTX 4050 6GBOperating System: Windows 11 HomeBattery: 4-cell lithium-ion (up to 10 hours battery life)Connectivity: Wi-Fi 6E, Bluetooth 5.3, Thunderbolt 4, USB-C, HDMI 2.1Engineered by Dell, this professional-grade laptop delivers supreme processing power, stunning visual fidelity, and robust build quality for power users and creators.', 1564.99, 27, 'products/2026/09/02/LAP-SKU-2017.png', 1, '2026-09-02 11:21:30.600999', '2026-09-02 11:21:32.346899', 78, 'LAP-SKU-2017', NULL),
(1469, 'Acer EliteBook Ultra Model 20', 'acer-elitebook-ultra-model-20', 'Processor: Intel Core i9-13900HRAM: 32GB DDR5Storage: 1TB NVMe SSDDisplay: 17.3-inch Full HD 240HzGraphics: Intel Iris Xe GraphicsOperating System: Windows 11 HomeBattery: 4-cell lithium-ion (up to 10 hours battery life)Connectivity: Wi-Fi 6E, Bluetooth 5.3, Thunderbolt 4, USB-C, HDMI 2.1Engineered by Acer, this professional-grade laptop delivers supreme processing power, stunning visual fidelity, and robust build quality for power users and creators.', 1699.99, 43, 'products/2026/09/02/LAP-SKU-2020.png', 1, '2026-09-02 11:21:35.697012', '2026-09-08 13:06:38.573691', 78, 'LAP-SKU-2020', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `products_productimage`
--

CREATE TABLE `products_productimage` (
  `id` bigint(20) NOT NULL,
  `image` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `product_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product_agent_productcsvimport`
--

CREATE TABLE `product_agent_productcsvimport` (
  `id` bigint(20) NOT NULL,
  `file` varchar(100) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `processed` tinyint(1) NOT NULL,
  `processed_at` datetime(6) DEFAULT NULL,
  `result` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `product_agent_productcsvimport`
--

INSERT INTO `product_agent_productcsvimport` (`id`, `file`, `uploaded_at`, `processed`, `processed_at`, `result`) VALUES
(6, 'product_imports/products_F8fHk1C.csv', '2026-08-17 14:10:29.221460', 1, '2026-08-17 14:10:42.296733', 'Created: 3\nUpdated: 0\nSkipped: 0\nImages downloaded: 3\nImages processed: 3\nImages failed: 0'),
(23, 'product_imports/django_laptops_only_fLO2YLN.csv', '2026-09-02 11:19:30.124012', 1, '2026-09-02 11:21:37.380189', 'Created: 20\nUpdated: 0\nSkipped: 0\nImages downloaded: 12\nImages processed: 12\nImages failed: 8');

-- --------------------------------------------------------

--
-- Table structure for table `recommendations_cachedrecommendation`
--

CREATE TABLE `recommendations_cachedrecommendation` (
  `id` bigint(20) NOT NULL,
  `session_key` varchar(40) DEFAULT NULL,
  `last_updated` datetime(6) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `recommendations_cachedrecommendation`
--

INSERT INTO `recommendations_cachedrecommendation` (`id`, `session_key`, `last_updated`, `user_id`) VALUES
(1, NULL, '2026-09-01 13:43:38.184753', 2),
(2, 'j5tlmlgcbiamn0yicfqjldewl61q0i9i', '2026-09-01 13:43:38.193269', NULL),
(3, NULL, '2026-09-01 13:43:38.177007', 1),
(4, NULL, '2026-09-01 13:43:38.167477', 3);

-- --------------------------------------------------------

--
-- Table structure for table `recommendations_cachedrecommendation_recommended_products`
--

CREATE TABLE `recommendations_cachedrecommendation_recommended_products` (
  `id` bigint(20) NOT NULL,
  `cachedrecommendation_id` bigint(20) NOT NULL,
  `product_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `recommendations_cachedrecommendation_recommended_products`
--

INSERT INTO `recommendations_cachedrecommendation_recommended_products` (`id`, `cachedrecommendation_id`, `product_id`) VALUES
(69, 1, 1046),
(70, 1, 1052),
(71, 1, 1054),
(66, 1, 1063),
(108, 1, 1064),
(68, 1, 1065),
(54, 1, 1083),
(55, 1, 1084),
(20, 2, 1063),
(87, 2, 1064),
(46, 2, 1065),
(47, 2, 1066),
(24, 2, 1067),
(63, 2, 1083),
(64, 2, 1084),
(65, 2, 1085),
(77, 3, 1038),
(120, 3, 1040),
(98, 3, 1041),
(121, 3, 1042),
(122, 3, 1044),
(123, 3, 1045),
(119, 3, 1061),
(83, 3, 1085),
(118, 4, 1039),
(117, 4, 1043),
(93, 4, 1049),
(116, 4, 1057),
(109, 4, 1059),
(112, 4, 1062),
(114, 4, 1084),
(115, 4, 1085);

-- --------------------------------------------------------

--
-- Table structure for table `recommendations_userinteraction`
--

CREATE TABLE `recommendations_userinteraction` (
  `id` bigint(20) NOT NULL,
  `session_key` varchar(40) DEFAULT NULL,
  `action_type` varchar(10) NOT NULL,
  `weight` double NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `product_id` bigint(20) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `recommendations_userinteraction`
--

INSERT INTO `recommendations_userinteraction` (`id`, `session_key`, `action_type`, `weight`, `created_at`, `product_id`, `user_id`) VALUES
(1, 'kcasnqfwczr2noi9rthmofkbf8evvjfr', 'VIEW', 1, '2026-08-19 12:09:35.150510', 1084, 2),
(2, 'mpru9rhxkiykj5nqnj9hfbe5lmjf4kq9', 'VIEW', 1, '2026-08-19 12:52:38.976365', 1063, 2),
(3, 'mpru9rhxkiykj5nqnj9hfbe5lmjf4kq9', 'CART', 3.5, '2026-08-19 13:14:09.129474', 1063, 2),
(4, 'mpru9rhxkiykj5nqnj9hfbe5lmjf4kq9', 'VIEW', 1, '2026-08-19 13:21:35.504770', 1054, 2),
(5, 'mpru9rhxkiykj5nqnj9hfbe5lmjf4kq9', 'CART', 3.5, '2026-08-19 13:21:36.831740', 1054, 2),
(6, 'dkwe4zducweh0dkruk73nwxih119bon6', 'VIEW', 1, '2026-08-19 14:09:59.158467', 1083, 2),
(7, 'dkwe4zducweh0dkruk73nwxih119bon6', 'VIEW', 1, '2026-08-19 14:12:29.374498', 1083, 2),
(8, 'dkwe4zducweh0dkruk73nwxih119bon6', 'VIEW', 1, '2026-08-19 14:20:05.642567', 1051, 2),
(9, 'dkwe4zducweh0dkruk73nwxih119bon6', 'VIEW', 1, '2026-08-19 14:21:58.437700', 1052, 2),
(10, 'dkwe4zducweh0dkruk73nwxih119bon6', 'CART', 3.5, '2026-08-19 14:21:59.578258', 1052, 2),
(11, 'dkwe4zducweh0dkruk73nwxih119bon6', 'VIEW', 1, '2026-08-19 14:22:31.257426', 1083, 2),
(12, 'dkwe4zducweh0dkruk73nwxih119bon6', 'CART', 3.5, '2026-08-19 14:22:32.304883', 1083, 2),
(13, 'dkwe4zducweh0dkruk73nwxih119bon6', 'VIEW', 1, '2026-08-19 14:26:18.358778', 1083, 2),
(14, 'j5tlmlgcbiamn0yicfqjldewl61q0i9i', 'VIEW', 1, '2026-08-19 14:36:18.602310', 1064, NULL),
(15, 'df5tzsju0vcqhyn7im1p44qdpe9c992u', 'VIEW', 1, '2026-08-19 14:41:17.343570', 1064, 2),
(16, 'zicw2j26xh2r18sw6df4tnbespyi83mz', 'VIEW', 1, '2026-08-20 09:38:36.141168', 1065, 2),
(17, 'zicw2j26xh2r18sw6df4tnbespyi83mz', 'VIEW', 1, '2026-08-20 09:38:55.694935', 1064, 2),
(18, 'zicw2j26xh2r18sw6df4tnbespyi83mz', 'VIEW', 1, '2026-08-20 09:39:11.852284', 1048, 2),
(19, 'zicw2j26xh2r18sw6df4tnbespyi83mz', 'VIEW', 1, '2026-08-20 09:40:10.186597', 1084, 2),
(20, 'zicw2j26xh2r18sw6df4tnbespyi83mz', 'CART', 3.5, '2026-08-20 09:40:14.401914', 1084, 2),
(21, 'zicw2j26xh2r18sw6df4tnbespyi83mz', 'VIEW', 1, '2026-08-20 09:40:45.445920', 1056, 2),
(22, 'zicw2j26xh2r18sw6df4tnbespyi83mz', 'VIEW', 1, '2026-08-20 09:40:52.582632', 1054, 2),
(23, 'zicw2j26xh2r18sw6df4tnbespyi83mz', 'VIEW', 1, '2026-08-20 09:44:23.881405', 1067, 2),
(24, 'zicw2j26xh2r18sw6df4tnbespyi83mz', 'VIEW', 1, '2026-08-20 09:44:28.715600', 1066, 2),
(25, 'zicw2j26xh2r18sw6df4tnbespyi83mz', 'VIEW', 1, '2026-08-20 09:44:46.270171', 1055, 2),
(26, 'zicw2j26xh2r18sw6df4tnbespyi83mz', 'VIEW', 1, '2026-08-20 09:45:32.217654', 1052, 2),
(27, 'zicw2j26xh2r18sw6df4tnbespyi83mz', 'VIEW', 1, '2026-08-20 09:45:41.640882', 1046, 2),
(28, 'zicw2j26xh2r18sw6df4tnbespyi83mz', 'CART', 3.5, '2026-08-20 09:45:44.507991', 1046, 2),
(29, 'px3cnxabfcph6nkc9l1abb8ud5f22t2v', 'VIEW', 1, '2026-08-20 10:14:56.056152', 1083, 2),
(30, 'px3cnxabfcph6nkc9l1abb8ud5f22t2v', 'VIEW', 1, '2026-08-20 10:15:40.220581', 1065, 2),
(31, 'px3cnxabfcph6nkc9l1abb8ud5f22t2v', 'CART', 3.5, '2026-08-20 10:15:44.536799', 1065, 2),
(32, 'px3cnxabfcph6nkc9l1abb8ud5f22t2v', 'VIEW', 1, '2026-08-20 10:15:58.908655', 1084, 2),
(34, '2x3iysnzgxy8m7ovg38jzc188y7hlszv', 'VIEW', 1, '2026-08-20 14:46:07.074020', 1049, 3),
(35, '2x3iysnzgxy8m7ovg38jzc188y7hlszv', 'CART', 3.5, '2026-08-20 14:46:08.661980', 1049, 3),
(36, 'dzl98vylyrybarlvbyq82xkuvbpqhg3u', 'VIEW', 1, '2026-08-20 16:18:25.057794', 1064, 2),
(37, 'dzl98vylyrybarlvbyq82xkuvbpqhg3u', 'CART', 3.5, '2026-08-20 16:18:28.202685', 1064, 2),
(38, 'l90rc8nd8vjcvqyaku4trohwi5szhwgi', 'VIEW', 1, '2026-08-21 12:54:38.242597', 1043, 1),
(39, 'l90rc8nd8vjcvqyaku4trohwi5szhwgi', 'VIEW', 1, '2026-08-21 13:07:24.936566', 1057, 1),
(40, 'l90rc8nd8vjcvqyaku4trohwi5szhwgi', 'VIEW', 1, '2026-08-21 13:07:37.491304', 1053, 1),
(41, 'l90rc8nd8vjcvqyaku4trohwi5szhwgi', 'VIEW', 1, '2026-08-21 13:38:35.549983', 1038, 1),
(42, 'l90rc8nd8vjcvqyaku4trohwi5szhwgi', 'CART', 3.5, '2026-08-21 13:38:36.744069', 1038, 1),
(43, 'l90rc8nd8vjcvqyaku4trohwi5szhwgi', 'VIEW', 1, '2026-08-21 15:38:21.382911', 1039, 1),
(44, 'l90rc8nd8vjcvqyaku4trohwi5szhwgi', 'VIEW', 1, '2026-08-24 09:34:57.318341', 1084, 1),
(45, 'l90rc8nd8vjcvqyaku4trohwi5szhwgi', 'VIEW', 1, '2026-08-24 14:06:20.316393', 1084, 1),
(46, '9hozyga7cadieaoqehjp9fyfl7mbv8rr', 'VIEW', 1, '2026-08-27 11:51:42.070765', 1084, 3),
(47, 'astljtb6qm15r2zaaqxn4kp6yqesnzpr', 'VIEW', 1, '2026-08-27 14:55:13.614484', 1084, 3),
(48, 'astljtb6qm15r2zaaqxn4kp6yqesnzpr', 'CART', 3.5, '2026-08-27 14:55:15.012663', 1084, 3),
(49, 'syop2n19hh55kj7mka5hzbvydvdo662y', 'VIEW', 1, '2026-09-01 10:07:58.294153', 1038, 3),
(50, 'syop2n19hh55kj7mka5hzbvydvdo662y', 'VIEW', 1, '2026-09-01 10:08:04.447234', 1083, 3),
(51, 'syop2n19hh55kj7mka5hzbvydvdo662y', 'VIEW', 1, '2026-09-01 10:21:02.217008', 1062, 3),
(52, 'syop2n19hh55kj7mka5hzbvydvdo662y', 'CART', 3.5, '2026-09-01 10:21:05.096949', 1062, 3),
(53, 'syop2n19hh55kj7mka5hzbvydvdo662y', 'VIEW', 1, '2026-09-01 10:21:19.287445', 1084, 3),
(54, 'syop2n19hh55kj7mka5hzbvydvdo662y', 'CART', 3.5, '2026-09-01 10:21:20.401396', 1084, 3),
(55, 'syop2n19hh55kj7mka5hzbvydvdo662y', 'VIEW', 1, '2026-09-01 10:21:30.834318', 1084, 3),
(56, 'syop2n19hh55kj7mka5hzbvydvdo662y', 'CART', 3.5, '2026-09-01 10:21:31.537165', 1084, 3),
(57, 'syop2n19hh55kj7mka5hzbvydvdo662y', 'VIEW', 1, '2026-09-01 10:21:37.135199', 1059, 3),
(58, 'syop2n19hh55kj7mka5hzbvydvdo662y', 'CART', 3.5, '2026-09-01 10:21:38.072428', 1059, 3),
(59, 'fnhlknabcxp463sg3xao6ph5uwqhaehp', 'VIEW', 1, '2026-09-01 13:20:00.369126', 1084, 3),
(60, 'fnhlknabcxp463sg3xao6ph5uwqhaehp', 'VIEW', 1, '2026-09-01 13:35:08.266260', 1084, 3),
(61, 'fnhlknabcxp463sg3xao6ph5uwqhaehp', 'VIEW', 1, '2026-09-01 13:38:01.169460', 1062, 3),
(63, 'qg9wcbcxjwn8blco33w6ytd6hewqoh0l', 'VIEW', 1, '2026-09-02 11:25:50.744586', 1455, 3),
(64, 'qg9wcbcxjwn8blco33w6ytd6hewqoh0l', 'VIEW', 1, '2026-09-02 11:26:12.581951', 1465, 3),
(65, 'qg9wcbcxjwn8blco33w6ytd6hewqoh0l', 'VIEW', 1, '2026-09-02 11:26:25.983150', 1450, 3),
(66, 'ulk3k4j7n6i7omw1mibankvf5mgotnsd', 'VIEW', 1, '2026-09-03 14:34:55.954950', 1463, 3),
(67, 'ulk3k4j7n6i7omw1mibankvf5mgotnsd', 'VIEW', 1, '2026-09-03 14:38:53.194737', 1456, 3),
(68, 'ulk3k4j7n6i7omw1mibankvf5mgotnsd', 'VIEW', 1, '2026-09-03 14:38:57.041659', 1459, 3),
(69, 'ulk3k4j7n6i7omw1mibankvf5mgotnsd', 'VIEW', 1, '2026-09-03 15:35:06.375571', 1461, 3),
(70, 'ulk3k4j7n6i7omw1mibankvf5mgotnsd', 'VIEW', 1, '2026-09-03 15:36:56.973946', 1084, 3),
(71, 'ulk3k4j7n6i7omw1mibankvf5mgotnsd', 'VIEW', 1, '2026-09-03 15:44:27.940738', 1062, 3),
(72, 'ulk3k4j7n6i7omw1mibankvf5mgotnsd', 'CART', 3.5, '2026-09-03 15:44:29.090700', 1062, 3),
(73, 'wj9ngq4fiu1rgk2swrr5ncurmf9mvkji', 'VIEW', 1, '2026-09-04 10:12:36.716230', 1450, 3),
(74, 'wj9ngq4fiu1rgk2swrr5ncurmf9mvkji', 'CART', 3.5, '2026-09-04 10:12:38.165893', 1450, 3),
(75, 'wj9ngq4fiu1rgk2swrr5ncurmf9mvkji', 'VIEW', 1, '2026-09-04 10:30:06.424357', 1461, 3),
(76, 'wj9ngq4fiu1rgk2swrr5ncurmf9mvkji', 'VIEW', 1, '2026-09-04 10:30:12.626078', 1454, 3),
(77, 'wj9ngq4fiu1rgk2swrr5ncurmf9mvkji', 'VIEW', 1, '2026-09-04 10:31:58.473785', 1454, 3),
(81, 'd8bq2wkb2okmabu5dqc15qb6pimwmnrc', 'VIEW', 1, '2026-09-04 14:41:24.546990', 1469, 4),
(82, 'd8bq2wkb2okmabu5dqc15qb6pimwmnrc', 'VIEW', 1, '2026-09-08 13:06:02.710494', 1469, 4),
(83, 'd8bq2wkb2okmabu5dqc15qb6pimwmnrc', 'CART', 3.5, '2026-09-08 13:06:04.825594', 1469, 4),
(84, 'd8bq2wkb2okmabu5dqc15qb6pimwmnrc', 'VIEW', 1, '2026-09-08 13:32:32.109955', 1065, 4),
(85, 'd8bq2wkb2okmabu5dqc15qb6pimwmnrc', 'CART', 3.5, '2026-09-08 13:32:33.516744', 1065, 4),
(86, 'd8bq2wkb2okmabu5dqc15qb6pimwmnrc', 'VIEW', 1, '2026-09-08 15:40:08.663033', 1464, 4),
(87, 'd8bq2wkb2okmabu5dqc15qb6pimwmnrc', 'CART', 3.5, '2026-09-08 15:40:13.053328', 1464, 4);

-- --------------------------------------------------------

--
-- Table structure for table `recommendations_userpreferenceprofile`
--

CREATE TABLE `recommendations_userpreferenceprofile` (
  `id` bigint(20) NOT NULL,
  `session_key` varchar(40) DEFAULT NULL,
  `target_price_min` decimal(10,2) NOT NULL,
  `target_price_max` decimal(10,2) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `favorite_category_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `recommendations_userpreferenceprofile`
--

INSERT INTO `recommendations_userpreferenceprofile` (`id`, `session_key`, `target_price_min`, `target_price_max`, `updated_at`, `favorite_category_id`, `user_id`) VALUES
(1, NULL, 0.00, 10000.00, '2026-08-20 11:26:09.729017', 78, 2),
(2, 'j5tlmlgcbiamn0yicfqjldewl61q0i9i', 0.00, 10000.00, '2026-09-01 13:43:38.193269', 69, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `search_searchlog`
--

CREATE TABLE `search_searchlog` (
  `id` bigint(20) NOT NULL,
  `query` longtext NOT NULL,
  `matched_intent_id` bigint(20) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `matched_product_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `search_searchlog`
--

INSERT INTO `search_searchlog` (`id`, `query`, `matched_intent_id`, `created_at`, `matched_product_id`) VALUES
(186, 'Dell', NULL, '2026-09-04 15:14:56.774296', NULL),
(187, 'Hassan', NULL, '2026-09-04 15:25:42.212515', NULL),
(188, 'order 1', NULL, '2026-09-04 15:26:34.480122', NULL),
(189, 'order1', NULL, '2026-09-04 15:26:42.173350', NULL),
(190, 'orders', NULL, '2026-09-04 15:26:49.510042', NULL),
(191, 'PROCESSING', NULL, '2026-09-04 15:27:31.580695', NULL),
(192, 'completed', NULL, '2026-09-04 15:27:46.169253', NULL),
(193, 'completed', NULL, '2026-09-04 15:27:58.518885', NULL),
(194, 'completed', NULL, '2026-09-04 15:27:59.448657', NULL),
(195, 'completed', NULL, '2026-09-04 15:28:00.077097', NULL),
(196, 'completed', NULL, '2026-09-04 15:28:00.297562', NULL),
(197, 'wireless-gamepad-controller', NULL, '2026-09-04 15:28:39.530409', NULL),
(198, 'wireless-gamepad-controller', NULL, '2026-09-04 15:28:44.079849', NULL),
(199, 'wireless-gamepad-controller', NULL, '2026-09-04 15:28:46.129120', NULL),
(200, 'wireless-gamepad-controller', NULL, '2026-09-04 15:28:46.815259', NULL),
(201, 'wireless-gamepad-controller', NULL, '2026-09-04 15:28:47.514025', NULL),
(202, 'wireless-gamepad-controller', NULL, '2026-09-04 15:28:48.025394', NULL),
(203, 'wireless-gamepad-controller', NULL, '2026-09-04 15:28:48.277237', NULL),
(204, 'wireless-gamepad-controller', NULL, '2026-09-04 15:28:49.285691', NULL),
(205, 'wireless-gamepad-controller', NULL, '2026-09-04 15:28:51.400342', NULL),
(206, 'wireless', NULL, '2026-09-04 15:28:58.233949', NULL),
(207, 'Wireless Gamepad Controller', NULL, '2026-09-04 15:29:11.150805', NULL),
(208, 'Hassan', NULL, '2026-09-04 15:43:40.918975', NULL),
(209, 'DELIVERED', NULL, '2026-09-04 16:20:54.526786', NULL),
(210, 'DELIVERED', NULL, '2026-09-04 16:20:56.666836', NULL),
(211, 'Hassan', NULL, '2026-09-04 16:21:04.163289', NULL),
(212, 'Lahore', NULL, '2026-09-04 16:21:11.045715', NULL),
(213, 'Lahore', NULL, '2026-09-04 16:21:12.444875', NULL),
(214, 'Lahore order', NULL, '2026-09-04 16:21:16.397544', NULL),
(215, 'pending orders', NULL, '2026-09-04 16:21:24.062804', NULL),
(216, 'pending orders', NULL, '2026-09-04 16:21:25.525269', NULL),
(217, 'pending orders', NULL, '2026-09-04 16:21:25.823624', NULL),
(218, 'pending orders', NULL, '2026-09-04 16:21:26.007131', NULL),
(219, 'pending orders', NULL, '2026-09-04 16:21:26.160360', NULL),
(220, 'pending orders', NULL, '2026-09-04 16:21:26.310268', NULL),
(221, 'pending orders', NULL, '2026-09-04 16:21:28.139636', NULL),
(222, 'pending', NULL, '2026-09-04 16:21:31.213958', NULL),
(223, 'processing orders', NULL, '2026-09-04 16:21:40.292857', NULL),
(224, 'processing orders', NULL, '2026-09-04 16:21:43.228057', NULL),
(225, 'processing orders', NULL, '2026-09-04 16:21:44.054657', NULL),
(226, 'Hassan', NULL, '2026-09-04 16:21:54.250959', NULL),
(227, 'Hassan', NULL, '2026-09-04 16:21:56.762870', NULL),
(228, 'completed', NULL, '2026-09-04 16:22:03.025067', NULL),
(229, 'PROCESSING', NULL, '2026-09-04 16:22:18.301538', NULL),
(230, 'PROCESSING', NULL, '2026-09-04 16:22:24.232563', NULL),
(231, 'PROCESSING', NULL, '2026-09-04 16:22:24.805274', NULL),
(232, 'PROCESSING', NULL, '2026-09-04 16:22:25.322032', NULL),
(233, 'PROCESSING', NULL, '2026-09-04 16:22:25.516071', NULL),
(234, 'Hassan', NULL, '2026-09-04 16:24:18.810536', NULL),
(235, 'Hassan', NULL, '2026-09-04 16:24:19.929490', NULL),
(236, 'Hassan', NULL, '2026-09-04 16:24:20.962643', NULL),
(237, 'order 1', NULL, '2026-09-04 16:24:27.756870', NULL),
(238, 'orders', NULL, '2026-09-04 16:24:31.925968', NULL),
(239, 'ORDERS', NULL, '2026-09-04 16:24:40.627161', NULL),
(240, 'ORDERS', NULL, '2026-09-04 16:24:42.399400', NULL),
(241, 'Total Products', NULL, '2026-09-04 16:34:38.108855', NULL),
(242, 'Total Users', NULL, '2026-09-04 16:34:53.076339', NULL),
(243, 'Total Users', NULL, '2026-09-04 16:34:54.572984', NULL),
(244, 'Total Users', NULL, '2026-09-04 16:34:55.938533', NULL),
(245, 'Total Users', NULL, '2026-09-04 16:34:56.719568', NULL),
(246, 'Hassan', NULL, '2026-09-04 17:00:51.430862', NULL),
(247, 'Hassan', NULL, '2026-09-04 17:05:55.760954', NULL),
(248, 'Hassan', NULL, '2026-09-04 17:06:11.970831', NULL),
(249, 'orders jinka payment atka hua hai', NULL, '2026-09-04 18:09:30.570717', NULL),
(250, 'price 500 se zyada wale products', NULL, '2026-09-04 18:10:33.794259', NULL),
(251, 'pichle hafte ke active users', NULL, '2026-09-04 18:10:55.694340', NULL),
(252, 'price 500 se zyada wale products', NULL, '2026-09-04 18:35:14.918122', NULL),
(253, 'active users', NULL, '2026-09-04 18:35:57.669073', NULL),
(254, 'mujhy active orders batao', NULL, '2026-09-04 18:36:22.687990', NULL),
(255, 'mujhy orders batao', NULL, '2026-09-04 18:36:53.058155', NULL),
(256, 'mujhy orders ki list dedo', NULL, '2026-09-04 18:37:13.220546', NULL),
(257, 'orders ki list dedo', NULL, '2026-09-04 18:37:29.351089', NULL),
(258, 'pending orders ki list dedo', NULL, '2026-09-04 18:37:54.526316', NULL),
(259, 'COMPLETED orders ki list dedo', NULL, '2026-09-04 18:38:34.247456', NULL),
(260, 'Dell laptop', NULL, '2026-09-04 18:38:57.496138', NULL),
(261, 'Lahore', NULL, '2026-09-08 11:43:01.596570', NULL),
(262, 'active', NULL, '2026-09-08 11:43:01.682517', NULL),
(263, 'DELIVERED', NULL, '2026-09-08 11:43:02.290696', NULL),
(264, 'pending', NULL, '2026-09-08 11:43:02.822428', NULL),
(265, 'pending', NULL, '2026-09-08 11:49:35.829835', NULL),
(266, 'pending', NULL, '2026-09-08 11:57:05.402717', NULL),
(267, 'pending', NULL, '2026-09-08 11:57:22.005897', NULL),
(268, 'active users dikhao', NULL, '2026-09-08 11:58:02.402225', NULL),
(269, 'price 500 se zyada wale products', NULL, '2026-09-08 11:58:40.303292', NULL),
(270, 'stock khatam ho chuka products', NULL, '2026-09-08 11:59:17.253970', NULL),
(271, 'products k stocks dikhao', NULL, '2026-09-08 11:59:59.562985', NULL),
(272, 'orders jo deliver ho chuke hain', NULL, '2026-09-08 12:00:34.218341', NULL),
(273, 'processing wale orders', NULL, '2026-09-08 12:01:08.635999', NULL),
(274, 'inactive ya suspended users', NULL, '2026-09-08 12:01:45.569061', NULL),
(275, 'inactive ya suspended users', NULL, '2026-09-08 12:02:50.644567', NULL),
(276, 'active ya suspended users', NULL, '2026-09-08 12:02:57.802635', NULL),
(277, 'active users', NULL, '2026-09-08 12:03:16.014911', NULL),
(278, 'active users', NULL, '2026-09-08 12:03:54.475558', NULL),
(279, 'price 500 se zyada wale products', NULL, '2026-09-08 12:36:35.425385', NULL),
(280, 'active users', NULL, '2026-09-08 12:40:38.004272', NULL),
(281, 'pending', NULL, '2026-09-08 13:00:30.179543', NULL),
(282, 'pending', NULL, '2026-09-08 13:04:13.678832', NULL),
(283, 'active users dikhao', NULL, '2026-09-08 13:05:25.478641', NULL),
(284, 'orders', NULL, '2026-09-08 13:07:06.501576', NULL),
(285, 'order', NULL, '2026-09-08 13:07:26.062147', NULL),
(286, 'new order dikhao', NULL, '2026-09-08 13:08:11.453160', NULL),
(287, 'active users', NULL, '2026-09-08 14:52:16.984613', NULL),
(288, 'active users dikhao', NULL, '2026-09-08 14:52:42.969908', NULL),
(289, 'price 500 se zyada wale products', NULL, '2026-09-08 15:56:48.145416', NULL),
(290, 'price 500 se zyada wale products', NULL, '2026-09-08 15:57:04.904892', NULL),
(291, 'price 500 se zyada wale products', NULL, '2026-09-08 16:00:03.885819', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts_user`
--
ALTER TABLE `accounts_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `accounts_user_groups`
--
ALTER TABLE `accounts_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  ADD KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `accounts_user_user_permissions`
--
ALTER TABLE `accounts_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  ADD KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `intents_intent`
--
ALTER TABLE `intents_intent`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `intent_name` (`intent_name`);

--
-- Indexes for table `orders_order`
--
ALTER TABLE `orders_order`
  ADD PRIMARY KEY (`id`),
  ADD KEY `orders_order_user_id_e9b59eb1_fk_accounts_user_id` (`user_id`);

--
-- Indexes for table `orders_orderitem`
--
ALTER TABLE `orders_orderitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `orders_orderitem_order_id_fe61a34d_fk_orders_order_id` (`order_id`),
  ADD KEY `orders_orderitem_product_id_afe4254a_fk_products_product_id` (`product_id`);

--
-- Indexes for table `products_category`
--
ALTER TABLE `products_category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `slug` (`slug`);

--
-- Indexes for table `products_product`
--
ALTER TABLE `products_product`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD UNIQUE KEY `sku` (`sku`),
  ADD KEY `products_product_category_id_9b594869_fk_products_category_id` (`category_id`),
  ADD KEY `products_product_is_active_2e95eb0a` (`is_active`),
  ADD KEY `products_product_name_fa23bcd2` (`name`),
  ADD KEY `products_product_price_9b2ae7ca` (`price`),
  ADD KEY `products_pr_is_acti_085b05_idx` (`is_active`,`price`),
  ADD KEY `products_product_brand_37465a28` (`brand`);

--
-- Indexes for table `products_productimage`
--
ALTER TABLE `products_productimage`
  ADD PRIMARY KEY (`id`),
  ADD KEY `products_productimage_product_id_e747596a_fk_products_product_id` (`product_id`);

--
-- Indexes for table `product_agent_productcsvimport`
--
ALTER TABLE `product_agent_productcsvimport`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `recommendations_cachedrecommendation`
--
ALTER TABLE `recommendations_cachedrecommendation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `recommendations_cachedrecommendation_session_key_824ff3c3` (`session_key`),
  ADD KEY `recommendat_session_c0b1ea_idx` (`session_key`),
  ADD KEY `recommendat_user_id_f418f5_idx` (`user_id`);

--
-- Indexes for table `recommendations_cachedrecommendation_recommended_products`
--
ALTER TABLE `recommendations_cachedrecommendation_recommended_products`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `recommendations_cachedre_cachedrecommendation_id__1c8c1592_uniq` (`cachedrecommendation_id`,`product_id`),
  ADD KEY `recommendations_cach_product_id_fe729279_fk_products_` (`product_id`);

--
-- Indexes for table `recommendations_userinteraction`
--
ALTER TABLE `recommendations_userinteraction`
  ADD PRIMARY KEY (`id`),
  ADD KEY `recommendations_user_product_id_19f141fd_fk_products_` (`product_id`),
  ADD KEY `recommendations_userinteraction_session_key_8e2805f7` (`session_key`),
  ADD KEY `recommendations_userinteraction_action_type_b1b9e2de` (`action_type`),
  ADD KEY `recommendations_userinteraction_created_at_95f455cd` (`created_at`),
  ADD KEY `recommendat_user_id_34cbbd_idx` (`user_id`,`action_type`),
  ADD KEY `recommendat_session_55d69a_idx` (`session_key`,`action_type`);

--
-- Indexes for table `recommendations_userpreferenceprofile`
--
ALTER TABLE `recommendations_userpreferenceprofile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `recommendations_user_favorite_category_id_23f35585_fk_products_` (`favorite_category_id`),
  ADD KEY `recommendations_userpreferenceprofile_session_key_321410ae` (`session_key`);

--
-- Indexes for table `search_searchlog`
--
ALTER TABLE `search_searchlog`
  ADD PRIMARY KEY (`id`),
  ADD KEY `search_searchlog_matched_intent_id_b3a9e690_fk_intents_intent_id` (`matched_intent_id`),
  ADD KEY `search_searchlog_matched_product_id_07256dfa_fk_products_` (`matched_product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts_user`
--
ALTER TABLE `accounts_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `accounts_user_groups`
--
ALTER TABLE `accounts_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accounts_user_user_permissions`
--
ALTER TABLE `accounts_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=69;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `intents_intent`
--
ALTER TABLE `intents_intent`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `orders_order`
--
ALTER TABLE `orders_order`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `orders_orderitem`
--
ALTER TABLE `orders_orderitem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `products_category`
--
ALTER TABLE `products_category`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=96;

--
-- AUTO_INCREMENT for table `products_product`
--
ALTER TABLE `products_product`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `products_productimage`
--
ALTER TABLE `products_productimage`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=325;

--
-- AUTO_INCREMENT for table `product_agent_productcsvimport`
--
ALTER TABLE `product_agent_productcsvimport`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `recommendations_cachedrecommendation`
--
ALTER TABLE `recommendations_cachedrecommendation`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `recommendations_cachedrecommendation_recommended_products`
--
ALTER TABLE `recommendations_cachedrecommendation_recommended_products`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=124;

--
-- AUTO_INCREMENT for table `recommendations_userinteraction`
--
ALTER TABLE `recommendations_userinteraction`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=88;

--
-- AUTO_INCREMENT for table `recommendations_userpreferenceprofile`
--
ALTER TABLE `recommendations_userpreferenceprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `search_searchlog`
--
ALTER TABLE `search_searchlog`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=292;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accounts_user_groups`
--
ALTER TABLE `accounts_user_groups`
  ADD CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `accounts_user_user_permissions`
--
ALTER TABLE `accounts_user_user_permissions`
  ADD CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `orders_order`
--
ALTER TABLE `orders_order`
  ADD CONSTRAINT `orders_order_user_id_e9b59eb1_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `orders_orderitem`
--
ALTER TABLE `orders_orderitem`
  ADD CONSTRAINT `orders_orderitem_order_id_fe61a34d_fk_orders_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`),
  ADD CONSTRAINT `orders_orderitem_product_id_afe4254a_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`);

--
-- Constraints for table `products_product`
--
ALTER TABLE `products_product`
  ADD CONSTRAINT `products_product_category_id_9b594869_fk_products_category_id` FOREIGN KEY (`category_id`) REFERENCES `products_category` (`id`);

--
-- Constraints for table `products_productimage`
--
ALTER TABLE `products_productimage`
  ADD CONSTRAINT `products_productimage_product_id_e747596a_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`);

--
-- Constraints for table `recommendations_cachedrecommendation`
--
ALTER TABLE `recommendations_cachedrecommendation`
  ADD CONSTRAINT `recommendations_cach_user_id_9c2aa672_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `recommendations_cachedrecommendation_recommended_products`
--
ALTER TABLE `recommendations_cachedrecommendation_recommended_products`
  ADD CONSTRAINT `recommendations_cach_cachedrecommendation_bae41b59_fk_recommend` FOREIGN KEY (`cachedrecommendation_id`) REFERENCES `recommendations_cachedrecommendation` (`id`),
  ADD CONSTRAINT `recommendations_cach_product_id_fe729279_fk_products_` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`);

--
-- Constraints for table `recommendations_userinteraction`
--
ALTER TABLE `recommendations_userinteraction`
  ADD CONSTRAINT `recommendations_user_product_id_19f141fd_fk_products_` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`),
  ADD CONSTRAINT `recommendations_user_user_id_a92ee9d6_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `recommendations_userpreferenceprofile`
--
ALTER TABLE `recommendations_userpreferenceprofile`
  ADD CONSTRAINT `recommendations_user_favorite_category_id_23f35585_fk_products_` FOREIGN KEY (`favorite_category_id`) REFERENCES `products_category` (`id`),
  ADD CONSTRAINT `recommendations_user_user_id_78537bd6_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

--
-- Constraints for table `search_searchlog`
--
ALTER TABLE `search_searchlog`
  ADD CONSTRAINT `search_searchlog_matched_intent_id_b3a9e690_fk_intents_intent_id` FOREIGN KEY (`matched_intent_id`) REFERENCES `intents_intent` (`id`),
  ADD CONSTRAINT `search_searchlog_matched_product_id_07256dfa_fk_products_` FOREIGN KEY (`matched_product_id`) REFERENCES `products_product` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
