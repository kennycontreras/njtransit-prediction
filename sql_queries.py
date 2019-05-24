
# CREATE TABLES


create_tweet_table = ("""
    CREATE TABLE public.tweets_alert
    (
        start_time bigint,
        datetime timestamp with time zone,
        year int,
        month int,
        day int,
        tweet text
    )
    WITH (
        OIDS = FALSE
    );
""")


# INSERT TABLES


tweets_alert_insert = ("""
    INSERT INTO tweets_alert (start_time, datetime, year, month, day, tweet) \
    VALUES (%s, %s, %s, %s, %s, %s);
""")
