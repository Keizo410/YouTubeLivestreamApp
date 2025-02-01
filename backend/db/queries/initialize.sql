drop table if EXISTS livechat_data;

CREATE TABLE IF NOT EXISTS listener (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) unique
);


CREATE TABLE IF NOT EXISTS youtuber (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) unique
);

CREATE TABLE IF NOT EXISTS channel (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) not null unique,
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

INSERT INTO youtuber (name) VALUES ('Youtuber A') on CONFLICT (name) do nothing;

INSERT INTO channel (name, youtuber_id) VALUES 
('Channel 1', 1) on conflict (name, youtuber_id) do nothing;

INSERT INTO listener (name) VALUES ('Listener X') on CONFLICT (name) do nothing;
INSERT INTO listener (name) VALUES ('Listener Y') on CONFLICT (name) do nothing;
INSERT INTO listener (name) VALUES ('Listener Z') on CONFLICT (name) do nothing;

INSERT INTO livestream (currentTime, date, channel_id, listener_id, donation, comment) VALUES
('14:30:00', '2025-01-01', 1, 1, 50.0, 'Great stream!') on CONFLICT (currentTime, donation, comment) do nothing;
INSERT INTO livestream (channel_id, listener_id, donation, comment) VALUES
(1, 1, 5.0, 'Awesome!');
INSERT INTO livestream (channel_id, listener_id, donation, comment) VALUES
(1, 1, 200.0, 'Great stream!');


