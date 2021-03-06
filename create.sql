PGDMP     )    9                z         	   TennisATP    14.2    14.2     ?           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                        0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    25520 	   TennisATP    DATABASE     o   CREATE DATABASE "TennisATP" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_United States.1252';
    DROP DATABASE "TennisATP";
                postgres    false            ?            1259    25720    match_stats    TABLE     ?   CREATE TABLE public.match_stats (
    tournament_id character varying(50),
    winner_id integer,
    loser_id integer,
    date character varying(20),
    score character varying(50),
    winner_points real,
    loser_points real
);
    DROP TABLE public.match_stats;
       public         heap    postgres    false            ?            1259    25710    player    TABLE     ?   CREATE TABLE public.player (
    player_id integer NOT NULL,
    name character varying(50),
    location character varying(5),
    height real,
    hand character(2)
);
    DROP TABLE public.player;
       public         heap    postgres    false            ?            1259    25715 
   tournament    TABLE     ?   CREATE TABLE public.tournament (
    tournament_id character varying(50) NOT NULL,
    name character varying(50),
    surface character varying(10),
    year integer
);
    DROP TABLE public.tournament;
       public         heap    postgres    false            ?            1259    25738    tournament_stats    TABLE     &  CREATE TABLE public.tournament_stats (
    tournament_id character varying(50),
    w_ace real,
    w_df real,
    w_svpt real,
    w_svgms real,
    w_bpsaved real,
    w_bpfaced real,
    l_ace real,
    l_df real,
    l_svpt real,
    l_svgms real,
    l_bpsaved real,
    l_bpfaced real
);
 $   DROP TABLE public.tournament_stats;
       public         heap    postgres    false            i           2606    25714    player player_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.player
    ADD CONSTRAINT player_pkey PRIMARY KEY (player_id);
 <   ALTER TABLE ONLY public.player DROP CONSTRAINT player_pkey;
       public            postgres    false    209            l           2606    25719    tournament tournament_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.tournament
    ADD CONSTRAINT tournament_pkey PRIMARY KEY (tournament_id);
 D   ALTER TABLE ONLY public.tournament DROP CONSTRAINT tournament_pkey;
       public            postgres    false    210            m           1259    25759    idx_matchstats    INDEX     ?   CREATE INDEX idx_matchstats ON public.match_stats USING btree (tournament_id, winner_id, loser_id, date, score, winner_points, loser_points);
 "   DROP INDEX public.idx_matchstats;
       public            postgres    false    211    211    211    211    211    211    211            g           1259    25757 
   idx_player    INDEX     U   CREATE INDEX idx_player ON public.player USING btree (name, location, height, hand);
    DROP INDEX public.idx_player;
       public            postgres    false    209    209    209    209            j           1259    25758    idx_tournament    INDEX     c   CREATE INDEX idx_tournament ON public.tournament USING btree (tournament_id, name, surface, year);
 "   DROP INDEX public.idx_tournament;
       public            postgres    false    210    210    210    210            p           2606    25733 %   match_stats match_stats_loser_id_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.match_stats
    ADD CONSTRAINT match_stats_loser_id_fkey FOREIGN KEY (loser_id) REFERENCES public.player(player_id);
 O   ALTER TABLE ONLY public.match_stats DROP CONSTRAINT match_stats_loser_id_fkey;
       public          postgres    false    211    3177    209            n           2606    25723 *   match_stats match_stats_tournament_id_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.match_stats
    ADD CONSTRAINT match_stats_tournament_id_fkey FOREIGN KEY (tournament_id) REFERENCES public.tournament(tournament_id);
 T   ALTER TABLE ONLY public.match_stats DROP CONSTRAINT match_stats_tournament_id_fkey;
       public          postgres    false    210    211    3180            o           2606    25728 &   match_stats match_stats_winner_id_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.match_stats
    ADD CONSTRAINT match_stats_winner_id_fkey FOREIGN KEY (winner_id) REFERENCES public.player(player_id);
 P   ALTER TABLE ONLY public.match_stats DROP CONSTRAINT match_stats_winner_id_fkey;
       public          postgres    false    3177    209    211            q           2606    25741 4   tournament_stats tournament_stats_tournament_id_fkey    FK CONSTRAINT     ?   ALTER TABLE ONLY public.tournament_stats
    ADD CONSTRAINT tournament_stats_tournament_id_fkey FOREIGN KEY (tournament_id) REFERENCES public.tournament(tournament_id);
 ^   ALTER TABLE ONLY public.tournament_stats DROP CONSTRAINT tournament_stats_tournament_id_fkey;
       public          postgres    false    210    3180    212           