-- Step 1: Insert the Youtuber, if not already present
INSERT INTO youtuber (name)
VALUES ('%s')
ON CONFLICT (name) DO NOTHING;

-- Step 2: Insert the Channel linked to the Youtuber (with the correct youtuber_id)
INSERT INTO channel (name, youtuber_id)
VALUES 
    ('%s', (SELECT id FROM youtuber WHERE name = '%s'))
ON CONFLICT (name) DO NOTHING;