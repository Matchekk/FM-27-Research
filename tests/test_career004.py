from copy import deepcopy
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from research.career_readonly004 import (PROBES,digest,public_report,section_summary,
    snapshot,summarize_probe)


class SnapshotTests(unittest.TestCase):
    def test_stable_copy_and_exclusive_existing_target(self):
        with tempfile.TemporaryDirectory() as temp:
            source=Path(temp)/'approved.fm';source.write_bytes(b'own synthetic fixture')
            target=Path(temp)/'private/snapshot.fm'
            r=snapshot(source,target,'approved.fm')
            self.assertTrue(r['stable']);self.assertEqual(digest(source),digest(target))
            with self.assertRaises(FileExistsError):snapshot(source,target,'approved.fm')
            self.assertEqual(target.read_bytes(),b'own synthetic fixture')

    def test_unapproved_source_and_size_stop_before_copy(self):
        with tempfile.TemporaryDirectory() as temp:
            source=Path(temp)/'other.fm';target=Path(temp)/'private.fm'
            with self.assertRaises(ValueError):snapshot(source,target,'approved.fm')
            source.write_bytes(b'123')
            with self.assertRaises(ValueError):snapshot(source,target,'other.fm',max_bytes=2)
            self.assertFalse(target.exists())

    def test_source_drift_is_retained_and_never_stable(self):
        with tempfile.TemporaryDirectory() as temp:
            source=Path(temp)/'approved.fm';target=Path(temp)/'private.fm'
            source.write_bytes(b'synthetic')
            with patch('research.career_readonly004.digest',side_effect=['a'*64,'a'*64,'b'*64]):
                r=snapshot(source,target,'approved.fm')
            self.assertFalse(r['stable']);self.assertTrue(target.exists())


class PublicCoverageTests(unittest.TestCase):
    def receipt(self):
        return dict(source_sha256_before='a'*64,source_sha256_after_copy='a'*64,
                    snapshot_sha256='a'*64,bytes=30,size_unchanged=True,mtime_unchanged=True,stable=True)

    def test_failure_missing_and_unresolved_are_not_zero_or_release(self):
        events=[dict(probe='open',status='ok',coverage=dict(game='FM27')),
                dict(probe='managed_clubs',status='failed',error_type='ReaderCheckError',private_error='PRIVATE_NAME PRIVATE_PATH'),
                dict(probe='players',status='started')]
        r=public_report(events,self.receipt(),dict(version='synthetic'),dict(status='timeout'),'a'*64)
        by={x['probe']:x for x in r['probes']}
        self.assertEqual(len(by),12);self.assertEqual(by['players']['status'],'started_unresolved')
        self.assertEqual(by['training']['status'],'not_started')
        self.assertNotIn('PRIVATE_NAME',str(r));self.assertNotIn('PRIVATE_PATH',str(r))
        for name in ('native_released','career_advance_released','replay_released',
                     'source_semantics_verified','career_rng_independence_verified'):
            self.assertIs(r[name],False)

    def test_post_reader_source_change_is_explicit(self):
        r=public_report([],self.receipt(),{},dict(status='completed'),'b'*64)
        self.assertFalse(r['snapshot']['stable_through_reader'])

    def test_metadata_uses_whitelist_and_claim_not_ui_truth(self):
        info=SimpleNamespace(game='FM27',build='27.0.1+2503222',known_build=True,
            game_date=date(2026,8,1),time_slot=0,save_name='PRIVATE_NAME',
            sections=[SimpleNamespace(name='game_info',schema=1,compressed_size=2,decompressed_size=3)])
        r=section_summary(info)
        self.assertFalse(r['game_date_semantics_verified']);self.assertNotIn('PRIVATE_NAME',str(r))
        info.sections[0].name='C:/PRIVATE/PATH'
        with self.assertRaises(ValueError):section_summary(info)

    def test_training_keeps_unknown_raw_code_without_label_guess(self):
        @dataclass
        class Calendar:
            weeks: tuple
            name: str='PRIVATE_NAME'
        day=SimpleNamespace(sessions=(SimpleNamespace(raw=304),SimpleNamespace(raw=303)))
        week=SimpleNamespace(week_start=date(2026,8,1),days=(day,))
        r=summarize_probe('training',[Calendar((week,))],{},None)
        self.assertEqual(r['teams'][0]['raw_session_counts'],{'303':1,'304':1})
        self.assertIsNone(r['individual_participation']);self.assertNotIn('PRIVATE_NAME',str(r))


if __name__=='__main__':unittest.main()
