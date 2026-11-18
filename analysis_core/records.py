from dataclasses import dataclass
from pathlib import Path
import hashlib
import json
import math

def canonical(value):
    """稳定编码原始资料，拒绝不可交换的非有限数字。"""
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)

@dataclass(frozen=True)
class Study:
    name: str
    tables_json: str
    options_json: str

    @classmethod
    def from_dict(cls, value, schema):
        if not isinstance(value,dict) or not isinstance(value.get('name'),str) or not value['name'].strip():
            raise ValueError('study name is required')
        tables=value.get('tables')
        if not isinstance(tables,dict):
            raise ValueError('tables must be an object')
        for table,fields in schema.items():
            if table not in tables or not isinstance(tables[table],list):
                raise ValueError('missing table: '+table)
            for index,row in enumerate(tables[table]):
                if not isinstance(row,dict):
                    raise ValueError(f'{table}[{index}] must be an object')
                missing=set(fields)-row.keys()
                if missing:
                    raise ValueError(f'{table}[{index}] missing: '+','.join(sorted(missing)))
        options=value.get('options',{})
        if not isinstance(options,dict):
            raise ValueError('options must be an object')
        return cls(value['name'],canonical(tables),canonical(options))

    @classmethod
    def read(cls,path,schema):
        return cls.from_dict(json.loads(Path(path).read_text(encoding='utf-8')),schema)

    @property
    def tables(self):
        return json.loads(self.tables_json)

    @property
    def options(self):
        return json.loads(self.options_json)

    def to_dict(self):
        return dict(name=self.name,tables=self.tables,options=self.options)

    @property
    def digest(self):
        return hashlib.sha256(canonical(self.to_dict()).encode('utf-8')).hexdigest()

def numeric_summary(rows,field):
    """分别核对资料条数、空值及有限数值，不推断缺失值。"""
    values=[]
    missing=0
    for row in rows:
        value=row.get(field)
        if value is None:
            missing+=1
        elif isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
            raise ValueError('not a finite numeric field: '+field)
        else:
            values.append(value)
    return dict(rows=len(rows),observed=len(values),missing=missing,total=sum(values))

def group_rows(rows,keys):
    """保留原始顺序分组，缺少属性与显式空值分别保留。"""
    output={}
    for row in rows:
        key=tuple((field in row,row.get(field)) for field in keys)
        output.setdefault(key,[]).append(dict(row))
    return output
