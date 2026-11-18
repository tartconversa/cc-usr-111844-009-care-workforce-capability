def active_certificates(rows, date):
    """按资质有效期返回原始证书，不估计人员空余工时。"""
    return [dict(r) for r in rows if r['start'] <= date and (r['end'] is None or date < r['end'])]

def person_contracts(rows,person):
    """查询同一人的全部机构合同，不把多份合同变成多个人。"""
    return [dict(r) for r in rows if r['person']==person]

def contract_shares(rows):
    """核对每个人的合同全职份额，不推断实际在岗工时。"""
    result={}
    for row in rows:
        if not 0<=row['share']<=1:
            raise ValueError('invalid employment share')
        key=row['person']
        result[key]=result.get(key,0)+row['share']
    return result
