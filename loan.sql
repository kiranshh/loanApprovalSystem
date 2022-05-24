

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";




CREATE TABLE `data` (
  `id` int(10) UNSIGNED NOT NULL,
  `Email` varchar(20) DEFAULT NULL,
  `Gender` int(11) DEFAULT NULL,
  `Married` int(11) DEFAULT NULL,
  `Dependents` int(11) DEFAULT NULL,
  `Education` int(11) DEFAULT NULL,
  `SelfEmployed` int(11) DEFAULT NULL,
  `ApplicantIncome` int(11) DEFAULT NULL,
  `CoapplicantIncome` int(11) DEFAULT NULL,
  `LoanAmount` int(11) DEFAULT NULL,
  `LoanAmountTerm` int(11) DEFAULT NULL,
  `CreditHistory` int(11) DEFAULT NULL,
  `PropertyArea` int(11) DEFAULT NULL,
  `Label` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



INSERT INTO `data` (`id`, `Email`, `Gender`, `Married`, `Dependents`, `Education`, `SelfEmployed`, `ApplicantIncome`, `CoapplicantIncome`, `LoanAmount`, `LoanAmountTerm`, `CreditHistory`, `PropertyArea`, `Label`) VALUES
(1, 'a@gmail.com', 1, 0, 1, 1, 1, 5000, 2000, 200, 360, 1, 2, 1),
(3, 'c@gmail.com', 1, 0, 0, 1, 1, 5000, 2000, 1000, 360, 1, 2, 0),
(4, 'abcd@gmail.com', 1, 0, 1, 1, 1, 30000, 0, 2000, 360, 1, 1, 0);



CREATE TABLE `users` (
  `id` smallint(5) UNSIGNED NOT NULL,
  `name` varchar(20) NOT NULL,
  `email` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



INSERT INTO `users` (`id`, `name`, `email`, `password`) VALUES
(1, 'abcd', 'abcd@gmail.com', '123456'),
(5, 'dj', 'dj@gmail.com', '1234'),
(6, 'abc', 'abc@gmail.com', '123'),
(9, 'admin', 'admin@gmail.com', 'admin@123'),
(10, 'a', 'a@gmail.com', '12'),
(11, '', '', ''),
(12, 'c', 'c@gmail.com', '12345');


ALTER TABLE `data`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `data`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;


ALTER TABLE `users`
  MODIFY `id` smallint(5) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

