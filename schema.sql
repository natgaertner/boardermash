--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: mashes; Type: TABLE; Schema: public; Owner: boardermash; Tablespace: 
--

CREATE TABLE mashes (
    winner_name character varying(255),
    loser_name character varying(255),
    "timestamp" timestamp without time zone,
    remote_addr text,
    uuid text
);


ALTER TABLE public.mashes OWNER TO boardermash;

--
-- Name: players; Type: TABLE; Schema: public; Owner: boardermash; Tablespace: 
--

CREATE TABLE players (
    name character varying(255),
    score double precision
);


ALTER TABLE public.players OWNER TO boardermash;

--
-- Name: uuid_unique; Type: CONSTRAINT; Schema: public; Owner: boardermash; Tablespace: 
--

ALTER TABLE ONLY mashes
    ADD CONSTRAINT uuid_unique UNIQUE (uuid);


--
-- Name: player_score_index; Type: INDEX; Schema: public; Owner: boardermash; Tablespace: 
--

CREATE INDEX player_score_index ON players USING btree (score);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

