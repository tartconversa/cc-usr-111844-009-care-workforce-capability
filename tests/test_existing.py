from pathlib import Path
import json
import tempfile
import unittest
from analysis_core.records import Study, canonical, numeric_summary, group_rows
from analysis_core.archive import Archive
from analysis_core.schema import SCHEMA
from analysis_core import workforce

EXAMPLE=Path(__file__).resolve().parents[1]/'examples'/'study.json'

class ExistingContracts(unittest.TestCase):
    def setUp(self):
        self.raw=json.loads(EXAMPLE.read_text(encoding='utf-8'))
        self.study=Study.from_dict(self.raw,SCHEMA)

    def test_current_domain_query(self):
        tables=self.study.tables
        result=workforce.active_certificates(tables['certificates'], '2026-11-01')
        self.assertEqual(len(result),1)

    def test_roundtrip_and_immutable_copies(self):
        copy=self.study.tables
        copy.clear()
        self.assertTrue(self.study.tables)
        self.assertEqual(Study.from_dict(self.study.to_dict(),SCHEMA),self.study)

    def test_missing_field_is_distinct_from_null(self):
        first=next(iter(SCHEMA))
        field=SCHEMA[first][0]
        self.raw['tables'][first][0].pop(field)
        with self.assertRaisesRegex(ValueError,'missing'):
            Study.from_dict(self.raw,SCHEMA)

    def test_canonical_order(self):
        self.assertEqual(canonical(dict(b=2,a=1)),canonical(dict(a=1,b=2)))
        with self.assertRaises(ValueError):
            canonical(dict(a=float('nan')))

    def test_archive_independent_revisions(self):
        with tempfile.TemporaryDirectory() as directory:
            with Archive(str(Path(directory)/'studies.sqlite3')) as store:
                first=store.add(self.study)
                self.assertEqual(store.add(self.study),first)
                self.raw['options']['note']='补充资料'
                changed=Study.from_dict(self.raw,SCHEMA)
                second=store.add(changed)
                self.assertNotEqual(first,second)
                self.assertEqual(len(store.revisions(self.study.name)),2)
                self.assertEqual(store.read(self.study.name,first,SCHEMA),self.study)
                with self.assertRaises(KeyError):
                    store.read(self.study.name,'unknown',SCHEMA)

    def test_numeric_missing_and_zero(self):
        result=numeric_summary([dict(x=None),dict(x=0),dict(x=2)],'x')
        self.assertEqual(result,dict(rows=3,observed=2,missing=1,total=2))

    def test_group_presence(self):
        self.assertEqual(len(group_rows([{},dict(x=None)],['x'])),2)

    def test_contracts_do_not_create_two_people(self):
        rows=self.study.tables['roster']
        self.assertEqual(len(workforce.person_contracts(rows,'c1')),2)
        self.assertEqual(workforce.contract_shares(rows),{'c1':1})
        cert=self.study.tables['certificates']
        self.assertEqual(workforce.active_certificates(cert,'2026-12-31'),[])

if __name__=='__main__':
    unittest.main()
