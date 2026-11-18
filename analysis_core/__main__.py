import argparse
import json
from .records import Study
from .archive import Archive
from .schema import SCHEMA
from . import workforce

def main():
    parser=argparse.ArgumentParser(description='研究原始资料核对')
    parser.add_argument('input')
    parser.add_argument('--archive')
    args=parser.parse_args()
    study=Study.read(args.input,SCHEMA)
    tables=study.tables
    if args.archive:
        with Archive(args.archive) as store:
            store.add(study)
    print(json.dumps(dict(name=study.name,digest=study.digest,
        table_rows={k:len(v) for k,v in tables.items()},
        raw_query=workforce.active_certificates(tables['certificates'], '2026-11-01')),ensure_ascii=False,sort_keys=True))

if __name__=='__main__':
    main()
