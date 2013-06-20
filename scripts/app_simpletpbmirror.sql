
SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `app_simpletpbmirror`
--

-- --------------------------------------------------------

--
-- 表的结构 `all_resource`
--

CREATE TABLE IF NOT EXISTS `all_resource` (
  `resource_id` int(11) NOT NULL AUTO_INCREMENT,
  `resource_name` text NOT NULL,
  `typeL1` varchar(255) NOT NULL,
  `typeL2` varchar(255) NOT NULL,
  `magnet` varchar(255) NOT NULL,
  `size` varchar(255) NOT NULL DEFAULT 'Unknown',
  `hotrank` int(11) NOT NULL DEFAULT '0',
  `fetch_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `extern_info` tinyint(1) NOT NULL,
  `language` varchar(255) NOT NULL DEFAULT 'EN',
  `ed2k` text NOT NULL,
  `score_like` int(11) NOT NULL DEFAULT '0',
  `score_bury` int(11) NOT NULL DEFAULT '0',
  `group_id` int(11) NOT NULL DEFAULT '-1',
  `resource_info_id` int(11) NOT NULL DEFAULT '-1',
  `is_spider` int(11) NOT NULL DEFAULT '0',
  `count_distinct` int(11) NOT NULL,
  PRIMARY KEY (`resource_id`),
  UNIQUE KEY `magnet` (`magnet`),
  KEY `hotrank` (`hotrank`),
  KEY `time` (`fetch_time`),
  KEY `resource_info_id` (`resource_info_id`),
  KEY `group_id` (`group_id`),
  FULLTEXT KEY `type` (`typeL1`,`typeL2`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=499119 ;

--
-- 转存表中的数据 `all_resource`
--
-- 使用中 (#13001 - Select on too many rows)

-- --------------------------------------------------------

--
-- 表的结构 `resource_info`
--

CREATE TABLE IF NOT EXISTS `resource_info` (
  `resource_info_id` int(11) NOT NULL AUTO_INCREMENT,
  `resource_id` int(11) DEFAULT '0',
  `typeL1` text NOT NULL,
  `pubdate` datetime DEFAULT NULL,
  `summary` text,
  `country` text,
  `director` text,
  `aka` text,
  `localname` text,
  `sourceURL` text,
  `imgURL` text,
  `rating` int(11) DEFAULT '0',
  `source_site` varchar(255) NOT NULL DEFAULT 'douban',
  `fetch_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`resource_info_id`),
  KEY `resource_id` (`resource_id`),
  KEY `rating` (`rating`),
  KEY `rating_2` (`rating`),
  KEY `fetch_time` (`fetch_time`),
  KEY `source_site` (`source_site`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=84470 ;

