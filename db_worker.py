{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "3fe4945d",
   "metadata": {},
   "outputs": [],
   "source": [
    "from configparser import ConfigParser\n",
    "import psycopg2\n",
    "import requests\n",
    "from typing import Dict, List"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "daced821",
   "metadata": {},
   "outputs": [],
   "source": [
    "def load_connection_info(\n",
    "    ini_filename: str\n",
    ") -> Dict[str, str]:\n",
    "    parser = ConfigParser()\n",
    "    parser.read(ini_filename)\n",
    "# Create a dictionary of the variables stored under the \"postgresql\" section of the .ini\n",
    "    conn_info = {param[0]: param[1] for param in\n",
    "parser.items(\"postgresql\")}\n",
    "    return conn_info\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "044e7abe",
   "metadata": {},
   "outputs": [],
   "source": [
    "def create_db(\n",
    "    conn_info: Dict[str, str],\n",
    ") -> None:\n",
    "    psql_connection_string = \"user=\"\\\n",
    "    f\"{conn_info['user']} password={conn_info['password']}\"\n",
    "    conn = psycopg2.connect(psql_connection_string)\n",
    "    cur = conn.cursor()\n",
    "    conn.autocommit = True\n",
    "    sql_query = f\"CREATE DATABASE {conn_info['database']}\"\n",
    "    try:\n",
    "        cur.execute(sql_query)\n",
    "    except Exception as e:\n",
    "        print(f\"{type(e).__name__}: {e}\")\n",
    "        print(f\"Query: {cur.query}\")\n",
    "        cur.close()\n",
    "    else:\n",
    "            conn.autocommit = False"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "646fa101",
   "metadata": {},
   "outputs": [],
   "source": [
    "def create_table(\n",
    "    sql_query: str,\n",
    "    conn: psycopg2.extensions.connection,\n",
    "    cur: psycopg2.extensions.cursor\n",
    ") -> None:\n",
    "    try:\n",
    " # Execute the table creation query\n",
    "        cur.execute(sql_query)\n",
    "    except Exception as e:\n",
    "        print(f\"{type(e).__name__}: {e}\")\n",
    "        print(f\"Query: {cur.query}\")\n",
    "        conn.rollback()\n",
    "        cur.close()\n",
    "    else:\n",
    "        conn.commit()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "3181bbaf",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "DuplicateDatabase: ОШИБКА:  база данных \"weather\" уже существует\n",
      "\n",
      "Query: b'CREATE DATABASE weather'\n"
     ]
    }
   ],
   "source": [
    "conn_info = load_connection_info(\"db.ini\")\n",
    "create_db(conn_info)\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "5a658797",
   "metadata": {},
   "outputs": [],
   "source": [
    "connection = psycopg2.connect(**conn_info)\n",
    "cursor = connection.cursor()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3b88df5c",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "\n",
    "            \n",
    "            \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "20792c0f",
   "metadata": {},
   "outputs": [],
   "source": [
    "location_sql = \"\"\"\n",
    "    CREATE TABLE IF NOT EXISTS location (\n",
    "         id SERIAL PRIMARY KEY,\n",
    "         name VARCHAR(200) UNIQUE NOT NULL,\n",
    "         region VARCHAR(200) NOT NULL,\n",
    "         country VARCHAR(200) NOT NULL,\n",
    "         tz_id VARCHAR(200) NOT NULL,\n",
    "         local_time TIMESTAMP NOT NULL,\n",
    "         last_update TIMESTAMP NOT NULL DEFAULT now(),\n",
    "         local_time_epoch NUMERIC(10) NOT NULL,\n",
    "         lat NUMERIC(5, 2) NOT NULL,\n",
    "         lon NUMERIC(5, 2) NOT NULL\n",
    "         );\n",
    "\"\"\"\n",
    "create_table(location_sql, connection, cursor)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "id": "a5b88564",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "InterfaceError: cursor already closed\n",
      "Query: b'\\n    CREATE TABLE IF NOT EXISTS current (\\n         id SERIAL PRIMARY KEY,\\n         condition_id SERIAL REFERENCES condition(id) MATCH SIMPLE\\nON UPDATE CASCADE ON DELETE RESTRICT,\\n         wind_dir VARCHAR(3) NOT NULL,\\n         last_update TIMESTAMP NOT NULL DEFAULT now(),\\n         data_published_epoch NUMERIC(10) NOT NULL,\\n         data_published TIMESTAMP NOT NULL,\\n         temp_c NUMERIC(10,2) NOT NULL,\\n         temp_f NUMERIC(10,2) NOT NULL,\\n         wind_mph NUMERIC(10,2) NOT NULL,\\n         wind_kph NUMERIC(10,2) NOT NULL,\\n         wind_degree NUMERIC(10) NOT NULL,\\n         pressure_mb NUMERIC(10, 2) NOT NULL,\\n         pressure_in NUMERIC(10, 2) NOT NULL,\\n         precip_mm NUMERIC(10, 2) NOT NULL,\\n         precip_in NUMERIC(10, 2) NOT NULL,\\n        69\\n         humidity NUMERIC(10, 2) NOT NULL,\\n         feelslike_c NUMERIC(10, 2) NOT NULL,\\n         feelslike_f NUMERIC(10, 2) NOT NULL,\\n         vis_km NUMERIC(10, 2) NOT NULL,\\n         vis_miles NUMERIC(10, 2) NOT NULL,\\n         uv NUMERIC(10, 2) NOT NULL,\\n         gust_mph NUMERIC(10, 2) NOT NULL,\\n         gust_kph NUMERIC(10, 2) NOT NULL,\\n         is_day BOOLEAN NOT NULL,\\n         cloud BOOLEAN NOT NULL\\n         );\\n'\n"
     ]
    }
   ],
   "source": [
    "# Create the \"condition\" tablet\n",
    "condition_sql = \"\"\"\n",
    "    CREATE TABLE IF NOT EXISTS condition (\n",
    "         id SERIAL PRIMARY KEY,\n",
    "         icon VARCHAR(200) NOT NULL,\n",
    "         text VARCHAR(50) NOT NULL,\n",
    "         last_update TIMESTAMP NOT NULL DEFAULT now(),\n",
    "         code NUMERIC(10) NOT NULL\n",
    "         );\n",
    "\"\"\"\n",
    "create_table(condition_sql, connection, cursor)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "697960fd",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "2e9f7f33",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "InterfaceError: cursor already closed\n",
      "Query: b'\\n    CREATE TABLE IF NOT EXISTS current (\\n        id SERIAL PRIMARY KEY,\\n        condition_id SERIAL REFERENCES condition(id) MATCH SIMPLE\\nON UPDATE CASCADE ON DELETE RESTRICT,\\n    wind_dir VARCHAR(3) NOT NULL,\\n    last_update TIMESTAMP NOT NULL DEFAULT now(),\\n    data_published_epoch NUMERIC(10) NOT NULL,\\n    data_published TIMESTAMP NOT NU\\n    LL,\\n    temp_c NUMERIC(10,2) NOT NULL,\\n    temp_f NUMERIC(10,2) NOT NULL,\\n    wind_mph NUMERIC(10,2) NOT NULL,\\n    wind_kph NUMERIC(10,2) NOT NULL,\\n    wind_degree NUMERIC(10) NOT NULL,\\n    pressure_mb NUMERIC(10, 2) NOT NULL,\\n    pressure_in NUMERIC(10, 2) NOT NULL,\\n    precip_mm NUMERIC(10, 2) NOT NULL,\\n    precip_in NUMERIC(10, 2) NOT NULL,\\n    humidity NUMERIC(10, 2) NOT NULL,\\n    feelslike_c NUMERIC(10, 2) NOT NULL,\\n    feelslike_f NUMERIC(10, 2) NOT NULL,\\n    vis_km NUMERIC(10, 2) NOT NULL,\\n    vis_miles NUMERIC(10, 2) NOT NULL,\\n    uv NUMERIC(10, 2) NOT NULL,\\n    gust_mph NUMERIC(10, 2) NOT NULL,\\n    gust_kph NUMERIC(10, 2) NOT NULL,\\n    is_day BOOLEAN NOT NULL,\\n    cloud BOOLEAN NOT NULL\\n );\\n\\n'\n"
     ]
    }
   ],
   "source": [
    "current_sql = \"\"\"\n",
    "    CREATE TABLE IF NOT EXISTS current (\n",
    "        id SERIAL PRIMARY KEY,\n",
    "        condition_id SERIAL REFERENCES condition(id) MATCH SIMPLE\n",
    "ON UPDATE CASCADE ON DELETE RESTRICT,\n",
    "    wind_dir VARCHAR(3) NOT NULL,\n",
    "    last_update TIMESTAMP NOT NULL DEFAULT now(),\n",
    "    data_published_epoch NUMERIC(10) NOT NULL,\n",
    "    data_published TIMESTAMP NOT NULL,\n",
    "    temp_c NUMERIC(10,2) NOT NULL,\n",
    "    temp_f NUMERIC(10,2) NOT NULL,\n",
    "    wind_mph NUMERIC(10,2) NOT NULL,\n",
    "    wind_kph NUMERIC(10,2) NOT NULL,\n",
    "    wind_degree NUMERIC(10) NOT NULL,\n",
    "    pressure_mb NUMERIC(10, 2) NOT NULL,\n",
    "    pressure_in NUMERIC(10, 2) NOT NULL,\n",
    "    precip_mm NUMERIC(10, 2) NOT NULL,\n",
    "    precip_in NUMERIC(10, 2) NOT NULL,\n",
    "    humidity NUMERIC(10, 2) NOT NULL,\n",
    "    feelslike_c NUMERIC(10, 2) NOT NULL,\n",
    "    feelslike_f NUMERIC(10, 2) NOT NULL,\n",
    "    vis_km NUMERIC(10, 2) NOT NULL,\n",
    "    vis_miles NUMERIC(10, 2) NOT NULL,\n",
    "    uv NUMERIC(10, 2) NOT NULL,\n",
    "    gust_mph NUMERIC(10, 2) NOT NULL,\n",
    "    gust_kph NUMERIC(10, 2) NOT NULL,\n",
    "    is_day BOOLEAN NOT NULL,\n",
    "    cloud BOOLEAN NOT NULL\n",
    " );\n",
    "\n",
    "\"\"\"\n",
    "create_table(current_sql, connection, cursor)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "08ba3af8",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "InterfaceError: cursor already closed\n",
      "Query: b'\\n    CREATE TABLE IF NOT EXISTS current (\\n        id SERIAL PRIMARY KEY,\\n        condition_id SERIAL REFERENCES condition(id) MATCH SIMPLE\\nON UPDATE CASCADE ON DELETE RESTRICT,\\n    wind_dir VARCHAR(3) NOT NULL,\\n    last_update TIMESTAMP NOT NULL DEFAULT now(),\\n    data_published_epoch NUMERIC(10) NOT NULL,\\n    data_published TIMESTAMP NOT NU\\n    LL,\\n    temp_c NUMERIC(10,2) NOT NULL,\\n    temp_f NUMERIC(10,2) NOT NULL,\\n    wind_mph NUMERIC(10,2) NOT NULL,\\n    wind_kph NUMERIC(10,2) NOT NULL,\\n    wind_degree NUMERIC(10) NOT NULL,\\n    pressure_mb NUMERIC(10, 2) NOT NULL,\\n    pressure_in NUMERIC(10, 2) NOT NULL,\\n    precip_mm NUMERIC(10, 2) NOT NULL,\\n    precip_in NUMERIC(10, 2) NOT NULL,\\n    humidity NUMERIC(10, 2) NOT NULL,\\n    feelslike_c NUMERIC(10, 2) NOT NULL,\\n    feelslike_f NUMERIC(10, 2) NOT NULL,\\n    vis_km NUMERIC(10, 2) NOT NULL,\\n    vis_miles NUMERIC(10, 2) NOT NULL,\\n    uv NUMERIC(10, 2) NOT NULL,\\n    gust_mph NUMERIC(10, 2) NOT NULL,\\n    gust_kph NUMERIC(10, 2) NOT NULL,\\n    is_day BOOLEAN NOT NULL,\\n    cloud BOOLEAN NOT NULL\\n );\\n\\n'\n"
     ]
    }
   ],
   "source": [
    "# Create the \"weather\" table\n",
    "weather_sql = \"\"\"\n",
    "    CREATE TABLE IF NOT EXISTS weather (\n",
    "        id SERIAL PRIMARY KEY,\n",
    "        location_id SERIAL REFERENCES location(id) MATCH SIMPLE ON\n",
    "UPDATE CASCADE ON DELETE RESTRICT,\n",
    "        current_id SERIAL REFERENCES location(id) MATCH SIMPLE ON\n",
    "UPDATE CASCADE ON DELETE RESTRICT,\n",
    "        last_update TIMESTAMP NOT NULL DEFAULT now()\n",
    " );\n",
    "\"\"\"\n",
    "create_table(weather_sql, connection, cursor)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "a395d73b",
   "metadata": {},
   "outputs": [],
   "source": [
    "connection.close()\n",
    "cursor.close()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "4c3000e2",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
