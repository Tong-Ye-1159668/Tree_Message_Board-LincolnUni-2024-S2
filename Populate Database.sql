USE tree_message_board;

-- -----------------------------------------------------
-- Create Example Users
-- -----------------------------------------------------
-- User passwords are all just the username with "pass" appended:
--
-- User     Password
-- ------   --------
-- member1 member1pass
-- member2, member2pass
-- member3, member3pass
-- member4, member4pass
-- member5, member5pass
-- member6, member6pass
-- member7, member7pass
-- member8, member8pass
-- member9, member9pass
-- member10, member10pass
-- member11, member11pass
-- member12, member12pass
-- member13, member13pass
-- member14, member14pass
-- member15, member15pass
-- member16, member16pass
-- member17, member17pass
-- member18, member18pass
-- member19, member19pass
-- member20, member20pass
-- moderator1, moderator1pass
-- moderator2, moderator2pass
-- moderator3, moderator3pass
-- moderator4, moderator4pass
-- moderator5, moderator5pass
-- admin1, admin1pass
-- admin2, admin2pass
--
-- Hashes were generated using the included password_hash_generator.py script,
-- with the salt 'ExampleSaltValue'.
-- -----------------------------------------------------

INSERT INTO `tree_message_board`.`users` (`username`, `password_hash`, `email`, `first_name`, `last_name`, `birth_date`, `location`, `role`, `status`) VALUES
    ('member1', '54bc0acc7214112f5dd40cb27c0aca349f2916bd34a192994aefcced302afc99', 'member1@example.com', 'Kim', 'Smith', '1962-10-22', 'Nelson', 'member', 'active'),
    ('member2', '7882ffaf2d4e8d2c6a8bad4ee530577675ee1ad5b072384894da98909a479191', 'member2@example.com', 'Adam', 'Elsher', '1982-08-12', 'Gore', 'member', 'active'),
	('member3', 'a76257d3530b3c63f0a639f022cd76945494294adc8a7e652aa9f2dab894f927', 'member3@example.com', 'Tom', 'Solace', '1987-09-20', 'Auckland', 'member', 'active'),
	('member4', '50e06cef6205010b2dc13b7fd5fd961d74d2df10d7e17c1d5da1556ce7f80866', 'member4@example.com', 'Iris', 'Levine', '1986-08-22', 'Hamilton', 'member', 'active'),
    ('member5', '8f2c1ad66212e14e3e4ea747f5b0aa8fbe0491067fbbf49dcae74c6ef19b6de0', 'member5@example.com', 'Penny', 'Thatcher', '1993-07-15', 'Rotorua', 'member', 'active'),
    ('member6', 'c1d80725c3d723b5c44b557b11bf524fc8f13c34b7df63791a2e80430691106b', 'member6@example.com', 'Judy', 'Raven', '1990-03-12', 'Tauranga', 'member', 'active'),
    ('member7', '5d609f6fc79844e7ec2f59a28a17f965e74e673e357f848b2c1cc3cbf1900b98', 'member7@example.com', 'Rebecca', 'Bardot', '1991-02-07', 'Napier', 'member', 'active'),
    ('member8', '6518d511dfb09a4bbc47036cb1ffb6cd0a90d5caca311398491ac08ac3cb35ce', 'member8@example.com', 'Ruby', 'Hansley', '1992-01-05', 'Christchurch', 'member', 'active'),
    ('member9', '4e820c05ba69d7594edb8cca4f0d91c10945f4d60145afd543c467972524b990', 'member9@example.com', 'Correna', 'Cromwell', '1994-05-01', 'Queenstown', 'member', 'active'),
    ('member10', '2941e74a8bbbd51fb3d0ba7c811e3728ea802317a37da0e1e917dcf5b5aa058f', 'member10@example.com', 'Sarah', 'Ashley', '1995-12-02', 'Auckland', 'member', 'active'),
    ('member11', '9c5a9728e332c6fa4462c981f2cd6778173f353474a5380aa7f1540553c3dc65', 'member11@example.com', 'Christine', 'Monroe', '1993-11-05', 'Auckland', 'member', 'active'),
    ('member12', 'd755942dc6133bc8e3d107417d9c57c919eda043e4ea2622f0c815c9c559836f', 'member12@example.com', 'Wendy', 'West', '1990-10-04', 'Auckland', 'member', 'active'),
    ('member13', 'c2f38db274dc066a392f28eca9b0c75d7ce4357ea5dd14c14c4aabcaaa31e453', 'member13@example.com', 'Lily', 'Langley', '1980-10-15', 'Christchurch', 'member', 'active'),
    ('member14', '5ea88ad03d745fd8ddc1bd26fa61a0e38248e88f10a34f6489941ddb48c90ff1', 'member14@example.com', 'Joe', 'Daughtler', '1978-08-12', 'Christchurch', 'member', 'active'),
    ('member15', '0772fca807b0a74adf8cb84429bcb76914cff065df51f6da9f39c2a78d05efbf', 'member15@example.com', 'Todd', 'Madison', '1973-09-27', 'Christchurch', 'member', 'active'),
    ('member16', 'b0609821b0487cba3223af1e9ad0e16b3a8084991f7b528d91fbf8a9e7713814', 'member16@example.com', 'David', 'Marley', '1970-06-28', 'Wellington', 'member', 'active'),
    ('member17', '187269ef0349d18351f5665ba534df9bfb662f82ec8dc655f392f1ecfea1daf6', 'member17@example.com', 'Luca', 'Ellis', '1983-07-17', 'Wellington', 'member', 'active'),
    ('member18', '88a416408a04972670afad619f1bc9b4f53445a28c8317b5c9b37e28602a759b', 'member18@example.com', 'Jack', 'Hope', '1984-09-19', 'Wellington', 'member', 'active'),
    ('member19', '2d9875f152531b2000a3712585e1b0c0f60803e8e4ebdb0d5b7018f1f1fed7f3', 'member19@example.com', 'Leo', 'Cassidy', '1984-08-02', 'Invercargill', 'member', 'active'),
    ('member20', 'f496f45dc0baab895fd671cef90638a2951ea67559e89629a5383e773ad23d2e', 'member20@example.com', 'Beau', 'Lopez', '1992-10-09', 'Invercargill', 'member', 'active'),
    ('moderator1', '9ad390c970da1af0f2fed6b4a978559861ba52e6f8972b295c75f26b4f62dc09', 'moderator1@example.com', 'Leon', 'Jenkins', '1992-09-05', 'Invercargill', 'moderator', 'active'),
    ('moderator2', '4d87d4509541a9669b3bf47833a4214baceaa06fa115993d9b4d16d07bd6f6c1', 'moderator2@example.com', 'Carter', 'Poverly', '1994-02-21', 'No', 'moderator', 'active'),
    ('moderator3', '6de73bcd48d61793713b26987859eb8a4e0397f972b1af50f77d5d38766415f7', 'moderator3@example.com', 'Cooper', 'McKenna', '1991-01-17', 'Mars', 'moderator', 'active'),
    ('moderator4', '124d556de13188267a4ab03ac28ad1185bba5bf88a5376a4dd311472d75206d1', 'moderator4@example.com', 'Isla', 'Gonzales', '1983-11-16', 'USA', 'moderator', 'active'),
    ('moderator5', '5e4290bee5d76dac5291e2de7a4707c225f37cba26c0675fb15f2db605e2801a', 'moderator5@example.com', 'Charles', 'Keller', '1985-12-14', 'Japan', 'moderator', 'active'),
    ('admin1', '01f640a587bdb95de911eca1e72ac6149c4845f037a1677a56daf362110fb19b', 'admin1@example.com', 'Harry', 'Potter', '1990-08-31', 'Hogwarts', 'admin', 'active'),
    ('admin2', '2a11ac7047de69766bd0ea609aaa32a97595e00b388e954e2eb8de6e26eedf6e', 'admin2@example.com', 'James', 'Potter', '1968-08-01', 'UK', 'admin', 'active');
