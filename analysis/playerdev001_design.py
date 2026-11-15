"""Exact declared ST package/attribute changes; no native execution."""
from copy import deepcopy
from research.native import require
from research.startpolicy import decode_records, encode_records
from analysis.stless003_design import validate_cells

ARMS=('A','B','C','D')

def level(arm):
    require(arm in ARMS,'Unknown arm')
    return 80 if arm in ('B','D') else 60

def compile_arm(raw, base, side, arm, catalog):
    require(type(side) is int and side in (0,1),'Invalid side')
    dose=level(arm); dlf=arm in ('C','D')
    config=deepcopy(base);team=config['teams'][side]
    require(team['lineup']==list(range(11)),'Identity/lineup drift')
    cell=team['phases'][0][10]
    require(cell['position']=='ST' and cell['role']=='CentreForward' and int(cell['duty'])==0,'ST baseline drift')
    require(team['phases'][1][10]['position']=='ST' and team['phases'][1][10]['role']=='OPCentreForward','OOP baseline drift')
    require(all(v==0 for v in cell['instructions'].values()),'Explicit PI drift')
    require(team['players'][10]['attributes'][54]==60,'JR baseline drift')
    roles={r['id']:r for r in catalog['roles']}
    require(int(roles['CentreForward']['flags'])==2048 and int(roles['DeepLyingForward']['flags'])==1024,'Role catalog drift')
    cell['role']='DeepLyingForward' if dlf else 'CentreForward'
    team['players'][10]['attributes'][54]=dose
    validate_cells(config,side,catalog)
    changed=[];records=[];found_attribute=found_role=0
    for record in decode_records(raw):
        kind,s,slot,field,value=record;new=record
        if (kind,s,slot,field)==(1,side,10,54):
            require(value==60,'Binary JR baseline drift');found_attribute+=1
            new=(kind,s,slot,field,dose)
        if (kind,s,slot)==(4,side,10):
            require((field,value)==(0,2048),'Binary role baseline drift');found_role+=1
            new=(kind,s,slot,0,1024 if dlf else 2048)
        if new!=record:changed.append(dict(before=list(record),after=list(new)))
        records.append(new)
    require(found_attribute==found_role==1,'Unique attribute/role records required')
    require(len(changed)==int(dose==80)+int(dlf),'Undeclared change count')
    restored=deepcopy(config)
    restored['teams'][side]['players'][10]['attributes'][54]=60
    restored['teams'][side]['phases'][0][10]['role']='CentreForward'
    require(restored==base,'Undeclared config changes')
    return encode_records(records),config,dict(role=cell['role'],raw_jr=dose,changed_records=changed,
        target_logical_slot=10,target_roster_slot=10,attribute_index=54,oop_unchanged=True,undeclared_changes=0)
