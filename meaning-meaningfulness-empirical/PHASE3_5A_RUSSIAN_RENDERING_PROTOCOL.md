---
title: "Phase 3.5a Russian human-native rendering — protocol + AI-draft starter + user QC handoff"
date: 2026-05-27
session: Phase 3.5a (NEW required per user mid-session addendum)
covers_stylized_fact: "SF3 — cross-language collaboration preserving meaning while losing meaningfulness (Paper A 2026ao §SF3)"
status: "AI-drafted starter provided; AWAITS user human-native Russian-language pass before re-extraction and isomorphism computation"
human_native_required: true
---

# Phase 3.5a Russian human-native rendering — protocol + AI-draft starter + user QC handoff

## Why this Phase exists

Paper A 2026ao's SF3 states that "ρ is cohort-conditional and reconstructed per language; σ produces a language-invariant S." The framework's strongest single test of SF3 is to produce a Russian-language rendering of the paper's substrate by a Russian-native operator and verify whether the re-extracted spine preserves the locked propositions of the source.

User direction (a mid-work addendum): "Phase 3.5a (NEW required) — Task γ Russian human-native rendering." The "human-native" qualifier means the Russian rendering should be produced by a native Russian speaker (user) rather than by an LLM operating in Russian. (Phase 3.5b is the separate stretch task that tests cross-LLM Russian-operator robustness; the two phases are distinct.)

## Source-text selection (recommended)

Two candidate source texts. User selects one before producing the human-native rendering.

**Option A (recommended for SF3 evidence value): paper.md v1.0.0 §Abstract**

- Length: ~200 words in English
- Audience: tier-1 academic readership
- Density: highest information-per-word in the paper
- Why preferred: maximum compression already; rendering preservation result is the cleanest SF3 demonstration; easy to compare under strict typed-DAG re-extraction; published-research-substrate-already

**Option B: paper.md v1.0.0 §Theory §Positioning against adjacent strategy literatures**

- Length: ~700 words in English
- Audience: strategy-literature-engaged academic readership
- Density: moderate; includes named theoretical anchors
- Why considered: tests preservation of the integrative-engagement claims (Kaplan-Vakili 2015, Carlile 2004, etc.) across Russian rendering — a richer test, but at higher render-time cost

Default: Option A unless user explicitly asks for Option B.

## Rendering specifications

The user-produced Russian rendering must:

1. **Preserve all locked propositions of the source text** at semantic level. Locked propositions in the abstract:
   - P4 demonstration on two twin pairs at Rec = 4
   - Random-graph null baseline showing Pr(Rec ≥ 3 by chance) ≈ .000
   - Two self-application renderings (Substack + LinkedIn) preserving 11/14 and 4/4 substrate items
   - Secondary β/δ ordering supporting P3
   - Inter-coder κ pre-registered for v1.1.0
   - Engagement with recombinant-search and knowledge-representation scholarship
2. **Render at Russian-native register** — formal academic Russian appropriate for an SMJ-tier Russian-language audience. Direct calque from English is NOT human-native; a native speaker re-renders for Russian academic conventions (which differ from English on hedging density, sentence-length conventions, narrative-arc cues, citation density).
3. **Output as a single Markdown file**: `RENDERING_PB_ABSTRACT_RU.md` with frontmatter `rendering_language: ru`, `source_text_id: PB_v1_3_0_abstract`, `produced_by: human_native_russian_speaker`, `produced_at: 2026-MM-DD`.

## AI-draft starter

Below is a Claude-Opus-produced Russian rendering of paper.md v1.0.0 §Abstract. **This is NOT a final artifact**. The user reviews this draft as a starting point and either (a) edits substantively to bring it to human-native register, OR (b) replaces it entirely with a fresh native rendering, OR (c) authorizes use of the draft as research artifact only (NOT as published rendering) with the explicit caveat that the rendering is AI-produced.

### Source (English; from paper.md v1.0.0 §Abstract)

> This paper supplies an empirical demonstration of Zharnikov's (2026ao) Proposition P4 — rendering-equivalence under spine-preservation — in management theory. P4 holds that two prose renderings of a locked structural substrate converge on conclusions when both renderings preserve the substrate's typed-graph structure. The paper extends the companion theory's Heisenberg–Schrödinger historical existence proof into contemporary strategy research via retroactive structural extractions of two pairs of independently-authored papers: a dynamic-capabilities pair (Eisenhardt and Martin 2000 + Zollo and Winter 2002) and a knowledge-based-view pair from the SMJ Winter 1996 Special Issue (Grant 1996 + Liebeskind 1996). The recombination metric Rec returns 4 linked propositions with preserved antecedents on each pair. A random-graph null baseline shows Pr(Rec ≥ 3 by chance) ≈ .000 across 1,000 size-matched shadows. Two additional renderings of substrates already in the corpus — a 1,615-word practitioner-register Substack rendering of the paper's own structure and a 1,044-word LinkedIn rendering of the focal-pair shared substrate — preserve 11 of 14 locked propositions and 4 of 4 substrate items respectively. Secondary β/δ estimates satisfy the cost-asymmetry ordering. Inter-coder reliability on axiom A1 is pre-registered for v1.1.0 execution. The paper engages recombinant-search and knowledge-representation scholarship as theoretical antecedents.

### AI-draft Russian rendering (Claude Opus 4.7; FOR USER QC ONLY)

> Настоящая работа представляет эмпирическое подтверждение Положения P4 Жарникова (2026ao) — эквивалентности представлений при сохранении структурного остова (spine) — на материале теории менеджмента. P4 утверждает, что два прозаических представления одного зафиксированного структурного остова сходятся в выводах в том случае, когда оба представления сохраняют типизированную графовую структуру остова. Работа распространяет историческое доказательство существования из сопутствующей теории — пара Гейзенберга–Шрёдингера в основаниях квантовой механики — на современные стратегические исследования посредством ретроспективной структурной экстракции двух пар независимо написанных статей: пары по динамическим способностям (Eisenhardt and Martin 2000 + Zollo and Winter 2002) и пары по знаниецентричному взгляду на фирму из зимнего выпуска SMJ 1996 года (Grant 1996 + Liebeskind 1996). Метрика рекомбинации Rec возвращает 4 связанных предложения с сохранёнными предшественниками для каждой пары. Нулевой базовый уровень на случайных графах показывает, что Pr(Rec ≥ 3 случайно) ≈ .000 на 1 000 симулированных «теневых» остовах сопоставимого размера. Два дополнительных представления остовов, уже присутствующих в корпусе — Substack-представление в практическом регистре на 1 615 слов, отражающее собственную структуру работы, и LinkedIn-представление на 1 044 слова, отражающее общий остов фокальной пары, — сохраняют соответственно 11 из 14 зафиксированных предложений и 4 из 4 элементов остова. Дополнительные оценки β/δ соответствуют упорядочиванию ассимметрии затрат. Меж-кодировочная надёжность аксиомы A1 предзарегистрирована для исполнения в версии v1.1.0. Работа вступает в диалог с литературой по рекомбинантному поиску и репрезентации знаний как с теоретическими антецедентами.

**~270 words in Russian** (Russian typically renders ~30% longer than English at academic register on the same content).

### Known AI-draft limitations user should address

1. **Register**: AI-draft uses "Положение" for "Proposition" — common but not the only Russian academic-tradition convention. Native speaker may prefer "Утверждение", "Постулат", or "Тезис" depending on the work's epistemic stance.
2. **Term: "remarkably"-class hedging**: English academic prose hedges heavily ("approximately," "supplies an empirical demonstration"); Russian academic register often hedges less or uses different hedging markers. Native pass should adjust.
3. **Term: "корпус"** — "corpus" as a body of papers is rendered as "корпус", which is correct technical Russian but the connotation in everyday Russian leans toward "body" (anatomical). Native speaker may prefer "массив исследований" or "набор работ".
4. **Calque alert**: "сохраняют... элементов остова" is a fairly direct calque; native speaker may rephrase as "обеспечивают сохранность" or restructure the sentence.
5. **Reference formatting**: English-style "Eisenhardt and Martin 2000" is the standard form for citations even in Russian academic writing for strategy/management literature (where SMJ etc. are cited natively); this is appropriate. Native speaker confirms.
6. **Number formatting**: "1 000" uses Russian thin-space-as-thousands separator (correct); "≈ .000" uses leading-zero-suppressed English convention which the AMA style requires — verify Russian-target-venue allows or replace with "≈ 0,000" using Russian decimal comma.

## Post-rendering protocol (after user produces / approves Russian text)

1. User produces or approves the final Russian rendering and saves as `RENDERING_PB_ABSTRACT_RU.md`.
2. Operator (any subsequent session, Claude or human) re-extracts the spine from the Russian rendering using paper_a:appendix_B_protocol applied in reverse, using the same 10-node-type taxonomy + 17-edge-type catalog as for the English-source extraction. Output: `VALIDATION_CASE_PB_RUSSIAN_RENDERING_SPINE.yaml`.
3. The re-extracted Russian-rendering spine is compared against the source-text spine (extracted from paper.md v1.0.0 §Abstract under the same schema) for preservation of locked propositions, with attention to:
   - Same-claim preservation (does each English locked claim have a Russian-rendering counterpart?)
   - Same-node-typing preservation (does each Russian counterpart receive the same node type?)
   - Same-antecedent-edge preservation (does each Russian counterpart preserve the antecedent edges its English source had?)
4. Output: `CROSS_LANGUAGE_PRESERVATION_PB_RU.md` summarizing the preservation rate + per-claim verdict + any rendering-cost-frontier observations specific to the Russian-language register.
5. The Russian-rendering preservation result is integrated into paper.md v1.1.0 (NOT v1.0.0) §Discussion §SF3 cross-language preservation evidence subsection.

## Falsifier

- **≥ 90% locked-proposition preservation** (strict): SF3 holds at the Paper B abstract scale; cross-language P4 demonstration succeeds.
- **70-90% strict preservation, ≥ 95% semantic preservation**: SF3 holds with rendering-cost-frontier observations specific to Russian (analogous to Phase 2 / Phase 2.5 findings).
- **< 70% strict / < 95% semantic preservation**: SF3 weakens at this rendering boundary; trigger schema-refinement or honest disclosure that cross-language preservation requires register-specific operator discipline beyond what a single-pass rendering supplies.

## Why this phase stops here without computing the isomorphism

Per this work init prompt's design ("If only ONE task lands: do α") and the human-native requirement, computing an isomorphism on an AI-drafted Russian rendering would be lower-quality SF3 evidence than the human-native pass produces. The AI-draft is offered as Russian-rendering accelerant for user QC; the isomorphism computation waits for the human-native text.

this phase closes Phase 3.5a at:
- **Protocol documented** (this file)
- **AI-draft starter provided** (above; Claude Opus 4.7 produced; flagged as not-human-native)
- **User QC handoff** (user produces / edits / replaces / approves the final Russian rendering; user controls when re-extraction runs)

## Integration into v1.0.0 paper.md

The Phase 3.5a status (protocol locked + AI-draft + awaiting human-native pass) is disclosed honestly in paper.md v1.0.0 §Discussion §Cross-language preservation (NEW subsection) as the v1.1.0-scheduled SF3 evidence point. Actual cross-language preservation result lands in v1.1.0 once the human-native rendering exists.

---

*Phase 3.5a closes with Russian-rendering protocol locked + AI-draft starter + user-QC handoff. Cross-language preservation evidence lands at v1.1.0 with the human-native pass. Phase 3.5b (multi-LLM Russian-operator robustness) is a separate scope item; see PHASE3_5B_MULTI_LLM_OPERATOR_PROTOCOL.md.*
