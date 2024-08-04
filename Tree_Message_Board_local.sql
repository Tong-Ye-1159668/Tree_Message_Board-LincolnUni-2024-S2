CREATE SCHEMA IF NOT EXISTS `tree_message_board` DEFAULT CHARACTER SET utf8 ;
USE `tree_message_board` ;

-- -----------------------------------------------------
-- Tabble `Tree_Message_Board`.`users`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(20) NOT NULL UNIQUE,
  `password_hash` CHAR(64) NOT NULL,
  `email` VARCHAR(320) NOT NULL,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `birth_date` DATE NOT NULL,
  `location` VARCHAR(50) NOT NULL,
  `profile_image` VARCHAR(255) DEFAULT 'default.png',
  role ENUM('member', 'moderator', 'admin') NOT NULL,
  status ENUM('active', 'inactive') NOT NULL,
  PRIMARY KEY (`user_id`));
  
-- -----------------------------------------------------
-- Table `Tree_Message_Board`.`messages`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `messages` (
  `message_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `content` TEXT NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  PRIMARY KEY (`message_id`),
  INDEX `user_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_message_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `tree_message_board`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
    
-- -----------------------------------------------------
-- Table `Tree_Message_Board`.`replies`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `replies` (
  `reply_id` INT NOT NULL AUTO_INCREMENT,
  `message_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `content` TEXT NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  PRIMARY KEY (`reply_id`),
  INDEX `message_idx` (`message_id` ASC) VISIBLE,
  INDEX `user_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_reply_message`
    FOREIGN KEY (`message_id`)
    REFERENCES `tree_message_board`.`messages` (`message_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_reply_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `tree_message_board`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
    