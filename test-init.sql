-- Test database initialization script

-- Connect to the 'test_codex' database
\c test_codex;

CREATE TABLE IF NOT EXISTS  public.unique_translation_table
(
    id SERIAL PRIMARY KEY,
    source_language text,
    target_language text,
    source_text     text,
    target_text     text,
    source_table_name      text,
    source_comment  text,
    weight          integer,
    description text
);

-- Load data from CSV
COPY public.unique_translation_table(source_language, target_language, source_text, target_text, source_table_name, source_comment, weight)
    FROM '/docker-entrypoint-initdb.d/unique_translation_table.csv'
    DELIMITER ','
    CSV HEADER;

-- Create or replace the available_languages_view
CREATE OR REPLACE VIEW public.available_languages_view(source_language, target_language) AS
SELECT DISTINCT source_language,
                target_language
FROM unique_translation_table
WHERE length(source_language) = 2
  AND length(target_language) = 2;

-- Create or replace the Daitch Mokotoff function

CREATE OR REPLACE FUNCTION dms_diff(code1 TEXT, code2 TEXT)
    RETURNS INTEGER AS
$$
DECLARE
    diff INTEGER := 0;
    i    INTEGER;
BEGIN
    FOR i IN 1..LENGTH(code1)
        LOOP
            IF SUBSTRING(code1, i, 1) != SUBSTRING(code2, i, 1) THEN
                diff := diff + 1;
            END IF;
        END LOOP;
    RETURN diff;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION array_dms_diff(code1 TEXT[], code2 TEXT[])
    RETURNS INTEGER AS
$$
DECLARE
    diff INTEGER := 0;
    i    INTEGER;
BEGIN
    FOR i IN 1..LEAST(array_length(code1, 1), array_length(code2, 1))
        LOOP
            diff := diff + dms_diff(code1[i], code2[i]);
        END LOOP;
    RETURN diff;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION my_daitch_mokotoff(input_string TEXT)
    RETURNS TEXT[] AS
$$
DECLARE
    result       TEXT[] := '{}';
    current_code TEXT   := '';
    i            INTEGER;
    char         TEXT;
    prev_char    TEXT   := '';
BEGIN
    -- Convert input to lowercase
    input_string := LOWER(input_string);

    FOR i IN 1..LENGTH(input_string)
        LOOP
            char := SUBSTRING(input_string FROM i FOR 1);

            -- Apply Daitch-Mokotoff rules (including Cyrillic characters)
            CASE
                -- Vowels (including Cyrillic)
                WHEN char IN ('a', 'e', 'i', 'o', 'u', 'y', 'а', 'е', 'и', 'і', 'о', 'у', 'ы', 'э', 'ю', 'я')
                    THEN IF i = 1 THEN
                        current_code := current_code || '0';
                    END IF;
                -- B sounds
                WHEN char IN ('b', 'б') THEN current_code := current_code || '7';
                -- F, V, W sounds
                WHEN char IN ('f', 'v', 'w', 'ф', 'в') THEN current_code := current_code || '7';
                -- G, K sounds
                WHEN char IN ('g', 'k', 'г', 'к', 'х') THEN current_code := current_code || '5';
                -- H sound
                WHEN char IN ('h', 'г') THEN IF i = 1 OR prev_char IN
                                                         ('a', 'e', 'i', 'o', 'u', 'а', 'е', 'и', 'і', 'о', 'у', 'ы',
                                                          'э', 'ю', 'я') THEN
                    current_code := current_code || '5';
                END IF;
                -- C, J, S, X, Z sounds
                WHEN char IN ('c', 'j', 'q', 's', 'x', 'z', 'ц', 'ч', 'ш', 'щ', 'ж', 'з', 'с')
                    THEN current_code := current_code || '4';
                -- D, T sounds
                WHEN char IN ('d', 't', 'д', 'т') THEN current_code := current_code || '3';
                -- L sound
                WHEN char IN ('l', 'л') THEN current_code := current_code || '8';
                -- M, N sounds
                WHEN char IN ('m', 'n', 'м', 'н') THEN current_code := current_code || '6';
                -- R sound
                WHEN char IN ('r', 'р') THEN current_code := current_code || '9';
                -- P sound
                WHEN char IN ('p', 'п') THEN current_code := current_code || '7';
                ELSE
                -- Ignore other characters
                END CASE;

            -- Keep only the first 6 digits
            IF LENGTH(current_code) > 6 THEN
                current_code := LEFT(current_code, 6);
                EXIT;
            END IF;

            prev_char := char;
        END LOOP;

    -- Pad with zeros if less than 6 digits
    current_code := RPAD(current_code, 6, '0');

    -- Add the code to the result array
    result := result || current_code;

    RETURN result;
END;
$$ LANGUAGE plpgsql;