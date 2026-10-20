from trainer.pipeline import Pipeline, PipelineState


class _Src:
    def __init__(self):
        self.n = 0

    def poll(self):
        self.n += 1
        return [{"kind": "input.delta", "dx": 1, "dy": 1}]


class _Proc:
    def process(self, ev, state):
        ev["processed"] = True
        return ev


class _Sink:
    def __init__(self):
        self.seen = []

    def emit(self, ev):
        self.seen.append(ev)


def test_pipeline_runs_one_tick():
    p = Pipeline("t")
    s, proc, sink = _Src(), _Proc(), _Sink()
    p.register_source(s)
    p.register_processor(proc)
    p.register_sink(sink)

    # run a single iteration manually
    for ev in s.poll():
        for pr in p.processors:
            ev = pr.process(ev, p.state)
        for sk in p.sinks:
            sk.emit(ev)

    assert len(sink.seen) == 1
    assert sink.seen[0]["processed"] is True


def test_state_defaults():
    st = PipelineState()
    assert st.aim_enabled and st.esp_enabled and st.recoil_enabled