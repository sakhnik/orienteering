import psycopg2
import defs
from defs import pg_ns
from result_parser import Name


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
                self.by_id = {id: (f"{last} {first}", self.parse_ranking(note))
                              for id, siid, first, last, note in rows}
                self.by_name = {}
                for _, (name, rank) in self.by_id.items():
                    self.by_name[name] = rank

    def parse_ranking(self, note: str) -> str:
        try:
            return note.split(',')[1].strip()
        except AttributeError:
            return ""
        except IndexError:
            return ""

    def get_name(self, id: int) -> str:
        name, _ = self.by_id[id]
        return name

    def get_ranking(self, name: str) -> str:
        return self.by_name.get(name, "")
