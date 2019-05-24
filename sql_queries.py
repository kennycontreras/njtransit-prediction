
# CREATE TABLES


create_tweet_table = ("""
    CREATE TABLE public.tweets_alert
    (
        start_time bigint,
        datetime timestamp with time zone,
        year int,
        month int,
        day int,
        id_tweet text,
        tweet text
    )
    WITH (
        OIDS = FALSE
    );
""")


"""
DROP TABLE IF EXISTS public.tweets_alert

CREATE TABLE public.tweets_alert
    (
        start_time bigint,
        datetime TIMESTAMP WITH TIME zone,
        YEAR int,
        MONTH int,
        DAY int,
        id_tweet text,
        tweet text
    )
    WITH (
        OIDS = FALSE
    );


ALTER TABLE public.tweets_alert
    OWNER TO student;

"""


# INSERT TABLES


tweets_alert_insert = ("""
    INSERT INTO tweets_alert (start_time, datetime, year, month, day, id_tweet, tweet) \
    VALUES (%s, %s, %s, %s, %s, %s, %s);
""")


# SELECT

tweets_alert_select = ("""
    SELECT MAX(CAST(ID_TWEET AS BIGINT)) AS INT FROM TWEETS_ALERT;
""")
