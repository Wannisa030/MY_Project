-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 14, 2023 at 12:20 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rov`
--

-- --------------------------------------------------------

--
-- Table structure for table `provinces`
--

CREATE TABLE `provinces` (
  `code` int(2) NOT NULL,
  `name_th` varchar(150) DEFAULT '',
  `name_th_short` varchar(10) DEFAULT '',
  `name_en` varchar(150) DEFAULT '',
  `geography_id` int(5) DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `provinces`
--

INSERT INTO `provinces` (`code`, `name_th`, `name_th_short`, `name_en`, `geography_id`) VALUES
(10, 'กรุงเทพมหานคร', 'กทม', 'Bangkok', 2),
(11, 'สมุทรปราการ', 'สป', 'Samut Prakan', 2),
(12, 'นนทบุรี', 'นบ', 'Nonthaburi', 2),
(13, 'ปทุมธานี', 'ปท', 'Pathum Thani', 2),
(14, 'พระนครศรีอยุธยา', 'อย', 'Phra Nakhon Si Ayutthaya', 2),
(15, 'อ่างทอง', 'อท', 'Ang Thong', 2),
(16, 'ลพบุรี', 'ลบ', 'Loburi', 2),
(17, 'สิงห์บุรี', 'สห', 'Sing Buri', 2),
(18, 'ชัยนาท', 'ชน', 'Chai Nat', 2),
(19, 'สระบุรี', 'สบ', 'Saraburi', 2),
(20, 'ชลบุรี', 'ชบ', 'Chon Buri', 5),
(21, 'ระยอง', 'รย', 'Rayong', 5),
(22, 'จันทบุรี', 'จบ', 'Chanthaburi', 5),
(23, 'ตราด', 'ตร', 'Trat', 5),
(24, 'ฉะเชิงเทรา', 'ฉท', 'Chachoengsao', 5),
(25, 'ปราจีนบุรี', 'ปจ', 'Prachin Buri', 5),
(26, 'นครนายก', 'นย', 'Nakhon Nayok', 2),
(27, 'สระแก้ว', 'สก', 'Sa Kaeo', 5),
(30, 'นครราชสีมา', 'นม', 'Nakhon Ratchasima', 3),
(31, 'บุรีรัมย์', 'บร', 'Buri Ram', 3),
(32, 'สุรินทร์', 'สร', 'Surin', 3),
(33, 'ศรีสะเกษ', 'ศก', 'Si Sa Ket', 3),
(34, 'อุบลราชธานี', 'อบ', 'Ubon Ratchathani', 3),
(35, 'ยโสธร', 'ยส', 'Yasothon', 3),
(36, 'ชัยภูมิ', 'ชย', 'Chaiyaphum', 3),
(37, 'อำนาจเจริญ', 'อจ', 'Amnat Charoen', 3),
(38, 'หนองบัวลำภู', 'บก', 'Nong Bua Lam Phu', 3),
(39, 'ขอนแก่น', 'นภ', 'Khon Kaen', 3),
(40, 'อุดรธานี', 'ขก', 'Udon Thani', 3),
(41, 'เลย', 'อธ', 'Loei', 3),
(42, 'หนองคาย', 'เลย', 'Nong Khai', 3),
(43, 'มหาสารคาม', 'นค', 'Maha Sarakham', 3),
(44, 'ร้อยเอ็ด', 'มค', 'Roi Et', 3),
(45, 'กาฬสินธุ์', 'รอ', 'Kalasin', 3),
(46, 'สกลนคร', 'กส', 'Sakon Nakhon', 3),
(47, 'นครพนม', 'สน', 'Nakhon Phanom', 3),
(48, 'มุกดาหาร', 'นพ', 'Mukdahan', 3),
(49, 'เชียงใหม่', 'มห', 'Chiang Mai', 1),
(50, 'ลำพูน', 'ชม', 'Lamphun', 1),
(51, 'ลำปาง', 'ลพ', 'Lampang', 1),
(52, 'อุตรดิตถ์', 'ลป', 'Uttaradit', 1),
(53, 'แพร่', 'อด', 'Phrae', 1),
(54, 'น่าน', 'พร', 'Nan', 1),
(55, 'พะเยา', 'นน', 'Phayao', 1),
(56, 'เชียงราย', 'พย', 'Chiang Rai', 1),
(57, 'แม่ฮ่องสอน', 'ชร', 'Mae Hong Son', 1),
(58, 'นครสวรรค์', 'มส', 'Nakhon Sawan', 2),
(60, 'อุทัยธานี', 'นว', 'Uthai Thani', 2),
(61, 'กำแพงเพชร', 'อน', 'Kamphaeng Phet', 2),
(62, 'ตาก', 'กพ', 'Tak', 4),
(63, 'สุโขทัย', 'ตก', 'Sukhothai', 2),
(64, 'พิษณุโลก', 'สท', 'Phitsanulok', 2),
(65, 'พิจิตร', 'พล', 'Phichit', 2),
(66, 'เพชรบูรณ์', 'พจ', 'Phetchabun', 2),
(67, 'ราชบุรี', 'พช', 'Ratchaburi', 4),
(70, 'กาญจนบุรี', 'รบ', 'Kanchanaburi', 4),
(71, 'สุพรรณบุรี', 'กจ', 'Suphan Buri', 2),
(72, 'นครปฐม', 'สพ', 'Nakhon Pathom', 2),
(73, 'สมุทรสาคร', 'นป', 'Samut Sakhon', 2),
(74, 'สมุทรสงคราม', 'สค', 'Samut Songkhram', 2),
(75, 'เพชรบุรี', 'สส', 'Phetchaburi', 4),
(76, 'ประจวบคีรีขันธ์', 'พบ', 'Prachuap Khiri Khan', 4),
(77, 'นครศรีธรรมราช', 'ปข', 'Nakhon Si Thammarat', 6),
(80, 'กระบี่', 'นศ', 'Krabi', 6),
(81, 'พังงา', 'กบ', 'Phangnga', 6),
(82, 'ภูเก็ต', 'พง', 'Phuket', 6),
(83, 'สุราษฎร์ธานี', 'ภก', 'Surat Thani', 6),
(84, 'ระนอง', 'สฎ', 'Ranong', 6),
(85, 'ชุมพร', 'รน', 'Chumphon', 6),
(86, 'สงขลา', 'ชพ', 'Songkhla', 6),
(90, 'สตูล', 'สข', 'Satun', 6),
(91, 'ตรัง', 'สต', 'Trang', 6),
(92, 'พัทลุง', 'ตง', 'Phatthalung', 6),
(93, 'ปัตตานี', 'พท', 'Pattani', 6),
(94, 'ยะลา', 'ปน', 'Yala', 6),
(95, 'นราธิวาส', 'ยล', 'Narathiwat', 6),
(96, 'บึงกาฬ', 'นธ', 'buogkan', 3);

-- --------------------------------------------------------

--
-- Table structure for table `score_result`
--

CREATE TABLE `score_result` (
  `score_id` int(2) NOT NULL,
  `sc_name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `score_result`
--

INSERT INTO `score_result` (`score_id`, `sc_name`) VALUES
(1, 'กรุณาเลือก'),
(2, 'win'),
(3, 'lose'),
(4, 'draw');

-- --------------------------------------------------------

--
-- Table structure for table `tb_hero`
--

CREATE TABLE `tb_hero` (
  `hero_id` int(5) NOT NULL,
  `hero_name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_hero`
--

INSERT INTO `tb_hero` (`hero_id`, `hero_name`) VALUES
(1, 'AIRI'),
(2, 'ALELSTER'),
(3, 'ALICE'),
(4, 'ALLAIN'),
(5, 'AMILY'),
(6, 'ANNETTE'),
(7, 'AOL'),
(8, 'ARDUIN'),
(9, 'ARUM'),
(10, 'ASTRID'),
(11, 'ATA'),
(12, 'AYA'),
(13, 'AZZEN\'KA'),
(14, 'BALDUM'),
(15, 'KAINE'),
(16, 'BRIGHT'),
(17, 'BUTERFLY'),
(18, 'CAPHENY'),
(19, 'CELICA'),
(20, 'CHAUGNAR'),
(21, 'CRESHT'),
(22, 'D\'ARCY'),
(23, 'DEXTRA'),
(24, 'DIAO CHAN'),
(25, 'DIRAK'),
(26, 'ELAND\'ORR'),
(27, 'ELSU'),
(28, 'ENZO'),
(29, 'ERROL'),
(30, 'FENNIK'),
(31, 'FORENTINO'),
(32, 'GILDUR'),
(33, 'GRAKK'),
(34, 'HAYATE'),
(35, 'IGGY'),
(36, 'IGNIS'),
(37, 'ILLUMIA'),
(38, 'ISHAR'),
(39, 'JINNA'),
(40, 'KAHLII'),
(41, 'KEERA'),
(42, 'KIL\'GROTH'),
(43, 'KRIKNAK'),
(44, 'KRIXI'),
(45, 'KRIZZIX'),
(46, 'LAURIEL'),
(47, 'LAVILLE'),
(48, 'LILIANA'),
(49, 'LINDIS'),
(50, 'LORION'),
(51, 'LU BU'),
(52, 'LUMBURR'),
(53, 'MALOCH'),
(54, 'MARJA'),
(55, 'MAX'),
(56, 'MGANGA'),
(57, 'MINA'),
(58, 'MOREN'),
(59, 'MORTOS'),
(60, 'MURAD'),
(61, 'NAKROTH'),
(62, 'NATALYA'),
(63, 'OMEGA'),
(64, 'OMEN'),
(65, 'ORMARR'),
(66, 'PAINE'),
(67, 'PREYTA'),
(68, 'QI'),
(69, 'QUILLEN'),
(70, 'RAZ'),
(71, 'RIKTOR'),
(72, 'ROUIE'),
(73, 'ROURKE'),
(74, 'ROXIE'),
(75, 'RYOMA'),
(76, 'SEPHERA'),
(77, 'SINESTREA'),
(78, 'SKUD'),
(79, 'SLIMZ'),
(80, 'SUPER MAN'),
(81, 'TAARA'),
(82, 'TACHI'),
(83, 'TEEMEE'),
(84, 'TEERI'),
(85, 'TEL\'ANNAS'),
(86, 'THANE'),
(87, 'THE FLASH'),
(88, 'THE JOKER'),
(89, 'THORNE'),
(90, 'TORO'),
(91, 'TULEN'),
(92, 'VALHEIN'),
(93, 'VEERA'),
(94, 'VERES'),
(95, 'VIOLET'),
(96, 'VOLKATH'),
(97, 'WIRO'),
(98, 'WISP'),
(99, 'WONDER WOMAN'),
(100, 'WUKONG'),
(101, 'XENIEL'),
(102, 'Y\'BNETH'),
(103, 'YAN'),
(104, 'YENA'),
(105, 'YORN'),
(106, 'YUE'),
(107, 'ZANIS'),
(108, 'ZATA'),
(109, 'ZEPHYS'),
(110, 'ZILL'),
(111, 'ZIP'),
(112, 'ZUKA'),
(113, 'BONNIE'),
(114, 'BIJAN'),
(115, 'HELEN');

-- --------------------------------------------------------

--
-- Table structure for table `tb_match`
--

CREATE TABLE `tb_match` (
  `match_id` int(5) NOT NULL,
  `kill` int(3) DEFAULT NULL,
  `dead` int(3) DEFAULT NULL,
  `assist` int(3) DEFAULT NULL,
  `money` int(10) DEFAULT NULL,
  `point` float DEFAULT NULL,
  `mvp` int(2) DEFAULT NULL,
  `damage` int(5) DEFAULT NULL,
  `damage_` float DEFAULT NULL,
  `take_damage` int(5) DEFAULT NULL,
  `take_damage_` float DEFAULT NULL,
  `teamfight` int(3) DEFAULT NULL,
  `teamfight_` float DEFAULT NULL,
  `date_match` date DEFAULT NULL,
  `hero_id` int(5) DEFAULT NULL,
  `position_id` int(5) DEFAULT NULL,
  `player_id` int(5) DEFAULT NULL,
  `win` int(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_match`
--

INSERT INTO `tb_match` (`match_id`, `kill`, `dead`, `assist`, `money`, `point`, `mvp`, `damage`, `damage_`, `take_damage`, `take_damage_`, `teamfight`, `teamfight_`, `date_match`, `hero_id`, `position_id`, `player_id`, `win`) VALUES
(216, 6, 6, 1, 13520, 6.7, 0, 76561, 18.6, 71921, 15.1, 7, 41.2, '2023-08-12', 34, 4, 68, 3),
(217, 4, 7, 2, 10031, 5.7, 0, 105747, 25.6, 77549, 16.3, 6, 35.3, '2023-08-12', 62, 3, 69, 3),
(218, 1, 8, 8, 7753, 5.6, 0, 28381, 6.9, 134745, 28.3, 9, 52.9, '2023-08-12', 90, 1, 70, 3),
(219, 6, 4, 5, 17860, 9.5, 1, 133054, 32.3, 69970, 14.7, 11, 64.7, '2023-08-12', 49, 5, 71, 3),
(220, 0, 6, 7, 9945, 5.3, 0, 68547, 16.6, 122558, 25.7, 7, 41.2, '2023-08-12', 53, 2, 72, 3),
(221, 8, 1, 8, 15596, 14.4, 1, 141449, 29.7, 43772, 10.6, 16, 51.6, '2023-08-12', 95, 4, 73, 2),
(222, 4, 4, 12, 11749, 11.9, 0, 81450, 17.1, 127898, 31, 16, 51.6, '2023-08-12', 99, 0, 74, 2),
(223, 6, 7, 9, 12183, 10, 0, 99284, 20.8, 85680, 20.8, 15, 48.4, '2023-08-12', 96, 2, 75, 2),
(224, 8, 2, 9, 12292, 13, 0, 99479, 20.9, 40480, 9.8, 7, 54.8, '2023-08-12', 44, 3, 76, 2),
(225, 5, 3, 15, 12171, 13, 0, 55081, 11.6, 114460, 27.8, 20, 64.5, '2023-08-12', 14, 1, 77, 2),
(226, 3, 5, 3, 7258, 3.7, 0, 45717, 26.1, 47241, 14.6, 6, 60, '2023-08-12', 100, 5, 75, 3),
(227, 1, 5, 0, 6185, 4.2, 0, 21732, 12.4, 92217, 28.4, 1, 10, '2023-08-12', 74, 2, 74, 3),
(228, 1, 6, 4, 4881, 2.3, 0, 27935, 15.9, 46411, 14.3, 5, 50, '2023-08-12', 24, 3, 76, 3),
(229, 4, 7, 4, 7827, 3.7, 0, 56566, 32.3, 53008, 16.3, 8, 80, '2023-08-12', 34, 4, 73, 3),
(230, 1, 7, 6, 6271, 4.3, 1, 23414, 13.4, 85561, 26.4, 7, 70, '2023-08-12', 14, 1, 77, 3),
(231, 4, 3, 11, 9030, 7.3, 0, 54695, 16.9, 35491, 20.2, 15, 50, '2023-08-12', 95, 4, 68, 2),
(232, 7, 3, 6, 7949, 7.5, 0, 43143, 13.3, 23075, 13.2, 13, 43.3, '2023-08-12', 108, 3, 0, 2),
(233, 1, 2, 23, 7877, 10.8, 0, 24392, 7.5, 57498, 32.8, 24, 80, '2023-08-12', 33, 1, 0, 2),
(234, 13, 0, 12, 12751, 15.4, 1, 136914, 42.2, 19551, 11.1, 25, 83.3, '2023-08-12', 89, 4, 71, 2),
(235, 5, 2, 5, 8940, 8.5, 0, 65294, 20.1, 39749, 22.7, 10, 33.3, '2023-08-12', 64, 2, 72, 2);

-- --------------------------------------------------------

--
-- Table structure for table `tb_player`
--

CREATE TABLE `tb_player` (
  `player_id` int(5) NOT NULL,
  `name` varchar(150) DEFAULT NULL,
  `surname` varchar(150) DEFAULT NULL,
  `name_player` varchar(150) DEFAULT NULL,
  `id_gameplayer` varchar(150) DEFAULT NULL,
  `school_id` int(5) DEFAULT NULL,
  `team_id` int(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_player`
--

INSERT INTO `tb_player` (`player_id`, `name`, `surname`, `name_player`, `id_gameplayer`, `school_id`, `team_id`) VALUES
(67, 'a', 'a', 'a', 'a', 8, 20),
(68, 'qq', 'q', 'ᴛғᴅ~ᴜᴊɪx', 'q', 8, 47),
(69, 'w', 'w', 'ᴛғᴅ~ᴡɪᴛᴏᴏɴ', 'w', 8, 47),
(70, 'e', 'r', 'TFD~SAENGSU', 'e', 8, 47),
(71, 'r', 'r', 'ᴛғᴅ~ᴘᴏʀ-ʙʟᴏɢ', 'r', 8, 47),
(72, 't', 't', 'ᴛғᴅ~ᴛᴇᴇʀᴀᴘᴀᴛ', 't', 8, 47),
(73, 'y', 'y', 'DPK.FILM', 'y', 9, 48),
(74, 'u', 'u', 'DPK.BAS', 'u', 9, 48),
(75, 'i', 'i', 'DPK.OOM', 'i', 9, 48),
(76, 'o', 'o', 'DPK.PHOB', 'o', 9, 48),
(77, 'l', 'l', 'DPK.TAR', 'l', 9, 48);

-- --------------------------------------------------------

--
-- Table structure for table `tb_position`
--

CREATE TABLE `tb_position` (
  `position_id` int(5) NOT NULL,
  `position_name` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_position`
--

INSERT INTO `tb_position` (`position_id`, `position_name`) VALUES
(1, 'Romaing'),
(2, 'Off_lane'),
(3, 'Mid_lane'),
(4, 'Safe_lane'),
(5, 'Jungle');

-- --------------------------------------------------------

--
-- Table structure for table `tb_result`
--

CREATE TABLE `tb_result` (
  `result_id` int(5) NOT NULL,
  `round_match` int(2) DEFAULT NULL,
  `date_match` date DEFAULT NULL,
  `resultsA` int(2) DEFAULT NULL,
  `resultsB` int(2) NOT NULL,
  `team_a` int(5) DEFAULT NULL,
  `team_b` int(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_result`
--

INSERT INTO `tb_result` (`result_id`, `round_match`, `date_match`, `resultsA`, `resultsB`, `team_a`, `team_b`) VALUES
(58, 1, '2023-08-12', 3, 2, 47, 48),
(59, 2, '2023-08-12', 3, 2, 48, 47);

-- --------------------------------------------------------

--
-- Table structure for table `tb_schools`
--

CREATE TABLE `tb_schools` (
  `school_id` int(5) NOT NULL,
  `school_name` varchar(150) DEFAULT NULL,
  `city` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_schools`
--

INSERT INTO `tb_schools` (`school_id`, `school_name`, `city`) VALUES
(8, 'ขยัน', 'กรุงเทพมหานคร'),
(9, 'ดีเด่น', 'แม่ฮ่องสอน');

-- --------------------------------------------------------

--
-- Table structure for table `tb_team`
--

CREATE TABLE `tb_team` (
  `team_id` int(5) NOT NULL,
  `team_name` varchar(150) DEFAULT NULL,
  `school_id` int(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_team`
--

INSERT INTO `tb_team` (`team_id`, `team_name`, `school_id`) VALUES
(20, 'No.1', 8),
(47, 'PEPO', 8),
(48, 'REDROOM', 9);

-- --------------------------------------------------------

--
-- Table structure for table `tb_user`
--

CREATE TABLE `tb_user` (
  `user_id` int(5) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_user`
--

INSERT INTO `tb_user` (`user_id`, `username`, `password`) VALUES
(1, 'admin', '123456789');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `provinces`
--
ALTER TABLE `provinces`
  ADD PRIMARY KEY (`code`);

--
-- Indexes for table `score_result`
--
ALTER TABLE `score_result`
  ADD PRIMARY KEY (`score_id`);

--
-- Indexes for table `tb_hero`
--
ALTER TABLE `tb_hero`
  ADD PRIMARY KEY (`hero_id`);

--
-- Indexes for table `tb_match`
--
ALTER TABLE `tb_match`
  ADD PRIMARY KEY (`match_id`);

--
-- Indexes for table `tb_player`
--
ALTER TABLE `tb_player`
  ADD PRIMARY KEY (`player_id`),
  ADD KEY `school_id` (`school_id`),
  ADD KEY `team_id` (`team_id`);

--
-- Indexes for table `tb_position`
--
ALTER TABLE `tb_position`
  ADD PRIMARY KEY (`position_id`);

--
-- Indexes for table `tb_result`
--
ALTER TABLE `tb_result`
  ADD PRIMARY KEY (`result_id`);

--
-- Indexes for table `tb_schools`
--
ALTER TABLE `tb_schools`
  ADD PRIMARY KEY (`school_id`);

--
-- Indexes for table `tb_team`
--
ALTER TABLE `tb_team`
  ADD PRIMARY KEY (`team_id`),
  ADD KEY `school_id` (`school_id`);

--
-- Indexes for table `tb_user`
--
ALTER TABLE `tb_user`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `score_result`
--
ALTER TABLE `score_result`
  MODIFY `score_id` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `tb_hero`
--
ALTER TABLE `tb_hero`
  MODIFY `hero_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=122;

--
-- AUTO_INCREMENT for table `tb_match`
--
ALTER TABLE `tb_match`
  MODIFY `match_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=236;

--
-- AUTO_INCREMENT for table `tb_player`
--
ALTER TABLE `tb_player`
  MODIFY `player_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=79;

--
-- AUTO_INCREMENT for table `tb_position`
--
ALTER TABLE `tb_position`
  MODIFY `position_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `tb_result`
--
ALTER TABLE `tb_result`
  MODIFY `result_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;

--
-- AUTO_INCREMENT for table `tb_schools`
--
ALTER TABLE `tb_schools`
  MODIFY `school_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `tb_team`
--
ALTER TABLE `tb_team`
  MODIFY `team_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `tb_user`
--
ALTER TABLE `tb_user`
  MODIFY `user_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tb_player`
--
ALTER TABLE `tb_player`
  ADD CONSTRAINT `tb_player_ibfk_1` FOREIGN KEY (`school_id`) REFERENCES `tb_schools` (`school_id`),
  ADD CONSTRAINT `tb_player_ibfk_2` FOREIGN KEY (`team_id`) REFERENCES `tb_team` (`team_id`);

--
-- Constraints for table `tb_team`
--
ALTER TABLE `tb_team`
  ADD CONSTRAINT `tb_team_ibfk_1` FOREIGN KEY (`school_id`) REFERENCES `tb_schools` (`school_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
