# MODON Portfolio – Project Control Review
**Weaknesses and corrective actions, project by project**

| | |
|---|---|
| Review date | 27-Oct-2026 |
| Latest data date reviewed | 19 to 21 Oct 2026 (W3/W4 uploads) |
| Sources | Only the `MD Files` conversions in this repository: schedule exports (XER→MD), WPR workbooks, risk/issue logs, procurement logs, look-aheads, failed-start lists, presentations, and the BOQ/drawing MDs |
| Method | (1) A script computed schedule-health metrics on every schedule MD: status counts, forecast vs contract finish, negative/high float, BEI, activities past their planned finish but still open, actuals dated after the data date, and activity-level slip against the baseline. (2) A line-by-line review of the weekly reports for progress, cost, procurement, resources, engineering, HSE/QA, risk and reporting quality. |

> **Main portfolio message:** On most projects the headline SPI says "ahead" while the schedule says "late". The SPI comes from front-loaded cost weighting or a re-baselined plan. The real drivers of delay sit in a few areas: MV/SEC power interfaces, utility clashes, long-lead electrical and air-dome procurement, and consultant review backlogs. A further problem is that weekly reports often copy figures forward from the previous week without updating them.

---

## 1. Portfolio dashboard

### 1.1 Data availability (what can be controlled at all)

| # | Project | BOQ | Drawings | Baseline | Weekly updates | Controllability |
|---|---|---|---|---|---|---|
| 01 | Riyadh 4th IC Infrastructure (RHD4-02-002) | – | – | ✅ (unscheduled, no float) | W1, W2, W3 (W2 WPR only; XER only inside ZIP) | Partial |
| 02 | Jeddah 3rd IC Infrastructure | – | – | ⚠ RAR, no MD | – | **None** |
| 03 | Al-Kharj IC Networks (KHJ1-02-007) | ✅ | ⚠ cover + list only | ✅ | W2–W4 | Good |
| 04 | Jeddah 3rd IC Completion | – | – | ⚠ RAR, no MD | – | **None** |
| 05, 06, 10, 11, 13, 14, 20, 23, 24 | (9 projects) | – | – | – | – | **None – nothing uploaded** |
| 07 | Sudair Ph.2 Pt.2 Infrastructure (SUD1-02-011) | – | – | ✅ (only inside W4) | W1–W4 | Good |
| 08 | Jeddah 1st IC 1 km² (JDH1-02-003) | – | – | ✅ | W1–W3 | Good |
| 09 | Tabuk Networks Completion | – | – | ✅ (Revised Rev 02) | W1–W3 | Good |
| 12 | Jeddah Oasis Land Dev. (JHD4-02-007) | – | – | ✅ (Recovery BL) | W1–W3 | Good |
| 15 | Hail Ready Factories Pkg 3 (HAL1-05-009) | – | – | ❌ | W1–W4 (dashboard .xlsb not converted) | Weak |
| 16 | Makkah 2nd IC Networks (MKH2-02-003) | – | – | ✅ | W1–W3 | Good |
| 17 | Makkah 2nd IC Akishiya Roads (MKH2-02-004) | – | – | ✅ | W1–W3 | Good |
| 18 | Sudair SAR Passenger Station (SUD1-05-018) | – | – | ✅ | – | **Baseline only** |
| 19 | Stadiums – Central (MLTX-02-003) | – | – | ✅ (Recovery) | W1–W2 (W3 misfiled under 22) | Good |
| 21 | Stadiums – Western (MLTX-02-004) | – | – | ✅ (B1, no float) | W1–W3 | Good |
| 22 | Stadiums – Eastern | – | – | – | W3, but **it is project 19's report** | **None** |
| 25 | Najran Craftsmen (NJR1-05-005 / NJR1-01-007) | – | – | ✅ | W1–W3 (no schedule update) | Partial |

- 12 of 25 projects (48%) have no usable control data: 02, 04, 05, 06, 10, 11, 13, 14, 20, 22 (holds project 19's report), 23, 24. Project 18 has only a 6-month-old baseline.
- Only 1 project has a BOQ.
- Only 1 project has any drawing content.

### 1.2 Status summary (latest week)

**Reading the table:**
- **Forecast vs contract:** positive means late, negative means early.
- **Reported SPI:** the SPI stated in the WPR.
- **BEI (Baseline Execution Index):** activities finished ÷ activities the baseline required finished by the data date. 0.95 or above is acceptable. This index is computed from the schedule MD files.
- **Rating:** the overall project rating, explained in the legend under the table.

| # | Project | Time elapsed | Earned vs planned | Reported SPI | Forecast finish | vs contract | Total float (min) | BEI | Rating |
|---|---|---|---|---|---|---|---|---|---|
| 01 | Riyadh 4th IC | 35% | 21.0 / 22.2 % | 0.95 (was 0.51) | 06-Feb-29 | **+252 d** | n/a | n/a | 🔴 |
| 03 | Al-Kharj IC | 44% | 35.2 / 34.2 % (physical 47.0 / 52.5) | 1.03 (physical 0.89) | 20-Nov-27 | –12 d* | **–170 d** | 0.83 | 🔴 |
| 07 | Sudair Ph.2 Pt.2 | 52% | 48.3 / 39.1 % | 1.23 | 05-Jul-27 (pinned) | 0 d* | 0 (constrained) | **0.75** | 🟠 |
| 08 | Jeddah 1st IC | 46% | 78.7 / 53.2 % | 1.48 | 20-May-28 | **+184 d** | –157 d | 0.85 | 🔴 |
| 09 | Tabuk Networks | 56% | 48.0 / 37.7 % (vs revised plan) | 1.27 (≈0.72 vs original) | 07-Oct-27 | +34 d | –29 d | 0.89 | 🟠 |
| 12 | Jeddah Oasis | 61% | 95.2 / 61.4 % | 1.55 | 14-Jan-27 | –129 d (but +57 d vs MODON target 23-Nov-26) | +102 d | 1.00 | 🟡 |
| 15 | Hail Factories Pkg 3 | 88% | 98.2 / 93.2 % | 1.05 | 02-Nov-26 | –31 d* | 0 | n/a (no baseline) | 🟠 |
| 16 | Makkah 2nd IC Networks | 45% | 77.7 / 55.8 % | 1.39 | 30-Aug-27 | +16 d (improving) | –14 d | 0.95 | 🟡 |
| 17 | Akishiya Roads | 28% | 33.4 / 19.1 % | 1.74 | 14-Oct-27 | **+51 d** (worsening) | –43 d | 0.81 | 🔴 |
| 19 | Stadiums – Central | 80% | 69.0 / 80.3 % | 0.86 | 07 to 10 Feb-27 | **+53 to 56 d** | –47 d | 0.88 | 🔴 |
| 21 | Stadiums – Western | 68% | 35.4 / 39.1 % | 0.90 | 09-May-27 | **+104 d** | –85 d | 0.88 | 🔴 |
| 25 | Najran Craftsmen | 76% | 98.5 / 77.9 % (100% vs crash plan) | 1.27 | 15-Oct-26 (passed) | missed own target | n/a | n/a | 🟡 |
| 18 | Sudair SAR Station | – | not reported | – | – | – | – | – | ⚫ |
| 02, 04, 05, 06, 10, 11, 13, 14, 20, 22, 23, 24 | – | – | not reported | – | – | – | – | – | ⚫ |

\* These forecast figures are not credible. The reasons are in each project's section below.

**Rating legend:**
- 🔴 critical: delay of 50 days or more, or a non-credible forecast hiding a large delay.
- 🟠 at risk.
- 🟡 watch.
- ⚫ no data, so the project cannot be controlled.

### 1.3 Schedule-health evidence (computed from the schedule MDs)

| # | Latest update | Activities (done / in progress / not started) | Open activities past planned finish | Activities with negative float | Activities slipped vs baseline (median) | Weekly finish movement |
|---|---|---|---|---|---|---|
| 03 | 17-Oct | 3,531 / 257 / 2,092 | 100 (same in all 3 weeks) | 701 | 4,170 (median +111 d) | 02-Dec → 17-Nov → 20-Nov-27 |
| 07 | 19-Oct | 787 / 300 / 1,028 | 74 to 108 | 0 (finish constrained) | 628 (up to +249 d) | locked at 05-Jul-27 |
| 08 | 20-Oct | 1,278 / 204 / 423 | 57 | 457 | 1,222 (median +21 d) | **+7 d every week** |
| 09 | 19-Oct | 587 / 203 / 702 | 42 | 220 | 663 (up to +138 d) | 02 → 03 → 07-Oct-27 |
| 12 | 20-Oct | 1,176 / 24 / 18 | 1 | 0 | 626 (up to +211 d) | stable |
| 15 | 19-Oct | 1,701 / 60 / 66 | 23 | 0 | n/a | 17 → 01 → 07 → 02-Nov-26 |
| 16 | 20-Oct | 312 / 30 / 57 | 9 | 43 | 351 (median +25 d) | 26-Sep → 12-Sep → 30-Aug-27 |
| 17 | 20-Oct | 148 / 34 / 199 | 2 | 168 (44% of network) | 325 (median +22 d) | +4 to 7 d every week |
| 19 | 09-Oct | 1,591 / 205 / 133 | 108 | 205 | 638 | **+7 d every week; 0 activities completed in the week** |
| 21 | 19-Oct | 1,728 / 21 / 385 | 0 | 330 | 686 (up to +111 d) | **+7 d every week** |

**What the patterns mean:**
- **A forecast that moves 7 days every 7 days** (08, 19, 21, and almost 17) means the driving path made no progress during the week. In each case the driving path is an approval, procurement or third-party item that is restarted at the data date every week instead of being progressed.
- **"Open activities past planned finish"** means the update was not rescheduled properly: activities remain open with finish dates already behind the data date. This shows on 03 (100, constant), 07 (74 to 108), 19 (108) and 15 (23).
- **Actual dates after the data date** were found in 03, 07 and 15. These are invalid actuals.

---

## 2. Cross-portfolio weaknesses (systemic)

| # | Weakness | Where | Impact |
|---|---|---|---|
| S1 | **SPI masks delay.** Cost-weighted EV is front-loaded, or SPI is measured against a re-baselined or recovery plan. Projects report SPI 1.2 to 1.7 while the forecast is late and float is negative. | 03, 07, 08, 09, 12, 16, 17, 25 | Management sees projects as "green" when they are late. |
| S2 | **Power and SEC interfaces are the dominant critical path.** Items include the SEC agreement, substation location, FAT waiver, MV route clashes, HV/MV cable clashes, and Aramco/Green Riyadh clashes. Several have been open for 6 to 10 months. | 01, 03, 07, 08, 09, 12, 21 | These issues sit with the owner or a third party, and they create EOT exposure for MODON. |
| S3 | **Long-lead electrical and specialist procurement not placed**: MV cable, RMUs, substations, LV panels, poles, air-dome cables/membrane, curtain wall. | 01, 07, 08, 09, 19, 21 | These items drive the negative float. |
| S4 | **Cash flow: invoices sit unapproved or unpaid**: 07 (SAR 24.6M, 0 approved), 21 (SAR 4.9M, 0 approved), 03 (SAR 49.7M, 0 paid), 12 (IPCs 8 to 10), 25 (SAR 3.5M), 17 and 16 (approved but unpaid). | 03, 07, 12, 16, 17, 21, 25 | Contractor liquidity suffers, slowdowns follow, and claim risk grows. |
| S5 | **Stale or copied data.** Manpower, HSE hours, shop-drawing counts and risk logs are identical across weeks; risk logs are byte-identical; narratives are copied word for word. | All with updates | The weekly report cannot be relied on for decisions. |
| S6 | **Template corruption**: `#REF!` and `#DIV/0!` errors, rows pasted from another project, wrong project codes, PMs, regions or dates, and the "21.1M / 20.9M" residue left in invoice logs. | 01, 03, 08, 09, 12, 16, 17, 21, 22 | Weak data governance; reports conflict with each other. |
| S7 | **Risk and issue registers are not managed.** They are empty, all closed, HSE-only, or have broken dashboard counts (for example "246 open, all categories 0"). | All | Risks are only escalated after they become delays. |
| S8 | **Baseline integrity.** Baselines have no float calculated (01, 21) or are captured mid-execution (21 B1 had 1,377 activities complete; 12 and 19 are recovery baselines). Some are absent (15) or unreadable (02, 04). | 01, 02, 04, 12, 15, 19, 21 | Variance against the true contract commitment cannot be measured. |
| S9 | **Scope changes with no CCO or EOT**: revised BOQ –SAR 70.9M (01); added roads and culverts (16); telecom manholes and stormwater redesign (09). | 01, 09, 16 | The contract record diverges from the work actually being done. |
| S10 | **Resources below plan while behind** (01: –60%, 17: –53%, 21: –60%, 03: –22%), or **above plan with low output** (07: 181%, 22/19: 2 to 3×), which points to productivity or loading problems. | 01, 03, 07, 17, 19, 21 | |
| S11 | **Consultant review bottleneck**: MSAs delayed 22 to 144 days, an RFI at 111 days (19), and Code-B drawings never upgraded (09, 01). | 01, 09, 19 | |
| S12 | **Missing uploads**: 12 projects have no usable data, and 15's dashboard is not convertible (.xlsb). | Portfolio | |

---

## 3. Project-by-project analysis

### 01 – Riyadh 4th Industrial City Infrastructure Networks (RHD4-02-002) 🔴

**Contract:** Al-Rawaf / EGIS. SAR 445M. Contract completion 30-May-2028. **Forecast 06-Feb-2029 (+252 d)**. Time elapsed 35%, earned progress 21%.

**Weaknesses**
1. **The SPI recovery comes from re-planning, not from performance.**
   - Planned value fell from SAR 157M to 99M in three weeks, and the weekly planned value went negative (–24.8M).
   - SPI moved from 0.51 to 0.95 as the update switched from Rev.07 to RVSD01_REV01.
   - Earned value rose only about SAR 13M over the same period.
   - The baseline MD (RVSD01_REV01) has **no total float on any of its 8,625 activities**. The baseline was never scheduled, or was exported unscheduled.
   - Baseline approval is still "Under Develop" 11 months after handover.
2. **Earthworks carry the overall SPI** (3.12). Every zone is behind:
   - Z1: 0
   - Z2: 0.17
   - Z7: 0.37
   - Z4: 0.46
   - Procurement physical progress: SPI 0.05
3. **Critical utility clashes have been open 303 days**, each scored 25 (critical):
   - SEC HV on C2
   - SEC MV on C8
   - Green Riyadh vents and cathodic protection
   - Aramco gas on C8 and RD-L10

   All four are owned by the "Contractor", although they are third-party interfaces. Their target dates were missed by about 170 days.
4. **Milestone "Complete MV & Road Works" (30-Sep-2026) is reported on time**, but MV is 0.27% complete, asphalt 8% and kerbs 0%. The MV subcontractor is still "to be selected".
5. **Procurement has barely started.** Of 970 MTS lines, only 8 are delivered. There are no POs for 31 RMUs, 63 LV panels, 13 unit substations or the generators. The delivery tracker in the 15-Oct file is dated 16-Sep.
6. **Manpower is 252 in each of three months** (an obvious copy), against a plan of 635 in September. Saudi staff is 0.
7. **Finance:**
   - The revised BOQ is SAR 374M against a SAR 445M contract, with no CCO.
   - The invoice figures in the presentation (54.98M invoiced, 41.8M paid) conflict with the WPR (71.0M invoiced, 0 paid).
   - The S-curve formula is broken.
8. **Reporting:**
   - There is no 05-Oct report.
   - Every report is named "WPR#15".
   - The schedule updates are only inside ZIP files, with no MD conversion.
   - The HSE inspection is from July (score 55%).
   - The risk log has the wrong project ID.

**Corrective actions**

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Approve one baseline, scheduled with float calculated. Restate PV/EV/SPI against it and publish the reconciliation of Rev.07 to RVSD01. | Contractor planner / EGIS / MODON PMO | 2 weeks |
| 2 | Move the four utility clashes to MODON-owned interface actions. Hold an executive meeting with SEC, Aramco and Green Riyadh, with dated decisions. | MODON PM | 2 weeks |
| 3 | Award the MV subcontract. Issue POs for RMUs, LV panels, substations and generators. Submit a recovery schedule for the missed 30-Sep milestone. | Contractor | 30 days |
| 4 | Formalise the SAR 70.9M BOQ reduction as a CCO. Reconcile invoiced, approved and paid amounts across all files. | EGIS QS / MODON contracts | 2 weeks |
| 5 | Ramp manual labour to plan: 302 in November, with a peak of 1,033 in Mar-27. Report Saudisation. | Contractor | 30 days |
| 6 | Upload the XER updates unzipped. Issue sequentially numbered WPRs. Hold a new HSE inspection. Add an RFI log. | Contractor document control (DC) / EGIS | Next WPR |

---

### 02 – Jeddah 3rd IC Infrastructure ⚫ and 04 – Jeddah 3rd IC Completion ⚫

**Weaknesses**
- The only upload for each project is a baseline in RAR format, which cannot be converted to MD. There are no weekly updates, no BOQ and no drawings, so the projects are uncontrolled from the portfolio's perspective.

**Corrective actions**
- The contractor or consultant should re-upload the baseline as XER/XLSX (not RAR) and start weekly WPR and XER uploads from the next data date.
- The MODON PMO should confirm whether these contracts are active.

---

### 03 – Al-Kharj Industrial City Infrastructure Networks (KHJ1-02-007 / ID 3121) 🔴

**Contract:** Moffreh / EGIS / SAPL. SAR 307.9M including VAT (BOQ SAR 267.7M excluding VAT). Contract completion 02-Dec-2027. Time elapsed 44%.

**Weaknesses**
1. **Two progress measures disagree.**
   - The cost-based SPI is 1.03 ("ahead").
   - The physical SPI is 0.89, with progress 5.5% behind.
   - Procurement SPI is 0.78, and testing and commissioning is 0% against 25% planned.
2. **The schedule is deep in negative float, but the forecast finish shows early.**
   - 701 open activities have negative float, as low as –170 days.
   - These are concentrated in precast curbs, earthworks, bituminous and aggregate base courses, and roads 1 and 24.
   - The float is driven by interim milestones that slipped: Road Works by –36 days and the MV Network by –29 days. Both baselines were 02-Oct-26.
   - The forecast completion date is still shown with 0 days of variance.
   - 4,170 activities have slipped against the baseline, with a median slip of +111 days. The BEI is 0.83.
3. **The update is not progressed properly.**
   - 100 open activities have planned finishes before the data date, unchanged across three weeks.
   - Some actual dates fall after the data date.
   - The baseline file is named "22.Oct.2026" but has a data date of 03-Dec-2025, so it may have been re-saved after approval.
4. **Site and interface blockers:**
   - Obstructions on Local Roads 18, 19 and 20.
   - A diesel tank with no owner.
   - The crusher area has not been handed over.
   - The MV route clashes with water and irrigation lines.
   - The box culvert clashes with existing LV/MV and water lines.
   - MV cable delivery is waiting for SEC to waive the factory acceptance test (FAT).
5. **Procurement:**
   - The interlock sample is not approved and delivery has stopped (3,000 of 129,381 LM).
   - Paving blocks are 0 of 130,000.
   - ICT manholes are 0 of 214.
   - Plantation is 0.
6. **Cash flow:** SAR 49.7M has been invoiced against SAR 108M earned, and **nothing has been approved or paid**.
7. **Manpower** is 529 against a plan of 677 (–22%), and the figure is copied into every week. November requires 841, a 59% ramp-up. Equipment is not reported (`#REF!`).
8. **Quality:** FIR rejections are rising (27 per week), with sewer at 19 of 70 rejected. 179 as-built drawings have not been submitted.
9. **Reporting:**
   - The dashboard has 43 `#REF!` cells.
   - The risk register is stale, with all treatment dates passed and one future "identified" date. It does not include any of the current issues.
   - The quality and HSE numbers are carried forward from the previous week.
   - The project has two IDs.
   - The BOQ check cells show `#REF!`.
   - SAR 68.5M of "close-out" is used to balance the BOQ to the VAT-inclusive value.

**Corrective actions**

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Report a single progress measure, physical, alongside the BEI. Publish real milestone forecasts. Submit a recovery plan for Road Works and the MV Network. | Contractor planner / EGIS | 1 week |
| 2 | Re-progress the XER. Close or re-plan the 100 overdue activities and remove actual dates that fall after the data date. Confirm the approved baseline file and its date. | Contractor planner | Next update |
| 3 | Hold a site-obstacle and utility-clash workshop covering the diesel tank owner, the crusher area, Local Roads 18–20, and the MV and box culvert routing. | MODON PM / EGIS | 2 weeks |
| 4 | Escalate the SEC FAT waiver through MODON. Close the interlock sample approval and firm up the ICT manhole and plantation dates. | MODON PM / Contractor procurement | 10 days |
| 5 | Certify and pay invoices 1–5, and publish a payment-ageing table. | MODON contracts and finance / EGIS QS | 2 weeks |
| 6 | Run a root-cause analysis of the sewer and road FIR rejections. Submit the as-builts. | EGIS QA/QC / Contractor | 2 weeks |
| 7 | Repair the dashboard links. Reissue a live risk register covering the MV clash, the FAT waiver, interlock, cash flow and the manpower ramp-up. | Contractor document controller | Next WPR |

---

### 07 – Sudair IC Infrastructure Ph.2 Part 2 (SUD1-02-011) 🟠

**Contract:** TDC / EGIS. SAR 193.9M including VAT. Contract completion 05-Jul-2027. Time elapsed 52%.

**Weaknesses**
1. **The forecast finish is pinned to the contract date.**
   - The forecast is exactly 05-Jul-2027 in every update, with a minimum total float of exactly 0.
   - 628 activities have slipped against the baseline, by up to 249 days.
   - 74 to 108 open activities are past their planned finish.
   - The BEI is **0.75**, the worst in the portfolio.

   This pattern means a must-finish constraint is hiding the real delay. The reported SPI of 1.23 is not believable next to a BEI of 0.75.
2. **The lead is eroding.** Weekly earned value was below plan in 3 of 4 weeks. In week W4, physical man-hours earned were only 41% of plan.
   - Electrical SPI is about 0.68, with zero earned this week.
   - CCTV SPI is about 0.64.
   - Procurement physical progress is 60% against 99% planned.
3. **The MV power package has stalled.**
   - The substation location is unconfirmed by SEC/MODON (risk H16).
   - Material submittals for 51.5 km of MV cable and 5 unit substations have not been submitted; the cable was required on site by 31-May.
   - Street-light poles are at 1 of 592 and lighting panels at 0 of 52.
   - Testing and commissioning for TSE already has zero float.
4. **Milestones:** technical submittals are 164 days late and the engineering phase 207 days late. Both dates have passed but are still marked "UP".
5. **Cash flow:** four interim payment certificates totalling SAR 24.6M have none approved and none paid. Billing lags earned value by about SAR 57M.
6. **Productivity:** manpower is 607 against 335 planned (181%) and equipment is 220 against 104, yet weekly output is below plan.
7. **NCRs are rising,** from 1 to 5 open.
8. **Reporting:**
   - The W2 header is dated 28-Sep.
   - Dashboard schedule statistics are frozen at 711 completed while the XER shows 787.
   - Three different progress figures are reported (48.3%, 32.3% and 0.03%).
   - MV cable status flips between delivered and not submitted.
   - Risk log actions are offset by one row.
   - The baseline appears only inside W4 and was never uploaded to 3-Baseline.

**Corrective actions**

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Remove or relax the finish constraint and reschedule so float shows the true position. Report the BEI and the critical-path SPI. | Contractor planner / EGIS | Next update |
| 2 | Get SEC/MODON to confirm the substation location. The contractor submits the MV cable and unit substation submittals within 7 days of that confirmation. Agree a 4-week electrical recovery plan. | MODON PM / Contractor | 2 weeks |
| 3 | Certify IPCs 1–4 and record approval and payment dates. | EGIS / MODON finance | 2 weeks |
| 4 | Review productivity: earned man-hours against headcount, and the 150 idle equipment units. Re-load the resource plan. | EGIS | 2 weeks |
| 5 | Link the dashboard to the XER, fix the `#REF!` errors, and retire the stale Conclusion sheet. Upload the approved baseline to 3-Baseline. | Contractor document control | Next WPR |

---

### 08 – Jeddah 1st Industrial City Infrastructure 1 km² (JDH1-02-003) 🔴

**Contract:** Al Enjaz / EGIS. SAR 86.8M. Contract completion 18-Nov-2027. **Forecast 20-May-2028 (+184 d), slipping exactly 7 days every week.**

**Weaknesses**
1. **The SPI of 1.48 hides a 184-day delay.**
   - Roads & MV earned value has been frozen at 73.25% for three weeks.
   - Non-critical networks are far ahead of plan: shallow networks are at 83% against 24% planned.
   - 457 activities (24% of the schedule) have negative float of –157 days.
2. **Root cause: the MODON–SEC agreement for the MV network has been open about 310 days.** Its target date was 30-Dec-25.
   - The driving path is "Material fabrication for MV cable", which has not started.
   - POs for the MV cable, street-lighting substations and RMUs have not been submitted.
   - The MV shop drawing is 0% physically complete.
3. **No EOT notice or time-impact analysis** has been submitted, although the delay is owner-caused.
4. **Weekly physical progress collapsed in W3** to 0.27% against 0.78% planned. Manual labour fell from 220 to 130.
5. **HSE is declining.** The safety score fell from 0.86 to 0.77, there were 0 toolbox talks, and the "leadership tours" item failed.
6. **Contradictions across files:**
   - Summary sheets show a finish of 30-Nov-2026 and a different project code.
   - The Material Monitoring file shows MV material as 100% delivered, while the procurement log says the PO was never submitted.
   - SAR 5.43M of earned value is booked to Testing & Commissioning, which is "Not Started" in P6.
   - The procurement log contains a pasted row from another project.
   - There is no risk register.

**Corrective actions**

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Escalate the SEC MV agreement to executive level with a decision date. Allow procurement of the MV cable and RMUs in parallel, at risk, if the agreement is only a formality. | MODON PM / Executive | 2 weeks |
| 2 | The contractor submits an EOT notice and time-impact analysis. MODON assesses its exposure. | Contractor / EGIS contracts | 30 days |
| 3 | Re-sequence the road and MV work so road works not dependent on MV can proceed. Report the critical-path SPI. | Contractor planner | Next update |
| 4 | Reconcile Material Monitoring against the Procurement Log, and Testing earned value against P6. Correct the summary sheets. | EGIS | 1 week |
| 5 | Restart toolbox talks and leadership tours, and restore manual labour. | Contractor HSE / Contractor PM | Immediate |
| 6 | Create a risk register and fix the `#REF!` errors and the foreign row. | Contractor document control | 2 weeks |

---

### 09 – Tabuk Additional Networks Completion (TAB1-02-003 / -01-009) 🟠

**Contract:** ASAS / EGIS. SAR 140.5M. Contract completion 03-Sep-2027. **Forecast 07-Oct-2027 (+34 d, worsening each week).** Time elapsed 56%.

**Weaknesses**
1. **The re-baseline hides the original slip.**
   - The reported SPI of 1.27 is measured against "Revised Schedule Rev 02", which has a data date of 03-Jun-2026 and was approved on an unknown date.
   - Against the original plan (64.8–66.9% planned), the SPI is about 0.72.
   - Zone 1 is +237 days late against the original plan, and preliminary submittals +346 days.
2. **Velocity is too low.** Average progress is about 0.5% per week, but the remaining work needs about 1.14% per week to finish on time.
3. **Earned value is not validated.** Reported EV is 48%, against 38.4% inspected (FIR) and 32.9% invoiced, which suggests EV is overstated by about SAR 13M.
4. **Critical issues are not being closed.**
   - The MV connection to the substation has been open since June, with the same "response tomorrow" status every week.
   - 277 shop drawings are stuck at Code B.
   - The Shinko fence is blocking electrical works.
   - 220 activities carry negative float (–29 d), driven by electrical, CCTV and telecom trenching.
5. **Procurement:** there is no PO for telecom material (required by 03-Jun) or for pole foundations. Poles are needed on site by 29-Oct, and delivery has not started.
6. **Finance:**
   - Advance-payment recovery is 0 after 13–14 IPCs, against an advance of SAR 14.05M.
   - Scope changes (telecom manholes, stormwater redesign) have no CCO.
   - IPC payment cycles run 53–92 days.
7. **Reporting:**
   - The project has three different project IDs.
   - Manpower and equipment show three different values.
   - The risk dashboard formulas are broken ("236 open").
   - Risk target dates roll forward every week.
   - Residue from another template remains ("Ready Built Factories XYZ", 21.1M).

**Corrective actions**

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Report SPI against both the original and revised baselines. Document Rev 02 approval, including any EOT basis. | EGIS / MODON PMO | 2 weeks |
| 2 | Submit a recovery plan targeting at least 1.1% per week, focused on Zone 3, MV cable and roads. | Contractor | 2 weeks |
| 3 | Escalate the MV substation connection and the Shinko fence to the utility and plot owner. Set a 30-day deadline to upgrade all Code-B drawings to Code A. | MODON PM / EGIS | 1 week |
| 4 | Reconcile EV with FIR. Apply advance-payment recovery. Register CCOs for the scope changes. | EGIS QS | Next IPC |
| 5 | Issue POs for telecom material and pole foundations. | Contractor procurement | 1 week |
| 6 | Use one project ID and one manpower source, fix the live risk formulas, and stop rolling target dates forward. | Contractor document control | Before W4 |

---

### 12 – Jeddah Oasis Land Development (JHD4-02-007) 🟡

**Contract:** Al Enjaz / EGIS. SAR 57.3M. Contract completion 23-May-2027. The schedule forecast is 14-Jan-2027, which is early against the contract, **but about 57 days late against MODON's crashed target of 23-Nov-2026**.

**Weaknesses**
1. **The project is not tracked against the target that matters.** The WPR reports "124 days early" against the contract. It does not report progress against the 23-Nov-26 crash target.
   - Two milestones have failed: plot earthworks (–70 to –177 d depending on the file) and road works (–23 d).
   - Forecasts for road works and MV completion are dated 13-Oct, which is in the past, and are not actualised.
2. **The schedule has no critical path.** The minimum float is +102 days because float is measured to the contract date, not to the crash target.
3. **Earned value exceeds BOQ value.** Roads show 110% earned and electrical 110%; the sewage lift station shows an SPI of 250. The recovery baseline cut planned value from 74% to 61%, which inflates SPI.
4. **Slowing:** weekly physical progress was 0.36% against 1.35% planned.
5. **Cash flow:** IPC 8 has waited about 51 days and IPCs 9–10 are awaiting PM approval. IPC 7 was approved but is unpaid.
6. **The risk and issue logs are 100% "Closed"**, including the SEC MV approval, which is still "to be finalized".
7. **Reporting:**
   - Three different completion dates appear.
   - The PM name differs between files.
   - Resources are identical for three weeks.
   - The failed-start sheet 2 dates from March.
   - The look-ahead planned value is 0.
   - FIR dates include the year 2062.

**Corrective actions**

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Add the 23-Nov-26 target as a constraint in the schedule and WPR. Submit a recovery plan for plot earthworks and road works. | Contractor planner / EGIS | 1 week |
| 2 | Cap earned value at BOQ value per WBS, and reconcile it with FIR and IPC figures. | EGIS cost control | Before next IPC |
| 3 | Approve IPCs 8–10 and pay IPC 7. | MODON PM / Finance | 2 weeks |
| 4 | Reopen live risks: SEC energisation, lift-station T&C, and handover. | Contractor / EGIS | Next WPR |
| 5 | Unify contract data and names, and refresh resources from daily reports. | Contractor document control | Next WPR |

---

### 15 – Hail Ready Factories Package 3, 20 factories (HAL1-05-009) 🟠

**Contract:** P6 budget SAR 44.6M. Baseline 04-Dec-25 to 03-Dec-26. Forecast 02-Nov-26. Time elapsed 88%, earned value 98%.

**Weaknesses**
1. **No baseline is uploaded, and the weekly dashboard (.xlsb) has no MD conversion.** Cost, HSE, quality, resources, submittals and risks therefore cannot be verified.
2. **The forecast is not credible.**
   - 126 open activities and close-out are due within about 14 days.
   - Durations were compressed to hold the date: close-out from 30 to 13 days, roads from 69 to 60.
   - The "Engineering & Materials" milestone (about 193 days late) and the civil completion milestone (about 97 days late) are re-forecast to the data date every week.
3. **Logic errors.**
   - T&C completion (21-Oct) comes before construction completion (31-Oct).
   - The XER project ID is HAL1-05-10 and its start date is 2023.
   - 23 open activities are past their planned finish.
   - Some actual dates are after the data date.
4. **Finishing works are lagging** at about 0.5 SPI: specialties, metal works, fences and gates, roads (72%), and geotextile (the start date moves every week). Earned value of 98% looks front-loaded.

**Corrective actions**

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Upload the approved baseline. Issue the dashboard as .xlsx or PDF. | Contractor document control | 1 week |
| 2 | Fix the project ID, start date and T&C logic. Actualise or re-plan the stuck milestones. Issue a day-by-day close-out plan for the 20 factories. | Contractor planner / Consultant | Next update |
| 3 | Run a readiness and punch walk per block. Assign dedicated crews to roads, fences, metal works and specialties. | Consultant / Contractor | 2 weeks |
| 4 | Add contract identity, EOT, invoice and HSE summaries to the WPR. | MODON PM | Next WPR |

---

### 16 – Makkah 2nd IC Networks Completion (MKH2-02-003) 🟡

**Contract:** Al Enjaz / EGIS. SAR 52.0M. Contract completion 14-Aug-2027. **Forecast 30-Aug-2027 (+16 d). The delay has improved from +43 d.** Time elapsed 45%.

**Weaknesses**
1. **Earned value is front-loaded.** SPI is 1.39 while total float is negative.
   - Open drain channel SPI is about 4.0 and electrical about 5.4.
   - The box culvert is shown 100% complete although its slabs are still being poured.
   - Wearing course is 0.7% complete and sits on the critical path, together with the Ring Road connection and the Ramp-2 electrical works.
2. **The 27-day recovery in 2 weeks is unexplained.** The EV forecast curve is artificial: about SAR 0.28M per month until February, then a jump. Monthly EV fell from 3.97M (September) to 1.71M (October).
3. **Unregistered scope additions:** Collector 9, Road 52, Al Gloud Road and culverts 3–4. None has a CCO or EOT, and the issue log is empty.
4. **Contract dates conflict.** File 16 shows 24-Nov-25 to 23-May-26, the WPR shows 2026–2027, and the baseline approval is dated before award. Hijri dates are invalid.
5. **Manual labour is falling** (121 → 105) while the plan ramps up to 161. No PO has been placed for pavement markings.
6. **The risk log (file 17) is byte-identical for three weeks.** The culvert 4 risk is "Open" in one file and "Closed" in another.

**Corrective actions**

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Audit the P6 earning rules for channels, electrical and the culvert. Restate EV on a quantity basis. | EGIS planner | 2 weeks |
| 2 | Submit a recovery plan for wearing course, Ring Road connection and Ramp-2 electrical, with a manpower ramp-up to plan. | Contractor | 2 weeks |
| 3 | Issue CCOs and an EOT assessment for the added scope. | EGIS QS / MODON contracts | 30 days |
| 4 | Create a single contract-data master and correct files 15 and 16. | MODON PM | 30 days |
| 5 | Keep the risk and issue logs live and issue the pavement-marking PO. | Contractor | From W4 |

---

### 17 – Makkah 2nd IC Akishiya Roads (MKH2-02-004) 🔴

**Contract:** Al Enjaz / EGIS. SAR 38.0M including VAT. Contract completion 24-Aug-2027. **Forecast 14-Oct-2027 (+51 d), worsening by 4–7 days per week.** Time elapsed 28%.

**Weaknesses**
1. **SPI is 1.74, but the forecast slips every week.** 44% of the network (168 activities) is critical at –43 d, and the BEI is 0.81. The planned-value basis is inconsistent with the EV chart, so the SPI is unreliable.
2. **The delay has no explanation.** The "Delay reasons", "Challenges" and Top-5 Issues fields are all blank, and the issue log is empty.
3. **Resources are short:** labour is 68 against 145 planned (–53%) and equipment 62 against 80. The dashboard shows the opposite picture.
4. **Procurement:** aggregate base, bituminous base, kerbs, interlock and markings are 0% delivered, with need dates from November to January.
5. **Backlog is growing:** failed starts rose from 24 to 29 and pending FIRs from 8 to 29.
6. **Copied project data:**
   - Milestones, procurement IDs and risk rows come from MKH2-02-003.
   - The XER project ID is "MKH2-02-14".
   - Contract value appears as both 21.1M and 33.0M.
   - Baseline approval is dated before award.
   - The risk file is byte-identical across weeks.
7. **Cash:** IPC-3 (SAR 3.99M) is approved but unpaid, and no IPC has been raised after 27-Sep.

**Corrective actions**

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Submit a delay analysis for the 51 days, and a recovery schedule with labour raised to 145. | Contractor planner / PM | 1 week |
| 2 | Expedite POs for aggregate base, asphalt, kerbs and interlock ahead of the November–December need dates. | Contractor procurement | Weekly |
| 3 | Remove MKH2-02-003 content. Use one source for contract value, invoices and resources. Fix `#REF!` errors. | EGIS / Contractor document control | Next WPR |
| 4 | Fill the issue and risk logs with owners, dates and ageing. | Contractor / EGIS | 2 weeks |
| 5 | Pay IPC-3. The contractor submits IPC-4. | MODON finance / Contractor | 1 week |
| 6 | Close the 29 pending FIRs. | EGIS QA/QC | 2 weeks |

---

### 18 – Sudair SAR Passenger Station (SUD1-05-018) ⚫

**Weaknesses**
- The only upload is a baseline: 855 activities, data date 07-Apr-2026, finish 06-Aug-2027. No weekly reports or schedule updates have been submitted in **six months**, so progress, cost and risk are unknown.

**Corrective actions**
- The MODON PM should obtain the latest schedule update and WPR within one week, then enforce weekly uploads.
- The planner should check the baseline for logic quality. It has 195 critical activities and 23 activities longer than 44 days.

---

### 19 – Stadiums / Playgrounds Initiative – Central (Qassim, Hail, Tabuk) (MLTX-02-003) 🔴

**Contract:** ADV (Advanced Construction) / Egis. SAR 35.7M. Recovery baseline finish 16-Dec-2026. **Forecast 07–10 Feb-2027 (+53 to 56 d, slipping about 7 days per week).** Time elapsed about 80%.

**Weaknesses**
1. **The project is behind on a recovery baseline that was already reset.** Earned is 69% against 80% planned (SPI 0.85–0.86), and the gap is widening.
   - Tabuk drives the finish (–47 d).
   - **The Air Dome has stalled:** Qassim is at 35% and Tabuk at 29%, against plans above 60%. Earned value did not move between W1 and W2. Tabuk Air Dome mechanical and electrical work is at 0% against 84% planned.
2. **No activity was completed between W1 and W2** (1,591 completed in both). Failed starts rose from 69 to 77, and 108 open activities are past their planned finish.
3. **Consultant review bottleneck:**
   - Only 1 of 13 material source approvals is approved; 9 have been delayed with Egis for 22–144 days.
   - RFI-0021 (Tabuk utility connections) has been open 111 days.
   - Septic tank drawings have been in review for 110 days.
4. **Long-lead items:**
   - Air Dome supply has a 150-day lead time and is still "under review".
   - Panels, lighting and fire alarm have a 120-day lead time and are still "under process".
   - The curtain wall is a failed start at two sites.
5. **Resources are 2–3 times the plan, yet output is behind.** This points to a productivity or planning problem.
6. **Reporting:**
   - Until W3 there was no standard WPR, so no cost, HSE, risk or resource data was available.
   - **The W3 report is misfiled under project 22 (Eastern).**
   - Only IPC-01 (SAR 2.3M, 6.5%) has been invoiced against 69% earned, and its payment data is contradictory.
   - 10 NCRs and 170 FIRs are open.
   - Contract codes are mixed (02-003 and 05-047).

**Corrective actions**

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Clear the 9 overdue material source approvals and RFI-0021. Set a 14-day review SLA and report review ageing weekly. | Egis / MODON PM | 5 working days |
| 2 | Submit a resourced Air Dome recovery plan (cable, membrane, HVAC, electrical) with confirmed supplier dates. Place the remaining POs for long-lead electrical items. | Contractor | 1 week |
| 3 | Submit a delay and EOT analysis against the original contract dates, and explain why no activities were completed in the week. | Contractor planner | Next update |
| 4 | Move the W3 report from folder 22 to 19/W3, and standardise on the full WPR workbook. | PMO / document control | Now |
| 5 | Encourage monthly IPCs and reconcile the IPC-01 payment and advance-payment figures. | Egis QS | 2 weeks |
| 6 | Close the open NCRs and the FIR backlog. | Contractor QA/QC | 2 weeks |

---

### 21 – Stadiums / Playgrounds Initiative – Western (Asir, Jazan, Jeddah) (MLTX-02-004) 🔴

**Contract:** Profast / EGIS. SAR 34.0M. Contract completion 25-Jan-2027. **Forecast 09-May-2027 (+104 d, slipping 5–7 days per week).** Time elapsed 68%.

**Weaknesses**
1. **The Air Dome is the driving path.**
   - Material approvals for the PVC membrane, steel tension cables, emergency doors and lock doors are "Not Started". They are re-dated to the data date every week, carrying –85 d float.
   - Long-lead air-dome items are at 0% delivery against 100% planned.
   - Supplier dates run from November to 25-Dec.
2. **Jazan is far behind** with an SPI of 0.68. The Jazan works milestone is at –110 d, the toilet building at –148 d and the playground at –150 d.
3. **Manual labour is 70 against 175 planned (–60%).**
4. **MV cables lie across the excavation route** (Jazan). The issue is owner-owned and missed its 17-Oct target.
5. **Cash flow:** five invoices totalling SAR 4.94M have none approved and none paid. The quarter target was SAR 15.5M; SAR 5.7M was achieved.
6. **The baseline is not valid as a baseline.** "B1" has a data date of 04-Jul-2026 with 1,377 activities already complete, and **no total float was calculated**.
7. **Reporting:**
   - The weekly total of earned value is double-counted.
   - File 16 carries another project's sector, PM, contractor and dates, and its narrative is the same in every week.
   - The milestone baseline for T&C is wrong (29-Apr-26).
   - The procurement log and manpower figures are stale.
   - The risk management plan, submitted in April, is still not approved.
   - The W1 schedule update is missing.

**Corrective actions**

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Close the air-dome material approvals this week. Obtain written delivery commitments from Global Sport Gate. Expedite fabrication. | Contractor / EGIS | 1 week |
| 2 | Raise manual labour to at least 150, with priority on Jazan. Submit a recovery schedule. | Contractor | 2 weeks |
| 3 | Hold a utility-authority meeting on the Jazan MV cables and set a dated closure. | MODON PM | 1 week |
| 4 | Certify the 5 pending invoices. | EGIS | 2 weeks |
| 5 | Re-issue a properly scheduled baseline (with float) or document the B1 approval. Fix the WPR Total formula, the milestone baselines and the file 16 header. Approve the risk management plan. | EGIS planning / document control | Before W4 |

---

### 22 – Stadiums Initiative – Eastern ⚫ (misfiled data)

**Weaknesses**
- The only file in this folder (WPR, 18-Oct) is **project 19's W3 report**. It has the same code (MLTX-02-003), the same name (Qassim/Hail/Tabuk) and is labelled "Central".
- No genuine Eastern Region data exists.

**Corrective actions**
- The PMO should move the file to `19-…/W3` immediately.
- The MODON PM should provide the Eastern contract code, baseline and weekly reports.

---

### 25 – Najran Craftsmen Initiative (NJR1-05-005 / NJR1-01-007) 🟡

**Contract:** Labenat Al Bena / EGIS. SAR 11.0M including VAT. Contract completion 02-Jan-2027. The committed early finish of 15-Oct-2026 **was missed**. Earned is 98.5% against a crash-plan target of 100%.

**Weaknesses**
1. **The forecast completion of 15-Oct is in the past and has not been updated.** T&C is still planned for 09–19 Dec, after the claimed completion. The long-lead milestone shows an actual date in the future (27-Oct).
2. **No schedule update has been uploaded.** Only the baseline exists, so the close-out cannot be checked against the schedule.
3. **Cash:** IPC-05 and IPC-06, worth SAR 3.48M, are unpaid. IPC-05 is about 50 days old, and nothing has been paid in 3 weeks.
4. **Identity:** the project uses two codes (NJR1-05-005 and NJR1-01-007) and two PM names.
5. **The risk and issue logs are empty** despite the handover risk. The Issues sheet contains only Excel serial numbers.
6. **Copied data:** manpower (35 against 132), HSE and quality figures are identical across all three weeks.

**Corrective actions**

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Issue a revised completion date with a close-out, T&C and snag plan. Upload the XER update. | Contractor / EGIS | 1 week |
| 2 | Release IPC-05 and IPC-06. | MODON PM / Finance | 2 weeks |
| 3 | Confirm the official project code and PM, and re-label the baseline. | PMO | Now |
| 4 | Populate the handover risks. Refresh manpower and HSE figures weekly. | EGIS | 1 week |

---

### 05, 06, 10, 11, 13, 14, 20, 23, 24 – No uploads ⚫

These projects are:
- 05 Dammam 3rd Ph2 Pt2 Zone J
- 06 Dammam 2nd Logistics 1 km²
- 10 Dammam 3rd Ph1 Pt2
- 11 Dammam 3rd 44 ready-built factories
- 13 Dhahran Tech Zones
- 14 Dammam Tech Zones
- 20 Dammam 3rd IC fence
- 23 Waad Al-Shamal fencing
- 24 Jeddah 3rd Logistics Ph1

**Weakness**
- Nothing has been uploaded for any of them: no BOQ, drawings, baseline or reports. The Eastern-sector projects (mostly Dammam) have no visibility at all.

**Corrective action**
- The MODON PMO should issue a data call to each PM within 1 week. The minimum package is the approved baseline (XER), the latest XER update, and the WPR (.xlsx).
- Where a project has not started (pre-award or design), record its status in the tracker so the gap is explained.

---

## 4. Portfolio-level corrective action plan (PMO)

| Priority | Action | Owner | Due |
|---|---|---|---|
| 1 | **Power and utility interface task force** (SEC, Aramco, Green Riyadh) covering projects 01, 03, 07, 08, 09, 12 and 21. Run one escalation register with an executive sponsor and dated decisions, reviewed every two weeks. | MODON Executive / PMO | 2 weeks |
| 2 | **SPI governance.** Every WPR reports, side by side: physical progress, cost EV, BEI, and critical-path float/forecast. Earned value is capped at BOQ value and reconciled with FIR. When the plan is re-baselined, SPI is also shown against the original baseline. | PMO / EGIS | Next reporting cycle |
| 3 | **Payment clearance drive.** Clear all pending IPCs across 03, 07, 12, 16, 17, 21 and 25, set an approval SLA (for example 14 days), and add a payment-ageing KPI to the dashboard. | MODON Finance / PM | 30 days |
| 4 | **Long-lead procurement watchlist.** Cover MV cable, RMUs, substations, panels, poles, Air Dome and curtain wall, with weekly PO and delivery tracking against need-by dates. | PMO / Contractors | Weekly |
| 5 | **Baseline validation checklist.** Float is calculated; no constraints hide delay (07); the baseline is captured before execution; the approval reference is recorded; the baseline is uploaded to 3-Baseline in XER (not RAR or ZIP). | PMO planning | 1 month |
| 6 | **WPR quality gate** before submission: no `#REF!` or `#DIV/0!`; the data date matches across all files; manpower, HSE and risk figures differ from last week or are justified; correct project code, PM and region; sequential report number. | EGIS document control | Immediate |
| 7 | **Live risk and issue management.** Each register has an owner, target date, ageing and score. Owner-caused issues are assigned to MODON, not the contractor. A Top-5 is reviewed in the weekly meeting. | All PMs | 2 weeks |
| 8 | **Consultant review SLA.** Submittals and MSAs reviewed within 14 days and RFIs within 7 days, with ageing reported weekly. Projects 19, 09 and 01 come first. | EGIS / MODON | Immediate |
| 9 | **Change control.** Register CCOs and EOT assessments for scope already being executed: 01 (BOQ –SAR 70.9M), 09, 16. | MODON contracts | 30 days |
| 10 | **Data completeness.** Upload data for the 12 projects that have none, convert the RAR/XLSB/ZIP files, and correct the 22→19 misfiling. | PMO / document control | 1 week |

---

### Appendix – How the schedule metrics were derived

- **Source.** Every `MD Files/*.md` that contains an "Activity status" table: 44 schedule conversions in total.
- **Activities past planned finish.** Activities not marked Completed whose planned finish date is earlier than the data date.
- **BEI.** Among activities whose baseline finish is on or before the update's data date, the share that are Completed in the update.
- **Activity slip.** The update finish date minus the baseline finish date, for activities whose IDs match between the two.
- **Limits.** Relationship (logic) data is not included in the MD conversions. That means checks for missing logic, leads/lags and relationship types could not be run; they need the native XER.
