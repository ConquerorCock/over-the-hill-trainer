from trainer.config import AimConfig, RecoilConfig
from trainer.processors.aim_processor import AimProcessor
from trainer.processors.recoil_processor import RecoilProcessor
from trainer.pipeline import PipelineState


class _MemStub:
    def attach(self): pass
    base_address = 0


def test_aim_passthrough_when_disabled():
    p = AimProcessor(_MemStub(), AimConfig(enabled=False))
    ev = {"kind": "input.delta", "dx": 5, "dy": 5}
    out = p.process(ev, PipelineState())
    assert "aim_delta" not in out


def test_recoil_emits_delta():
    p = RecoilProcessor(_MemStub(), RecoilConfig(enabled=True, pattern="ak", strength=1.0))
    ev = {"kind": "input.delta", "dx": 0, "dy": 0}
    out = p.process(ev, PipelineState())
    assert "recoil_delta" in out
    assert out["recoil_delta"]["dy"] > 0
</>
</>
</>
</>
</>
</>
</>
</>