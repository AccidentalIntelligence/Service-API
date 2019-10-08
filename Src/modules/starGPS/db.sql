CREATE OR REPLACE TABLE systems (
    id int not null auto_increment primary key,
    name varchar(128),
    affiliation varchar(128),
    description varchar(1024)
);

CREATE OR REPLACE TABLE locations (
    id int not null auto_increment primary key,
    name varchar(128),
    designation varchar(128),
    description varchar(1024),
    type varchar(24),
    subtype varchar(24),
    parent varchar(128) not null,
    habitable boolean,
    msl float default 0.0,
    atmo float default 0.0,
    om_radius float
)

CREATE OR REPLACE TABLE poi (
    id int not null auto_increment primary key,
    system varchar(128) not null,
    location varchar(128) not null,
    name varchar(56),
    owner varchar(56),
    type varchar(56),
    altitude float,
    coords varchar(56),
    facilities varchar(1024)
)

INSERT INTO locations (
    name,
    designation,
    description,
    type,
    subtype,
    parent,
    habitable,
    MSL,
    Atmo,
    om_radius
) VALUES (
    "Daymar",
    "Stanton 2b",
    "Named after the middle brother of the three siblings featured in the 25th century children’s tale, “A Gift for Baba,” this is the largest of Crusader’s moons. Daymar’s slightly eccentric orbit is said to represent his ease at getting lost in the story.",
    "S",
    "Moon",
    "Crusader",
    0,
    295.5,
    29.5,
    464.5
);

insert into poi (
    system,
    location,
    name,
    owner,
    type,
    altitude,
    coords,
    facilities
) values (
    "Stanton",
    "Daymar",
    "Wolf Point",
    "Crusader Industries",
    "Aid Shelter",
    0.0,
    '{"x":276.443536,"y":-9.384236,"z":103.100625}',
    "Aid Shelter"
)