# TABLE DESIGN

## student

| <u>SID</u> | PASSWORD | SNAME | DEPARTMENT | MAJOR | MAX | PUNISHED |
| :-: | :-: | :-: | :-: | :-: | :-: |:-:|
| char(15) | char(70) | ntext | nchar(20) | nchar(20) | int | int |

## administrator

| AID | PASSWORD |
| :--: | :--: |
| char(15) | char(70) |

## book

| <u>BID</u> | BNAME | AUTHOR | PUBLICATION_DATE | PRESS | POSITION | SUM | NUM |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| char(15) | ntext | ntext | char(12) | nchar(20) | char(10) | int | int |

## classify

| <u>BID</u> | <u>CLASSIFY</u> |
|:-:|:-:|
| char(15) | nchar(20) |

## borrowing_book

| <u>BID</u> | <u>SID</u> | <u>BORROW_DATE</u> | PUNISH |
|:-:|:-:|:-:|:-:|
| char(15) | char(15) | char(12) | int |

## log

| <u>BID</u> | <u>SID</u> | <u>BORROW_DATE</u> | BACK_DATE |
|:-:|:-:|:-:|:-:|
| char(15) | char(15) | char(12) | char(20) |
