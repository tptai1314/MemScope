# Kế hoạch tối đa (full-scope) — MemScope → JSA

Cập nhật: 2026-11-09. Đây là bản **đầy đủ nhất trong điều kiện thực tế**:
JSA rolling, chỉ có Android emulator, 1 người full-time. Toàn bộ dataset/hạng mục từng bị
đề xuất cắt đều được đưa lại, nhưng có **thứ tự ưu tiên, gate và fallback** để không biến
paper thành danh sách việc dở dang. Không có kết quả nào được bịa; mỗi ô bảng phải truy vết
được tới raw trace.

---

## 0. Track và ràng buộc

| Yếu tố | Giá trị | Hệ quả |
|---|---|---|
| Venue | Journal of Systems Architecture (rolling) | Không deadline cứng; 30 tuần là mốc tự đặt |
| Thiết bị | Android emulator (Windows host) | Không claim energy/thermal/StrongBox/Knox/phone latency |
| Nhân lực | 1 người full-time | Mỗi tuần 1 workstream chính; mọi thứ khác là phụ |
| Phạm vi | Full: T0 + T1 + T2 (gồm MemGUI-Bench, AndroidWorld) | 30 tuần + 2 tuần buffer |
| Mediation | App-level prototype trên emulator | Chỉ claim model property + mediation test; không claim complete mediation on device |
| Đóng gói | Reference implementation + emulator prototype + trace-driven evaluation | Contribution trung thực, đủ cho JSA nếu viết chặt |

**Ngày dự kiến:** W0 = 2026-11-09 → W30 ≈ 2027-06-07; buffer W31–W32.

---

## 1. Claim ladder (bắt buộc giữ)

### Tầng A — chứng minh (không phụ thuộc thiết bị)
- Admission soundness dưới 4 assumption.
- Expiry safety tại retrieval và release.
- Label monotonicity / conservative meet cho derived item.
- Cross-scope returned-plaintext non-disclosure *dưới complete mediation đã giả định*.
- Complexity bound của pre-ranking filtering.

### Tầng B — đo được (emulator + reference model)
- Out-of-scope retrieval rate, extraction yield, poisoned-write acceptance.
- Entitled Recall@k, EM/F1, FAMA, abstention, safety-critical survival.
- Attribution FAR/FRR, label meet accuracy, quarantine rate.
- p50/p95/p99 latency, storage amplification, compaction pause (emulator + Python).
- GUI task completion trên subset MemGUI-Bench/AndroidWorld (RQ7).

### Tầng C — không claim
- Semantic non-inference; leak qua model đã được cấp quyền; side channel; physical compromise.
- Energy/thermal/battery trên điện thoại thật; StrongBox/Knox behavior.
- Complete mediation trên thiết bị thương mại.

**Quy tắc:** mọi câu trong abstract phải ánh xạ vào A hoặc B; không câu nào rơi vào C.

---

## 2. Timeline 30 tuần

| Tuần | Workstream chính | Deliverable kiểm chứng |
|---|---|---|
| W0 | Khởi động | `git init`, tag `design-v1`, `DECISIONS.md` |
| W1 | Chốt lý thuyết/algorithm | Algorithm 1/2 + proof + code khớp; test cross-token |
| W2 | Data framework | Normalizer + schema validator + manifest generator |
| W3 | LoCoMo + LongMemEval | 2 adapter + golden test + split hash |
| W4 | Memora + PA-Bench | 2 adapter + invalidation/safety fields |
| W5 | Multi-app generator | 50 persona, 10²–10⁵ item, policy oracle, cross-app joins |
| W6 | Annotation handbook | Handbook v1 + 100 mẫu thử + sửa định nghĩa |
| W7–W8 | Annotation chính | 500 item + 250 query, 2 annotator, κ, adjudication |
| W9 | Baseline | 6 baseline chạy matched; unsupported reporting |
| W10 | Attack framework | Plugin contract + budget + strata + validation mode |
| W11 | SPORE + MINJA | Tái hiện/validate + negative controls |
| W12 | MEXTRA + ADAM | Tái hiện/validate; MemPoison-2 nếu kịp |
| W13 | Android prototype A | App + AIDL service + token + SQLCipher |
| W14 | Android prototype B | Keystore + audit + TTL + shadow-cache test |
| W15 | Cuttlefish (optional) | AOSP virtual device + privileged app; nếu host không hỗ trợ → bỏ |
| W16 | Instrumentation | Emulator trace parser + microbench harness |
| W17–W18 | RQ1 | Security matrix (6 method × 5 attack × 2 workload) |
| W19 | RQ2 | Utility/Pareto (4 dataset × 4 scope width × 3 k) |
| W20 | RQ3 + RQ4 | Attribution corpus + lifecycle scenarios |
| W21 | RQ5 + RQ6 | Emulator cost + retention/PA-Bench |
| W22–W23 | T2 GUI integration | MemGUI-Bench subset + AndroidWorld subset chạy được |
| W24–W25 | RQ7 | GUI task completion + memory-policy ablation |
| W26 | Phân tích | Bootstrap/Wilson/Holm; `results/*.tex` |
| W27 | Viết kết quả | Xóa placeholder; bảng/hình thật |
| W28 | Viết thân bài | Abstract/intro/discussion/limitations regenerate |
| W29 | Red team | 8 objection + negative controls + artifact audit |
| W30 | Đóng gói | Artifact + checksum + one-command + submit |
| W31–W32 | Buffer | Rerun κ thấp/attack lệch/thermal emulator |

**Gate:**
- **G0 (cuối W1):** `DECISIONS.md` xong; không đổi spec sau đó.
- **G1 (cuối W12):** SPORE + MINJA cho extraction ≥ 50% trên unscoped; nếu không → "stress test".
- **G2 (cuối W16):** prototype emulator chạy end-to-end 1 episode; nếu trượt → Python-only,
  RQ5 xuống appendix.
- **G3 (cuối W21):** toàn bộ T0 có kết quả + raw trace; nếu trượt → cắt T2 (W22–W25) để cứu paper.
- **G4 (cuối W25):** tất cả số liệu đóng băng; không chạy thêm thí nghiệm sau mốc này.

---

## 3. Chiến lược dữ liệu full-scope

### 3.1 Ma trận dataset

| Dataset | Tầng | Vai trò | Chi phí | RQ | Gate |
|---|---|---|---|---|---|
| LoCoMo | T0 | long-horizon utility | 3–4 ngày | RQ2 | Bắt buộc |
| LongMemEval | T0 | extraction/multi-session/temporal/abstention | 3–4 ngày | RQ2 | Bắt buộc |
| Memora | T0 | invalidation/forgetting/FAMA | 3–4 ngày | RQ2, RQ4 | Bắt buộc |
| PA-Bench protocol | T0 | safety-critical survival | 2–3 ngày | RQ6 | Bắt buộc |
| Multi-app synthetic | T0 | policy oracle, attack workload | 5–7 ngày | RQ1, RQ2 | Bắt buộc |
| ProfileFoundry | T1 | seed persona cho multi-app | 2–5 ngày | RQ1, RQ2 | Nên có |
| MemGUI-Bench (subset) | T2 | GUI agent memory | 3–4 tuần | RQ7 | Chỉ sau G3 |
| AndroidWorld (subset) | T2 | GUI task completion | 3–5 tuần | RQ7 | Chỉ sau G3 |

### 3.2 Quy tắc tích hợp từng bộ

**LoCoMo**
- Atomize theo turn + fact; giữ `conversation_id`, `session_id`, `turn_id`.
- Gắn label: purpose mặc định `social_support`; app `messaging`; consumer `primary_assistant`;
  sensitivity theo taxonomy; lifetime theo session horizon.
- Giữ nguyên official QA scorer; augmented score báo riêng.
- Không thay đổi text gốc; chỉ thêm metadata.

**LongMemEval**
- Giữ 5 ability ID: extraction, multi-session, temporal, update, abstention.
- Map mỗi evidence sang item; query giữ `question_type`, `answer`, `abstention` flag.
- Không tune prompt theo test; dev split riêng.

**Memora**
- Giữ chuỗi invalidation/update; mỗi item có `version`, `invalidated_by`, `valid_from`.
- FAMA scorer phải implement đúng định nghĩa paper gốc; test 10 ví dụ tay.

**PA-Bench protocol**
- Future-blind compression: ẩn câu hỏi tương lai khi nén.
- Safety facts: allergy, medication, emergency contact, pregnancy, implant.
- Byte budget cố định giữa các eviction method.
- Không dùng private data; chỉ dùng protocol công khai.

**Multi-app synthetic (core)**
- 50 persona; 5 app: messaging, calendar, health, shopping, travel.
- Item count scale: 10², 10³, 10⁴, 10⁵.
- Policy oracle: mỗi item có entitled consumers; mỗi query có unauthorized set.
- Cross-app joins: authorized, cần 2 token, bị cấm.
- Chèn: update, revocation, ambiguous purpose, malicious tool output.
- Generator phải deterministic theo seed; manifest ghi seed + hash.

**ProfileFoundry (T1)**
- Nếu artifact public: dùng để seed persona, giữ provenance.
- Nếu không: generator nội bộ đã có; ghi rõ "ProfileFoundry-style", không gọi là reproduction.

**MemGUI-Bench / AndroidWorld (T2)**
- Subset nhỏ: 100 task MemGUI, 50 task AndroidWorld.
- Chỉ chạy sau G3; license/version phải chạy được trên emulator hiện có.
- Nếu flaky > 20% task fail vì môi trường → báo riêng, không tính là utility loss.
- Kết quả RQ7 đặt ở section riêng, không trộn với RQ1–RQ6.

### 3.3 Schema và manifest (khớp repo)

Theo `MemScope/docs/data_format.md`, mỗi root có:

```text
<root>/
├── items.jsonl
├── queries.jsonl
├── splits.json
├── LICENSE_OR_TERMS.txt
├── PREPARATION_MANIFEST.json
├── policies.json          # mở rộng: policy đã biên dịch
└── authorship.json        # mở rộng: nguồn, version, checksum, annotator
```

Bắt buộc trong manifest: `origin_url`, `citation`, `version/commit`, `license_state`,
`download_date`, `raw_checksums`, `normalized_checksums`, `transformation_command`,
`annotation_handbook_version`, `annotator_agreement`, `split_hash`, `exclusions`.
Không commit dữ liệu có license; đặt ngoài repo, trỏ bằng manifest.

---

## 4. Annotation (500 item + 250 query)

**Mục tiêu:** ground truth đủ chắc để reviewer không thể nói "labels là do tác giả tự nghĩ".

1. **Handbook 10–12 trang**
   - 5 dimension: purpose, app, tool, consumer, sensitivity + lifetime.
   - Định nghĩa derived item: source set, phép meet, ngoại lệ declassification.
   - 20 ví dụ dương/âm/dễ nhầm cho mỗi dimension.
   - Quy tắc khi không chắc: chọn **hẹp hơn** (fail-closed) và ghi lý do.

2. **Lấy mẫu**
   - 500 item stratified: dataset × app × sensitivity × purpose × derived/direct.
   - 250 query stratified: RQ1 (unauthorized), RQ2 (entitled), RQ4 (expired/revoked), RQ6 (safety).
   - Giữ 10% làm "challenge set" chỉ dùng test, không tune.

3. **Quy trình**
   - 2 annotator độc lập, part-time 2–3 ngày/tuần, tổng 2 tuần.
   - Mỗi người annotate 100% mẫu; không chia đôi.
   - Tính Cohen's κ từng dimension; mục tiêu ≥ 0.70.
   - Dimension < 0.70 → sửa handbook, annotate lại 100 mẫu mới, tính lại.
   - Adjudication 100% disagreement bởi người thứ 3 (hoặc tác giả nếu chỉ 2 người);
     lưu lý do vào `adjudication.jsonl`.

4. **Báo cáo**
   - Bảng κ theo dimension + dataset.
   - Tỉ lệ disagreement + ví dụ điển hình.
   - Official score và augmented score **riêng**.
   - Ghi rõ annotation là của tác giả, không phải nhãn chính thức của benchmark.

5. **Kiểm soát chất lượng**
   - 10% mẫu annotate lại sau 1 tuần để đo intra-annotator agreement.
   - Spot-check bởi người ngoài nếu có.
   - Freeze handbook + sample hash trước khi annotate full.

---

## 5. Baseline (6 nhóm)

| Baseline | Mức | Cách làm | Fallback |
|---|---|---|---|
| Unscoped | Bắt buộc | đã có | — |
| Namespace (Mem0/Letta-style) | Bắt buộc | đã có; version-pin nếu chạy Mem0 thật | reference implementation |
| Prompt-only | Bắt buộc | đã có | — |
| AppSearch visibility | Bắt buộc (emulated) | mô phỏng visibility + caller UID | ghi "emulated" |
| GAAP-style IFC | Analytical | mô tả flow monitor, không có memory label | không bịa số |
| Audience-Bound / MNC | Analytical | mô tả scope model | không bịa số |

**Công bằng:** cùng history, query, ranker, k, seed, byte budget, model, số tool call.
Nếu baseline không biểu diễn được policy → "unsupported", không tính là denial.
Mọi baseline chạy qua cùng harness, cùng scorer, cùng split.

---

## 6. Attack (5 nhóm + negative controls)

| Attack | Tầng | Mục tiêu | Validation |
|---|---|---|---|
| SPORE | Bắt buộc | malicious tool persistence | tái tạo published yield ±5 điểm |
| MINJA | Bắt buộc | query-only injection | tái tạo admission rate |
| MEXTRA | Bắt buộc | black-box extraction | tái tạo extraction yield |
| ADAM | Nên có | adaptive extraction | nếu artifact không có → reimplementation |
| MemPoison | Nên có | triggerable/compositional | 2 setting, ghi rõ setting nào |

**5 success strata** (báo cáo tách):
1. Direct unauthorized item return.
2. Model paraphrase attributable to unauthorized item.
3. Unauthorized tool argument.
4. Poisoned item admission.
5. Poisoned behavior activation.
6. Availability degradation.

**6 negative controls bắt buộc:** shadow cache, replay token, always-accept attribution,
authorized-copy, ranker bypass, clock rollback. Mỗi cái phải phá được guarantee tương ứng;
kết quả được báo cáo, không giấu.

---

## 7. Android prototype (emulator)

### Tier-1 (bắt buộc)
- App Kotlin/Java, emulator API 34/35.
- `MemScopeManager` foreground service, process riêng, AIDL Binder.
- Caller identity: `Binder.getCallingUid()` + package + certificate digest.
- Token: HMAC-SHA256, key trong Android Keystore (software-backed; ghi rõ).
- Store: SQLCipher hoặc Room + column encryption; AppSearch local nếu khả thi
  (`androidx.appsearch:appsearch-local-storage`), ghi rõ không phải PlatformStorage.
- TTL, revocation epoch, audit content-free, tombstone, compaction.
- Agent SDK: `issueToken`, `write`, `retrieve`.

### Tier-2 (optional, chỉ nếu host hỗ trợ)
- Cuttlefish AOSP virtual device trên Linux/WSL2 + KVM.
- Privileged system app + signature permission; thử Binder identity thật.
- Nếu Windows host không hỗ trợ KVM/Cuttlefish → bỏ, ghi vào Limitations.

### Không làm
- Patch `system_server`, AppSearch PlatformStorage thật, AppFunctions interception,
  Knox/StrongBox. Ghi rõ khoảng cách trong Implementation + Limitations.

### Complete mediation audit
- Liệt kê mọi cache/log/cloud store trong build.
- Test shadow cache để thấy guarantee bị phá khi có đường vòng.
- Kết quả này là **positive evidence của giới hạn**, không phải điểm yếu bị giấu.

---

## 8. Ma trận thực nghiệm RQ1–RQ7

### RQ1 — Enforcement
- 6 method × 5 attack × 2 workload (multi-app, LoCoMo-augmented).
- 60 episode/cell, 5 seed.
- Metric: OSR, extraction yield, sensitive atom disclosure, poisoned-write acceptance.
- Acceptance: extraction giảm ≥ 10× so với unscoped; OSR < 1%.

### RQ2 — Utility/Pareto
- 4 dataset × 4 scope width × k ∈ {5,10,20}.
- Metric: entitled Recall@k, EM/F1, FAMA, abstention.
- Output: bảng + hình Pareto.
- Acceptance: mất ≤ 3 điểm accuracy ở scope mặc định.

### RQ3 — Derivation
- 1.200 cặp, 7 loại; 2 annotator; dev/test tách trước khi tune.
- Verifier: extractive, local NLI, optional cloud NLI.
- Metric: FAR, FRR, meet accuracy, quarantine rate.
- Acceptance: FAR < 5% ở high-sensitivity; nếu không → quarantine-first.

### RQ4 — Lifecycle
- 6 kịch bản × 200 trial.
- Kỳ vọng: 0 item hết hạn/bị thu hồi được trả; replay/clock rollback fail closed.

### RQ5 — System cost (emulator + reference model)
- Microbench: token, projection, policy, ranking, decrypt, audit.
- 30 rep × 3 restart; p50/p95/p99.
- Storage amplification, compaction pause, key-op cost.
- Python scale 10²–10⁵ item.
- Acceptance: p95 < 50 ms; ghi rõ không suy ra phone latency/energy.

### RQ6 — Retention
- PA-Bench + multi-app; 4 byte budget.
- Eviction: recency, relevance, size-only, random, MemScope.
- Metric: safety-critical survival.
- Acceptance: 100% hard-pinned; thắng baseline ≥ 10 điểm.

### RQ7 — GUI task completion (T2)
- MemGUI-Bench subset 100 task; AndroidWorld subset 50 task.
- Điều kiện: cùng app setup, cùng model, cùng seed; flaky task báo riêng.
- Metric: task success, tool-call count, memory-induced failure.
- Acceptance: không giảm > 5 điểm task success so với unscoped trên task hợp lệ.

### Ablations
Bỏ từng: purpose, app, tool, consumer, lifetime, pre-ranking filter, token binding, derived meet,
attribution verification, read-time TTL, epoch revalidation, policy-aware eviction, compartment
encryption. Mỗi ablation 1 dòng bảng + 1 hình.

---

## 9. Code changes (file-level)

| Ưu tiên | File | Việc |
|---|---|---|
| P0 | `src/memscope/data/adapters.py` | 4 adapter thật + policies/authorship + split hash |
| P0 | `src/memscope/experiments/run_evaluation.py` | Bỏ `NotImplementedError`; pipeline đầy đủ |
| P0 | `src/memscope/experiments/run_attacks.py` (mới) | 5 attack × 6 method × strata |
| P0 | `src/memscope/adapters/attacks.py` | SPORE/MINJA/MEXTRA/ADAM/MemPoison + validation |
| P0 | `src/memscope/metrics/core.py` | FAMA, abstention, atom disclosure, strata, per-query yield |
| P0 | `src/memscope/baselines/external.py` | AppSearch-visibility emulated; GAAP/audience analytical |
| P0 | `src/memscope/experiments/run_gui.py` (mới) | MemGUI/AndroidWorld harness (T2) |
| P1 | `src/memscope/experiments/run_annotation.py` (mới) | Sheet, κ, adjudication |
| P1 | `src/memscope/experiments/run_emulator_bench.py` (mới) | Trace parser → metrics |
| P1 | `scripts/make_paper_tables.py` (mới) | JSON → `results/*.tex` |
| P1 | `scripts/power_analysis.py` (mới) | N từ pilot |
| P1 | `scripts/freeze_protocol.py` (mới) | Hash + timestamp protocol trước final run |
| P1 | `android/` (mới) | Prototype app + AIDL + SDK + instrumentation |
| P1 | `sections/experiments.tex` + `figures/pgfplots_placeholder_results.tex` | Thay placeholder |
| P2 | CI | Python 3.11/3.12, ruff + mypy, artifact smoke |
| P2 | `docs/ec2_experiment_guide.md` | Lệnh chạy thật + manifest |

Quy ước: deterministic theo seed; không network trong test; `git init` + tag mỗi cell;
không commit dữ liệu license.

---

## 10. Thống kê

- Paired theo episode + seed; median + bootstrap 95% CI (10.000 resample).
- Tỉ lệ: Wilson; cặp: exact McNemar.
- Family: RQ1 attacks; RQ2 datasets; RQ5 components; RQ7 environments. Holm correction.
- Effect size: Cliff's delta hoặc chênh lệch + CI.
- Power: pilot 30 episode; Δ = 3 điểm, SD = 8 → n ≈ 56 → chọn 60/cell.
- Pre-registration: freeze protocol + analysis plan trước final run (`freeze_protocol.py`).
- Ghi mọi exclusion và failed run.

---

## 11. Viết paper (full-scope)

### Cấu trúc và độ dài mục tiêu
| Section | Trang | Trạng thái | Việc |
|---|---|---|---|
| Abstract | 0.3 | Có | Regenerate từ summary; bỏ phone claim |
| Introduction | 2 | Có | Thêm findings preview + 5 contribution |
| Related work | 2.5 | Có | Refresh T-14; thêm concurrent 2026 |
| Preliminaries | 1.5 | Có | Sửa theo `DECISIONS.md` |
| System model | 2 | Có | Giữ |
| Threat model | 1.5 | Có | Giữ + negative controls |
| Problem formulation | 1.5 | Có | Chốt atom + empty-GT |
| Methodology | 3 | Có | Sửa Algorithm 1/2 |
| Theory | 3 | Có | Map assumption → test |
| Implementation | 3 | **Viết lại** | Reference model + emulator prototype + TCB |
| Experiments | 7–8 | Placeholder | Thay toàn bộ |
| Discussion | 1.5 | Có | Kết quả ủng hộ/phủ định |
| Limitations | 1 | Có | Emulator-only, no complete mediation |
| Conclusion | 0.5 | Có | Regenerate |
| Appendix | 8–10 | Có | Proofs, reproducibility, policy examples |

### Bảng/hình phải có
- T1: Dataset + annotation κ.
- T2: RQ1 security matrix (6 × 5, CI).
- T3: RQ2 utility/Pareto.
- T4: RQ3 attribution FAR/FRR.
- T5: RQ4 lifecycle pass rate.
- T6: RQ5 latency/storage decomposition.
- T7: RQ6 retention survival.
- T8: RQ7 GUI task completion.
- T9: Ablations.
- F1: Architecture (đã có).
- F2: Method pipeline (đã có).
- F3: Token/sequence flow.
- F4: Pareto utility–privacy.
- F5: Retention under byte budget.
- F6: Latency breakdown.
- F7: Attack strata heatmap.
- F8: Lifecycle timeline.

### Narrative (5 contribution)
1. Labeled-memory abstraction + task-rooted token.
2. Verified derivation + conservative meet.
3. Retrieval-time expiry + policy-aware eviction.
4. Reference implementation + emulator prototype (honest TCB).
5. Attack/utility/retention/GUI evaluation with negative controls.

### Câu không được viết
- "on-device measurements", "phone energy", "complete mediation on Android", "StrongBox-backed",
  "deployed", "real users".
- Thay bằng: "emulator-based", "reference implementation", "under the complete-mediation
  assumption", "software-backed Keystore".

---

## 12. Rủi ro và fallback

| Rủi ro | Xác suất | Tác động | Fallback |
|---|---|---|---|
| Reviewer từ chối vì không có hệ thống thật | Cao | Reject | Nhấn formal + reference impl + attack eval; ghi rõ emulator; JSA phù hợp |
| SPORE/MINJA không tái tạo | Cao | RQ1 yếu | Reimplementation + validation; gọi "stress test" |
| Attribution FAR cao | Trung bình | RQ3 yếu | Quarantine-first + human review |
| Scope hẹp → utility sụp | Trung bình | RQ2 xấu | Pareto trung thực + policy default |
| κ < 0.70 | Trung bình | Ground truth yếu | Sửa handbook, annotate lại; báo κ thật |
| MemGUI/AndroidWorld flaky | Cao | RQ7 nhiễu | Subset nhỏ, báo flaky riêng, không tính utility |
| Windows không chạy Cuttlefish | Cao | Mất Tier-2 | Bỏ Tier-2, ghi Limitations |
| 1 người ốm/bận | Trung bình | Trễ | Buffer 2 tuần + cut-list |
| Hết thời gian | Trung bình | Trễ | Cut theo thứ tự dưới |

**Cut-list (cắt từ trên xuống):**
1. MemPoison setting 2
2. ADAM
3. Cuttlefish/Tier-2
4. RQ7 AndroidWorld subset
5. RQ7 MemGUI subset
6. ProfileFoundry (giữ generator nội bộ)
7. RQ6 → appendix
8. RQ4 reboot scenario

**Không được cắt:** SPORE, MINJA, MEXTRA, RQ1, RQ2, RQ5 latency, negative controls,
formal section, multi-app synthetic.

---

## 13. Definition of Done (submission gate)

- [ ] 0 placeholder/pending/expected-trend trong `main.pdf`.
- [ ] Mỗi số trong abstract có ≥ 1 bảng kèm CI + N + seed.
- [ ] `45+` test pass trên Python 3.11 và 3.12; test cho mọi assumption.
- [ ] 6 negative controls chạy và được báo cáo.
- [ ] Attack không tái tạo published number đều ghi "reimplementation".
- [ ] κ ≥ 0.70 cho mọi dimension dùng làm ground truth.
- [ ] Raw trace manifest: mỗi ô bảng → hash + config + seed + commit.
- [ ] Artifact one-command smoke test trên máy sạch (Docker/Linux + Windows notes).
- [ ] Protocol + analysis plan đã freeze trước final run.
- [ ] Literature refresh trong 14 ngày trước submit.
- [ ] Abstract/Implementation/Limitations không còn claim phone/energy/complete-mediation.
- [ ] Author/venue/ethics/funding/conflict đã điền.
- [ ] Rebuttal nội bộ cho 8 objection.
- [ ] Reproducibility appendix khớp từng file thật.

---

## 14. Sprint 0 mở rộng (14 ngày đầu)

**Ngày 1–2**
- `git init`, commit hiện trạng, tag `design-v1`.
- Tạo `DECISIONS.md` với 5 quyết định.
- Ghi track JSA/emulator/full-scope vào `DECISIONS.md`.
- Tạo `results/`, `results/README.md`, `protocol/` (freeze hash).

**Ngày 3–5**
- Sửa Algorithm 1/2 + proof + code; test cross-token.
- Sửa `docs/data_format.md` thêm `policies.json` + `authorship.json` (đã làm trong repo).
- Viết `normalizer` skeleton + manifest generator.

**Ngày 6–8**
- Gửi đơn xin LoCoMo/LongMemEval/Memora/PA-Bench.
- Viết `LocomoAdapter` + golden test trên 1 conversation.
- Viết `scripts/make_paper_tables.py` skeleton.

**Ngày 9–11**
- Viết `MemoraAdapter` + `PABenchAdapter` skeleton.
- Viết `scripts/freeze_protocol.py`.
- Chạy `pytest`, `run_synthetic_demo`, ghi baseline hash.

**Ngày 12–14**
- Họp gate G0: chốt spec, dataset, cut-list.
- Bắt đầu W1 chính thức: sửa theory + test.

---

## 15. Việc cần bạn xác nhận (để không chệch)

1. **T2 có bắt buộc không?** Nếu có, plan giữ 30 tuần; nếu không, rút còn 26 tuần.
2. **Có ai phụ annotation 2–3 ngày/tuần không?** Nếu không, phải giảm còn 300 item + 150 query
   hoặc kéo dài W7–W8 thêm 1 tuần.
3. **Host có Linux/WSL2 + KVM cho Cuttlefish không?** Nếu không, bỏ Tier-2 ngay từ W0.
4. **Có ngân sách API cho cloud NLI/agent không?** Nếu không, dùng local model và ghi rõ.

Trả lời 4 câu này sẽ chốt được timeline cuối cùng; mọi thứ còn lại trong plan đã ở mức
full-scope.
