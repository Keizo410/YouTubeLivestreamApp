drop table if EXISTS livechat_data;

CREATE TABLE IF NOT EXISTS listener (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) unique
);

CREATE TABLE IF NOT EXISTS youtuber (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) unique not null
);

CREATE TABLE IF NOT EXISTS channel (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) not null unique,
    channelId VARCHAR(255) not null unique,
    youtuber_id INTEGER REFERENCES youtuber(id) on delete CASCADE,
    CONSTRAINT unique_channel UNIQUE (name, youtuber_id)
);

CREATE TABLE IF NOT EXISTS livestream (
    id SERIAL PRIMARY KEY,
    currentTime TIME NOT NULL DEFAULT CURRENT_TIME,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    channel_id INTEGER REFERENCES channel(id) on DELETE CASCADE,
    listener_id INTEGER REFERENCES listener(id) on DELETE CASCADE,
    donation FLOAT,
    comment VARCHAR(1028),
    constraint unique_livestream unique (currentTime, donation, comment)
);

INSERT INTO youtuber (name) VALUES ('Unknown') on CONFLICT (name) do nothing;
INSERT INTO youtuber (name) VALUES ('StreamerA') ON CONFLICT (name) DO NOTHING;
INSERT INTO youtuber (name) VALUES ('StreamerB') ON CONFLICT (name) DO NOTHING;

INSERT INTO channel (name, channelId, youtuber_id) VALUES 
('Channel 1', '1', 1) on conflict (name, youtuber_id) do nothing;
INSERT INTO channel (name, channelId, youtuber_id) VALUES ('Channel Alpha', '2', 2) ON CONFLICT (name, youtuber_id) DO NOTHING;
INSERT INTO channel (name, channelId, youtuber_id) VALUES ('Channel Beta', '3', 3) ON CONFLICT (name, youtuber_id) DO NOTHING;

INSERT INTO listener (name) VALUES ('Unknown') on CONFLICT (name) do nothing;
INSERT INTO listener (name) VALUES ('Alice') ON CONFLICT (name) DO NOTHING;
INSERT INTO listener (name) VALUES ('Bob') ON CONFLICT (name) DO NOTHING;
INSERT INTO listener (name) VALUES ('Charlie') ON CONFLICT (name) DO NOTHING;

INSERT INTO livestream (currentTime, date, channel_id, listener_id, donation, comment) VALUES
('14:30:00', '2025-01-01', 1, 1, 50.0, 'Great stream!') on CONFLICT (currentTime, donation, comment) do nothing;
INSERT INTO livestream (channel_id, listener_id, donation, comment) VALUES
(1, 1, 5.0, 'Awesome!');
INSERT INTO livestream (channel_id, listener_id, donation, comment) VALUES
(1, 1, 200.0, 'Great stream!');


INSERT INTO livestream (currentTime, date, channel_id, listener_id, donation, comment) 
VALUES ('10:00:00', '2025-01-01', 1, 2, 25.0, 'Love it!') 
ON CONFLICT (currentTime, donation, comment) DO NOTHING;

INSERT INTO livestream (currentTime, date, channel_id, listener_id, donation, comment) 
VALUES ('11:15:00', '2025-01-02', 2, 3, 100.0, 'Keep going!') 
ON CONFLICT (currentTime, donation, comment) DO NOTHING;

INSERT INTO livestream (currentTime, date, channel_id, listener_id, donation, comment) 
VALUES ('11:45:00', '2025-01-02', 2, 2, 15.0, 'First time here!') 
ON CONFLICT (currentTime, donation, comment) DO NOTHING;

INSERT INTO livestream (currentTime, date, channel_id, listener_id, donation, comment) 
VALUES ('13:00:00', '2025-01-03', 3, 4, 300.0, 'Massive fan!') 
ON CONFLICT (currentTime, donation, comment) DO NOTHING;

INSERT INTO livestream (currentTime, date, channel_id, listener_id, donation, comment) 
VALUES ('13:20:00', '2025-01-03', 3, 2, 50.0, 'Great energy!') 
ON CONFLICT (currentTime, donation, comment) DO NOTHING;

INSERT INTO livestream (channel_id, listener_id, donation, comment) 
VALUES (2, 3, 20.0, 'Super cool!');

INSERT INTO livestream (channel_id, listener_id, donation, comment) 
VALUES (3, 4, 10.0, 'Just dropped by!');

