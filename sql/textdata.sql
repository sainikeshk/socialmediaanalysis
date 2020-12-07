CREATE SCHEMA IF NOT EXISTS `?` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `?`;
CREATE TABLE `?` (`UniqueID` varchar(128) DEFAULT NULL,`DateTime` datetime NOT NULL,`Source` varchar(64) NOT NULL,`ApplicationName` varchar(128) NOT NULL,`WhatsNew` text,`UpdateDate` datetime NOT NULL,`VersionNo` varchar(32) DEFAULT NULL,`Tag1` varchar(32) DEFAULT NULL,`Tag2` varchar(32) DEFAULT NULL,`Tag3` varchar(32) DEFAULT NULL,`Tag4` varchar(32) DEFAULT NULL,`Tag5` varchar(32) DEFAULT NULL,`Region` varchar(32) NOT NULL,`UserName` varchar(64) NOT NULL,`UserRating` float DEFAULT NULL,`TotalRating` float DEFAULT NULL,`ReviewTitle` text,`Review` text,`Reply` text,`NoOfReviews` bigint(20) DEFAULT NULL,`Helpful` varchar(8) DEFAULT NULL,`Retweets` varchar(8) DEFAULT NULL,`ScoreNeg` float DEFAULT NULL,`ScorePos` float DEFAULT NULL,`ScoreNeu` float DEFAULT NULL,`ScoreCom` float DEFAULT NULL,`Cumulative7Days` bigint(20) DEFAULT NULL,`Cumulative7DaysPos` bigint(20) DEFAULT NULL,`Cumulative7DaysNeg` bigint(20) DEFAULT NULL,`Cumulative7DaysNeu` bigint(20) DEFAULT NULL,`TopicCategory` varchar(128) DEFAULT NULL,`Topic` varchar(170) DEFAULT NULL,`SubTopic` varchar(170) DEFAULT NULL,`Flag` smallint(6) DEFAULT NULL,PRIMARY KEY (`DateTime`,`Source`,`ApplicationName`,`Region`,`UserName`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;