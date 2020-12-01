# -*- encoding: utf-8 -*-
"""
tests delegation primaily from keri.core.eventing

"""
import os

import pytest

from keri import kering
from keri.help import ogling
from keri.db import dbing
from keri.base import keeping
from keri.core import coring
from keri.core import eventing

blogger, flogger = ogling.ogler.getLoggers()


def test_delegation():
    """
    Test creation and validation of delegated identifer prefixes and events

    """
    # bob is the delegator del is bob's delegate

    bobSalt = coring.Salter(raw=b'0123456789abcdef').qb64
    delSalt = coring.Salter(raw=b'abcdef0123456789').qb64

    with dbing.openDB(name="bob") as bobDB, \
          keeping.openKeep(name="bob") as bobKp, \
          dbing.openDB(name="del") as delDB, \
          keeping.openKeep(name="del") as delKp:

        # Init key pair managers
        bobMgr = keeping.Manager(keeper=bobKp, salt=bobSalt)
        delMgr = keeping.Manager(keeper=delKp, salt=delSalt)

        # Init Keverys
        bobKvy = eventing.Kevery(baser=bobDB)
        delKvy = eventing.Kevery(baser=delDB)

        # Setup Bob by creating inception event
        verfers, digers = bobMgr.incept(stem='bob', temp=True) # algo default salty and rooted
        bobSrdr = eventing.incept(keys=[verfer.qb64 for verfer in verfers],
                                 nxt=coring.Nexter(digs=[diger.qb64 for diger in digers]).qb64,
                                 code=coring.CryOneDex.Blake3_256)

        bobPre = bobSrdr.ked["pre"]
        assert bobPre == 'EXmV-FiCyD7U76DoXSQoHlG30hFLD2cuYWEQPp0mEu1U'

        bobMgr.move(old=verfers[0].qb64, new=bobPre)  # move key pair label to prefix

        sigers = bobMgr.sign(ser=bobSrdr.raw, verfers=verfers)

        msg = bytearray(bobSrdr.raw)
        counter = coring.SigCounter(count=len(sigers))
        msg.extend(counter.qb64b)
        for siger in sigers:
            msg.extend(siger.qb64b)

        assert msg == bytearray(b'{"vs":"KERI10JSON0000fb_","pre":"EXmV-FiCyD7U76DoXSQoHlG30hFLD2c'
                                 b'uYWEQPp0mEu1U","sn":"0","ilk":"icp","sith":"1","keys":["DqI2cOZ0'
                                 b'6RwGNwCovYUWExmdKU983IasmUKMmZflvWdQ"],"nxt":"E7FuL3Z_KBgt_QAwuZ'
                                 b'i1lUFNC69wvyHSxnMFUsKjZHss","toad":"0","wits":[],"cnfg":[]}-AABA'
                                 b'A_-vC5z6_KnT2iWrA8-twdgh-BfjrWTlq8VN0sj6uQEyoE4zgoCive3x6GGvr1Hj'
                                 b'KHwpFRoXnsDsXanQV3QB0BQ')

        # apply msg to bob's Kevery
        bobKvy.processAll(ims=bytearray(msg))  # process local copy of msg
        bobK = bobKvy.kevers[bobPre]
        assert bobK.prefixer.qb64 == bobPre
        assert bobK.diger.qb64 == bobSrdr.dig
        assert bobK.diger.qb64 == 'Ey-05xXgtfYvKyMGa-dladxUQyXv4JaPg-gaKuXLfceQ'

        # apply msg to del's Kevery
        delKvy.processAll(ims=bytearray(msg))  # process remote copy of msg
        assert bobPre in delKvy.kevers

        # Setup Del's inception event assuming that Bob's next event will be an ixn delegating event
        verfers, digers = delMgr.incept(stem='del', temp=True) # algo default salty and rooted

        seal = eventing.SealLocation(pre=bobK.prefixer.qb64,
                                     sn="{:x}".format(bobK.sn+1),
                                     ilk=coring.Ilks.ixn,
                                     dig=bobK.diger.qb64)

        assert seal._asdict() == dict(pre='EXmV-FiCyD7U76DoXSQoHlG30hFLD2cuYWEQPp0mEu1U',
                                      sn='1',
                                      ilk='ixn',
                                      dig='Ey-05xXgtfYvKyMGa-dladxUQyXv4JaPg-gaKuXLfceQ')

        delSrdr = eventing.delcept(keys=[verfer.qb64 for verfer in verfers],
                                   seal=seal,
                                   nxt=coring.Nexter(digs=[diger.qb64 for diger in digers]).qb64)

        delPre = delSrdr.ked["pre"]
        assert delPre == 'Ek7M173EvQZ6kLjyorCwZK4XWwyNcSi6u7lz5-M6MyFE'

        delMgr.move(old=verfers[0].qb64, new=delPre)  # move key pair label to prefix
        assert delSrdr.dig == 'EeBPcw30IVCylYANEGOg3V8f4nBYMspEpqNaq2Y8_knw'

        # Now create delegating event
        seal = eventing.SealEvent(pre=delPre, dig=delSrdr.dig)
        bobSrdr = eventing.interact(pre=bobK.prefixer.qb64,
                                    dig=bobK.diger.qb64,
                                    sn=bobK.sn+1,
                                    data=[seal._asdict()])

        sigers = bobMgr.sign(ser=bobSrdr.raw, verfers=bobK.verfers)

        msg = bytearray(bobSrdr.raw)
        counter = coring.SigCounter(count=len(sigers))
        msg.extend(counter.qb64b)
        for siger in sigers:
            msg.extend(siger.qb64b)

        assert msg == bytearray(b'{"vs":"KERI10JSON00010e_","pre":"EXmV-FiCyD7U76DoXSQoHlG30hFLD2c'
                                b'uYWEQPp0mEu1U","sn":"1","ilk":"ixn","dig":"Ey-05xXgtfYvKyMGa-dla'
                                b'dxUQyXv4JaPg-gaKuXLfceQ","data":[{"pre":"Ek7M173EvQZ6kLjyorCwZK4'
                                b'XWwyNcSi6u7lz5-M6MyFE","dig":"EeBPcw30IVCylYANEGOg3V8f4nBYMspEpq'
                                b'Naq2Y8_knw"}]}-AABAA8_fyED6L-y6d8GUg1nKCMtfhyChd_6_bpfAXv1nMC76l'
                                b'zpyaPBTm0O6geoO9kBuaaBCz3ojPUDAtktikVRFlCA')

        # apply msg to bob's Kevery
        bobKvy.processAll(ims=bytearray(msg))  # process local copy of msg
        assert bobK.diger.qb64 == bobSrdr.dig  # key state updated so event was validated
        assert bobK.diger.qb64 == 'Eews7edyNg7fa-bze0UcCSCG4vitUo6dB5DetsoZA2NU'

        # apply msg to del's Kevery
        delKvy.processAll(ims=bytearray(msg))  # process remote copy of msg
        assert delKvy.kevers[bobPre].diger.qb64 == bobSrdr.dig

        # now create msg with Del's delegated inception event
        sigers = delMgr.sign(ser=delSrdr.raw, verfers=verfers)

        msg = bytearray(delSrdr.raw)
        counter = coring.SigCounter(count=len(sigers))
        msg.extend(counter.qb64b)
        for siger in sigers:
            msg.extend(siger.qb64b)

        assert msg ==bytearray(b'{"vs":"KERI10JSON000183_","pre":"Ek7M173EvQZ6kLjyorCwZK4XWwyNcSi'
                               b'6u7lz5-M6MyFE","sn":"0","ilk":"dip","sith":"1","keys":["DuK1x8yd'
                               b'pucu3480Jpd1XBfjnCwb3dZ3x5b1CJmuUphA"],"nxt":"EWWkjZkZDXF74O2bOQ'
                               b'4H5hu4nXDlKg2m4CBEBkUxibiU","toad":"0","wits":[],"cnfg":[],"seal'
                               b'":{"pre":"EXmV-FiCyD7U76DoXSQoHlG30hFLD2cuYWEQPp0mEu1U","sn":"1"'
                               b',"ilk":"ixn","dig":"Ey-05xXgtfYvKyMGa-dladxUQyXv4JaPg-gaKuXLfceQ'
                               b'"}}-AABAAMSF33ZiOLYH7Pg74MnMQjbfT_oq9wDeFy4ztfEWP0VagIKPqgYW_zrA'
                               b'kyJrZnQ-7-bfpekNtyRh3sN4doFseAg')


        # apply Del's delegated inception event message to bob's Kevery
        bobKvy.processAll(ims=bytearray(msg))  # process local copy of msg
        assert delPre in bobKvy.kevers  # successfully validated
        delK = bobKvy.kevers[delPre]
        assert delK.delegated
        assert delK.diger.qb64 == delSrdr.dig  # key state updated so event was validated
        assert delK.diger.qb64 == 'EeBPcw30IVCylYANEGOg3V8f4nBYMspEpqNaq2Y8_knw'

        # apply msg to del's Kevery
        delKvy.processAll(ims=bytearray(msg))  # process remote copy of msg
        assert delKvy.kevers[delPre].diger.qb64 == delSrdr.dig

        # Setup Del rotation event assuming that Bob's next event will be an ixn delegating event
        verfers, digers = delMgr.rotate(pre=delPre, temp=True)

        seal = eventing.SealLocation(pre=bobK.prefixer.qb64,
                                     sn="{:x}".format(bobK.sn+1),
                                     ilk=coring.Ilks.ixn,
                                     dig=bobK.diger.qb64)

        assert seal._asdict() == dict(pre='EXmV-FiCyD7U76DoXSQoHlG30hFLD2cuYWEQPp0mEu1U',
                                      sn='2',
                                      ilk='ixn',
                                      dig='Eews7edyNg7fa-bze0UcCSCG4vitUo6dB5DetsoZA2NU')

        delSrdr = eventing.deltate(pre=delK.prefixer.qb64,
                                   keys=[verfer.qb64 for verfer in verfers],
                                   dig=delK.diger.qb64,
                                   seal=seal,
                                   sn=delK.sn+1,
                                   nxt=coring.Nexter(digs=[diger.qb64 for diger in digers]).qb64)

        assert delSrdr.dig == 'EeiCC5kb8Ms2-T3lnx83kwEPq_iJBBL0QC03ab559Dts'

        # Now create delegating rotation event
        seal = eventing.SealEvent(pre=delK.prefixer.qb64, dig=delSrdr.dig)
        bobSrdr = eventing.interact(pre=bobK.prefixer.qb64,
                                    dig=bobK.diger.qb64,
                                    sn=bobK.sn+1,
                                    data=[seal._asdict()])

        sigers = bobMgr.sign(ser=bobSrdr.raw, verfers=bobK.verfers)

        msg = bytearray(bobSrdr.raw)
        counter = coring.SigCounter(count=len(sigers))
        msg.extend(counter.qb64b)
        for siger in sigers:
            msg.extend(siger.qb64b)

        assert msg == bytearray(b'{"vs":"KERI10JSON00010e_","pre":"EXmV-FiCyD7U76DoXSQoHlG30hFLD2c'
                                b'uYWEQPp0mEu1U","sn":"2","ilk":"ixn","dig":"Eews7edyNg7fa-bze0UcC'
                                b'SCG4vitUo6dB5DetsoZA2NU","data":[{"pre":"Ek7M173EvQZ6kLjyorCwZK4'
                                b'XWwyNcSi6u7lz5-M6MyFE","dig":"EeiCC5kb8Ms2-T3lnx83kwEPq_iJBBL0QC'
                                b'03ab559Dts"}]}-AABAA3V9qL1YINRBkSvkj-Q-NyMQoWpprrK05mrUYQNuc1EoP'
                                b'At9pBa8quPorxhB-Q0_DVAd5PI6zH9Wn5j0R_eZQDw')

        # apply msg to bob's Kevery
        bobKvy.processAll(ims=bytearray(msg))  # process local copy of msg
        assert bobK.diger.qb64 == bobSrdr.dig  # key state updated so event was validated

        # apply msg to del's Kevery
        delKvy.processAll(ims=bytearray(msg))  # process remote copy of msg
        assert delKvy.kevers[bobPre].diger.qb64 == bobSrdr.dig

        # now create msg from Del's delegated rotation event
        sigers = delMgr.sign(ser=delSrdr.raw, verfers=verfers)

        msg = bytearray(delSrdr.raw)
        counter = coring.SigCounter(count=len(sigers))
        msg.extend(counter.qb64b)
        for siger in sigers:
            msg.extend(siger.qb64b)

        assert msg == bytearray(b'{"vs":"KERI10JSON0001c2_","pre":"Ek7M173EvQZ6kLjyorCwZK4XWwyNcSi'
                                b'6u7lz5-M6MyFE","sn":"1","ilk":"drt","dig":"EeBPcw30IVCylYANEGOg3'
                                b'V8f4nBYMspEpqNaq2Y8_knw","sith":"1","keys":["DTf6QZWoet154o9wvze'
                                b'MuNhLQRr8JaAUeiC6wjB_4_08"],"nxt":"E8kyiXDfkE7idwWnAZQjHbUZMz-kd'
                                b'_yIMH0miptIFFPo","toad":"0","cuts":[],"adds":[],"data":[],"seal"'
                                b':{"pre":"EXmV-FiCyD7U76DoXSQoHlG30hFLD2cuYWEQPp0mEu1U","sn":"2",'
                                b'"ilk":"ixn","dig":"Eews7edyNg7fa-bze0UcCSCG4vitUo6dB5DetsoZA2NU"'
                                b'}}-AABAAXRILNpCj1-oLVbl4ZLSkNZTDDDudEVqk2nHxA--lNhacAI1P_5-uAjlr'
                                b'93cmy2WDXZA61ddtF7mI5SjRMnSqDA')

        # apply Del's delegated inception event message to bob's Kevery
        bobKvy.processAll(ims=bytearray(msg))  # process local copy of msg
        assert delK.delegated
        assert delK.diger.qb64 == delSrdr.dig  # key state updated so event was validated
        assert delK.diger.qb64 == 'EeiCC5kb8Ms2-T3lnx83kwEPq_iJBBL0QC03ab559Dts'

        # apply msg to del's Kevery
        delKvy.processAll(ims=bytearray(msg))  # process remote copy of msg
        assert delKvy.kevers[delPre].diger.qb64 == delSrdr.dig

    assert not os.path.exists(delKp.path)
    assert not os.path.exists(delDB.path)
    assert not os.path.exists(bobKp.path)
    assert not os.path.exists(bobDB.path)

    """End Test"""


if __name__ == "__main__":
    test_delegation()