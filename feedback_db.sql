-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Мар 26 2026 г., 21:29
-- Версия сервера: 5.6.51
-- Версия PHP: 7.3.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `feedback_db`
--

-- --------------------------------------------------------

--
-- Структура таблицы `feedbacks`
--

CREATE TABLE `feedbacks` (
  `id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  `user_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `message` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` enum('new','in_progress','completed') COLLATE utf8mb4_unicode_ci DEFAULT 'new',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `feedbacks`
--

INSERT INTO `feedbacks` (`id`, `author_id`, `user_name`, `category`, `message`, `status`, `created_at`, `updated_at`) VALUES
(1, 1, 'qwe', 'partnership', 'jija', 'new', '2026-03-26 11:02:12', '2026-03-26 15:52:10'),
(2, 0, 'kon mix', 'suggestion', 'fffre', 'completed', '2026-03-26 11:12:06', '2026-03-26 11:47:56'),
(3, 1, 'qwe', 'negative', '33', 'new', '2026-03-26 11:13:00', '2026-03-26 15:51:21'),
(4, 1, 'qwe', 'positive', 'asfgjhk', 'new', '2026-03-26 11:13:06', '2026-03-26 16:15:47'),
(5, 1, 'qwe', 'positive', 'as,pdo', 'completed', '2026-03-26 11:13:13', '2026-03-26 16:13:28'),
(6, 1, 'qwe', 'negative', 'asdasfagfdjxcvxcxcxc', 'new', '2026-03-26 11:13:18', '2026-03-26 16:13:23'),
(7, 1, 'qwe', 'error', '12343567w4w5tgedrfg', 'new', '2026-03-26 11:13:25', '2026-03-26 11:13:25'),
(8, 1, 'qwe', 'suggestion', 'asdasdaasfdafg', 'new', '2026-03-26 11:13:40', '2026-03-26 11:13:40'),
(9, 1, 'qwe', 'positive', '123577989787', 'new', '2026-03-26 11:13:45', '2026-03-26 11:13:45'),
(10, 1, 'qwe', 'positive', 'asfavzxcvzxv', 'new', '2026-03-26 11:13:50', '2026-03-26 11:13:50'),
(11, 1, 'qwe', 'suggestion', 'fgljopl,ghpok,fpohgk', 'new', '2026-03-26 11:14:00', '2026-03-26 11:14:00'),
(12, 1, 'qwe', 'suggestion', '12345sdfaSd', 'in_progress', '2026-03-26 11:14:05', '2026-03-26 11:47:49'),
(13, 1, 'qwe', 'Положительный', 'урааааа', 'new', '2026-03-26 11:53:57', '2026-03-26 11:53:57'),
(14, 1, 'qwe', 'Проблема', 'меня булят жосска', 'new', '2026-03-26 12:27:57', '2026-03-26 12:27:57'),
(15, 0, 'kon mix', 'Предложение', 'ddfffff', 'new', '2026-03-26 13:06:48', '2026-03-26 13:06:48'),
(16, 0, 'kon mix', 'Предложение', 'frrrr', 'new', '2026-03-26 13:11:41', '2026-03-26 13:11:41'),
(17, 0, 'asds', 'Положительный', 'fghg', 'new', '2026-03-26 13:14:02', '2026-03-26 13:14:02'),
(18, 0, 'прикол', 'Положительный', 'да', 'new', '2026-03-26 13:18:52', '2026-03-26 13:18:52'),
(19, 0, 'прикол', 'Положительный', 'да', 'new', '2026-03-26 13:19:10', '2026-03-26 13:19:10'),
(20, 0, 'прикол', 'Положительный', 'да', 'new', '2026-03-26 13:19:50', '2026-03-26 13:19:50'),
(21, 0, 'прикол', 'Положительный', 'да', 'new', '2026-03-26 13:20:07', '2026-03-26 13:20:07'),
(22, 0, 'прикол', 'Положительный', 'да', 'new', '2026-03-26 13:20:24', '2026-03-26 13:20:24'),
(23, 0, 'прикол', 'Положительный', 'да', 'new', '2026-03-26 13:26:01', '2026-03-26 13:26:01'),
(24, 0, 'прикол', 'Положительный', 'да', 'new', '2026-03-26 13:26:25', '2026-03-26 13:26:25'),
(25, 0, 'прикол', 'Положительный', 'да', 'new', '2026-03-26 13:26:58', '2026-03-26 13:26:58'),
(26, 0, 'прикол', 'Положительный', 'да', 'new', '2026-03-26 13:27:39', '2026-03-26 13:27:39'),
(27, 0, 'прикол', 'Положительный', 'да', 'new', '2026-03-26 13:27:56', '2026-03-26 13:27:56'),
(28, 0, 'прикол', 'Положительный', 'да', 'new', '2026-03-26 13:28:05', '2026-03-26 13:28:05'),
(29, 0, 'прикол', 'Положительный', 'да', 'in_progress', '2026-03-26 13:28:13', '2026-03-26 14:12:46'),
(30, 0, 'прикол', 'Положительный', 'да', 'new', '2026-03-26 13:28:19', '2026-03-26 14:12:36'),
(31, 0, 'прикол', 'Положительный', 'да', 'in_progress', '2026-03-26 13:28:53', '2026-03-26 14:12:25'),
(32, 0, 'прикол', 'Положительный', 'да', 'in_progress', '2026-03-26 13:30:19', '2026-03-26 15:03:01'),
(33, 0, 'ff', 'Положительный', 'aa', 'new', '2026-03-26 13:32:44', '2026-03-26 15:03:03'),
(34, 0, 'sd', 'Предложение', 'a', 'completed', '2026-03-26 13:34:10', '2026-03-26 13:55:41'),
(35, 0, 'www', 'Положительный', 'qqq', 'in_progress', '2026-03-26 15:12:31', '2026-03-26 15:46:57'),
(36, 1, 'qwe', 'Проблема', 'dddfggg', 'completed', '2026-03-26 15:12:48', '2026-03-26 18:27:31');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` int(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `last_login` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `username`, `password_hash`, `role`, `created_at`, `last_login`) VALUES
(0, 'anon', '', 0, '2026-03-26 11:04:31', NULL),
(1, 'qwe', 'scrypt:32768:8:1$B3jvEpVjDcOX4gn8$e5937e9207f38c26c88d10f83ad84b89712390b955b8528287caab031754353c34ec73df83e5988f40aec0d6cf8a023d0d1dff35bcde92a79fb5d3ea041c7d35', 0, '2026-03-26 10:47:34', '2026-03-26 18:21:09'),
(3, 'admin', 'scrypt:32768:8:1$h7iq6pnyXnNBWIdt$0fecf944d916cfec20663c8079659f264da9dd13a4ab554c73c1dae67d940f903e15b955efaa31bd4ef3ca4017e6cd2c720b7125cbc4dad7fea2246f2dfe071f', 1, '2026-03-26 11:44:11', '2026-03-26 18:19:38'),
(4, 'asd', 'scrypt:32768:8:1$TdL4erCdbvCQ5Pc7$21cce8d726aff9d3946d0c95edf44caa95f1a02e08bbf76f5863c7efeda7c0b7439bb6b88383585220084162bb9ce423f05aa23f0fe13724285b17046cb80a59', 1, '2026-03-26 16:03:05', '2026-03-26 16:04:19');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `feedbacks`
--
ALTER TABLE `feedbacks`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_author_id` (`author_id`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_category` (`category`),
  ADD KEY `idx_created_at` (`created_at`),
  ADD KEY `idx_status_created` (`status`,`created_at`),
  ADD KEY `idx_author_status` (`author_id`,`status`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `feedbacks`
--
ALTER TABLE `feedbacks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `feedbacks`
--
ALTER TABLE `feedbacks`
  ADD CONSTRAINT `fk_feedbacks_author` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
