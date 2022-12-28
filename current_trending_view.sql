SELECT fact_current_trending.trending_rank, dim_video.name AS video, dim_video.views, dim_video.likes, dim_video.trending_start_date, dim_video.trending_end_date, dim_channel.name AS channel, dim_channel.subscribers, dim_date.date AS "trending date"
FROM warehouse.fact_current_trending
JOIN dim_video ON dim_video.video_key = fact_current_trending.video
JOIN dim_channel ON dim_channel.channel_key = fact_current_trending.channel
JOIN dim_date ON dim_date.date_key = fact_current_trending.date
ORDER BY fact_current_trending.trending_rank ASC;