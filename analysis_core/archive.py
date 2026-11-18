import json
import sqlite3
from .records import canonical, Study

class Archive:
    """保存原始研究资料，不覆盖同名修订。"""
    def __init__(self,path):
        self.connection=sqlite3.connect(path)
        self.connection.execute('PRAGMA foreign_keys=ON')
        self.connection.execute('CREATE TABLE IF NOT EXISTS studies (name TEXT NOT NULL, digest TEXT NOT NULL, payload TEXT NOT NULL, PRIMARY KEY(name,digest))')
        self.connection.commit()

    def add(self,study):
        with self.connection:
            self.connection.execute('INSERT OR IGNORE INTO studies VALUES(?,?,?)',(study.name,study.digest,canonical(study.to_dict())))
        return study.digest

    def read(self,name,digest,schema):
        result=self.connection.execute('SELECT payload FROM studies WHERE name=? AND digest=?',(name,digest)).fetchone()
        if result is None:
            raise KeyError((name,digest))
        study=Study.from_dict(json.loads(result[0]),schema)
        if study.digest != digest:
            raise ValueError('archive digest mismatch')
        return study

    def revisions(self,name):
        return [r[0] for r in self.connection.execute('SELECT digest FROM studies WHERE name=? ORDER BY digest',(name,))]

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self,*args):
        self.close()
