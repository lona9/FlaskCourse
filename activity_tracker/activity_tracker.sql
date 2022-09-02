create table log_date (
  id integer primary key autoincrement,
  entry_date date not null
);

create table activities (
  id integer primary key autoincrement,
  name text not null,
  time numeric not null,
  distance numeric not null,
  calories integer not null
);

create table activity_date (
  activity_id integer not null,
  log_date_id integer not null,
  primary key(activity_id, log_date_id)
);
