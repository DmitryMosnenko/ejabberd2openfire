#!/usr/bin/python

import sys,pprint,time

if len(sys.argv) != 3:
    print "Usage: ejabberd2openfire.py <ejabberd dumpfile> <openfire import/export XML file> -- where the openfire xml file will be created // overwritten"
    sys.exit()

ejdump=open(sys.argv[1], "r").read()
ofirexml=open(sys.argv[2], "w")

substdict = {'remove':'-1',
             'none':'0',
             'to':'1',
             'from':'2',
             'both':'3'}
recvstdict = {'none':'-1',
              'subscribe':'1',
              'unsubscribe':'2'
              }
askstdict = {'in':'1',
             'out':'0',
             'none':'-1'
             }

userpws = {}
rosters = {}

fromidx=0
while ejdump.find("{passwd", fromidx) != -1:
    nidx=ejdump.find("{passwd", fromidx)
    eidx=ejdump.find("}.",nidx)
    finstr=ejdump[nidx:eidx+2]
    if "record_name" in finstr:
        fromidx=eidx
    else:
        uid, domain, pw = finstr.replace("{","").replace("}","").replace('"',"").split(",")[1:]
        userpws[(uid,domain)] = pw[0:-1]
        fromidx=eidx

fromidx=0
while ejdump.find("{roster", fromidx) != -1:
    nidx=ejdump.find("{roster", fromidx)
    eidx=ejdump.find("}.",nidx)
    finstr=ejdump[nidx:eidx+2].replace("\n","")
    if "record_name" in finstr or "roster_groups" in finstr:
        fromidx=eidx
    else:
        fina = []
        for i in finstr.replace("{","").replace("}","").replace('"',"").split(","):
            fina.append(i.strip())
        fromusr = tuple(fina[1:3])
        tousr = tuple(fina[3:5])
        subst = fina[12]
        recvst = fina[13]
        askst = fina[13]
        
        if not subst in substdict.keys():
            subst = 'none'
        if not recvst in recvstdict.keys():
            recvst = 'none'
        if not askst in askstdict.keys():
            askst = 'none'
        
        group = None
        if '[' in fina[14] and ']' in fina[14] and '[]' not in fina[14]:
            group = fina[14].strip().strip( '[]' )
        name = ""
        if fina[11] != "[]":
            name = fina[11]
        fromidx=eidx
        if not fromusr in rosters:
            rosters[fromusr]=[]
        if tousr[0]=='[]':
            tousr=('',tousr[1])
        name=name.replace("<","").replace(">","") # TODO: replace with correctly escaped fun
        rosters[fromusr].append( (tousr,name,subst,askst,recvst,group) )


ofirexml.write('<?xml version="1.0" encoding="UTF-8"?>\n<Openfire>\n\n')

# pprint.pprint( userpws.keys() )
# pprint.pprint( rosters.keys() )
for user,pw in userpws.iteritems():
    ofirexml.write("""
  <User>
    <Username>%s</Username>
    <Email></Email>
    <Name></Name>
    <Password>%s</Password>
    <CreationDate>%s</CreationDate>
    <ModifiedDate>%s</ModifiedDate>
    <Roster>"""%(user[0],pw,int(time.time()), int(time.time())))
    
    if user in rosters.keys():
        for i in rosters[user]:
            subst = substdict[ i[2] ]
            askst = askstdict[ i[3] ]
            recvst = recvstdict[ i[4] ]
            jid = "@".join(i[0]).strip("@")
            if i[5] != None:
                ofirexml.write("""
      <Item jid="%s" askstatus="%s" recvstatus="%s" substatus="%s" name="%s" >
        <Group>%s</Group>
      </Item>"""%( jid, askst, recvst, subst, i[1], i[5] ))
            else:
                ofirexml.write("""
      <Item jid="%s" askstatus="%s" recvstatus="%s" substatus="%s" name="%s" />"""%( jid, askst, recvst, subst, i[1]))
                
    ofirexml.write("""
    </Roster>""")
    
    ofirexml.write("""
  </User>""")
    
ofirexml.write('\n</Openfire>')
ofirexml.close()
