drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null,
  file text not null
);


drop table if exists reply_entries;
create table reply_entries (
  child_id integer primary key autoincrement,
  parent_id text not null,
  title text not null,
  text text not null,
  file text not null
);


drop table if exists naughty_words;
create table naughty_words (
  naughty_word text not null,
  good_word text not null
);

insert into naughty_words (naughty_word,good_word) values("shit","oops");
insert into naughty_words (naughty_word,good_word) values("poop", "stool");
insert into naughty_words (naughty_word,good_word) values("fuck","shucks");
insert into naughty_words (naughty_word,good_word) values("sucks","is awesome");
