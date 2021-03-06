-- 
-- SQL 
--
CREATE TABLE IF NOT EXISTS `place` ( 
  `uuid` TEXT NOT NULL UNIQUE, 
  `volume` INTEGER NOT NULL, 
  `free_volume` INTEGER NOT NULL,
  `is_empty` BOOLEAN NOT NULL DEFAULT 1,
  `weight` INTEGER NOT NULL DEFAULT 0, 
  PRIMARY KEY(`uuid`)
);
CREATE INDEX IF NOT EXISTS place_idx_volume ON `place`(`volume`);
CREATE INDEX IF NOT EXISTS place_idx_is_empty ON `place`(`is_empty`);
CREATE INDEX IF NOT EXISTS place_idx_weight ON `place`(`weight`);


CREATE TABLE IF NOT EXISTS `cell` (
  `uuid` TEXT NOT NULL UNIQUE, 
  `x_coordinate` INTEGER NOT NULL, 
  `y_coordinate` INTEGER NOT NULL,
  `name` TEXT NOT NULL, --
  `is_empty` BOOLEAN NOT NULL DEFAULT 1,
  PRIMARY KEY(`uuid`)
);

CREATE INDEX IF NOT EXISTS cell_idx_name ON `cell`(`name`);


CREATE TABLE IF NOT EXISTS `place_has_cells` (
  `place_uuid` NOT NULL, 
  `cell_uuid` NOT NULL UNIQUE,
  PRIMARY KEY(`place_uuid`, `cell_uuid`),
  FOREIGN KEY(`place_uuid`) REFERENCES `place`(`uuid`),
  FOREIGN KEY(`cell_uuid`) REFERENCES `cell`(`uuid`)
);

CREATE INDEX IF NOT EXISTS `place_has_cells_idx_place_uuid` ON `place_has_cells`(`place_uuid`);

CREATE TABLE IF NOT EXISTS `thing` (
  `uuid` TEXT NOT NULL UNIQUE,
  `name` TEXT NOT NULL DEFAULT '',
  `mass` INTEGER NOT NULL,
  `width` INTEGER NOT NULL,
  `height` INTEGER NOT NULL,
  `depth`  INTEGER NOT NULL,
  PRIMARY KEY(`uuid`)
);

CREATE TABLE IF NOT EXISTS `place_has_thing` (
  `place_uuid` TEXT NOT NULL UNIQUE,
  `thing_uuid` TEXT NOT NULL UNIQUE,
  PRIMARY KEY(`place_uuid`, `thing_uuid`),
  FOREIGN KEY(`place_uuid`) REFERENCES `place`(`uuid`),
  FOREIGN KEY(`thing_uuid`) REFERENCES `thing`(`uuid`) 
);

CREATE TABLE IF NOT EXISTS `remote_warehouse` (
  `thing_uuid` TEXT NOT NULL UNIQUE,
  PRIMARY KEY(`thing_uuid`),
  FOREIGN KEY(`thing_uuid`) REFERENCES `thing`(`uuid`)
);
