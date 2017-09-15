-- phpMyAdmin SQL Dump
-- version 4.1.4
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Aug 19, 2017 at 02:28 AM
-- Server version: 5.6.15-log
-- PHP Version: 5.5.8

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `khabarnameh`
--
CREATE DATABASE IF NOT EXISTS `khabarnameh` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `khabarnameh`;

-- --------------------------------------------------------

--
-- Table structure for table `city`
--

CREATE TABLE IF NOT EXISTS `city` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `province_id` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_city_province1_idx` (`province_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=441 ;

--
-- Dumping data for table `city`
--

INSERT INTO `city` (`id`, `province_id`, `name`) VALUES
(0, 0, 'شهر را انتخاب کنید.'),
(1, 1, 'تبريز'),
(2, 1, 'كندوان'),
(3, 1, 'بندر شرفخانه'),
(4, 1, 'مراغه'),
(5, 1, 'ميانه'),
(6, 1, 'شبستر'),
(7, 1, 'مرند'),
(8, 1, 'جلفا'),
(9, 1, 'سراب'),
(10, 1, 'هاديشهر'),
(11, 1, 'بناب'),
(12, 1, 'كليبر'),
(13, 1, 'تسوج'),
(14, 1, 'اهر'),
(15, 1, 'هريس'),
(16, 1, 'عجبشير'),
(17, 1, 'هشترود'),
(18, 1, 'ملكان'),
(19, 1, 'بستان آباد'),
(20, 1, 'ورزقان'),
(21, 1, 'اسكو'),
(22, 1, 'آذر شهر'),
(23, 1, 'قره آغاج'),
(24, 1, 'ممقان'),
(25, 1, 'صوفیان'),
(26, 1, 'ایلخچی'),
(27, 1, 'خسروشهر'),
(28, 1, 'باسمنج'),
(29, 1, 'سهند'),
(30, 2, 'اروميه'),
(31, 2, 'نقده'),
(32, 2, 'ماكو'),
(33, 2, 'تكاب'),
(34, 2, 'خوي'),
(35, 2, 'مهاباد'),
(36, 2, 'سر دشت'),
(37, 2, 'چالدران'),
(38, 2, 'بوكان'),
(39, 2, 'مياندوآب'),
(40, 2, 'سلماس'),
(41, 2, 'شاهين دژ'),
(42, 2, 'پيرانشهر'),
(43, 2, 'سيه چشمه'),
(44, 2, 'اشنويه'),
(45, 2, 'چایپاره'),
(46, 2, 'پلدشت'),
(47, 2, 'شوط'),
(48, 3, 'اردبيل'),
(49, 3, 'سرعين'),
(50, 3, 'بيله سوار'),
(51, 3, 'پارس آباد'),
(52, 3, 'خلخال'),
(53, 3, 'مشگين شهر'),
(54, 3, 'مغان'),
(55, 3, 'نمين'),
(56, 3, 'نير'),
(57, 3, 'كوثر'),
(58, 3, 'كيوي'),
(59, 3, 'گرمي'),
(60, 4, 'اصفهان'),
(61, 4, 'فريدن'),
(62, 4, 'فريدون شهر'),
(63, 4, 'فلاورجان'),
(64, 4, 'گلپايگان'),
(65, 4, 'دهاقان'),
(66, 4, 'نطنز'),
(67, 4, 'نايين'),
(68, 4, 'تيران'),
(69, 4, 'كاشان'),
(70, 4, 'فولاد شهر'),
(71, 4, 'اردستان'),
(72, 4, 'سميرم'),
(73, 4, 'درچه'),
(74, 4, 'کوهپایه'),
(75, 4, 'مباركه'),
(76, 4, 'شهرضا'),
(77, 4, 'خميني شهر'),
(78, 4, 'شاهين شهر'),
(79, 4, 'نجف آباد'),
(80, 4, 'دولت آباد'),
(81, 4, 'زرين شهر'),
(82, 4, 'آران و بيدگل'),
(83, 4, 'باغ بهادران'),
(84, 4, 'خوانسار'),
(85, 4, 'مهردشت'),
(86, 4, 'علويجه'),
(87, 4, 'عسگران'),
(88, 4, 'نهضت آباد'),
(89, 4, 'حاجي آباد'),
(90, 4, 'تودشک'),
(91, 4, 'ورزنه'),
(92, 6, 'ايلام'),
(93, 6, 'مهران'),
(94, 6, 'دهلران'),
(95, 6, 'آبدانان'),
(96, 6, 'شيروان چرداول'),
(97, 6, 'دره شهر'),
(98, 6, 'ايوان'),
(99, 6, 'سرابله'),
(100, 7, 'بوشهر'),
(101, 7, 'تنگستان'),
(102, 7, 'دشتستان'),
(103, 7, 'دير'),
(104, 7, 'ديلم'),
(105, 7, 'كنگان'),
(106, 7, 'گناوه'),
(107, 7, 'ريشهر'),
(108, 7, 'دشتي'),
(109, 7, 'خورموج'),
(110, 7, 'اهرم'),
(111, 7, 'برازجان'),
(112, 7, 'خارك'),
(113, 7, 'جم'),
(114, 7, 'کاکی'),
(115, 7, 'عسلویه'),
(116, 7, 'بردخون'),
(117, 8, 'تهران'),
(118, 8, 'ورامين'),
(119, 8, 'فيروزكوه'),
(120, 8, 'ري'),
(121, 8, 'دماوند'),
(122, 8, 'اسلامشهر'),
(123, 8, 'رودهن'),
(124, 8, 'لواسان'),
(125, 8, 'بومهن'),
(126, 8, 'تجريش'),
(127, 8, 'فشم'),
(128, 8, 'كهريزك'),
(129, 8, 'پاكدشت'),
(130, 8, 'چهاردانگه'),
(131, 8, 'شريف آباد'),
(132, 8, 'قرچك'),
(133, 8, 'باقرشهر'),
(134, 8, 'شهريار'),
(135, 8, 'رباط كريم'),
(136, 8, 'قدس'),
(137, 8, 'ملارد'),
(138, 9, 'شهركرد'),
(139, 9, 'فارسان'),
(140, 9, 'بروجن'),
(141, 9, 'چلگرد'),
(142, 9, 'اردل'),
(143, 9, 'لردگان'),
(144, 9, 'سامان'),
(145, 10, 'قائن'),
(146, 10, 'فردوس'),
(147, 10, 'بيرجند'),
(148, 10, 'نهبندان'),
(149, 10, 'سربيشه'),
(150, 10, 'طبس مسینا'),
(151, 10, 'قهستان'),
(152, 10, 'درمیان'),
(153, 11, 'مشهد'),
(154, 11, 'نيشابور'),
(155, 11, 'سبزوار'),
(156, 11, 'كاشمر'),
(157, 11, 'گناباد'),
(158, 11, 'طبس'),
(159, 11, 'تربت حيدريه'),
(160, 11, 'خواف'),
(161, 11, 'تربت جام'),
(162, 11, 'تايباد'),
(163, 11, 'قوچان'),
(164, 11, 'سرخس'),
(165, 11, 'بردسكن'),
(166, 11, 'فريمان'),
(167, 11, 'چناران'),
(168, 11, 'درگز'),
(169, 11, 'كلات'),
(170, 11, 'طرقبه'),
(171, 11, 'سر ولایت'),
(172, 12, 'بجنورد'),
(173, 12, 'اسفراين'),
(174, 12, 'جاجرم'),
(175, 12, 'شيروان'),
(176, 12, 'آشخانه'),
(177, 12, 'گرمه'),
(178, 12, 'ساروج'),
(179, 13, 'اهواز'),
(180, 13, 'ايرانشهر'),
(181, 13, 'شوش'),
(182, 13, 'آبادان'),
(183, 13, 'خرمشهر'),
(184, 13, 'مسجد سليمان'),
(185, 13, 'ايذه'),
(186, 13, 'شوشتر'),
(187, 13, 'انديمشك'),
(188, 13, 'سوسنگرد'),
(189, 13, 'هويزه'),
(190, 13, 'دزفول'),
(191, 13, 'شادگان'),
(192, 13, 'بندر ماهشهر'),
(193, 13, 'بندر امام خميني'),
(194, 13, 'اميديه'),
(195, 13, 'بهبهان'),
(196, 13, 'رامهرمز'),
(197, 13, 'باغ ملك'),
(198, 13, 'هنديجان'),
(199, 13, 'لالي'),
(200, 13, 'رامشیر'),
(201, 13, 'حمیدیه'),
(202, 13, 'دغاغله'),
(203, 13, 'ملاثانی'),
(204, 13, 'شادگان'),
(205, 13, 'ویسی'),
(206, 14, 'زنجان'),
(207, 14, 'ابهر'),
(208, 14, 'خدابنده'),
(209, 14, 'كارم'),
(210, 14, 'ماهنشان'),
(211, 14, 'خرمدره'),
(212, 14, 'ايجرود'),
(213, 14, 'زرين آباد'),
(214, 14, 'آب بر'),
(215, 14, 'قيدار'),
(216, 15, 'سمنان'),
(217, 15, 'شاهرود'),
(218, 15, 'گرمسار'),
(219, 15, 'ايوانكي'),
(220, 15, 'دامغان'),
(221, 15, 'بسطام'),
(222, 16, 'زاهدان'),
(223, 16, 'چابهار'),
(224, 16, 'خاش'),
(225, 16, 'سراوان'),
(226, 16, 'زابل'),
(227, 16, 'سرباز'),
(228, 16, 'نيكشهر'),
(229, 16, 'ايرانشهر'),
(230, 16, 'راسك'),
(231, 16, 'ميرجاوه'),
(232, 17, 'شيراز'),
(233, 17, 'اقليد'),
(234, 17, 'داراب'),
(235, 17, 'فسا'),
(236, 17, 'مرودشت'),
(237, 17, 'خرم بيد'),
(238, 17, 'آباده'),
(239, 17, 'كازرون'),
(240, 17, 'ممسني'),
(241, 17, 'سپيدان'),
(242, 17, 'لار'),
(243, 17, 'فيروز آباد'),
(244, 17, 'جهرم'),
(245, 17, 'ني ريز'),
(246, 17, 'استهبان'),
(247, 17, 'لامرد'),
(248, 17, 'مهر'),
(249, 17, 'حاجي آباد'),
(250, 17, 'نورآباد'),
(251, 17, 'اردكان'),
(252, 17, 'صفاشهر'),
(253, 17, 'ارسنجان'),
(254, 17, 'قيروكارزين'),
(255, 17, 'سوريان'),
(256, 17, 'فراشبند'),
(257, 17, 'سروستان'),
(258, 17, 'ارژن'),
(259, 17, 'گويم'),
(260, 17, 'داريون'),
(261, 17, 'زرقان'),
(262, 17, 'خان زنیان'),
(263, 17, 'کوار'),
(264, 17, 'ده بید'),
(265, 17, 'باب انار/خفر'),
(266, 17, 'بوانات'),
(267, 17, 'خرامه'),
(268, 17, 'خنج'),
(269, 17, 'سیاخ دارنگون'),
(270, 18, 'قزوين'),
(271, 18, 'تاكستان'),
(272, 18, 'آبيك'),
(273, 18, 'بوئين زهرا'),
(274, 19, 'قم'),
(275, 5, 'طالقان'),
(276, 5, 'نظرآباد'),
(277, 5, 'اشتهارد'),
(278, 5, 'هشتگرد'),
(279, 5, 'كن'),
(280, 5, 'آسارا'),
(281, 5, 'شهرک گلستان'),
(282, 5, 'اندیشه'),
(283, 5, 'كرج'),
(284, 5, 'نظر آباد'),
(285, 5, 'گوهردشت'),
(286, 5, 'ماهدشت'),
(287, 5, 'مشکین دشت'),
(288, 20, 'سنندج'),
(289, 20, 'ديواندره'),
(290, 20, 'بانه'),
(291, 20, 'بيجار'),
(292, 20, 'سقز'),
(293, 20, 'كامياران'),
(294, 20, 'قروه'),
(295, 20, 'مريوان'),
(296, 20, 'صلوات آباد'),
(297, 20, 'حسن آباد'),
(298, 21, 'كرمان'),
(299, 21, 'راور'),
(300, 21, 'بابك'),
(301, 21, 'انار'),
(302, 21, 'کوهبنان'),
(303, 21, 'رفسنجان'),
(304, 21, 'بافت'),
(305, 21, 'سيرجان'),
(306, 21, 'كهنوج'),
(307, 21, 'زرند'),
(308, 21, 'بم'),
(309, 21, 'جيرفت'),
(310, 21, 'بردسير'),
(311, 22, 'كرمانشاه'),
(312, 22, 'اسلام آباد غرب'),
(313, 22, 'سر پل ذهاب'),
(314, 22, 'كنگاور'),
(315, 22, 'سنقر'),
(316, 22, 'قصر شيرين'),
(317, 22, 'گيلان غرب'),
(318, 22, 'هرسين'),
(319, 22, 'صحنه'),
(320, 22, 'پاوه'),
(321, 22, 'جوانرود'),
(322, 22, 'شاهو'),
(323, 23, 'ياسوج'),
(324, 23, 'گچساران'),
(325, 23, 'دنا'),
(326, 23, 'دوگنبدان'),
(327, 23, 'سي سخت'),
(328, 23, 'دهدشت'),
(329, 23, 'ليكك'),
(330, 24, 'گرگان'),
(331, 24, 'آق قلا'),
(332, 24, 'گنبد كاووس'),
(333, 24, 'علي آباد كتول'),
(334, 24, 'مينو دشت'),
(335, 24, 'تركمن'),
(336, 24, 'كردكوي'),
(337, 24, 'بندر گز'),
(338, 24, 'كلاله'),
(339, 24, 'آزاد شهر'),
(340, 24, 'راميان'),
(341, 25, 'رشت'),
(342, 25, 'منجيل'),
(343, 25, 'لنگرود'),
(344, 25, 'رود سر'),
(345, 25, 'تالش'),
(346, 25, 'آستارا'),
(347, 25, 'ماسوله'),
(348, 25, 'آستانه اشرفيه'),
(349, 25, 'رودبار'),
(350, 25, 'فومن'),
(351, 25, 'صومعه سرا'),
(352, 25, 'بندرانزلي'),
(353, 25, 'كلاچاي'),
(354, 25, 'هشتپر'),
(355, 25, 'رضوان شهر'),
(356, 25, 'ماسال'),
(357, 25, 'شفت'),
(358, 25, 'سياهكل'),
(359, 25, 'املش'),
(360, 25, 'لاهیجان'),
(361, 25, 'خشک بيجار'),
(362, 25, 'خمام'),
(363, 25, 'لشت نشا'),
(364, 25, 'بندر کياشهر'),
(365, 26, 'خرم آباد'),
(366, 26, 'ماهشهر'),
(367, 26, 'دزفول'),
(368, 26, 'بروجرد'),
(369, 26, 'دورود'),
(370, 26, 'اليگودرز'),
(371, 26, 'ازنا'),
(372, 26, 'نور آباد'),
(373, 26, 'كوهدشت'),
(374, 26, 'الشتر'),
(375, 26, 'پلدختر'),
(376, 27, 'ساري'),
(377, 27, 'آمل'),
(378, 27, 'بابل'),
(379, 27, 'بابلسر'),
(380, 27, 'بهشهر'),
(381, 27, 'تنكابن'),
(382, 27, 'جويبار'),
(383, 27, 'چالوس'),
(384, 27, 'رامسر'),
(385, 27, 'سواد كوه'),
(386, 27, 'قائم شهر'),
(387, 27, 'نكا'),
(388, 27, 'نور'),
(389, 27, 'بلده'),
(390, 27, 'نوشهر'),
(391, 27, 'پل سفيد'),
(392, 27, 'محمود آباد'),
(393, 27, 'فريدون كنار'),
(394, 28, 'اراك'),
(395, 28, 'آشتيان'),
(396, 28, 'تفرش'),
(397, 28, 'خمين'),
(398, 28, 'دليجان'),
(399, 28, 'ساوه'),
(400, 28, 'سربند'),
(401, 28, 'محلات'),
(402, 28, 'شازند'),
(403, 29, 'بندرعباس'),
(404, 29, 'قشم'),
(405, 29, 'كيش'),
(406, 29, 'بندر لنگه'),
(407, 29, 'بستك'),
(408, 29, 'حاجي آباد'),
(409, 29, 'دهبارز'),
(410, 29, 'انگهران'),
(411, 29, 'ميناب'),
(412, 29, 'ابوموسي'),
(413, 29, 'بندر جاسك'),
(414, 29, 'تنب بزرگ'),
(415, 29, 'بندر خمیر'),
(416, 29, 'پارسیان'),
(417, 29, 'قشم'),
(418, 30, 'همدان'),
(419, 30, 'ملاير'),
(420, 30, 'تويسركان'),
(421, 30, 'نهاوند'),
(422, 30, 'كبودر اهنگ'),
(423, 30, 'رزن'),
(424, 30, 'اسدآباد'),
(425, 30, 'بهار'),
(426, 31, 'يزد'),
(427, 31, 'تفت'),
(428, 31, 'اردكان'),
(429, 31, 'ابركوه'),
(430, 31, 'ميبد'),
(431, 31, 'طبس'),
(432, 31, 'بافق'),
(433, 31, 'مهريز'),
(434, 31, 'اشكذر'),
(435, 31, 'هرات'),
(436, 31, 'خضرآباد'),
(437, 31, 'شاهديه'),
(438, 31, 'حمیدیه شهر'),
(439, 31, 'سید میرزا'),
(440, 31, 'زارچ');

-- --------------------------------------------------------

--
-- Table structure for table `collections`
--

CREATE TABLE IF NOT EXISTS `collections` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `system_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `parent` int(11) DEFAULT NULL,
  `left_node` int(11) DEFAULT NULL,
  `right_node` int(11) DEFAULT NULL,
  `parent_col_p4` int(11) DEFAULT NULL,
  `coll_img` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_collections_system1_idx` (`system_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=108 ;

--
-- Dumping data for table `collections`
--

INSERT INTO `collections` (`id`, `system_id`, `name`, `parent`, `left_node`, `right_node`, `parent_col_p4`, `coll_img`) VALUES
(1, 1, 'مجموعه های سیستم', NULL, 0, 7, NULL, NULL),
(4, 1, 'اخبار عمومی', 1, 1, 2, NULL, NULL),
(106, 1, 'اخبار داخلی آسمانه', 1, 3, 4, NULL, NULL),
(107, 1, 'بخشنامه ها', 1, 5, 6, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `collections_roles`
--

CREATE TABLE IF NOT EXISTS `collections_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL,
  `collection_id` int(11) NOT NULL,
  `status` enum('yes','no') DEFAULT 'no',
  PRIMARY KEY (`id`),
  KEY `fk_collections_roles_roles1_idx` (`role_id`),
  KEY `fk_collections_roles_collections1_idx` (`collection_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=156 ;

--
-- Dumping data for table `collections_roles`
--

INSERT INTO `collections_roles` (`id`, `role_id`, `collection_id`, `status`) VALUES
(61, 4, 4, 'no'),
(144, 1, 4, 'no'),
(145, 1, 1, 'no'),
(146, 3, 4, 'no'),
(147, 3, 1, 'no'),
(152, 2, 4, 'yes'),
(153, 2, 106, 'yes'),
(154, 2, 107, 'no'),
(155, 2, 1, 'no');

-- --------------------------------------------------------

--
-- Table structure for table `editors_collections`
--

CREATE TABLE IF NOT EXISTS `editors_collections` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `collection_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_editors_collections_users1_idx` (`user_id`),
  KEY `fk_editors_collections_collections1_idx` (`collection_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `editors_setting`
--

CREATE TABLE IF NOT EXISTS `editors_setting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `edit_news` enum('DISABLE','OWN','ALL') NOT NULL DEFAULT 'OWN',
  `direct_publish` enum('YES','NO') NOT NULL DEFAULT 'NO',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`),
  KEY `fk_editors_setting_users1_idx` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `manager`
--

CREATE TABLE IF NOT EXISTS `manager` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `passwd` varchar(45) NOT NULL,
  `first_name` varchar(45) DEFAULT NULL,
  `last_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `manager`
--

INSERT INTO `manager` (`id`, `username`, `passwd`, `first_name`, `last_name`) VALUES
(1, 'admin', 'bf6217c6113165c413c1f754f8ec02c3', 'مدیرکل', 'سیستم');

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE IF NOT EXISTS `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `system_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `text` text NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('sent','viewed','deleted') NOT NULL DEFAULT 'sent',
  `msg_type` enum('s2u','u2s') NOT NULL DEFAULT 'u2s',
  `type` enum('sms','advice') DEFAULT 'sms',
  PRIMARY KEY (`id`),
  KEY `fk_messages_users1_idx` (`user_id`),
  KEY `fk_messages_system1_idx` (`system_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `news`
--

CREATE TABLE IF NOT EXISTS `news` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `system_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `web_text` text,
  `text` text,
  `_type` enum('notification','news','gallery','important','favorite','instant') NOT NULL DEFAULT 'news',
  `public` tinyint(1) NOT NULL DEFAULT '0',
  `status` enum('PUBLISHED','DRAFT','DISABLED') NOT NULL DEFAULT 'DRAFT',
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `visit` int(11) DEFAULT '0',
  `like` int(11) DEFAULT '0',
  `comment` int(11) DEFAULT '0',
  `news_site_id` varchar(45) DEFAULT NULL,
  `source_news_site` text,
  PRIMARY KEY (`id`),
  KEY `fk_news_users1_idx` (`user_id`),
  KEY `fk_news_system1_idx` (`system_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1659 ;

--
-- Dumping data for table `news`
--

INSERT INTO `news` (`id`, `system_id`, `user_id`, `title`, `web_text`, `text`, `_type`, `public`, `status`, `date`, `visit`, `like`, `comment`, `news_site_id`, `source_news_site`) VALUES
(1652, 1, 1, 'پاتریک مودیانو برنده نوبل ادبیات 2014', '<p>در سالی که انتظار می رفت جایزه ی نوبل ادبیات به میلان کوندرا ،<br />فیلیپ راث و یا هاروکی موراکامی تعلق گیرد در کمال شگفتی پاتریک مودیانو ی فرانسوی<br />برنده ی میدان شد و علاوه بر اعتبار ادبی ، جایزه ی یک میلیون و صد هزار دلاری<br />نقدی نوبل ادبیات را نیز از آن خود کرد . از آن جایی که تا به حال کتابی از<br />مودیانو نخوانده ام قاعدتن نمی توانم در مورد سبک و روش نویسندگی مودیانو چیزی<br />بنویسم ولی من به شخصه بیشتر طرفدار موراکامی هستم اگر چه غنای ادبی کارهای کوندرا<br />را خیلی دوست دارم و حتی از نوشته های تحلیلی اش مثل " هنر رمان " هم<br />بسیار لذت می برم ولی کماکان به خاطر کلیت کارهایی که از موراکامی خوانده ام و<br />بخصوص داستان های کوتاه اش ، که چند تایی از بهترین هایش را می توانید در مجموعه<br />داستان گربه های آدم خوار بخوانید ، ترجیح می دادم موراکامی برنده ی این کارزار<br />باشد . البته این را در حالی می گویم که هنوز مهم ترین اثر موراکامی " کافکا<br />در کرانه " را نخوانده ام . </p>', 'در سالی که انتظار می رفت جایزه ی نوبل ادبیات به میلان کوندرا ، فیلیپ راث و یا هاروکی موراکامی تعلق گیرد در کمال شگفتی پاتریک مودیانو ی فرانسوی برنده ی میدان شد و علاوه بر اعتبار ادبی ، جایزه ی یک میلیون و صد هزار دلاری نقدی نوبل ادبیات را نیز از آن خود کرد . از آن جایی که تا به حال کتابی از مودیانو نخوانده ام قاعدتن نمی توانم در مورد سبک و روش نویسندگی مودیانو چیزی بنویسم ولی من به شخصه بیشتر طرفدار موراکامی هستم اگر چه غنای ادبی کارهای کوندرا را خیلی دوست دارم و حتی از نوشته های تحلیلی اش مثل " هنر رمان " هم بسیار لذت می برم ولی کماکان به خاطر کلیت کارهایی که از موراکامی خوانده ام و بخصوص داستان های کوتاه اش ، که چند تایی از بهترین هایش را می توانید در مجموعه داستان گربه های آدم خوار بخوانید ، ترجیح می دادم موراکامی برنده ی این کارزار باشد . البته این را در حالی می گویم که هنوز مهم ترین اثر موراکامی " کافکا در کرانه " را نخوانده ام . ', 'news', 1, 'PUBLISHED', '2016-01-25 00:28:30', 49, 3, 2, NULL, NULL),
(1653, 1, 1, 'اپ اداره سلامت شهرداری تولید شد', '<p>آسمانه اپ اداره سلامت شهرداری را تولید کرد. برید ببینید کیف کنید.</p>\r\n<p>اینو حسینی از اداره سلامت شهرداری تهران سفارش گرفته.&nbsp;</p>\r\n<p>&nbsp;</p>\r\n<p>&nbsp;</p>', 'آسمانه اپ اداره سلامت شهرداری را تولید کرد. برید ببینید کیف کنید. \r\n اینو حسینی از اداره سلامت شهرداری تهران سفارش گرفته. \r\n \r\n', 'news', 1, 'PUBLISHED', '2016-04-26 06:26:32', 36, 4, 3, NULL, NULL),
(1654, 1, 1, 'شکوفه های ایران، شایسته ی کودکان ایرانی', '<p>جدیدترین محصول تلفن همراه آسمانه با&nbsp;نام &ldquo;شکوفه های ایران&rdquo; قرار است اوقات خوش و آموزنده ای را برای کودکان شما فراهم آورد. این محصول با گرافیکی چشمگیر و خیره کننده بسیاری از مطالب آموزنده را با شیوه ای نوین و جذاب به کودکان ارائه خواهد نمود. جهت اطلاع از چگونگی تهیه این محصول با ما تماس بگیرید.</p>', 'جدیدترین محصول تلفن همراه آسمانه با نام  شکوفه های ایران  قرار است اوقات خوش و آموزنده ای را برای کودکان شما فراهم آورد. این محصول با گرافیکی چشمگیر و خیره کننده بسیاری از مطالب آموزنده را با شیوه ای نوین و جذاب به کودکان ارائه خواهد نمود. جهت اطلاع از چگونگی تهیه این محصول با ما تماس بگیرید.', 'news', 1, 'PUBLISHED', '2016-04-26 07:41:28', 50, 4, 1, NULL, NULL),
(1655, 1, 1, 'تست 1', '<p>تست 1</p>', 'تست 1', 'news', 1, 'PUBLISHED', '2017-02-19 08:22:20', 19, 0, 0, NULL, NULL),
(1656, 1, 1, 'تست 2', '<p>تست 2</p>', 'تست 2', 'news', 1, 'PUBLISHED', '2017-03-04 04:56:38', 7, 0, 0, NULL, NULL),
(1657, 1, 1, 'معرفی نرم افزار به صورت تستی', '<p>این یک نرم افزار کودکانه سالم می باشد&nbsp;این یک نرم افزار کودکانه سالم می باشد&nbsp;این یک نرم افزار کودکانه سالم می باشد&nbsp;این یک نرم افزار کودکانه سالم می باشد&nbsp;این یک نرم افزار کودکانه سالم می باشد&nbsp;این یک نرم افزار کودکانه سالم می باشد&nbsp;این یک نرم افزار کودکانه سالم می باشد&nbsp;این یک نرم افزار کودکانه سالم می باشد&nbsp;این یک نرم افزار کودکانه سالم می باشد&nbsp;این یک نرم افزار کودکانه سالم می باشد&nbsp;این یک نرم افزار کودکانه سالم می باشد&nbsp;این یک نرم افزار کودکانه سالم می باشد&nbsp;این یک نرم افزار کودکانه سالم می باشد&nbsp;این یک نرم افزار کودکانه سالم می باشد&nbsp;این یک نرم افزار کودکانه سالم می باشد&nbsp;</p>', 'این یک نرم افزار کودکانه سالم می باشد این یک نرم افزار کودکانه سالم می باشد این یک نرم افزار کودکانه سالم می باشد این یک نرم افزار کودکانه سالم می باشد این یک نرم افزار کودکانه سالم می باشد این یک نرم افزار کودکانه سالم می باشد این یک نرم افزار کودکانه سالم می باشد این یک نرم افزار کودکانه سالم می باشد این یک نرم افزار کودکانه سالم می باشد این یک نرم افزار کودکانه سالم می باشد این یک نرم افزار کودکانه سالم می باشد این یک نرم افزار کودکانه سالم می باشد این یک نرم افزار کودکانه سالم می باشد این یک نرم افزار کودکانه سالم می باشد این یک نرم افزار کودکانه سالم می باشد', 'news', 1, 'PUBLISHED', '2017-03-07 09:40:13', 10, 0, 0, NULL, NULL),
(1658, 1, 1, 'تست خبر', '<p>oibibovovbo</p>', 'oibibovovbo', 'news', 1, 'PUBLISHED', '2017-05-08 16:10:20', 0, 0, 0, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `news_collections`
--

CREATE TABLE IF NOT EXISTS `news_collections` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `news_id` int(11) NOT NULL,
  `collection_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_news_collections_news1_idx` (`news_id`),
  KEY `fk_news_collections_collections1_idx` (`collection_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=12594 ;

--
-- Dumping data for table `news_collections`
--

INSERT INTO `news_collections` (`id`, `news_id`, `collection_id`) VALUES
(12579, 1652, 4),
(12582, 1654, 106),
(12583, 1653, 106),
(12584, 1655, 4),
(12585, 1656, 4),
(12586, 1656, 106),
(12587, 1656, 107),
(12588, 1656, 1),
(12589, 1657, 4),
(12590, 1657, 4),
(12591, 1657, 4),
(12592, 1658, 4),
(12593, 1658, 106);

-- --------------------------------------------------------

--
-- Table structure for table `news_comments`
--

CREATE TABLE IF NOT EXISTS `news_comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `system_id` int(11) NOT NULL,
  `news_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `text` varchar(150) NOT NULL,
  `confirmed` enum('yes','no') NOT NULL DEFAULT 'no',
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_new_comments_news1_idx` (`news_id`),
  KEY `fk_new_comments_users1_idx` (`user_id`),
  KEY `fk_news_comments_system1_idx` (`system_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=7 ;

-- --------------------------------------------------------

--
-- Table structure for table `news_favorite`
--

CREATE TABLE IF NOT EXISTS `news_favorite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `news_id` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` int(11) NOT NULL,
  `system_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_news_favorite_news1_idx` (`news_id`),
  KEY `fk_news_favorite_users1_idx` (`user_id`),
  KEY `fk_news_favorite_system1_idx` (`system_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

-- --------------------------------------------------------

--
-- Table structure for table `news_file`
--

CREATE TABLE IF NOT EXISTS `news_file` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_name` varchar(45) DEFAULT NULL,
  `file_random_name` varchar(45) DEFAULT NULL,
  `news_id` int(11) NOT NULL,
  `system_id` int(11) NOT NULL,
  `file_type` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_news_file_news1_idx` (`news_id`),
  KEY `fk_news_file_system1_idx` (`system_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `news_file`
--

INSERT INTO `news_file` (`id`, `file_name`, `file_random_name`, `news_id`, `system_id`, `file_type`) VALUES
(2, 'Audi', '82458098951015.mp4', 1653, 1, 'video');

-- --------------------------------------------------------

--
-- Table structure for table `news_likes`
--

CREATE TABLE IF NOT EXISTS `news_likes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `system_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `news_id` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_id_UNIQUE` (`system_id`,`user_id`,`news_id`),
  KEY `fk_news_likes_news1_idx` (`news_id`),
  KEY `fk_news_likes_users1_idx` (`user_id`),
  KEY `fk_news_likes_system1_idx` (`system_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=16 ;

-- --------------------------------------------------------

--
-- Table structure for table `news_link`
--

CREATE TABLE IF NOT EXISTS `news_link` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `link_name` varchar(45) DEFAULT NULL,
  `link_address` text,
  `news_id` int(11) NOT NULL,
  `system_id` int(11) NOT NULL,
  `random_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_news_link_news1_idx` (`news_id`),
  KEY `fk_news_link_system1_idx` (`system_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=21 ;

--
-- Dumping data for table `news_link`
--

INSERT INTO `news_link` (`id`, `link_name`, `link_address`, `news_id`, `system_id`, `random_id`) VALUES
(18, 'وبلاگ مرد مرده ', 'http://dead-notes.com/adbeat/book_entries/985-%D9%BE%D8%A7%D8%AA%D8%B1%DB%8C%DA%A9-%D9%85%D9%88%D8%AF%DB%8C%D8%A7%D9%86%D9%88-%D8%A8%D8%B1%D9%86%D8%AF%D9%87-%DB%8C-%D8%AC%D8%A7%DB%8C%D8%B2%D9%87-%DB%8C-%D9%86%D9%88%D8%A8%D9%84-%D8%A7%D8%AF%D8%A8%DB%8C%D8%A7%D8%AA-2014.html', 1652, 1, '59280861234252850'),
(19, 'آسمانه', 'http://asemanehco.ir/', 1653, 1, '32858082820638692'),
(20, 'آسمانه', 'http://asemanehco.ir/main/', 1654, 1, '96995190898667780');

-- --------------------------------------------------------

--
-- Table structure for table `news_pic`
--

CREATE TABLE IF NOT EXISTS `news_pic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `system_id` int(11) NOT NULL,
  `news_id` int(11) NOT NULL,
  `pic_name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_news_pic_news1_idx` (`news_id`),
  KEY `fk_news_pic_system1_idx` (`system_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=12858 ;

--
-- Dumping data for table `news_pic`
--

INSERT INTO `news_pic` (`id`, `system_id`, `news_id`, `pic_name`) VALUES
(12843, 1, 1652, '66083743144539.jpg'),
(12844, 1, 1652, '57302134470617.jpg'),
(12845, 1, 1652, '79347244047928.jpg'),
(12846, 1, 1652, '87585300575592.jpg'),
(12847, 1, 1652, '11185100154316.jpg'),
(12848, 1, 1653, '26838999715142.jpg'),
(12849, 1, 1654, '66278866684641.jpg'),
(12850, 1, 1654, '71175728519836.jpg'),
(12851, 1, 1654, '30706738086968.jpg'),
(12852, 1, 1655, '12175126280321.jpg'),
(12853, 1, 1656, '26345392309020.jpg'),
(12854, 1, 1657, '69834091832079.png'),
(12855, 1, 1657, '7694747163505.jpg'),
(12856, 1, 1657, '70555176526983.jpg'),
(12857, 1, 1657, '87267881886619.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `news_tag`
--

CREATE TABLE IF NOT EXISTS `news_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `news_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `news_id_UNIQUE` (`news_id`,`tag_id`),
  KEY `fk_news_tag_tags1_idx` (`tag_id`),
  KEY `fk_news_tag_news1_idx` (`news_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=29 ;

--
-- Dumping data for table `news_tag`
--

INSERT INTO `news_tag` (`id`, `news_id`, `tag_id`) VALUES
(14, 1652, 13),
(15, 1652, 14),
(16, 1652, 15),
(26, 1653, 16),
(27, 1653, 17),
(28, 1653, 18),
(23, 1654, 16),
(24, 1654, 19),
(25, 1654, 20);

-- --------------------------------------------------------

--
-- Table structure for table `news_visit`
--

CREATE TABLE IF NOT EXISTS `news_visit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `news_id` int(11) NOT NULL,
  `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` int(11) NOT NULL,
  `system_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_news_visit_news1_idx` (`news_id`),
  KEY `fk_news_visit_users1_idx` (`user_id`),
  KEY `fk_news_visit_system1_idx` (`system_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1166 ;

--
-- Dumping data for table `news_visit`
--

INSERT INTO `news_visit` (`id`, `news_id`, `date`, `user_id`, `system_id`) VALUES
(1011, 1652, '2016-04-26 05:41:16', 20, 1),
(1012, 1652, '2016-04-26 05:56:20', 20, 1),
(1013, 1652, '2016-04-26 05:57:03', 20, 1),
(1094, 1652, '2017-01-17 20:24:04', 20, 1),
(1095, 1652, '2017-01-17 21:44:03', 20, 1),
(1119, 1655, '2017-03-01 17:13:05', 20, 1),
(1120, 1652, '2017-03-01 17:13:28', 20, 1),
(1121, 1652, '2017-03-01 17:14:08', 20, 1),
(1122, 1652, '2017-03-01 17:17:43', 20, 1),
(1123, 1652, '2017-03-01 17:18:52', 20, 1),
(1124, 1652, '2017-03-01 17:22:54', 20, 1),
(1125, 1655, '2017-03-01 18:01:06', 20, 1),
(1126, 1655, '2017-03-01 18:01:27', 20, 1),
(1127, 1652, '2017-03-01 18:01:50', 20, 1),
(1128, 1652, '2017-03-01 18:02:03', 20, 1),
(1129, 1652, '2017-03-01 18:02:10', 20, 1),
(1130, 1652, '2017-03-01 18:02:12', 20, 1),
(1131, 1652, '2017-03-01 18:02:43', 20, 1);

-- --------------------------------------------------------

--
-- Table structure for table `notification_by_type`
--

CREATE TABLE IF NOT EXISTS `notification_by_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `_type` enum('notification','news','gallery','important','favorite','instant') DEFAULT 'news',
  `name` varchar(45) DEFAULT NULL,
  `status` enum('yes','no') DEFAULT 'no',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=7 ;

--
-- Dumping data for table `notification_by_type`
--

INSERT INTO `notification_by_type` (`id`, `_type`, `name`, `status`) VALUES
(1, 'important', 'خبر مهم', 'yes'),
(2, 'instant', 'خبر فوری', 'yes'),
(3, 'notification', 'اطلاعیه', 'yes'),
(4, 'news', 'خبر', 'yes'),
(5, 'favorite', 'خبر برگزیده', 'yes'),
(6, 'gallery', 'گالری عکس', 'no');

-- --------------------------------------------------------

--
-- Table structure for table `permissions`
--

CREATE TABLE IF NOT EXISTS `permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `system_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `perm_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_permissions_users1_idx` (`user_id`),
  KEY `fk_permissions_system1_idx` (`system_id`),
  KEY `fk_permissions_system_permissions1_idx` (`perm_name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1613 ;

--
-- Dumping data for table `permissions`
--

INSERT INTO `permissions` (`id`, `system_id`, `user_id`, `perm_name`) VALUES
(1540, 1, 1, 'dashboard'),
(1541, 1, 1, 'messages::send'),
(1542, 1, 1, 'messages::received'),
(1543, 1, 1, 'messages'),
(1544, 1, 1, 'news::add'),
(1545, 1, 1, 'news::management'),
(1546, 1, 1, 'news::pending'),
(1547, 1, 1, 'news'),
(1548, 1, 1, 'collections::management'),
(1549, 1, 1, 'collections::access_collections'),
(1550, 1, 1, 'collections'),
(1554, 1, 1, 'users::user_management'),
(1555, 1, 1, 'users::add'),
(1556, 1, 1, 'users::roles_management'),
(1557, 1, 1, 'users::user_role_management'),
(1558, 1, 1, 'users::permissions'),
(1559, 1, 1, 'users::editors'),
(1560, 1, 1, 'users'),
(1561, 1, 1, 'poll::poll_insert'),
(1562, 1, 1, 'poll::poll_answer'),
(1563, 1, 1, 'poll'),
(1564, 1, 1, 'comment_pending'),
(1565, 1, 1, 'suggestions'),
(1566, 1, 1, 'setting'),
(1567, 1, 1, 'help'),
(1568, 1, 1, 'messages::sent'),
(1569, 1, 1, 'collections::default_collections'),
(1570, 1, 1, 'users::system_manage_user_guest'),
(1571, 1, 1, 'setting::notification_by_type');

-- --------------------------------------------------------

--
-- Table structure for table `plans`
--

CREATE TABLE IF NOT EXISTS `plans` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `plan_name` varchar(45) NOT NULL,
  `plan_type` enum('public','private') NOT NULL DEFAULT 'public',
  `price` varchar(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `plans`
--

INSERT INTO `plans` (`id`, `plan_name`, `plan_type`, `price`) VALUES
(1, 'سیستم', 'public', '00000'),
(2, 'زیر سیستم', 'public', '00000');

-- --------------------------------------------------------

--
-- Table structure for table `plan_features`
--

CREATE TABLE IF NOT EXISTS `plan_features` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `plan_id` int(11) NOT NULL,
  `max_users` int(11) DEFAULT NULL,
  `active_days` int(11) DEFAULT NULL,
  `sub_system` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_plan_features_plans1_idx` (`plan_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `plan_features`
--

INSERT INTO `plan_features` (`id`, `plan_id`, `max_users`, `active_days`, `sub_system`) VALUES
(1, 1, 10000, 365, 0),
(2, 2, 10000, 365, 0);

-- --------------------------------------------------------

--
-- Table structure for table `plan_permissions`
--

CREATE TABLE IF NOT EXISTS `plan_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `plan_id` int(11) NOT NULL,
  `permission_id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_plan_permissions_plans1_idx` (`plan_id`),
  KEY `fk_plan_permissions_system_permissions1_idx` (`permission_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=73 ;

--
-- Dumping data for table `plan_permissions`
--

INSERT INTO `plan_permissions` (`id`, `plan_id`, `permission_id`) VALUES
(1, 1, 'collections'),
(2, 1, 'collections::access_collections'),
(3, 1, 'collections::management'),
(4, 1, 'comment_pending'),
(5, 1, 'dashboard'),
(6, 1, 'help'),
(7, 1, 'messages'),
(8, 1, 'messages::received'),
(9, 1, 'messages::send'),
(10, 1, 'news'),
(11, 1, 'news::add'),
(12, 1, 'news::management'),
(13, 1, 'news::pending'),
(14, 1, 'poll'),
(15, 1, 'poll::poll_answer'),
(16, 1, 'poll::poll_insert'),
(17, 1, 'suggestions'),
(21, 1, 'users'),
(22, 1, 'users::add'),
(23, 1, 'users::editors'),
(24, 1, 'users::permissions'),
(25, 1, 'users::roles_management'),
(26, 1, 'users::user_management'),
(27, 1, 'users::user_role_management'),
(31, 2, 'collections'),
(32, 2, 'collections::access_collections'),
(33, 2, 'collections::management'),
(34, 2, 'comment_pending'),
(35, 2, 'dashboard'),
(36, 2, 'help'),
(37, 2, 'messages'),
(38, 2, 'messages::received'),
(39, 2, 'messages::send'),
(40, 2, 'news'),
(41, 2, 'news::add'),
(42, 2, 'news::management'),
(43, 2, 'news::pending'),
(44, 2, 'poll'),
(45, 2, 'poll::poll_answer'),
(46, 2, 'poll::poll_insert'),
(47, 2, 'suggestions'),
(48, 2, 'users'),
(49, 2, 'users::add'),
(50, 2, 'users::editors'),
(51, 2, 'users::permissions'),
(52, 2, 'users::roles_management'),
(53, 2, 'users::user_management'),
(54, 2, 'users::user_role_management'),
(55, 1, 'setting'),
(56, 1, 'messages::sent'),
(57, 2, 'messages::sent'),
(59, 1, 'setting::notification_by_type'),
(60, 1, 'users::system_manage_user_guest'),
(61, 1, 'collections::default_collections'),
(62, 2, 'collections::default_collections');

-- --------------------------------------------------------

--
-- Table structure for table `poll_answer`
--

CREATE TABLE IF NOT EXISTS `poll_answer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`,`question_id`),
  KEY `fk_answer_users1_idx` (`user_id`),
  KEY `fk_answer_question1_idx` (`question_id`),
  KEY `fk_answer_item1_idx` (`item_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=18 ;

--
-- Dumping data for table `poll_answer`
--

INSERT INTO `poll_answer` (`id`, `user_id`, `question_id`, `item_id`, `date`) VALUES
(16, 20, 1, 3, '2017-01-17 06:08:04'),
(17, 20, 3, 11, '2017-01-17 06:08:10');

-- --------------------------------------------------------

--
-- Table structure for table `poll_item`
--

CREATE TABLE IF NOT EXISTS `poll_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) NOT NULL,
  `item` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_item_question1_idx` (`question_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=13 ;

--
-- Dumping data for table `poll_item`
--

INSERT INTO `poll_item` (`id`, `question_id`, `item`) VALUES
(1, 1, 'خیلی کم'),
(2, 1, 'کم'),
(3, 1, 'متوسط'),
(4, 1, 'زیاد'),
(5, 1, 'خیلی زیاد'),
(6, 2, '4500 تومان'),
(7, 2, '3500 تومان'),
(8, 2, '1200 تومان'),
(9, 2, 'سه تا 100 تومان'),
(10, 3, 'خیلی'),
(11, 3, 'شونصد میلیون دلار'),
(12, 3, 'دو زار');

-- --------------------------------------------------------

--
-- Table structure for table `poll_question`
--

CREATE TABLE IF NOT EXISTS `poll_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `system_id` int(11) NOT NULL,
  `question` text,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('active','deactive') NOT NULL DEFAULT 'active',
  `parent_question` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_question_system1_idx` (`system_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `poll_question`
--

INSERT INTO `poll_question` (`id`, `system_id`, `question`, `date`, `status`, `parent_question`) VALUES
(1, 1, 'سلام\r\nاین نظر سنجی داخلی آسمانه است\r\nدر مورد اپ پیام رسان\r\nبه نظرتون این اپ می فروشه یا نه؟', '2016-04-26 06:08:09', 'active', 0),
(2, 1, 'سلام\r\nاین نظر سنجی دومه\r\nحدود قیمت محصول نیمه شعبان', '2016-04-26 07:22:33', 'active', 0),
(3, 1, 'به نظرتون خورشید پنهان چقدر می فروشه', '2016-05-03 10:21:50', 'active', 0);

-- --------------------------------------------------------

--
-- Table structure for table `province`
--

CREATE TABLE IF NOT EXISTS `province` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=32 ;

--
-- Dumping data for table `province`
--

INSERT INTO `province` (`id`, `name`) VALUES
(0, 'استان را انتخاب کنید.'),
(1, 'آذربايجان شرقي'),
(2, 'آذربايجان غربي'),
(3, 'اردبيل'),
(4, 'اصفهان'),
(5, 'البرز'),
(6, 'ايلام'),
(7, 'بوشهر'),
(8, 'تهران'),
(9, 'چهارمحال بختياري'),
(10, 'خراسان جنوبي'),
(11, 'خراسان رضوي'),
(12, 'خراسان شمالي'),
(13, 'خوزستان'),
(14, 'زنجان'),
(15, 'سمنان'),
(16, 'سيستان و بلوچستان'),
(17, 'فارس'),
(18, 'قزوين'),
(19, 'قم'),
(20, 'كردستان'),
(21, 'كرمان'),
(22, 'كرمانشاه'),
(23, 'كهكيلويه و بويراحمد'),
(24, 'گلستان'),
(25, 'گيلان'),
(26, 'لرستان'),
(27, 'مازندران'),
(28, 'مركزي'),
(29, 'هرمزگان'),
(30, 'همدان'),
(31, 'يزد');

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE IF NOT EXISTS `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `system_id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `title` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_roles_system1_idx` (`system_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`id`, `system_id`, `name`, `title`) VALUES
(1, 1, 'ADMIN', 'مدیریت کل'),
(2, 1, 'USER', 'کاربر'),
(3, 1, 'EDITOR', 'ویرایشگر'),
(4, 1, 'GUEST', 'مهمان');

-- --------------------------------------------------------

--
-- Table structure for table `settings`
--

CREATE TABLE IF NOT EXISTS `settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(127) DEFAULT NULL,
  `value` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `slider_images`
--

CREATE TABLE IF NOT EXISTS `slider_images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `system_id` int(11) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `image_type` enum('simple','news_link','external_link') DEFAULT 'simple',
  PRIMARY KEY (`id`),
  KEY `fk_slider_images_system1_idx` (`system_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `slider_images`
--

INSERT INTO `slider_images` (`id`, `system_id`, `title`, `name`, `date`, `image_type`) VALUES
(1, 1, '233', '26347670328516.jpg', '2017-07-28 21:05:15', 'simple'),
(4, 1, 'http://127.0.0.1:8850/System/SliderImages', '65763188143926.jpg', '2017-07-28 21:10:30', 'external_link'),
(5, 1, '{"id": 1658, "title": "\\u062a\\u0633\\u062a \\u062e\\u0628\\u0631"}', '32076225544980.jpg', '2017-07-28 21:14:28', 'news_link');

-- --------------------------------------------------------

--
-- Table structure for table `subticket`
--

CREATE TABLE IF NOT EXISTS `subticket` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(1000) DEFAULT NULL,
  `file` varchar(100) DEFAULT NULL,
  `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `type` varchar(45) DEFAULT NULL,
  `tickets_id` int(11) NOT NULL,
  `users_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_subticket_tickets1_idx` (`tickets_id`),
  KEY `fk_subticket_users1_idx` (`users_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `sub_domain`
--

CREATE TABLE IF NOT EXISTS `sub_domain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `site_id` varchar(45) DEFAULT NULL,
  `sub_domain` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `suggestions`
--

CREATE TABLE IF NOT EXISTS `suggestions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `system_id` int(11) NOT NULL,
  `text` varchar(500) DEFAULT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('READ','UNREAD','DELETE') NOT NULL DEFAULT 'UNREAD',
  `read_by` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_suggestions_system1_idx` (`system_id`),
  KEY `fk_suggestions_users1_idx` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

-- --------------------------------------------------------

--
-- Table structure for table `system`
--

CREATE TABLE IF NOT EXISTS `system` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `pname` varchar(255) DEFAULT NULL,
  `pic` varchar(45) DEFAULT NULL,
  `color` varchar(10) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `admin_username` varchar(50) DEFAULT NULL,
  `tel` varchar(20) NOT NULL,
  `province_id` int(11) DEFAULT NULL,
  `city_id` int(11) DEFAULT NULL,
  `status` enum('active','deactive','indebted') NOT NULL DEFAULT 'deactive',
  `confirmed` enum('yes','no') NOT NULL DEFAULT 'yes',
  `reg_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `email` varchar(50) NOT NULL,
  `parent_system_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_system_city1_idx` (`city_id`),
  KEY `fk_system_province1_idx` (`province_id`),
  KEY `fk_system_system1_idx` (`parent_system_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `system`
--

INSERT INTO `system` (`id`, `name`, `pname`, `pic`, `color`, `address`, `admin_username`, `tel`, `province_id`, `city_id`, `status`, `confirmed`, `reg_date`, `email`, `parent_system_id`) VALUES
(1, '', 'خبرنامه', 'new.jpg', '#63A0DD', 'تهران', 'admin_asemaneh', '09179527827', 8, 117, 'active', 'yes', '2015-08-15 22:45:47', '1', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `system_permissions`
--

CREATE TABLE IF NOT EXISTS `system_permissions` (
  `name` varchar(100) NOT NULL,
  `title` varchar(100) DEFAULT NULL,
  `handlers` varchar(500) NOT NULL,
  `url` varchar(100) NOT NULL,
  `default` tinyint(4) NOT NULL DEFAULT '1',
  `icon` varchar(45) DEFAULT NULL,
  `parent` varchar(100) DEFAULT NULL,
  `perm_order` int(11) DEFAULT '0',
  PRIMARY KEY (`name`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `system_permissions`
--

INSERT INTO `system_permissions` (`name`, `title`, `handlers`, `url`, `default`, `icon`, `parent`, `perm_order`) VALUES
('collections', 'مجموعه ها', 'null', '#', 1, NULL, NULL, 60),
('collections::access_collections', 'مجموعه های مجاز هر نقش', '["SystemCollectionRolesHandler"]', 'system_collections_roles', 1, NULL, 'collections', 80),
('collections::default_collections', 'مجموعه های پیش فرض هر نقش', '["SystemDefaultCollectionRolesHandler"]', 'system_default_collections_roles', 1, NULL, 'collections', 85),
('collections::management', 'مدیریت مجموعه ها', '["SystemCollectionsHandler", "SystemCollectionsActionHandler"]', 'system_collections', 1, NULL, 'collections', 70),
('comment_pending', 'نظرات خبرها', '["ShowCommentsHandler"]', 'system_comments', 1, NULL, NULL, 171),
('dashboard', 'داشبورد', '["SystemDashboardHandler"]', 'system_dashboard', 1, NULL, NULL, 10),
('help', 'راهنمای سیستم', '["SystemHelpHandler"]', 'system_help', 1, NULL, NULL, 210),
('messages', 'پیام ها', 'null', '#', 1, NULL, NULL, 11),
('messages::received', 'پیام های دریافتی', '["ReceivedMessagesHandler"]', 'system_messages_received', 1, NULL, 'messages', 13),
('messages::send', 'ارسال پیام جدید', '["SendMessagesHandler"]', 'system_messages_send_new', 1, NULL, 'messages', 12),
('messages::sent', 'پیام های ارسالی', '["SentMessagesHandler"]', 'system_messages_sent', 1, NULL, 'messages', 14),
('news', 'مدیریت خبرها', 'null', '#', 1, NULL, NULL, 20),
('news::add', 'افزودن خبر جدید', '["SystemAddNewsHandler"]', 'system_add_news', 1, NULL, 'news', 30),
('news::management', 'مدیریت خبرها', '["SystemNewsManagementHandler", "SystemNewsEditHandler","GetCollectionsHandler"]', 'system_news_management', 1, NULL, 'news', 40),
('news::pending', 'خبرهای در انتظار تائید', '["SystemPendingNewsHandler"]', 'system_news_waiting', 1, NULL, 'news', 50),
('poll', 'نظرسنجی', 'null', '#', 1, NULL, NULL, 169),
('poll::poll_answer', 'نتیجه نظرسنجی', '["PollResultHandler"]', 'system_poll_result', 1, NULL, 'poll', 187),
('poll::poll_insert', 'ایجاد نظرسنجی', '["PollInsertHandler"]', 'system_poll_insert', 1, NULL, 'poll', 186),
('setting', 'تنظیمات', 'null', '#', 1, NULL, NULL, 200),
('setting::notification_by_type', 'مدیریت اعلان', '["SystemSettingsNotificationHandler"]', 'system_settings_notification', 1, NULL, 'setting', 201),
('suggestions', 'انتقادات و پیشنهادات', '["SuggestionsHandler"]', 'system_suggestions', 1, NULL, NULL, 190),
('users', 'مدیریت کاربران', 'null', '#', 1, NULL, NULL, 110),
('users::add', 'افزودن کاربران جدید', '["SystemUmAddUsersHandler"]', 'system_um_add_users', 1, NULL, 'users', 130),
('users::editors', 'تعریف نویسنده', '["SystemURmEditorManagementHandler"]', 'system_urm_editors', 1, NULL, 'users', 170),
('users::permissions', 'مجوز های دسترسی', '["SystemPermissionsHandler"]', 'system_permissions', 1, NULL, 'users', 160),
('users::roles_management', 'گروه های کاربری سیستم', '["SystemRolesHandler"]', 'system_roles', 1, NULL, 'users', 141),
('users::system_manage_user_guest', 'پروفایل مهمان', '["SystemManageUserGuestHandler"]', 'system_manage_user_guest', 1, NULL, 'users', 151),
('users::user_management', 'لیست کاربران', '["SystemUmAUsersListHandler"]', 'system_um_users_list', 1, NULL, 'users', 120),
('users::user_role_management', 'مدیریت نقش های کاربر', '["SystemUserRolesManagementHandler"]', 'system_user_management_roles', 1, NULL, 'users', 150);

-- --------------------------------------------------------

--
-- Table structure for table `system_plans`
--

CREATE TABLE IF NOT EXISTS `system_plans` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `system_id` int(11) NOT NULL,
  `plan_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_id_UNIQUE` (`system_id`),
  KEY `fk_system_plans_system1_idx` (`system_id`),
  KEY `fk_system_plans_plans1_idx` (`plan_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `system_plans`
--

INSERT INTO `system_plans` (`id`, `system_id`, `plan_id`) VALUES
(1, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `system_plan_features`
--

CREATE TABLE IF NOT EXISTS `system_plan_features` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `system_id` int(11) NOT NULL,
  `max_users` int(11) DEFAULT NULL,
  `active_days` int(11) DEFAULT NULL,
  `sub_system` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_system_plan_fetures_system1_idx` (`system_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `system_plan_features`
--

INSERT INTO `system_plan_features` (`id`, `system_id`, `max_users`, `active_days`, `sub_system`) VALUES
(1, 1, 10000, 365, 0);

-- --------------------------------------------------------

--
-- Table structure for table `tags`
--

CREATE TABLE IF NOT EXISTS `tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `system_id` int(11) NOT NULL,
  `name` varchar(45) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_tags_system1_idx` (`system_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=21 ;

--
-- Dumping data for table `tags`
--

INSERT INTO `tags` (`id`, `system_id`, `name`, `date`) VALUES
(1, 1, 'تگ اول', '2015-10-30 09:05:03'),
(2, 1, 'معاونت بهداشتی', '2015-10-30 20:02:42'),
(3, 1, 'بهداشت مدارس', '2015-10-31 00:05:23'),
(4, 1, 'طرح آهن یاری', '2015-10-31 00:05:23'),
(5, 1, 'بیماران خاص', '2015-10-31 06:13:34'),
(6, 1, 'تالاسمی', '2015-10-31 06:13:34'),
(7, 1, 'ام اس', '2015-10-31 06:13:34'),
(9, 1, 'تست', '2015-11-12 16:17:28'),
(11, 1, 'خبر', '2015-11-30 06:29:06'),
(13, 1, 'رمان', '2016-01-25 00:28:31'),
(14, 1, 'نوبل', '2016-01-25 00:28:31'),
(15, 1, 'معرفی کتاب', '2016-01-25 00:28:31'),
(16, 1, 'اپلیکیشن', '2016-04-26 06:26:32'),
(17, 1, 'سلامت', '2016-04-26 06:26:32'),
(18, 1, 'شهرداری', '2016-04-26 06:26:32'),
(19, 1, 'آسمانه', '2016-04-26 07:41:29'),
(20, 1, 'کودک', '2016-04-26 07:41:29');

-- --------------------------------------------------------

--
-- Table structure for table `tickets`
--

CREATE TABLE IF NOT EXISTS `tickets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic` varchar(250) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `system_id` int(11) NOT NULL,
  `priority` varchar(45) NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_tickets_system1_idx` (`system_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `system_id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `status` enum('active','deactive') NOT NULL DEFAULT 'active',
  PRIMARY KEY (`id`),
  KEY `fk_users_system1_idx` (`system_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=62 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `system_id`, `username`, `password`, `first_name`, `last_name`, `status`) VALUES
(1, 1, 'admin_asemaneh', '35a342c62d3ae54ad5ff16a8a0a75bcae79a6', 'مدیریت', 'سیستم', 'active'),
(20, 1, 'guest', '42d3628c1a1aca0ab7ccc370dd3d99f840b57', 'کاربر', 'مهمان', 'active');

-- --------------------------------------------------------

--
-- Table structure for table `user_collections`
--

CREATE TABLE IF NOT EXISTS `user_collections` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `collection_id` int(11) NOT NULL,
  `device_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_user_collections_users1_idx` (`user_id`),
  KEY `fk_user_collections_collections1_idx` (`collection_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2013 ;

--
-- Dumping data for table `user_collections`
--

INSERT INTO `user_collections` (`id`, `user_id`, `collection_id`, `device_id`) VALUES
(1752, 20, 4, NULL),
(1831, 20, 4, 'a8d3dc245dabd42b'),
(1851, 20, 4, '750b16afa24e6fdc'),
(1855, 20, 4, '8e4e6c40fe1998c'),
(1916, 20, 4, '558b13efd95ff7d0'),
(1976, 20, 4, '4c7df176a00093e4'),
(1979, 20, 4, 'c6c9f001bea3602f'),
(1986, 20, 4, 'd4e4ae5d703f790c'),
(2003, 20, 4, '31213917a80764b3');

-- --------------------------------------------------------

--
-- Table structure for table `user_roles`
--

CREATE TABLE IF NOT EXISTS `user_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_user_roles_users_idx` (`user_id`),
  KEY `fk_user_roles_roles1_idx` (`role_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=385 ;

--
-- Dumping data for table `user_roles`
--

INSERT INTO `user_roles` (`id`, `user_id`, `role_id`) VALUES
(1, 1, 1),
(119, 20, 4);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `city`
--
ALTER TABLE `city`
  ADD CONSTRAINT `fk_city_province1` FOREIGN KEY (`province_id`) REFERENCES `province` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `collections`
--
ALTER TABLE `collections`
  ADD CONSTRAINT `fk_collections_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `collections_roles`
--
ALTER TABLE `collections_roles`
  ADD CONSTRAINT `fk_collections_roles_collections1` FOREIGN KEY (`collection_id`) REFERENCES `collections` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_collections_roles_roles1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `editors_collections`
--
ALTER TABLE `editors_collections`
  ADD CONSTRAINT `fk_editors_collections_collections1` FOREIGN KEY (`collection_id`) REFERENCES `collections` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_editors_collections_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `editors_setting`
--
ALTER TABLE `editors_setting`
  ADD CONSTRAINT `fk_editors_setting_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `fk_messages_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_messages_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `news`
--
ALTER TABLE `news`
  ADD CONSTRAINT `fk_news_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_news_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `news_collections`
--
ALTER TABLE `news_collections`
  ADD CONSTRAINT `fk_news_collections_collections1` FOREIGN KEY (`collection_id`) REFERENCES `collections` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_news_collections_news1` FOREIGN KEY (`news_id`) REFERENCES `news` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `news_comments`
--
ALTER TABLE `news_comments`
  ADD CONSTRAINT `fk_news_comments_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_new_comments_news1` FOREIGN KEY (`news_id`) REFERENCES `news` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_new_comments_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `news_favorite`
--
ALTER TABLE `news_favorite`
  ADD CONSTRAINT `fk_news_favorite_news1` FOREIGN KEY (`news_id`) REFERENCES `news` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_news_favorite_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_news_favorite_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `news_file`
--
ALTER TABLE `news_file`
  ADD CONSTRAINT `fk_news_file_news1` FOREIGN KEY (`news_id`) REFERENCES `news` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_news_file_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `news_likes`
--
ALTER TABLE `news_likes`
  ADD CONSTRAINT `fk_news_likes_news1` FOREIGN KEY (`news_id`) REFERENCES `news` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_news_likes_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_news_likes_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `news_link`
--
ALTER TABLE `news_link`
  ADD CONSTRAINT `fk_news_link_news1` FOREIGN KEY (`news_id`) REFERENCES `news` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_news_link_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `news_pic`
--
ALTER TABLE `news_pic`
  ADD CONSTRAINT `fk_news_pic_news1` FOREIGN KEY (`news_id`) REFERENCES `news` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_news_pic_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `news_tag`
--
ALTER TABLE `news_tag`
  ADD CONSTRAINT `fk_news_tag_news1` FOREIGN KEY (`news_id`) REFERENCES `news` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_news_tag_tags1` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `news_visit`
--
ALTER TABLE `news_visit`
  ADD CONSTRAINT `fk_news_visit_news1` FOREIGN KEY (`news_id`) REFERENCES `news` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_news_visit_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_news_visit_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `permissions`
--
ALTER TABLE `permissions`
  ADD CONSTRAINT `fk_permissions_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_permissions_system_permissions1` FOREIGN KEY (`perm_name`) REFERENCES `system_permissions` (`name`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_permissions_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `plan_features`
--
ALTER TABLE `plan_features`
  ADD CONSTRAINT `fk_plan_features_plans1` FOREIGN KEY (`plan_id`) REFERENCES `plans` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `plan_permissions`
--
ALTER TABLE `plan_permissions`
  ADD CONSTRAINT `fk_plan_permissions_plans1` FOREIGN KEY (`plan_id`) REFERENCES `plans` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_plan_permissions_system_permissions1` FOREIGN KEY (`permission_id`) REFERENCES `system_permissions` (`name`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `poll_answer`
--
ALTER TABLE `poll_answer`
  ADD CONSTRAINT `fk_answer_item1` FOREIGN KEY (`item_id`) REFERENCES `poll_item` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_answer_question1` FOREIGN KEY (`question_id`) REFERENCES `poll_question` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_answer_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `poll_item`
--
ALTER TABLE `poll_item`
  ADD CONSTRAINT `fk_item_question1` FOREIGN KEY (`question_id`) REFERENCES `poll_question` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `poll_question`
--
ALTER TABLE `poll_question`
  ADD CONSTRAINT `fk_question_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `roles`
--
ALTER TABLE `roles`
  ADD CONSTRAINT `fk_roles_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `slider_images`
--
ALTER TABLE `slider_images`
  ADD CONSTRAINT `fk_slider_images_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `subticket`
--
ALTER TABLE `subticket`
  ADD CONSTRAINT `fk_subticket_tickets1` FOREIGN KEY (`tickets_id`) REFERENCES `tickets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_subticket_users1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `suggestions`
--
ALTER TABLE `suggestions`
  ADD CONSTRAINT `fk_suggestions_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_suggestions_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `system`
--
ALTER TABLE `system`
  ADD CONSTRAINT `fk_system_city1` FOREIGN KEY (`city_id`) REFERENCES `city` (`id`) ON DELETE SET NULL ON UPDATE SET NULL,
  ADD CONSTRAINT `fk_system_province1` FOREIGN KEY (`province_id`) REFERENCES `province` (`id`) ON DELETE SET NULL ON UPDATE SET NULL,
  ADD CONSTRAINT `fk_system_system1` FOREIGN KEY (`parent_system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `system_plans`
--
ALTER TABLE `system_plans`
  ADD CONSTRAINT `fk_system_plans_plans1` FOREIGN KEY (`plan_id`) REFERENCES `plans` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_system_plans_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `system_plan_features`
--
ALTER TABLE `system_plan_features`
  ADD CONSTRAINT `fk_system_plan_fetures_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tags`
--
ALTER TABLE `tags`
  ADD CONSTRAINT `fk_tags_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `tickets`
--
ALTER TABLE `tickets`
  ADD CONSTRAINT `fk_tickets_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `fk_users_system1` FOREIGN KEY (`system_id`) REFERENCES `system` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `user_collections`
--
ALTER TABLE `user_collections`
  ADD CONSTRAINT `fk_user_collections_collections1` FOREIGN KEY (`collection_id`) REFERENCES `collections` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_user_collections_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `user_roles`
--
ALTER TABLE `user_roles`
  ADD CONSTRAINT `fk_user_roles_roles1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_user_roles_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
SET FOREIGN_KEY_CHECKS=1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
