# VALID-005 / MECH-003: passive process containment

This is a process-safety prerequisite, not a simulation or scientific result.
No FM executable, DLL, save, server, native adapter or game UI was started by
these tests. Existing observer source and native binaries remain unchanged.

## Admission and cleanup contract

`research/native_process005.py` provides:

```python
contained_call(command, env, log, output, timeout=90, on_start=None,
               *, max_processes=3, total_timeout=None)
confirmed_cleanup(output, expected_limit=None)
```

Only a harmless `sys._base_executable` capsule starts initially. It blocks on
private stdin. The parent assigns it to an unnamed, noninheritable Windows job,
checks membership in that specific job and reads back exact flags `0x2008`
(`KILL_ON_JOB_CLOSE | ACTIVE_PROCESS`) and the declared process limit. Only then
does it write the exclusive process receipt and send the authenticated GO
packet. The token is private stdin data; only its digest enters the capsule
environment, and neither enters receipts. The actual command environment loses
that digest and gains `FM27_CONTAINED_CALL_V1=1`.

No breakaway flags are permitted. Default limit 3 counts capsule, native host
parent and engine child. An explicit integer limit from 3 through 10 is
supported for a whole centrally supervised study: capsule, study Python child,
at most four host parents and four engine children. Ten processes never grants
permission for ten engine workers. No memory limit is claimed.

`timeout` observes progress in `log`; `None` disables this watchdog only when a
positive finite `total_timeout` is supplied. The whole-study caller retains
individual worker watchdogs. The output is exclusive stdout/stderr storage.
Actual-command cwd is `env['FM27_ENGINE_ROOT']` when present. Callbacks must be
bounded; this function does not interrupt a blocking Python callback.

Every path after Popen, including receipt errors, callback errors, stat errors,
normal exit, timeout and retained descendants, invokes `TerminateJobObject`,
waits for capsule exit and queries `JobObjectBasicAccountingInformation` until
`ActiveProcesses == 0`. An early parent exit with live descendants is an error,
followed by termination, rather than successful completion. Closing the last
job handle supplies a crash-safety fallback. If kernel zero plus capsule exit
cannot be confirmed, fallback closure never counts as confirmation.

Private receipts are `output.with_suffix('.process.json')` and
`output.with_suffix('.containment.json')`. The process receipt is written before
GO; its `host_start_permission_sent=False` is the historical pre-admission
state. The final receipt records whether GO was sent. Neither receipt contains
argv, command cwd, environment, token or raw command output.

`confirmed_cleanup(output, expected_limit=3)` strictly requires:

- schema `fm27.contained-call.v1`;
- `cleanup_confirmed is True` and `capsule_exit_confirmed is True`;
- `kernel_active_processes` is integer zero, excluding boolean false;
- `job_policy.limit_flags == 0x2008`, `kill_on_close is True`,
  `breakaway_allowed is False`, and the requested active process limit.

Missing, malformed or absent final receipts fail this predicate. An ordinary
post-start exception carries `.containment_evidence` after verified cleanup;
`CleanupUnconfirmed.evidence` carries unconfirmed cleanup and requires retaining
the external NativeLease/budget crash marker. A caller may conservatively retain
the marker when final receipt writing fails even if in-memory evidence says
zero. It must not start another native phase while cleanup remains uncertain.

Basic-accounting total-process and terminated-process values are raw Windows
counters, not unique launch counts or budget attempts. On this machine a
two-process chain returned total count 4; refusing CreateProcess at the cap can
return WinError 1816 without incrementing the terminated-process counter.
Central launch/budget ledgers remain authoritative for attempts.

## Harmless validation

Command: `python -m unittest tests.test_native_process005 -v` under the project
venv. Final run: **13 tests passed, 4.680 seconds** on Windows, Python 3.12.

Coverage: standard completion and token removal; assignment failure before GO;
pre-GO receipt failure; callback failure with a live parent/descendant;
post-GO progress-stat failure; progress and total timeouts; parent early exit;
an actual nested child job under cap 3; kernel refusal of a fourth process;
injected accounting failure resulting in CleanupUnconfirmed; final receipt IO
failure; cap 10 and invalid argument rejection; malformed receipt rejection.
The initial test pass had four assertion failures from treating Windows raw
accounting totals as unique process counts/limit terminations. The corrected
tests preserve cap 3, verify kernel cleanup and check actual WinError 1816.

No real observer/MECH host has yet been admitted by this module. The director
must review and integrate it, then serialize any preregistered native technical
probes under the existing global admission, seed, deadline and lease controls.
This change neither alters those controls nor grants a scientific main run.

## Platform references

The implementation uses the documented [Windows job-object lifetime and child
inheritance](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects),
[nested job behavior](https://learn.microsoft.com/en-us/windows/win32/procthread/nested-jobs),
[assignment API](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject)
and [basic accounting fields](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_accounting_information).
