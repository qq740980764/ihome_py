/*
Navicat MySQL Data Transfer

Source Server         : 192.168.11.128
Source Server Version : 50725
Source Host           : 192.168.11.128:3306
Source Database       : ihome_python04

Target Server Type    : MYSQL
Target Server Version : 50725
File Encoding         : 65001

Date: 2019-05-29 16:54:57
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `alembic_version`
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('0a8ead7837e5');

-- ----------------------------
-- Table structure for `ih_area_info`
-- ----------------------------
DROP TABLE IF EXISTS `ih_area_info`;
CREATE TABLE `ih_area_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ih_area_info
-- ----------------------------
INSERT INTO `ih_area_info` VALUES (null, null, '1', '东城区');
INSERT INTO `ih_area_info` VALUES (null, null, '2', '南城区');
INSERT INTO `ih_area_info` VALUES (null, null, '3', '西城区');
INSERT INTO `ih_area_info` VALUES (null, null, '4', '北城区');
INSERT INTO `ih_area_info` VALUES (null, null, '5', '南北城区');
INSERT INTO `ih_area_info` VALUES (null, null, '6', '东北城区');
INSERT INTO `ih_area_info` VALUES (null, null, '7', '南西城区');

-- ----------------------------
-- Table structure for `ih_facility_info`
-- ----------------------------
DROP TABLE IF EXISTS `ih_facility_info`;
CREATE TABLE `ih_facility_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ih_facility_info
-- ----------------------------
INSERT INTO `ih_facility_info` VALUES (null, null, '1', '水电');
INSERT INTO `ih_facility_info` VALUES (null, null, '2', '热水领域');
INSERT INTO `ih_facility_info` VALUES (null, null, '3', '空调');
INSERT INTO `ih_facility_info` VALUES (null, null, '4', '暖气');
INSERT INTO `ih_facility_info` VALUES (null, null, '5', '允许吸烟');
INSERT INTO `ih_facility_info` VALUES (null, null, '6', '饮水设备');
INSERT INTO `ih_facility_info` VALUES (null, null, '7', '牙具');
INSERT INTO `ih_facility_info` VALUES (null, null, '8', '香皂');

-- ----------------------------
-- Table structure for `ih_house_facility`
-- ----------------------------
DROP TABLE IF EXISTS `ih_house_facility`;
CREATE TABLE `ih_house_facility` (
  `house_id` int(11) NOT NULL,
  `facility_id` int(11) NOT NULL,
  PRIMARY KEY (`house_id`,`facility_id`),
  KEY `facility_id` (`facility_id`),
  CONSTRAINT `ih_house_facility_ibfk_1` FOREIGN KEY (`facility_id`) REFERENCES `ih_facility_info` (`id`),
  CONSTRAINT `ih_house_facility_ibfk_2` FOREIGN KEY (`house_id`) REFERENCES `ih_house_info` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ih_house_facility
-- ----------------------------
INSERT INTO `ih_house_facility` VALUES ('1', '1');
INSERT INTO `ih_house_facility` VALUES ('1', '2');

-- ----------------------------
-- Table structure for `ih_house_image`
-- ----------------------------
DROP TABLE IF EXISTS `ih_house_image`;
CREATE TABLE `ih_house_image` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `house_id` int(11) NOT NULL,
  `url` varchar(256) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `house_id` (`house_id`),
  CONSTRAINT `ih_house_image_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `ih_house_info` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ih_house_image
-- ----------------------------

-- ----------------------------
-- Table structure for `ih_house_info`
-- ----------------------------
DROP TABLE IF EXISTS `ih_house_info`;
CREATE TABLE `ih_house_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `area_id` int(11) NOT NULL,
  `title` varchar(64) NOT NULL,
  `price` int(11) DEFAULT NULL,
  `address` varchar(512) DEFAULT NULL,
  `room_count` int(11) DEFAULT NULL,
  `acreage` int(11) DEFAULT NULL,
  `unit` varchar(32) DEFAULT NULL,
  `capacity` int(11) DEFAULT NULL,
  `beds` varchar(64) DEFAULT NULL,
  `deposit` int(11) DEFAULT NULL,
  `min_days` int(11) DEFAULT NULL,
  `max_days` int(11) DEFAULT NULL,
  `order_count` int(11) DEFAULT NULL,
  `index_image_url` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `area_id` (`area_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `ih_house_info_ibfk_1` FOREIGN KEY (`area_id`) REFERENCES `ih_area_info` (`id`),
  CONSTRAINT `ih_house_info_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `ih_user_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ih_house_info
-- ----------------------------
INSERT INTO `ih_house_info` VALUES ('2019-05-29 16:47:11', '2019-05-29 16:47:11', '1', '4', '1', '1', '10200', '222', '2', '202', '2', '2', '2x1.8x2', '20200', '1', '2', '0', '');

-- ----------------------------
-- Table structure for `ih_order_info`
-- ----------------------------
DROP TABLE IF EXISTS `ih_order_info`;
CREATE TABLE `ih_order_info` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `house_id` int(11) NOT NULL,
  `begin_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `days` int(11) NOT NULL,
  `house_price` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `status` enum('WAIT_ACCEPT','WAIT_PAYMENT','PAID','WAIT_COMMENT','COMPLETE','CANCELED','REJECTED') DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`id`),
  KEY `house_id` (`house_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_ih_order_info_status` (`status`),
  CONSTRAINT `ih_order_info_ibfk_1` FOREIGN KEY (`house_id`) REFERENCES `ih_house_info` (`id`),
  CONSTRAINT `ih_order_info_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `ih_user_profile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ih_order_info
-- ----------------------------

-- ----------------------------
-- Table structure for `ih_user_profile`
-- ----------------------------
DROP TABLE IF EXISTS `ih_user_profile`;
CREATE TABLE `ih_user_profile` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `mobile` varchar(11) NOT NULL,
  `real_name` varchar(32) DEFAULT NULL,
  `id_card` varchar(20) DEFAULT NULL,
  `avatar_url` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobile` (`mobile`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ih_user_profile
-- ----------------------------
INSERT INTO `ih_user_profile` VALUES ('2019-05-29 14:44:00', '2019-05-29 14:44:59', '4', '王大锤123', 'pbkdf2:sha256:50000$KaXnONxz$39b0e54af4a6de272e348db9f9d08fdc60230b0e435670c86d19d2e331d8c8b5', '15347460537', '王大锤', '441522199610183755', 'Fneym2F5hk5pZ8bXxhvCCnwwq1T_');
