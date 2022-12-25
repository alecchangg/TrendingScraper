DELETE FROM warehouse.dim_channel
WHERE channel_key<1000;

ALTER TABLE warehouse.dim_channel AUTO_INCREMENT = 1;