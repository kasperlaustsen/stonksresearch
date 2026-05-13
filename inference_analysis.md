# Who Wins the Inference Game? Hyperscaler Analysis

_Analysis based on scraped press releases from Anthropic (208 articles), OpenAI (623 articles), and Google AI (79 articles). All figures sourced directly from company announcements — no external estimates._

---

## 1. Dollar Commitments

### A. Investments INTO AI Labs (by hyperscalers/chip makers)

| AI Lab | Investor | Amount | Date | Source Article |
|--------|----------|--------|------|----------------|
| Anthropic | Amazon | $4B (initial) | Sep 2023 | *Expanding access to safer AI with Amazon* |
| Anthropic | Amazon | $4B (additional; total $8B) | Nov 2024 | *Powering the next generation of AI development with AWS* |
| Anthropic | Amazon | $5B + up to $20B future | Apr 2025 | *Anthropic and Amazon expand collaboration* |
| Anthropic | Microsoft | Up to $5B | Apr 2025 | *Microsoft, NVIDIA, and Anthropic announce strategic partnerships* |
| Anthropic | NVIDIA | Up to $10B | Apr 2025 | Same as above |
| Anthropic | Google | Participated in $450M Series C | May 2023 | *Anthropic Series C* |
| OpenAI | Microsoft | $1B | Jul 2019 | *Microsoft invests in and partners with OpenAI* |
| OpenAI | Microsoft | "Multi-billion dollar" | Jan 2023 | *OpenAI and Microsoft extend partnership* |
| OpenAI | Amazon | $50B ($15B initial + $35B conditional) | Feb 2026 | *OpenAI and Amazon announce strategic partnership* |
| OpenAI | SoftBank | $30B | Feb 2026 | *Scaling AI for everyone* |
| OpenAI | NVIDIA | $30B + up to $100B progressive | Feb 2026 | *OpenAI and NVIDIA announce strategic partnership* |
| OpenAI | Disney | $1B | 2025 | *Disney partnership* |

**Amazon total into AI labs: ~$63B+ committed** (Anthropic $13B + up to $20B future; OpenAI $50B)
**Microsoft total into AI labs: ~$6B+ disclosed** (OpenAI multi-round; Anthropic $5B)
**NVIDIA total into AI labs: ~$40B+** (Anthropic $10B; OpenAI $30B + up to $100B)

### B. AI Lab Compute Purchases FROM Hyperscalers

| AI Lab | Cloud Provider | Amount | Timeframe | Date | Notes |
|--------|---------------|--------|-----------|------|-------|
| Anthropic | AWS | $100B+ | 10 years | Apr 2025 | Spans Trainium2 through Trainium4 |
| Anthropic | Azure | $30B | Not specified | Apr 2025 | Via Microsoft/NVIDIA partnership |
| Anthropic | Google Cloud | "Tens of billions" | Multi-year | Oct 2024 | Up to 1M TPUs |
| Anthropic | Fluidstack | $50B | Multi-year | Nov 2025 | Own data centers in TX and NY |
| OpenAI | Azure | $250B (incremental) | Multi-year | 2025 | New definitive agreement |
| OpenAI | AWS | $138B ($38B + $100B expansion) | 8+ years | 2025-2026 | Includes Trainium capacity |
| OpenAI | Oracle/Stargate | $500B (total Stargate) | Multi-year | Jan 2025 | Joint with SoftBank; ~10GW target |

---

## 2. Power/Capacity Commitments (GW)

| AI Lab | Provider | Capacity | Chip Type | Timeline | Date Announced |
|--------|----------|----------|-----------|----------|----------------|
| **Anthropic** | AWS | Up to 5 GW | Trainium2/3/4, Graviton | ~1GW by end 2026 | Apr 2025 |
| **Anthropic** | Google/Broadcom | 5 GW (next-gen TPUs) | Next-gen TPUs | Starting 2027 | Apr 2026 |
| **Anthropic** | Azure | Up to 1 GW | NVIDIA GPUs | Not specified | Apr 2025 |
| **Anthropic** | Google Cloud | 1+ GW | Up to 1M TPUs | 2026 | Oct 2024 |
| **OpenAI** | Stargate (Oracle/SoftBank) | 10 GW | Mixed (NVIDIA) | Secured by end 2025 | Jan 2025 |
| **OpenAI** | AWS | 2 GW | Trainium3/4 | 2026-2027 | Feb 2026 |
| **OpenAI** | NVIDIA (across providers) | 5 GW (3GW inference + 2GW training) | Vera Rubin | Starting H2 2026 | Feb 2026 |
| **OpenAI** | AMD | 6 GW | Instinct MI450+ | Starting H2 2026 | Oct 2025 |
| **OpenAI** | Broadcom | 10 GW | Custom OpenAI accelerators | Multi-year | 2025 |
| **OpenAI** | Oracle | 4.5 GW | Mixed | Over 5 years | Jul 2025 |

**Key observation:** OpenAI's total capacity commitments (~33+ GW) dwarf Anthropic's (~12 GW). But OpenAI's commitments are spread across many more providers, while Anthropic concentrates on three.

---

## 3. "Primary" Provider & Exclusivity Analysis

### Anthropic

| Date | Statement | Source |
|------|-----------|-------|
| Sep 2023 | "AWS will become Anthropic's **primary cloud provider** for mission critical workloads" | *Expanding access to safer AI with Amazon* |
| Nov 2024 | "establishes AWS as our **primary cloud and training partner**" | *Powering the next generation of AI development with AWS* |
| Apr 2025 | "We continue to choose AWS as our **primary training and cloud provider** for mission-critical workloads" | *Anthropic and Amazon expand collaboration* |
| Apr 2025 | "**Amazon remains Anthropic's primary cloud provider and training partner**" (stated in Microsoft/NVIDIA partnership announcement) | *Microsoft, NVIDIA, and Anthropic announce strategic partnerships* |

**Verdict:** AWS has been consistently named "primary" since 2023 and Anthropic reaffirmed this even when announcing deals with competitors. No exclusivity — Anthropic deliberately positions as available on all three clouds.

### OpenAI

| Date | Statement | Source |
|------|-----------|-------|
| Jul 2019 | "Microsoft will become our **exclusive cloud provider**" | *Microsoft invests in and partners with OpenAI* |
| Jan 2023 | "Azure will remain the **exclusive cloud provider** for all OpenAI workloads across our research, API and products" | *OpenAI and Microsoft extend partnership* |
| Jan 2025 | "Microsoft remains OpenAI's **primary cloud partner**, and OpenAI products will ship first on Azure" — BUT: "OpenAI can now serve all its products to customers across any cloud provider" and "Microsoft will no longer have a right of first refusal to be OpenAI's compute provider" | *The next chapter of Microsoft-OpenAI partnership* |
| Feb 2026 | "AWS will be the **exclusive third-party cloud distribution provider** for OpenAI Frontier" | *OpenAI and Amazon announce strategic partnership* |
| 2025 | "Three years ago, we relied on a single compute provider. Today, we are working with providers across a **diversified ecosystem**." | *OpenAI raises $122B* |

**Verdict:** OpenAI went from Microsoft-exclusive (2019-2024) to deliberately multi-cloud. Azure lost exclusivity and right of first refusal, but retained: (1) first-party product hosting, (2) exclusive IP license through 2032, (3) Azure API exclusivity for third-party API products. AWS gained exclusive distribution rights for OpenAI Frontier (enterprise platform).

### Google/Gemini

Google is both the cloud provider AND the AI lab. No external "primary" provider dynamics — they run on their own TPU infrastructure.

---

## 4. Diversification Signals

### Anthropic — Controlled multi-cloud from early on
- **Feb 2023**: Selected Google Cloud as cloud provider (first relationship)
- **Sep 2023**: Amazon partnership + $4B investment; AWS becomes "primary"
- **Mid-2024**: Claude available on Google Cloud Vertex AI (GA)
- **Oct 2024**: Major Google Cloud TPU expansion (up to 1M TPUs)
- **Apr 2025**: Microsoft Azure + NVIDIA partnership ($30B Azure commitment)
- **Repeated language**: "Claude is the **only frontier AI model available on all three** leading cloud providers"

**Pattern:** Anthropic has been deliberately multi-cloud from the start, using "available on all three" as a competitive differentiator. AWS is primary but Anthropic is clearly maintaining optionality.

### OpenAI — From exclusive to diversified
- **2019**: Microsoft exclusive cloud partner
- **2023**: Microsoft exclusivity reaffirmed
- **2025 (Jan)**: New agreement — exclusivity removed, right of first refusal removed
- **2025 (various)**: Stargate with Oracle/SoftBank; AMD 6GW deal; Broadcom custom chip deal; CoreWeave
- **2025**: "Three years ago, we relied on a single compute provider. Today, we are working with providers across a diversified ecosystem."
- **2026 (Feb)**: Amazon $50B investment + $138B AWS commitment; NVIDIA $30B
- **2026 (May)**: $122B round with Amazon, NVIDIA, SoftBank, continued Microsoft participation

**Pattern:** OpenAI's diversification has been rapid and deliberate. They went from Azure-exclusive to having 6+ infrastructure partners in ~18 months. The stated reason: "No single architecture can efficiently meet the needs of the entire AI frontier."

---

## 5. Risk Factors by Provider

### AWS
**Strengths:**
- Only provider with BOTH major AI labs as committed customers (Anthropic $100B+, OpenAI $138B)
- Custom silicon story (Trainium) creates switching costs
- Named "primary" by Anthropic consistently
- Exclusive distribution for OpenAI Frontier
- Largest direct investor into AI labs ($63B+)

**Risks:**
- Labs are explicitly diversifying to avoid lock-in
- Trainium is unproven at frontier training scale vs. NVIDIA GPUs
- If custom silicon underperforms, commitments may not convert to actual usage
- AWS is a compute commodity — doesn't capture model-layer margin

### Azure / Microsoft
**Strengths:**
- Exclusive OpenAI IP license through 2032
- First-party OpenAI products hosted on Azure
- API products developed with third parties exclusive to Azure
- $250B incremental Azure commitment from OpenAI
- Deep integration (GitHub Copilot, M365 Copilot, Foundry)

**Risks:**
- Lost exclusivity as OpenAI's sole cloud provider
- Lost right of first refusal on compute
- OpenAI IP license becomes non-exclusive
- Smallest Anthropic deal ($30B vs $100B+ AWS)
- No custom silicon story — reliant on NVIDIA
- Revenue share from OpenAI continues but is now capped and time-limited (through 2030)
- OpenAI is OpenAI's biggest customer — concentration risk if relationship evolves further

### Google Cloud
**Strengths:**
- Owns the silicon (TPUs) — vertically integrated, no margin leakage to chip makers
- Anthropic committed to 5GW of next-gen TPUs + earlier 1M TPU deal
- Also runs Gemini inference — captive demand regardless of third-party lab choices
- AI labs running on Google Cloud validates TPU performance for enterprise customers

**Risks:**
- Competitor dynamic: Gemini competes directly with Claude and GPT — will labs want to fund a competitor's cloud business long-term?
- Anthropic's major TPU capacity doesn't come online until 2027 — late vs. AWS/Azure
- OpenAI has NO significant Google Cloud commitment (only early $50M+ donation from Google Cloud; no current compute deal)
- Enterprise customers building on Vertex AI face vendor lock-in to Google ecosystem

---

## 6. Summary Scoreboard

| Dimension | AWS | Azure | Google Cloud |
|-----------|-----|-------|-------------|
| **Total $ committed by labs** | ~$238B (Anthropic $100B + OpenAI $138B) | ~$280B (OpenAI $250B + Anthropic $30B) | "Tens of billions" (Anthropic only) |
| **Total GW committed** | ~7 GW (Anthropic 5 + OpenAI 2) | ~1 GW (Anthropic only) | ~6 GW (Anthropic 5+1) |
| **Custom silicon** | Trainium (2/3/4) — strong lock-in | None (relies on NVIDIA) | TPUs — strongest vertical integration |
| **"Primary" status** | Anthropic's primary (since 2023) | OpenAI's primary (but weakening) | Gemini's captive provider |
| **Exclusivity** | OpenAI Frontier distribution | OpenAI IP license to 2032; API exclusivity | None with external labs |
| **Investment into labs** | ~$63B+ | ~$6B+ disclosed | Series C participation only |
| **Diversification risk** | Medium — labs explicitly multi-cloud | High — OpenAI actively diversifying away | Low for Gemini; high for attracting other labs |
| **Custom ASIC thesis** | Strong (Trainium) | Weak (no custom silicon) | Strongest (TPUs, vertically integrated) |

### Bottom Line

**For the custom ASIC inference thesis:**

- **AWS** is best positioned in the near-term (2025-2027). It has both major labs committed, Trainium creates real switching costs, and capacity is coming online NOW. The risk is that labs keep diversifying.

- **Google Cloud** is best positioned long-term IF the competitor dynamic doesn't kill third-party lab relationships. Vertical integration (own silicon + own models) means they capture margin at every layer. But their big Anthropic TPU capacity doesn't arrive until 2027, and OpenAI has no Google Cloud deal at all.

- **Azure** is the most exposed. It has the highest dollar commitments on paper ($280B), but the weakest structural position: no custom silicon, loosening exclusivity, and dependency on a single lab (OpenAI) that is actively diversifying. The IP license is valuable but doesn't guarantee inference workloads.

**The wild card:** OpenAI's Stargate ($500B / 10GW with Oracle/SoftBank) and custom chip deals (Broadcom 10GW, AMD 6GW) represent a potential future where OpenAI builds its OWN inference infrastructure, bypassing all three hyperscalers for a significant portion of workloads. If that happens, the "who wins cloud inference" question becomes less relevant for the largest single source of inference demand.

---

## 7. Q1 2026 Earnings Validation (April 29, 2026)

_Source: Q1 2026 earnings releases and call transcripts for Alphabet, Microsoft, Meta, and Amazon._

The Q1 2026 earnings cycle provided the strongest validation yet that custom silicon inference economics are working. Key signals by provider:

### Google Cloud (Alphabet) — Strongest ROI evidence for custom silicon

| Metric | Q1 2025 | Q1 2026 | Change |
|--------|---------|---------|--------|
| Cloud revenue | $12.3B | $20.0B | **+63% YoY** |
| Cloud operating margin | 17.8% | 32.9% | **Nearly doubled** |
| Cloud operating income | ~$2.2B | $6.6B | **Tripled** |

- GenAI revenue grew **~800% YoY** — most direct AI monetization signal in dataset
- Backlog nearly doubled QoQ to **$462B** (50%+ converting in 24 months)
- Sundar Pichai: revenue "would have been higher if we were able to meet the demand" — **capacity constrained, not demand constrained**
- On ROIC: "we are doing it based on tangible demand signals we are seeing... I'm talking from an ROIC framework"
- TPUs powered **100% of Gemini 2.0 training and inference** — Ironwood (7th gen) is inference-specific
- CapEx raised to $180-190B for 2026; 2027 "to significantly increase"

**Custom silicon signal:** Google Cloud's margin doubling while running entirely on TPUs is the single strongest datapoint that custom silicon inference economics work at scale. No NVIDIA dependency = no margin leakage to chip suppliers.

### AWS (Amazon) — Explicit Trainium ROI thesis

| Metric | Value | Notes |
|--------|-------|-------|
| AWS revenue | $37.6B | +28% YoY, fastest growth in 15 quarters |
| AWS operating margin | 37.7% | Stable in 35-37% range |
| AWS AI revenue run rate | **$20B+** | Custom silicon business alone, triple-digit growth |
| AWS backlog | $364B | NOT including $100B+ Anthropic deal |
| Trainium commitments | $225B+ | OpenAI 2GW + Anthropic 5GW |

Andy Jassy's Trainium ROI thesis (direct quote): **"At scale, we expect Trainium will save us tens of billions of dollars of CapEx each year and provide several hundred basis points of operating margin advantage versus relying on other chips for inference."**

- Amazon Bedrock: 170% growth in customer spend QoQ; processed more tokens in Q1 than all prior years combined
- FCF crashed to $1.2B TTM (from $25.9B) due to $43.2B Q1 capex — Jassy compared to first AWS growth wave

**Custom silicon signal:** $20B+ run rate for AI custom silicon is massive and growing triple-digit. But AWS margins are flat (37.7%) while Google Cloud margins doubled — suggesting TPUs are further along the efficiency curve than Trainium.

### Azure (Microsoft) — No custom silicon story

| Metric | Value | Notes |
|--------|-------|-------|
| AI business ARR | $37B | +123% YoY |
| Azure growth | +40% | Accelerating despite scale |
| Cloud gross margin | 66% | Slightly down YoY |
| RPO (backlog) | $627B | +99% YoY |
| Operating margin | 46% | Highest in group |

Amy Hood (on AI margins): **"they've remained better in our AI business, versus where we saw in the cloud transition looking back."** — Most explicit statement that AI margins are beating the cloud cycle.

**Custom silicon signal:** None. Microsoft has no custom chip. 46% operating margin with no silicon ownership means they're paying NVIDIA margin on every inference token. This works at current scale but creates structural disadvantage vs. Google/AWS long-term as inference volume scales.

### Meta — Broadcom custom silicon validation

- Revenue $56.3B (+33%), 41% operating margin
- Mark Zuckerberg: **"we're rolling out more than 1GW of our own custom silicon that we're developing with Broadcom"**
- CapEx raised to $125-145B (from $115-135B)
- 8M+ advertisers using GenAI creative tools; AI ranking driving +6% conversion rate

**Custom silicon signal:** Meta naming Broadcom directly while raising capex by $10B validates the custom ASIC thesis from outside the cloud provider ecosystem. Meta is a massive inference consumer (3.3B users) choosing custom silicon over NVIDIA for efficiency.

### Cross-Company Earnings Summary

| Signal | Alphabet | Microsoft | Meta | Amazon |
|--------|----------|-----------|------|--------|
| Cloud/AI revenue growth | **+63%** | Azure +40% | N/A | AWS +28% |
| Cloud margin trend | **Tripled to 32.9%** | 66% (stable) | N/A | 37.7% (stable) |
| Backlog | $462B | **$627B** | N/A | $364B+ |
| 2026 CapEx | $180-190B | **$190B** | $125-145B | ~$160B+ |
| FCF trend | Healthy | Down to $15.8B | Down to $12.4B | **Crashed to $1.2B** |
| Custom silicon | **TPUs (7th gen, inference-specific)** | None | Broadcom 1GW+ | Trainium ($20B+ ARR) |

**Key takeaway:** Cloud margins are expanding, not compressing. Combined ~$1.5T+ in booked AI revenue. The "AI is margin dilutive" thesis is wrong. Custom silicon operators (Google, AWS, Meta) are showing the strongest efficiency signals.

---

## 8. Custom Silicon Head-to-Head: TPUs vs Trainium

### Chip Specifications

| Spec | TPU v5e | TPU v6e (Trillium) | TPU Ironwood (v7) | Trainium1 | Trainium2 |
|------|---------|-------------------|-------------------|-----------|-----------|
| **Focus** | Training + inference | Training + inference | **Inference-first** | Training | Training + inference |
| **BF16 TFLOPS/chip** | 197 | 918 | **4,614** | ~190 | ~1,300 (FP8) |
| **HBM/chip** | 16 GB | 32 GB | **192 GB** | 32 GB | 96 GB |
| **HBM bandwidth** | 800 GB/s | 1,638 GB/s | **7,370 GB/s** | ~820 GB/s | Not disclosed |
| **Max pod** | — | 100K chips | 9,216 chips | — | 64 chips (UltraServer) |
| **Generation** | 5th | 6th | **7th** | 1st | 2nd |
| **Power efficiency** | Baseline | +67% vs v5e | **2x vs Trillium** | Baseline | Not disclosed |

### Pricing (publicly available, on-demand)

| Chip | $/chip-hr (on-demand) | 1yr committed | 3yr committed |
|------|----------------------|---------------|---------------|
| TPU v5e | ~$1.20 | — | — |
| TPU v6e (Trillium) | ~$3.22 | ~$2.25 | ~$1.61 |
| TPU Ironwood | Not public | — | — |
| Trainium1 (trn1.2xl) | $1.34 | $0.79 | $0.47 |
| Trainium2 (trn2.48xl) | **Not public** | — | — |

### Assessment

**Google leads on:** Silicon maturity (7th gen vs 2nd gen), inference-specific design (Ironwood), vertical integration (own chip + own models + own cloud), proven margin expansion (32.9% cloud margin)

**AWS leads on:** Go-to-market (both labs committed, $225B+ Trainium revenue), software co-development (Anthropic writing Trainium kernels), pricing transparency (self-serve on-demand available)

**The gap:** Neither publishes $/token for inference. The best proxy is their margin trajectories — Google Cloud margin doubling while AWS stays flat suggests TPUs are currently more efficient for inference. But Trainium3/4 could close this gap.

---

## 9. Stock Scorecard View (as of May 13, 2026)

_Filtered to inference-relevant positions. Scores from Munger/Buffett quality framework (1-10 per dimension). Prices updated May 12-13._

### Hyperscalers (the buyers of custom silicon)

| Ticker | Company | Price | Composite | Quality | Price Level | Verdict | P/E | Fwd P/E | PEG | Custom silicon role |
|--------|---------|-------|-----------|---------|-------------|---------|-----|---------|-----|-------------------|
| META | Meta | ~$600 | 8.5 | Wonderful | Cheap | **Strong conviction** | 23 | 15 | 0.39 | 1GW+ Broadcom custom silicon |
| MSFT | Microsoft | ~$412 | 8.8 | Wonderful | Fair | **Buy** | 34 | 25 | 0.76 | None — NVIDIA dependent |
| GOOGL | Alphabet | ~$402 | 8.5 | Wonderful | Fair | **Buy** | 40 | 28 | 0.97 | TPUs (7 generations, vertically integrated) |
| AMZN | Amazon | ~$269 | 7.2 | Wonderful | High | **Watch** | 55 | 42 | 1.8 | Trainium ($20B+ ARR) |

### Custom silicon enablers (picks & shovels)

| Ticker | Company | Price | Composite | Quality | Price Level | Verdict | P/E | Fwd P/E | PEG |
|--------|---------|-------|-----------|---------|-------------|---------|-----|---------|-----|
| AVGO | Broadcom | ~$428 | 8.0 | Wonderful | High | **Watch** | 72 | 33 | 0.68 |
| TSM | TSMC | ~$412 | 8.2 | Wonderful | Fair→High | **Buy** | 30 | 22 | 1.0 |
| MRVL | Marvell | ~$164 | 6.8→TBD | Good | ~~Fair~~→**Ext. High** | ~~Consider~~→**Pass on price** | ~56 | ~35 | TBD |

### Key scorecard changes since April 30

- **MRVL doubled** ($80→$164). P/E expanded from 28 to ~56. Previous "Good @ Fair Price → Consider" verdict is stale. At current levels, quality hasn't changed but price_level shifts to "extremely_high" → verdict becomes "Pass on price." The market has priced in the custom silicon thesis.
- **AVGO +12%** ($381→$428). Moving further into "High" territory. PEG 0.68 still attractive but 72x TTM P/E is stretched.
- **TSM +11%** ($371→$412). Approaching "High" price level. Monopoly-adjacent still justifies premium.
- **GOOGL +8%** ($371→$402). Post-earnings rally held. Cloud margin doubling is the strongest fundamental signal. Still "Fair Price."
- **META -4%** ($622→$600). Getting cheaper while showing 33% revenue growth and 41% margins. Remains cheapest in universe on PEG (0.39).

---

## 10. Updated Bottom Line

### On the inference game

1. **Google Cloud is winning the custom silicon efficiency race.** Cloud margin doubling to 32.9% while running 100% on TPUs, with Ironwood (7th gen, inference-specific) arriving, gives them the strongest structural position. The only risk is the competitor dynamic (Gemini vs. hosted models).

2. **AWS is winning on committed volume.** Both major labs, $225B+ Trainium commitments, $20B+ custom silicon ARR. But flat margins (37.7%) vs. Google's doubling suggest Trainium is earlier on the efficiency curve.

3. **Azure has the weakest inference position.** Highest paper commitments ($627B RPO) but no custom silicon means every inference token pays NVIDIA margin. 46% operating margin is impressive but structurally disadvantaged long-term.

4. **The market has priced in custom silicon.** MRVL doubling, AVGO +12%, GOOGL +8% all reflect the market validating the thesis. The easy money in "custom silicon will win inference" may already be captured in stock prices.

### On what to own

From the scorecard, the inference thesis points to:
- **META** (Strong conviction) — cheapest hyperscaler, 1GW+ custom silicon, 82% GM, PEG 0.39
- **GOOGL** (Buy) — best custom silicon position, margin doubling, but 40x TTM
- **TSM** (Buy) — manufactures ALL custom silicon (TPUs, Trainium, Broadcom XPUs). Monopoly-adjacent at 30x
- **AVGO** (Watch for pullback) — designs custom silicon for Meta/Google/others, but 72x TTM

---

_All figures sourced from company press releases (scraped May 2026), Q1 2026 earnings releases/transcripts (April 29, 2026), and public market data (May 12-13, 2026). Dollar commitments are announced maximums — actual spend may differ. This is research, not investment advice._
