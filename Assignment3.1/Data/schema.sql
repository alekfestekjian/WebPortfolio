drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);

drop table if exists reply_entries;
create table reply_entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null

);
