# Somint Project Context

## Claude's Perspective & Development Guide

**Project Name**: Somint  
**Purpose**: AI-powered PokÃ©mon card grading platform using Computer Vision + Claude LLM  
**Current Date**: November 2025  
**Development Status**: Pre-MVP (Core CV pipeline phase)

---

## 1. Project Vision & Philosophy

Somint is building **trust infrastructure** for card grading. Users uploading valuable cards ($100-$5000+) need confidence in grading accuracy. Every architectural decisionâ€”from CV pipeline robustness to explanation clarityâ€”serves this core principle.

The platform guides users through three main flows:

- **Grading**: Upload images â†’ receive estimated grade with detailed explanation
- **Selling**: Understand card condition before listing
- **Purchasing**: Validate seller claims with independent assessment

---

## 2. Core Feature Set

### Primary Features (MVP Focus)

- **Image Upload & Validation**: Reject non-compliant images (bad lighting, angles, backgrounds)
- **Quad Detection & Perspective Transform**: Standardize card orientation for consistent analysis
- **Subgrade Analysis**: Calculate centering, corner sharpness, edge quality
- **LLM Explanations**: Claude generates detailed grading explanations with reasoning transparency
- **Multi-Standard Support**: PSA, BGS, CGC grading standards (user-switchable)

### Current Scope

- **Card Type**: PokÃ©mon only
- **Subgrades**: Centering, corners, edges (surface defects deferred)
- **Users**: Individual collectors, casual traders (dealers as future expansion)

---

## 3. Subscription Tier Structure

### Free Tier

- 5 scans/month
- PSA standards only
- Summary explanations (200-300 words)
- Last 5 scans history
- No portfolio management

**Positioning**: Try-before-buy for curious users

### Explorer Tier

- 50 scans/month
- PSA + BGS standards
- Detailed explanations (500-800 words)
- Full searchable history
- Portfolio: up to 100 cards
- PDF export of grading reports

**Positioning**: Serious hobbyists who grade regularly

### Pro Tier

- Unlimited scans
- PSA + BGS + CGC standards
- Expert-level explanations (1000+ words with reasoning transparency)
- Full history + trend analysis
- Portfolio: unlimited + market value tracking
- JSON export for record-keeping
- Marketplace integration (price comparisons, listing prep)
- Batch processing (up to 10 cards/batch)
- API access (for dealers/platforms)

**Positioning**: Dealers, serious collectors, trading platforms

**Revenue Model**: Expected LLM costs ~$0.03-0.05 per grading with prompt caching optimization. Margin expansion via batch processing and tiered API access.

---

## 4. Technology Stack (Final)

### Backend

- **Language**: Go
  - Fast image pipeline processing
  - Goroutines for parallel CV operations
  - Minimal memory overhead
  - Simple deployment/scaling for MVP
- **Database**: PostgreSQL (user data, grading history, portfolio)
- **Cache**: Redis (session management, prompt cache coordination)
- **Message Queue**: Optionalâ€”RabbitMQ for async batch processing

### Frontend

- **Framework**: React + Vite
- **Why**: Vite's instant HMR critical for iterating on image upload UI; React ecosystem has solid image manipulation libraries
- **State Management**: Redux Toolkit or Zustand (start simple, scale as needed)
- **Image Preview**: React Image Crop or similar
- **Styling**: Tailwind CSS recommended

### Computer Vision Pipeline

- **OpenCV**: Classical CV for deterministic tasks
  - Image loading/color space conversion
  - Edge detection (Canny)
  - Contour finding & filtering
  - Quad approximation
  - Perspective transformation
  - Lighting/angle/background validation
- **YOLOv8**: Object detection for robustness (introduced post-week-8)

  - Card detection bounding box
  - Trained on 1000+ PokÃ©mon card images
  - Fallback/validation for OpenCV pipeline
  - Roboflow for dataset management

- **Python Backend**: Image processing service
  - FastAPI or Flask for CV microservice
  - Communicates with Go backend via REST/gRPC
  - Runs inference locally (no external API calls)

### LLM Integration

- **Provider**: Anthropic Claude
- **Model Versions**:
  - Claude 3.5 Sonnet: Primary (balanced cost/performance)
  - Claude 4.5: Future option for advanced reasoning
- **Key Features Utilized**:
  - Vision capabilities (direct image analysis)
  - 200K token context window (entire grading standard database in-context)
  - Prompt caching (5-minute cache for grading standards = 90% cost reduction)
  - Extended thinking (transparency in reasoning for Pro tier)

### Infrastructure

- **Hosting**: Docker containerization
  - Go backend container
  - Python CV service container
  - PostgreSQL/Redis containers
- **Deployment**: Initially self-hosted (AWS EC2 / DigitalOcean), scale to Kubernetes as needed
- **Cloud Storage**: AWS S3 or similar for card images (lifecycle policies to delete after 30 days post-grading)

---

## 5. Architecture Overview

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚   React Frontend    â”‚
â”‚  (Vite + Tailwind)  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
           â”‚ Upload 4-6 images
           â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚   Go REST API       â”‚
â”‚   (Backend Server)  â”‚
â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
     â”‚ Route to CV service
     â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  Python CV Microservice (FastAPI)   â”‚
â”‚                                     â”‚
â”‚  1. Validation Pipeline             â”‚
â”‚     - Lighting detection            â”‚
â”‚     - Angle verification            â”‚
â”‚     - Background checking           â”‚
â”‚                                     â”‚
â”‚  2. Standardization                 â”‚
â”‚     - YOLOv8 detection              â”‚
â”‚     - OpenCV quad detection         â”‚
â”‚     - Perspective transform         â”‚
â”‚                                     â”‚
â”‚  3. Analysis                        â”‚
â”‚     - Centering calculation         â”‚
â”‚     - Corner detection              â”‚
â”‚     - Edge quality assessment       â”‚
â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
     â”‚ Return metrics + transformed images
     â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚   Go Backend Processing             â”‚
â”‚                                     â”‚
â”‚   - Store in PostgreSQL             â”‚
â”‚   - Prepare Claude request          â”‚
â”‚   - Handle API communication        â”‚
â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
     â”‚ Send metrics + images to Claude
     â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  Claude API (Anthropic)             â”‚
â”‚                                     â”‚
â”‚  - Analyze images & metrics         â”‚
â”‚  - Generate explanation             â”‚
â”‚  - Reference grading standard       â”‚
â”‚  - Return detailed assessment       â”‚
â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
     â”‚
     â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  Go Backend                         â”‚
â”‚  - Parse Claude response            â”‚
â”‚  - Format for display               â”‚
â”‚  - Store grading record             â”‚
â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
     â”‚
     â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  React Frontend                     â”‚
â”‚  - Display grades & explanation     â”‚
â”‚  - Allow portfolio management       â”‚
â”‚  - Show trending insights (Pro)     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## 6. Development Roadmap (16 Weeks)

### Phase 1: Core Computer Vision Foundation (Weeks 1-8)

**Goal**: Build reliable quad detection & perspective transform

- **Weeks 1-2**: OpenCV Fundamentals

  - Image loading, color spaces (BGR vs HSV vs Grayscale)
  - Why color space selection matters for card grading
  - Build: Simple script testing color conversions on 10 sample cards

- **Weeks 3-4**: Edge Detection

  - Canny edge detection algorithm & parameter tuning
  - Experiment across different lighting conditions
  - Build: Edge detection that works reliably on your card dataset

- **Week 5**: Contour Finding & Filtering

  - Find card boundaries via contour detection
  - Filter by area/shape to isolate card
  - Build: Card boundary detection handling varied backgrounds

- **Weeks 6-7**: Perspective Transform

  - Homography & geometric transformations
  - Implement `getPerspectiveTransform()` + `warpPerspective()`
  - Build: Standardized top-down card views from 20 test images

- **Week 8**: Image Validation
  - Lighting detection (histogram analysis)
  - Angle consistency checks
  - Background uniformity detection
  - Build: Rejection system for unusable images

### Phase 2: Robustness & Enhancement (Weeks 9-10)

**Goal**: Introduce YOLOv8, validate against real data

- **Weeks 9-10**: YOLOv8 Integration
  - Train on 1000+ PokÃ©mon card images (Roboflow dataset)
  - Compare classical OpenCV vs neural network approach
  - Build: YOLOv8 detection as validation layer

### Phase 3: Grading Algorithms (Weeks 11-12)

**Goal**: Implement centering, corner, edge analysis

- **Week 11**: Centering Analysis

  - Border width measurement algorithms
  - Ratio calculations (left/right, top/bottom)
  - Threshold definition (what = 60/70/80 grade?)
  - Validation: Compare to 50 official PSA/BGS graded cards

- **Week 12**: Corner & Edge Analysis
  - Corner sharpness detection
  - Edge quality assessment
  - Soft corner identification
  - Build: Complete subgrade calculation pipeline

### Phase 4: Backend & LLM Integration (Weeks 13-14)

**Goal**: Connect CV â†’ Claude â†’ user

- **Week 13**: Go Backend Development

  - REST API endpoints for image upload/processing
  - Database schema (users, gradings, portfolio, standards)
  - Image storage management (S3/cloud storage)
  - Claude API integration setup

- **Week 14**: Prompt Engineering & Optimization
  - Design prompts for PSA/BGS/CGC standards
  - Implement prompt caching (90% cost reduction)
  - Test explanation quality & accuracy
  - Build: End-to-end grading pipeline

### Phase 5: Frontend & Polish (Weeks 15-16)

**Goal**: Launch MVP

- **Week 15**: React Frontend

  - Image upload interface
  - Real-time validation feedback
  - Grading results display
  - Standard toggle (PSA/BGS/CGC)
  - Portfolio management basic UI

- **Week 16**: Testing & Optimization
  - End-to-end testing on diverse card images
  - Performance optimization
  - Cost optimization validation
  - UX refinement based on testing
  - Deploy MVP

---

## 7. Key Technical Decisions & Rationale

### Why OpenCV Before YOLOv8?

Classical CV teaches you _why_ detection works. This allows debugging and domain-specific optimization. YOLOv8 comes after you understand the pipeline, making you a better ML engineer.

### Why Python Microservice for CV?

- OpenCV & YOLOv8 have best ecosystem support in Python
- Go has weaker CV libraries
- Microservice architecture allows independent scaling
- Simple REST communication between Go backend and Python service

### Why Claude for LLM?

- Vision capabilities (direct image analysis correlates with CV metrics)
- 200K token context (entire grading standard database in one conversation)
- Prompt caching (dramatic cost reduction for high-volume Pro users)
- Reasoning transparency (extended thinking for trust-critical application)
- Constitutional AI approach aligns with trustworthiness requirement

### Why Prompt Caching Critical?

- Store PSA/BGS/CGC standards once (5-minute cache window)
- Subsequent gradings only pay for new metrics + explanation
- ~90% cost reduction on input tokens
- Essential for Pro tier profitability

---

## 8. Grading Standards Database

You will need to research and document:

### PSA Standards

- Grade scale (1-10)
- Centering tolerances (55/45 = 8.0, etc.)
- Corner criteria (sharp = +1, soft = -1, etc.)
- Edge criteria (clean = +0, whitening = -2, etc.)

### BGS Standards

- Grade scale (1-10)
- Centering same as PSA (they align here)
- Corner/edge criteria (slightly stricter than PSA)

### CGC Standards

- Grade scale (1-10)
- Centering criteria (more lenient in lower grades)
- Corner/edge assessment (different terminology)

**Action**: Create structured JSON/YAML with these standards for Claude to reference.

---

## 9. Dataset Requirements

### For Training YOLOv8

- **Quantity**: 1000+ PokÃ©mon card images minimum
- **Annotation**: Bounding boxes around card boundary
- **Tool**: Roboflow (free tier acceptable)
- **Diversity**: Multiple angles, lighting conditions, backgrounds
- **Source**: Your own photos, community datasets (if available), synthetic generation if needed

### For Validation

- **Quantity**: 50-100 officially graded cards (PSA/BGS/CGC)
- **Purpose**: Compare your gradings vs official assessments
- **Metric**: Calculate accuracy percentage
- **Target**: 85%+ accuracy before MVP launch

---

## 10. Cost Analysis (Important for Pricing)

### Somint Operating Costs Per Grading

- **Open AI API**: Input ~8K tokens + Output ~1.5K tokens
  - Without caching: ~$0.007 input + $0.023 output = $0.030/grading
  - With caching: ~$0.001 input + $0.023 output = $0.024/grading (90% reduction on input)
- **Image Storage**: ~2-3 MB per grading
  - S3 cost: ~$0.000046 per GB = negligible
- **Compute**: Varies with architecture
  - EC2 baseline: ~$0.05-0.10 per inference (small instance)
- **Total Per Grading**: ~$0.03-0.04 with caching

### Pricing Strategy

- **Free**: 5/month Ã— $0.035 = $0.175/month cost (acceptable loss leader)
- **Explorer**: 50/month Ã— $0.035 = $1.75/month cost; charge $9.99/month = $8.24 margin
- **Pro**: Unlimited + batch processing reduces per-card to $0.02; charge $29.99/month

---

## 11. Success Metrics

### Technical

- Grading accuracy: 85%+ vs professional companies
- Image validation precision: 95%+ (minimize false rejections)
- Perspective transform accuracy: Verify borders are within 2% deviation
- API response time: <15 seconds for full pipeline

### User Experience

- User satisfaction with explanations: 4.5/5 stars target
- First-time user completion rate: 80%+ upload to grade
- Monthly active users retention: 60%+ after free tier

### Business

- Free â†’ Explorer conversion: 15%
- Explorer â†’ Pro conversion: 10%
- Average revenue per user: $2-5/month at scale

---

## 12. Known Challenges & Mitigation

### Challenge 1: Card Detection in Poor Lighting

**Why it's hard**: Different lighting conditions affect edge detection
**Mitigation**:

- Use HSV color space (lighting-invariant)
- Implement histogram equalization
- YOLOv8 trained on diverse lighting as fallback

### Challenge 2: Perspective Distortion at Extreme Angles

**Why it's hard**: Cards photographed at 45Â° angles create compression artifacts
**Mitigation**:

- Reject images where card isn't close to perpendicular
- Use angle consistency checks
- Train YOLOv8 to detect valid angle range

### Challenge 3: Surface Defects (Scratches, Print Lines)

**Why it's hard**: Requires pixel-level analysis; easy to confuse with lighting artifacts
**Mitigation**:

- Defer to future phase (not MVP scope)
- Focus on macro features (centering, corners, edges) first
- Plan surface defect detection as Phase 2

### Challenge 4: Grading Standard Variations

**Why it's hard**: PSA/BGS/CGC have subtle differences; easy to misinterpret
**Mitigation**:

- Research official grading guides extensively
- Have Claude explain the differences, not just apply rules
- Validate against real graded cards early

### Challenge 5: LLM Hallucination in Explanations

**Why it's hard**: Claude might invent details about cards
**Mitigation**:

- Prompt engineering: Be explicit about what you see vs. what you infer
- Always reference your CV metrics as ground truth
- Include "confidence level" in explanations
- Regular validation against user feedback

---

## 13. Future Roadmap (Post-MVP)

### Phase 6: Surface Defect Detection (Weeks 17-24)

- Advanced image analysis for scratches, print lines, spots
- Deep learning model fine-tuned for defect detection

### Phase 7: Marketplace Integration (Months 6-9)

- Price trending dashboard
- Marketplace listing preparation
- Seller recommendation engine

### Phase 8: Community & Analytics (Months 9-12)

- User rankings by grading accuracy
- Card trending/trending insights
- Trading platform partnerships

### Phase 9: API & Enterprise (Year 2)

- Public API for dealers/platforms
- Batch grading at scale
- White-label options

---

## 14. Resources & Learning Materials

### Computer Vision

- **PyImageSearch** (Adrian Rosebrock): Best practical tutorials
- **OpenCV Official Tutorials**: Comprehensive reference
- **"Learning OpenCV" (O'Reilly)**: Deep technical dives
- **YouTube**: Andreas Spiess for applied CV projects

### YOLOv8 & Deep Learning

- **Ultralytics Documentation**: Official, well-written
- **Roboflow**: Dataset management & annotation
- **"Deep Learning Specialization" (Coursera)**: If you want theory

### Claude & LLM Integration

- **Anthropic Documentation**: Your primary reference
- **Prompt Engineering Guides**: OpenAI & Anthropic resources
- **Vision Capabilities**: Test with your own card images first

### Backend (Go)

- **"Go by Example"**: Best way to learn idiomatic Go
- **Go Official Documentation**: Your reference
- **"Building REST APIs with Go" (Various tutorials)**: Practical

### Frontend (React + Vite)

- **React Official Docs**: Newly rewritten, excellent
- **Vite Documentation**: Straightforward
- **"React Design Patterns"**: As you scale

---

## 15. Project Management Notes

### Week-by-Week Checkpoints

- Week 4: Can detect card edges reliably on 5 test images
- Week 8: Perspective transform creates standardized cards from 20 test images
- Week 10: YOLOv8 model trained and validating
- Week 12: Grading calculations tested against 50 real cards
- Week 14: End-to-end pipeline working locally
- Week 16: MVP live with basic feature set

### Testing Strategy

- **Unit Tests**: For each CV algorithm (edge detection, contour finding, etc.)
- **Integration Tests**: Full pipeline on diverse card images
- **Validation Tests**: Compare your grades vs official graded cards
- **Load Tests**: Can you handle 10 concurrent users in Free tier?

### Documentation Requirements

- Code comments (especially for CV algorithmsâ€”they're non-obvious)
- API documentation (for Go backend endpoints)
- Prompt documentation (what each Claude prompt does, why)
- Deployment guide (how to run locally vs production)

---

## 16. Questions to Answer Before Starting

1. **Dataset**: Do you have access to official PSA/BGS/CGC graded card images for validation?
2. **Compute**: Will you run CV locally or use cloud GPU? (Local recommended for MVP)
3. **LLM Access**: Do you have Anthropic API access? (Set up early)
4. **Timeline**: Are you working full-time on this or part-time? (Adjust roadmap accordingly)
5. **MVP Definition**: What's the minimum to launch? (I recommend: upload â†’ standardize â†’ grade â†’ explain)

---

## 17. Contact & Support Notes

- **Stuck on OpenCV?**: PyImageSearch forum + OpenCV documentation
- **Stuck on Claude?**: Anthropic documentation + test simple prompts first
- **Stuck on Go?**: Go community is helpful; r/golang on Reddit
- **General Architecture**: Think through data flow before coding

---

**Last Updated**: November 7, 2025  
**Next Review**: After Week 4 checkpoint  
**Maintained By**: You + Claude (your CLI agent has this context)

---
