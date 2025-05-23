PGDMP  "    (                }            Rufkin    16.9    17.0 +    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    101595    Rufkin    DATABASE     �   CREATE DATABASE "Rufkin" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LC_COLLATE = 'C' LC_CTYPE = 'C.UTF-8';
    DROP DATABASE "Rufkin";
                     23P    false                        2615    131992    PlantDoctor    SCHEMA        CREATE SCHEMA "PlantDoctor";
    DROP SCHEMA "PlantDoctor";
                     23P    false            �           1259    132147    articles    TABLE     �   CREATE TABLE "PlantDoctor".articles (
    article_id integer NOT NULL,
    title character varying(100) NOT NULL,
    content text NOT NULL
);
 #   DROP TABLE "PlantDoctor".articles;
       PlantDoctor         heap r       23P    false    15            �           1259    132146    articles_article_id_seq    SEQUENCE     �   CREATE SEQUENCE "PlantDoctor".articles_article_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE "PlantDoctor".articles_article_id_seq;
       PlantDoctor               23P    false    385    15            �           0    0    articles_article_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE "PlantDoctor".articles_article_id_seq OWNED BY "PlantDoctor".articles.article_id;
          PlantDoctor               23P    false    384            �           1259    132156    care_schedule    TABLE     �   CREATE TABLE "PlantDoctor".care_schedule (
    care_schedule_id integer NOT NULL,
    plant_id integer,
    watering_frequency integer NOT NULL,
    frequency_feeding integer NOT NULL,
    last_watering date
);
 (   DROP TABLE "PlantDoctor".care_schedule;
       PlantDoctor         heap r       23P    false    15            �           1259    132155 "   care_schedule_care_schedule_id_seq    SEQUENCE     �   CREATE SEQUENCE "PlantDoctor".care_schedule_care_schedule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 @   DROP SEQUENCE "PlantDoctor".care_schedule_care_schedule_id_seq;
       PlantDoctor               23P    false    387    15            �           0    0 "   care_schedule_care_schedule_id_seq    SEQUENCE OWNED BY     w   ALTER SEQUENCE "PlantDoctor".care_schedule_care_schedule_id_seq OWNED BY "PlantDoctor".care_schedule.care_schedule_id;
          PlantDoctor               23P    false    386                       1259    132133    plants    TABLE     �   CREATE TABLE "PlantDoctor".plants (
    plant_id integer NOT NULL,
    name character varying(50) NOT NULL,
    plant_type_id integer,
    description text,
    recommendations text
);
 !   DROP TABLE "PlantDoctor".plants;
       PlantDoctor         heap r       23P    false    15            ~           1259    132132    plants_plant_id_seq    SEQUENCE     �   CREATE SEQUENCE "PlantDoctor".plants_plant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE "PlantDoctor".plants_plant_id_seq;
       PlantDoctor               23P    false    15    383            �           0    0    plants_plant_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE "PlantDoctor".plants_plant_id_seq OWNED BY "PlantDoctor".plants.plant_id;
          PlantDoctor               23P    false    382            }           1259    132126    plants_type    TABLE     x   CREATE TABLE "PlantDoctor".plants_type (
    plant_type_id integer NOT NULL,
    name character varying(50) NOT NULL
);
 &   DROP TABLE "PlantDoctor".plants_type;
       PlantDoctor         heap r       23P    false    15            |           1259    132125    plants_type_plant_type_id_seq    SEQUENCE     �   CREATE SEQUENCE "PlantDoctor".plants_type_plant_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ;   DROP SEQUENCE "PlantDoctor".plants_type_plant_type_id_seq;
       PlantDoctor               23P    false    381    15            �           0    0    plants_type_plant_type_id_seq    SEQUENCE OWNED BY     m   ALTER SEQUENCE "PlantDoctor".plants_type_plant_type_id_seq OWNED BY "PlantDoctor".plants_type.plant_type_id;
          PlantDoctor               23P    false    380            {           1259    132117    users    TABLE     �   CREATE TABLE "PlantDoctor".users (
    user_id integer NOT NULL,
    name character varying(50) NOT NULL,
    surname character varying(50) NOT NULL,
    login character varying(100) NOT NULL,
    password character varying(100) NOT NULL
);
     DROP TABLE "PlantDoctor".users;
       PlantDoctor         heap r       23P    false    15            z           1259    132116    users_user_id_seq    SEQUENCE     �   CREATE SEQUENCE "PlantDoctor".users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE "PlantDoctor".users_user_id_seq;
       PlantDoctor               23P    false    15    379            �           0    0    users_user_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE "PlantDoctor".users_user_id_seq OWNED BY "PlantDoctor".users.user_id;
          PlantDoctor               23P    false    378            2           2604    132150    articles article_id    DEFAULT     �   ALTER TABLE ONLY "PlantDoctor".articles ALTER COLUMN article_id SET DEFAULT nextval('"PlantDoctor".articles_article_id_seq'::regclass);
 I   ALTER TABLE "PlantDoctor".articles ALTER COLUMN article_id DROP DEFAULT;
       PlantDoctor               23P    false    385    384    385            3           2604    132159    care_schedule care_schedule_id    DEFAULT     �   ALTER TABLE ONLY "PlantDoctor".care_schedule ALTER COLUMN care_schedule_id SET DEFAULT nextval('"PlantDoctor".care_schedule_care_schedule_id_seq'::regclass);
 T   ALTER TABLE "PlantDoctor".care_schedule ALTER COLUMN care_schedule_id DROP DEFAULT;
       PlantDoctor               23P    false    386    387    387            1           2604    132136    plants plant_id    DEFAULT     �   ALTER TABLE ONLY "PlantDoctor".plants ALTER COLUMN plant_id SET DEFAULT nextval('"PlantDoctor".plants_plant_id_seq'::regclass);
 E   ALTER TABLE "PlantDoctor".plants ALTER COLUMN plant_id DROP DEFAULT;
       PlantDoctor               23P    false    382    383    383            0           2604    132129    plants_type plant_type_id    DEFAULT     �   ALTER TABLE ONLY "PlantDoctor".plants_type ALTER COLUMN plant_type_id SET DEFAULT nextval('"PlantDoctor".plants_type_plant_type_id_seq'::regclass);
 O   ALTER TABLE "PlantDoctor".plants_type ALTER COLUMN plant_type_id DROP DEFAULT;
       PlantDoctor               23P    false    380    381    381            /           2604    132120    users user_id    DEFAULT     |   ALTER TABLE ONLY "PlantDoctor".users ALTER COLUMN user_id SET DEFAULT nextval('"PlantDoctor".users_user_id_seq'::regclass);
 C   ALTER TABLE "PlantDoctor".users ALTER COLUMN user_id DROP DEFAULT;
       PlantDoctor               23P    false    378    379    379            �          0    132147    articles 
   TABLE DATA           E   COPY "PlantDoctor".articles (article_id, title, content) FROM stdin;
    PlantDoctor               23P    false    385   �3       �          0    132156    care_schedule 
   TABLE DATA           �   COPY "PlantDoctor".care_schedule (care_schedule_id, plant_id, watering_frequency, frequency_feeding, last_watering) FROM stdin;
    PlantDoctor               23P    false    387   Q4       �          0    132133    plants 
   TABLE DATA           d   COPY "PlantDoctor".plants (plant_id, name, plant_type_id, description, recommendations) FROM stdin;
    PlantDoctor               23P    false    383   �4       �          0    132126    plants_type 
   TABLE DATA           A   COPY "PlantDoctor".plants_type (plant_type_id, name) FROM stdin;
    PlantDoctor               23P    false    381   w5       �          0    132117    users 
   TABLE DATA           O   COPY "PlantDoctor".users (user_id, name, surname, login, password) FROM stdin;
    PlantDoctor               23P    false    379   �5       �           0    0    articles_article_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('"PlantDoctor".articles_article_id_seq', 2, true);
          PlantDoctor               23P    false    384            �           0    0 "   care_schedule_care_schedule_id_seq    SEQUENCE SET     W   SELECT pg_catalog.setval('"PlantDoctor".care_schedule_care_schedule_id_seq', 3, true);
          PlantDoctor               23P    false    386            �           0    0    plants_plant_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('"PlantDoctor".plants_plant_id_seq', 3, true);
          PlantDoctor               23P    false    382            �           0    0    plants_type_plant_type_id_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('"PlantDoctor".plants_type_plant_type_id_seq', 3, true);
          PlantDoctor               23P    false    380            �           0    0    users_user_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('"PlantDoctor".users_user_id_seq', 2, true);
          PlantDoctor               23P    false    378            =           2606    132154    articles articles_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY "PlantDoctor".articles
    ADD CONSTRAINT articles_pkey PRIMARY KEY (article_id);
 G   ALTER TABLE ONLY "PlantDoctor".articles DROP CONSTRAINT articles_pkey;
       PlantDoctor                 23P    false    385            ?           2606    132161     care_schedule care_schedule_pkey 
   CONSTRAINT     s   ALTER TABLE ONLY "PlantDoctor".care_schedule
    ADD CONSTRAINT care_schedule_pkey PRIMARY KEY (care_schedule_id);
 Q   ALTER TABLE ONLY "PlantDoctor".care_schedule DROP CONSTRAINT care_schedule_pkey;
       PlantDoctor                 23P    false    387            ;           2606    132140    plants plants_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY "PlantDoctor".plants
    ADD CONSTRAINT plants_pkey PRIMARY KEY (plant_id);
 C   ALTER TABLE ONLY "PlantDoctor".plants DROP CONSTRAINT plants_pkey;
       PlantDoctor                 23P    false    383            9           2606    132131    plants_type plants_type_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY "PlantDoctor".plants_type
    ADD CONSTRAINT plants_type_pkey PRIMARY KEY (plant_type_id);
 M   ALTER TABLE ONLY "PlantDoctor".plants_type DROP CONSTRAINT plants_type_pkey;
       PlantDoctor                 23P    false    381            5           2606    132124    users users_login_key 
   CONSTRAINT     X   ALTER TABLE ONLY "PlantDoctor".users
    ADD CONSTRAINT users_login_key UNIQUE (login);
 F   ALTER TABLE ONLY "PlantDoctor".users DROP CONSTRAINT users_login_key;
       PlantDoctor                 23P    false    379            7           2606    132122    users users_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY "PlantDoctor".users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 A   ALTER TABLE ONLY "PlantDoctor".users DROP CONSTRAINT users_pkey;
       PlantDoctor                 23P    false    379            A           2606    132162 )   care_schedule care_schedule_plant_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY "PlantDoctor".care_schedule
    ADD CONSTRAINT care_schedule_plant_id_fkey FOREIGN KEY (plant_id) REFERENCES "PlantDoctor".plants(plant_id);
 Z   ALTER TABLE ONLY "PlantDoctor".care_schedule DROP CONSTRAINT care_schedule_plant_id_fkey;
       PlantDoctor               23P    false    383    387    3643            @           2606    132141     plants plants_plant_type_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY "PlantDoctor".plants
    ADD CONSTRAINT plants_plant_type_id_fkey FOREIGN KEY (plant_type_id) REFERENCES "PlantDoctor".plants_type(plant_type_id);
 Q   ALTER TABLE ONLY "PlantDoctor".plants DROP CONSTRAINT plants_plant_type_id_fkey;
       PlantDoctor               23P    false    3641    381    383            �   �   x�u���0D�v���'ŐX�R"рe�Z��Yr����;8\y[�9𨬀��Y���fL�9��50	�x�*��9��1F�8�L�j�Iر��M;��E'v�8\�4�wm�_��i��.m�6z�?�=��      �   8   x�3�4BsN##c]3]C.#N#NcNK������1'��Ō�b���� E�	�      �   �   x�m��	1E�I)@���t1��֍��g4c�u��BB�/�7q:��E�M���P��2�	��Gw]�%��'(I-�k`vPR@[���J~���:�leK<��F��������)Et	%񡄨��(�I�|,�-��ϊA�S}in��:�z$��cM������I�ϥ	�߉*T�,�`f��o�ZM58�o�|����N      �   [   x���	�0�s�.
�:��Izu/��P(�v�d#��C�ǟn$dz(�6;\���/2��h�éPѹᡗMh�L�"�V:��:����:�      �   h   x�3�0�¦.�3.컰�3�,1/��!=713G/9?�� ���<�(%$�e�ya���Uo�0��֋M@�܂Ԓ���D�ޜLT��9�y�\1z\\\ 7:i     