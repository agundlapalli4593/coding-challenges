CREATE DATABASE `pulsd_db` /*!40100 DEFAULT CHARACTER SET utf8 */;

CREATE TABLE `tbl_events_log` (
  `event_id` varchar(5000) DEFAULT NULL,
  `status` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `tbl_event` (
  `event_id` varchar(5000) DEFAULT NULL,
  `event_title` varchar(5000) DEFAULT NULL,
  `event_description` varchar(5000) DEFAULT NULL,
  `event_user_id` varchar(5000) DEFAULT NULL,
  `event_date` varchar(5000) DEFAULT NULL,
  `event_time` varchar(5000) DEFAULT NULL,
  `event_location` varchar(5000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `tbl_user` (
  `user_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) DEFAULT NULL,
  `user_username` varchar(45) DEFAULT NULL,
  `user_password` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;


-- Stored PROCEDURE for user creation / sigup
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(20),
    IN p_username VARCHAR(20),
    IN p_password VARCHAR(20)
)
BEGIN
    if ( select exists (select 1 from tbl_user where user_username = p_username) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into tbl_user
        (
            user_name,
            user_username,
            user_password
        )
        values
        (
            p_name,
            p_username,
            p_password
        );
     
    END IF;
END$$
DELIMITER ;
