import unittest
from hashlib import sha256
from analysis.night_supervise import validate_phase_keys


class SharpnessRouteTests(unittest.TestCase):
    def test_exact_technical_boundary_and_no_loader(self):
        study='MECH-002-SHARPNESS-P0'
        keys=[f'tech-{h}-s{s}-{a}-r{r}' for h in ('high_press','deep_block') for s in (0,1)
              for a in ('S70-P0','S100-P0','S70-P1','S100-P1') for r in (0,1)]+['negative-malformed']
        validate_phase_keys(study,'prepare',[])
        validate_phase_keys(study,'technical',keys)
        for phase,bad in [('prepare',['loader']),('technical',keys[:-1]),('technical',keys[::-1])]:
            with self.assertRaises(ValueError):validate_phase_keys(study,phase,bad)

    def test_exact_main_blocks_and_context_allocation(self):
        study='MECH-002-SHARPNESS-P0'
        keys=sorted([f'{h}-{seed}-{s}-{a}' for h,start in (('high_press',1),('deep_block',33))
                     for seed in range(start,start+32) for s in (0,1)
                     for a in ('S70-P0','S100-P0','S70-P1','S100-P1')],key=lambda k:sha256(k.encode()).digest())
        validate_phase_keys(study,'main',keys)
        for bad in (keys[:-1],keys[::-1],keys+['extra'],[k.replace('deep_block-33-','deep_block-1-') for k in keys],
                    [k.replace('high_press-1-','high_press-4294967296-') for k in keys]):
            with self.assertRaises(ValueError):validate_phase_keys(study,'main',bad)


if __name__=='__main__':unittest.main()
