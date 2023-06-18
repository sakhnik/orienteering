import psycopg2
import defs
from defs import pg_ns


class PgStorage:
    def __init__(self):
        with psycopg2.connect(host=defs.pg_host,
                              database=defs.pg_db,
                              user=defs.pg_user,
                              password=defs.pg_pass) as conn:
            with conn.cursor() as cursor:
                query = f"SELECT a.id, a.siid, a.firstname, a.lastname, \
                    a.note \
                    FROM {pg_ns}.competitors a"
                cursor.execute(query)
                rows = cursor.fetchall()
                self.names = {id: (f"{last} {first}", self.parse_ranking(note))
                              for id, siid, first, last, note in rows}

    def parse_ranking(self, note: str) -> str:
        try:
            return note.split(',')[1].strip()
        except AttributeError:
            return ""
        except IndexError:
            return ""

    def get_name(self, id: int) -> str:
        name, _ = self.names[id]
        return name

    def get_ranking(self, id: int) -> str:
        _, rank = self.names[id]
        return rank
