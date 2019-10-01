-- phpMyAdmin SQL Dump
-- version 4.4.15.10
-- https://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Sep 27, 2019 at 10:19 PM
-- Server version: 5.6.45
-- PHP Version: 7.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `testdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `all_disk_partition`
--

DROP TABLE IF EXISTS `all_disk_partition`;
CREATE TABLE IF NOT EXISTS `all_disk_partition` (
  `hostname` varchar(30) DEFAULT NULL,
  `IP` varchar(30) DEFAULT NULL,
  `device_detail` varchar(30) DEFAULT NULL,
  `mount_point` varchar(30) DEFAULT NULL,
  `file_system_type` varchar(30) DEFAULT NULL,
  `total_size` int(20) DEFAULT NULL,
  `used_space` int(20) DEFAULT NULL,
  `free_space` int(20) DEFAULT NULL,
  `percent_free` float(20,1) DEFAULT NULL,
  `execution_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `all_large_directory`
--

DROP TABLE IF EXISTS `all_large_directory`;
CREATE TABLE IF NOT EXISTS `all_large_directory` (
  `host_name` varchar(30) DEFAULT NULL,
  `host_ip` varchar(30) DEFAULT NULL,
  `directory_name` varchar(100) DEFAULT NULL,
  `directory_size` int(30) DEFAULT NULL,
  `execution_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `all_large_file`
--

DROP TABLE IF EXISTS `all_large_file`;
CREATE TABLE IF NOT EXISTS `all_large_file` (
  `host_name` varchar(30) DEFAULT NULL,
  `host_ip` varchar(30) DEFAULT NULL,
  `mountpoint` varchar(30) DEFAULT NULL,
  `file_name` varchar(100) DEFAULT NULL,
  `file_size` int(30) DEFAULT NULL,
  `last_modified_date` varchar(30) DEFAULT NULL,
  `execution_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `size_by_extn`
--

DROP TABLE IF EXISTS `size_by_extn`;
CREATE TABLE IF NOT EXISTS `size_by_extn` (
  `hostname` varchar(100) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `directory_name` varchar(300) DEFAULT NULL,
  `file_type` varchar(100) DEFAULT NULL,
  `total_size` int(30) DEFAULT NULL,
  `execution_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
