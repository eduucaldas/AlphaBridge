DROP TABLE TOURNAMENT
DROP TABLE PAIR
DROP TABLE CARD
DROP TABLE VULNERABILITY
DROP TABLE POSITION
DROP TABLE BIDDING
DROP TABLE DEAL

CREATE TABLE TOURNAMENT (
  tournament_id INT NOT NULL PRIMARY KEY IDENTITY(1, 1), /*SMALLINT 0..65535*/
  tournament VARCHAR(50));

CREATE TABLE PAIR (
  pair_id INT NOT NULL PRIMARY KEY IDENTITY(1, 1), /*SMALLINT 0..65535*/
  pair VARCHAR(50));

CREATE TABLE CARD (
  card_id INT NOT NULL PRIMARY KEY IDENTITY(1, 1), /*TINYINT 0..255*/
  card VARCHAR(3)); /*VARCHAR(3) for the format "9s", "2c", "Ad", ... */

CREATE TABLE VULNERABILITY (
	vulnerability_id INT NOT NULL PRIMARY KEY IDENTITY(1, 1),
	vulnerability VARCHAR(10));

CREATE TABLE POSITION (
	position_id INT NOT NULL PRIMARY KEY IDENTITY(1, 1),
	position VARCHAR(10));

CREATE TABLE BIDDING (
	bidding_id INT NOT NULL PRIMARY KEY IDENTITY(1, 1), /*SMALLINT 0..65535*/
	bidding VARCHAR(40));

CREATE TABLE DEAL (
	deal_id INT NOT NULL PRIMARY KEY IDENTITY(1, 1), /*INT 0..4294967295 ?MEDIUMINT?*/
	NS_id INT,
	EW_id INT,
	tournament_id INT,
	bidding_id INT,
	leader_id INT,
	dealer_id INT,
	vulnerability_id INT,

	north_card1_id INT,
	north_card2_id INT,
	north_card3_id INT,
	north_card4_id INT,
	north_card5_id INT,
	north_card6_id INT,
	north_card7_id INT,
	north_card8_id INT,
	north_card9_id INT,
	north_card10_id INT,
	north_card11_id INT,
	north_card12_id INT,
	north_card13_id INT,

	south_card1_id INT,
	south_card2_id INT,
	south_card3_id INT,
	south_card4_id INT,
	south_card5_id INT,
	south_card6_id INT,
	south_card7_id INT,
	south_card8_id INT,
	south_card9_id INT,
	south_card10_id INT,
	south_card11_id INT,
	south_card12_id INT,
	south_card13_id INT,

	east_card1_id INT,
	east_card2_id INT,
	east_card3_id INT,
	east_card4_id INT,
	east_card5_id INT,
	east_card6_id INT,
	east_card7_id INT,
	east_card8_id INT,
	east_card9_id INT,
	east_card10_id INT,
	east_card11_id INT,
	east_card12_id INT,
	east_card13_id INT,

	west_card1_id INT,
	west_card2_id INT,
	west_card3_id INT,
	west_card4_id INT,
	west_card5_id INT,
	west_card6_id INT,
	west_card7_id INT,
	west_card8_id INT,
	west_card9_id INT,
	west_card10_id INT,
	west_card11_id INT,
	west_card12_id INT,
	west_card13_id INT,

	played_card1_id INT,
	played_card2_id INT,
	played_card3_id INT,
	played_card4_id INT,
	played_card5_id INT,
	played_card6_id INT,
	played_card7_id INT,
	played_card8_id INT,
	played_card9_id INT,
	played_card10_id INT,
	played_card11_id INT,
	played_card12_id INT,
	played_card13_id INT,
	played_card14_id INT,
	played_card15_id INT,
	played_card16_id INT,
	played_card17_id INT,
	played_card18_id INT,
	played_card19_id INT,
	played_card20_id INT,
	played_card21_id INT,
	played_card22_id INT,
	played_card23_id INT,
	played_card24_id INT,
	played_card25_id INT,
	played_card26_id INT,
	played_card27_id INT,
	played_card28_id INT,
	played_card29_id INT,
	played_card30_id INT,
	played_card31_id INT,
	played_card32_id INT,
	played_card33_id INT,
	played_card34_id INT,
	played_card35_id INT,
	played_card36_id INT,
	played_card37_id INT,
	played_card38_id INT,
	played_card39_id INT,
	played_card40_id INT,
	played_card41_id INT,
	played_card42_id INT,
	played_card43_id INT,
	played_card44_id INT,
	played_card45_id INT,
	played_card46_id INT,
	played_card47_id INT,
	played_card48_id INT,
	played_card49_id INT,
	played_card50_id INT,
	played_card51_id INT,
	played_card52_id INT);

ALTER TABLE DEAL ADD

	FOREIGN KEY (NS_id)
	REFERENCES PAIR (pair_id)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	FOREIGN KEY (EW_id)
	REFERENCES PAIR (pair_id)
	ON DELETE NO ACTION
	ON UPDATE NO ACTION,
	FOREIGN KEY (tournament_id)
	REFERENCES TOURNAMENT (tournament_id)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	FOREIGN KEY (bidding_id)
	REFERENCES BIDDING (bidding_id)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	FOREIGN KEY (leader_id)
	REFERENCES POSITION (position_id)
	ON DELETE NO ACTION
	ON UPDATE NO ACTION,
	FOREIGN KEY (dealer_id)
	REFERENCES POSITION (position_id)
	ON DELETE NO ACTION
	ON UPDATE NO ACTION;
	/*FOREIGN KEY (vulnerability_id)
	REFERENCES VULNERABILITY (vulnerability_id)
	ON DELETE CASCADE
	ON UPDATE CASCADE;*/