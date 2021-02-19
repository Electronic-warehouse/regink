-- 
-- SQL 
--

CREATE TABLE IF NOT EXISTS  `block` ( /* Обозначение блока */
  `uuid` TEXT NOT NULL UNIQUE, 
  `volume` INTEGER NOT NULL, 
  `free_volume` INTEGER NOT NULL, 
  `weight` INTEGER NOT NULL, 
  PRIMARY KEY(`uuid`)
);

CREATE TABLE IF NOT EXISTS  `cell` ( /* Обозначение ячейки */
  `uuid` TEXT NOT NULL UNIQUE, 
  `row` INTEGER NOT NULL, 
  `col` INTEGER NOT NULL, 
  `is_empty` INTEGER NOT NULL, 
  PRIMARY KEY(`uuid`)
);

CREATE TABLE IF NOT EXISTS `block_has_cells` ( /* Обозначение если у блока усть ячейка */
  `block_uuid` NOT NULL, 
  `cell_uuid` NOT NULL UNIQUE,
  PRIMARY KEY(`block_uuid`, `cell_uuid`) 
);

CREATE TABLE IF NOT EXISTS `thing` ( /* Обозначение предмета */
  `uuid` TEXT NOT NULL UNIQUE,
  `name` TEXT,
  `mass` INTEGER,
  PRIMARY KEY(`uuid`)
);

CREATE TABLE IF NOT EXISTS `block_has_thing` ( /* Обозначение блока с вещью */
  `block_uuid` TEXT NOT NULL UNIQUE,
  `thing_uuid` TEXT NOT NULL UNIQUE,
  PRIMARY KEY(`block_uuid`, `thing_uuid`)
);

CREATE TABLE IF NOT EXISTS `remote_storage` ( /* Обозначение удалённого склада */
  `thing_uuid` TEXT NOT NULL UNIQUE,
  PRIMARY KEY(`thing_uuid`)
);

