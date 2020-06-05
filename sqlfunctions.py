sql_functions = """
CREATE EXTENSION IF NOT EXISTS dblink;
CREATE OR REPLACE FUNCTION create_database() RETURNS void AS
$$
	BEGIN
		IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'tanksdatabase') THEN
			PERFORM dblink_exec('dbname=postgres user=postgres password=postgres',
			'CREATE DATABASE tanksdatabase');
		END IF;
	END
$$
LANGUAGE plpgsql;


CREATE EXTENSION IF NOT EXISTS dblink;
CREATE OR REPLACE FUNCTION delete_database() RETURNS void AS
$$
	BEGIN
		PERFORM dblink_exec('dbname=postgres user=postgres password=postgres',
		'DROP DATABASE IF EXISTS tanksdatabase');
	END
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION create_accounts_info() RETURNS void AS
$$
	BEGIN
			CREATE TABLE IF NOT EXISTS accounts(
			id integer PRIMARY KEY,
			nickname text NOT NULL,
			battles_amount integer NOT NULL,
			average_damage integer NOT NULL,
			clan text NOT NULL,
			tanks_amount integer NOT NULL,
			events_amount integer NOT NULL DEFAULT 0);

			CREATE INDEX on accounts(nickname);
	END
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION create_event_info() RETURNS void AS
$$
	BEGIN
			CREATE TABLE IF NOT EXISTS event(
			id integer PRIMARY KEY,
			event_name text NOT NULL,
			event_prize integer NOT NULL,
			account_id integer NOT NULL);

			CREATE INDEX on event(event_name);
            
			CREATE TRIGGER event_id_handler
			AFTER INSERT OR UPDATE OR DELETE ON
			event FOR EACH ROW EXECUTE PROCEDURE update_events_amount();
	END
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_accounts()
RETURNS TABLE(id integer,
			  nickname text,
			  battles_amount integer,
			  average_damage integer,
			  clan text,
			  tanks_amount integer,
			  events_amount integer)
AS
$func$
    BEGIN
        RETURN QUERY
        SELECT * FROM accounts;
    END
$func$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_events()
RETURNS TABLE(id integer,
			  event_name text,
			  event_prize integer,
			  account_id integer)
AS
$func$
    BEGIN
        RETURN QUERY
        SELECT * FROM event;
    END
$func$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION clear_accounts()
RETURNS void AS
$$
    BEGIN
        DELETE FROM accounts;
    END
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION clear_events()
RETURNS void AS
$$
    BEGIN
        DELETE FROM event;
    END
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION add_account(
              id integer,
			  nickname text,
			  battles_amount integer,
			  average_damage integer,
			  clan text,
			  tanks_amount integer,
			  events_amount integer)
RETURNS void AS
$$
    BEGIN
        INSERT INTO accounts VALUES
        (id, nickname, battles_amount, average_damage, clan, tanks_amount, events_amount) ON CONFLICT DO NOTHING;
    END
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION add_event(
              id integer,
			  event_name text,
			  event_prize integer,
			  account_id integer)
RETURNS void AS
$$
    BEGIN
        INSERT INTO event VALUES(id, event_name, event_prize, account_id) ON CONFLICT DO NOTHING;
    END
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION edit_account(
	          old_id integer,
			  new_nickname text,
			  new_battles_amount integer,
			  new_average_damage integer,
			  new_clan text,
			  new_tanks_amount integer,
			  new_events_amount integer)
RETURNS void AS
$$
    BEGIN
        UPDATE accounts
        SET nickname = new_nickname,
            battles_amount = new_battles_amount,
            average_damage = new_average_damage,
            clan = new_clan,
            tanks_amount = new_tanks_amount,
            events_amount = new_events_amount
        WHERE id = old_id;
    END
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION edit_event(
	          old_id integer,
			  new_event_name text,
			  new_event_prize integer,
			  new_account_id integer)
RETURNS void AS
$$
    BEGIN
        UPDATE event
        SET event_name = new_event_name,
            event_prize = new_event_prize,
            account_id = new_account_id
        WHERE id = old_id;
    END
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION find_account(nick_for_finding text)
RETURNS TABLE(id integer,
			  nickname text,
			  battles_amount integer,
			  average_damage integer,
			  clan text,
			  tanks_amount integer,
			  events_amount integer)
AS
$func$
    BEGIN
        RETURN QUERY
        SELECT * FROM accounts accs WHERE accs.nickname = nick_for_finding;
    END
$func$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION find_event(event_name_for_finding text)
RETURNS TABLE(id integer,
			  event_name text,
			  event_prize integer,
			  account_id integer)
AS
$func$
    BEGIN
        RETURN QUERY
        SELECT * FROM event ev WHERE ev.event_name = event_name_for_finding;
    END
$func$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_account_by_id(id_for_finding integer)
RETURNS void AS
$$
    BEGIN
        DELETE FROM accounts WHERE id = id_for_finding;
    END
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_account_by_nickname(nickname_for_finding text)
RETURNS void AS
$$
    BEGIN
        DELETE FROM accounts WHERE nickname = nickname_for_finding;
    END
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_event_by_id(id_for_finding integer)
RETURNS void AS
$$
    BEGIN
        DELETE FROM event WHERE id = id_for_finding;
    END
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_event_by_name(name_for_finding text)
RETURNS void AS
$$
    BEGIN
        DELETE FROM event WHERE event_name = name_for_finding;
    END
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_events_amount() RETURNS TRIGGER AS
$$
    BEGIN
        IF TG_OP = 'INSERT' THEN
            UPDATE accounts SET events_amount = (SELECT COUNT(*) FROM event ev WHERE ev.account_id = NEW.account_id) WHERE id = NEW.account_id;
            RETURN NEW;
        ELSIF TG_OP = 'DELETE' THEN
            UPDATE accounts SET events_amount = (SELECT COUNT(*) FROM event ev WHERE ev.account_id = OLD.account_id) WHERE id = OLD.account_id;
            RETURN OLD;
        ELSIF TG_OP = 'UPDATE' THEN
            UPDATE accounts SET events_amount = (SELECT COUNT(*) FROM event ev WHERE ev.account_id = OLD.account_id) WHERE id = OLD.account_id;
            UPDATE accounts SET events_amount = (SELECT COUNT(*) FROM event ev WHERE ev.account_id = NEW.account_id) WHERE id = NEW.account_id;
            RETURN NEW;
        END IF;
    END;
$$
LANGUAGE plpgsql;
"""