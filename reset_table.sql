DELETE FROM warehouse.dim_video
WHERE video_key<1000;

ALTER TABLE warehouse.dim_video AUTO_INCREMENT = 1;