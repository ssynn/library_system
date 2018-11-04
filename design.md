# TABLE DESIGN

## student

| SID | PASSWORD | SNAME | DEPARTMENT | MAJOR | LIMIT | PUNISHED |
| :-: | :-: | :-: | :-: | :-: | :-: |:-:|
| char(15) | text | ntext | nchar(20) | nchar(20) | int | int |

## administrator

| AID | passward |
| :--: | :--: |
| char(15) | text |

## book

| BID | BNAME | PUBLICATION_DATE | PRESS | POSITION | NUM |
|:-:|:-:|:-:|:-:|:-:|:-:|
| char(15) | text | char(12) | nchar(20) | char(10) | int |

## classify

| BID | CLASSIFY |
|:-:|:-:|
| char(15) | nchar(20) |

## borrowing_book

| BID | SID | BORROW_DATE |
|:-:|:-:|:-:|
| char(15) | char(15) | char(12) |

## log

| BID | SID | BORROW_DATE | BACK_DATE |
|:-:|:-:|:-:|:-:|
| char(15) | char(15) | char(12) | char(20) |
