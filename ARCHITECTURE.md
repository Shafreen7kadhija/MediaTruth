# MediaTruth — System Architecture

## 1. Overview

MediaTruth is an AI-powered media authenticity analysis platform that examines images and videos to estimate whether they are AI-generated or naturally captured.

The system combines AI detection, metadata inspection, provenance checks, and evidence aggregation to produce transparent and understandable analysis reports.

## 2. High-Level Architecture

The application follows a client-server architecture.

```text
                 USER
                  |
                  v
          REACT FRONTEND
                  |
                  v
           FLASK BACKEND
                  |
       +----------+----------+
       |          |          |
       v          v          v
   AI DETECTION  METADATA  PROVENANCE
     SERVICE    INSPECTOR   CHECKER
       |          |          |
       +----------+----------+
                  |
                  v
          EVIDENCE ENGINE
                  |
                  v
         RESULT GENERATION
                  |
                  v
          ANALYSIS REPORT
                  |
                  v
             FRONTEND
```

## 3. Component Responsibilities

### 3.1 Frontend

**Technology:** React, TypeScript, Tailwind CSS

Responsibilities:

* Provide an interface for uploading images and videos.
* Validate file types and display upload progress.
* Send media files to the backend.
* Display analysis results and confidence estimates.
* Present supporting evidence and explanations.
* Show analysis history.

### 3.2 Backend

**Technology:** Python, Flask

Responsibilities:

* Receive and validate uploaded media.
* Coordinate analysis services.
* Handle API communication.
* Aggregate detection results and supporting evidence.
* Generate structured analysis reports.
* Manage errors and temporary file cleanup.

### 3.3 AI Detection Service

The detection service will use an external AI media detection API selected after evaluating available providers.

Responsibilities:

* Analyze uploaded media.
* Retrieve model predictions and confidence scores when provided.
* Normalize responses into a consistent internal format.
* Handle API failures and unavailable results.

The external service will act as a detection provider, while MediaTruth will implement its own analysis workflow and reporting logic.

### 3.4 Metadata Inspector

Responsibilities:

* Extract available image and video metadata.
* Identify missing or unusual metadata.
* Inspect timestamps and software information when available.
* Present metadata as supporting context rather than definitive proof.

### 3.5 Provenance Checker

Responsibilities:

* Check for available Content Credentials or C2PA provenance information.
* Identify verifiable content history when supported.
* Distinguish verified provenance from missing or unavailable provenance.

Absence of provenance information does not automatically mean that media is AI-generated.

### 3.6 Evidence Aggregation Engine

This is a core component of MediaTruth.

Responsibilities:

* Combine AI detection results with metadata and provenance findings.
* Identify agreement or disagreement between evidence sources.
* Handle missing and conflicting signals.
* Produce an explainable assessment.
* Communicate uncertainty instead of forcing a definitive classification.

### 3.7 Database

**Technology:** SQLite

Responsibilities:

* Store analysis records.
* Maintain timestamps and result summaries.
* Support analysis history.
* Store report information without unnecessarily retaining original media files.

## 4. Analysis Workflow

1. The user uploads an image or video.
2. The frontend sends the file to the Flask backend.
3. The backend validates the file and its format.
4. The media is passed to the relevant analysis components.
5. The AI detection service returns its prediction.
6. The metadata inspector extracts available information.
7. The provenance checker examines available credentials.
8. The evidence aggregation engine evaluates the collected signals.
9. The backend generates a structured report.
10. The frontend displays the result, supporting evidence, and limitations.

## 5. Video Analysis Strategy

Video analysis will be performed through selected frame sampling rather than treating a single frame as representative of the entire video.

The planned workflow is:

1. Validate the uploaded video.
2. Extract frames at selected intervals.
3. Analyze sampled frames using the detection service.
4. Record frame-level predictions.
5. Aggregate the results while preserving uncertainty.
6. Present a frame-level summary to the user.

Frame-level predictions will be described as evidence from sampled frames, not definitive proof of the authenticity of the entire video.

## 6. Result Categories

MediaTruth will use three primary assessment categories:

* **Likely AI-generated:** Available evidence supports an AI-generated classification.
* **Likely natural:** Available evidence supports a naturally captured classification.
* **Uncertain:** Evidence is insufficient, unavailable, or conflicting.

These categories represent estimates rather than guarantees.

## 7. Error Handling and Privacy

* Reject unsupported file formats.
* Enforce upload size limits.
* Handle detection API timeouts and failures.
* Avoid exposing API keys in frontend code.
* Delete temporary media files after processing unless retention is explicitly required.
* Clearly communicate when analysis is incomplete.
* Avoid presenting missing metadata as evidence of manipulation.

## 8. Development Phases

| Phase | Work                               |
| ----- | ---------------------------------- |
| 1     | Research and architecture          |
| 2     | Detection provider evaluation      |
| 3     | Backend project setup              |
| 4     | Image analysis integration         |
| 5     | Metadata and provenance inspection |
| 6     | Evidence aggregation engine        |
| 7     | Frontend development               |
| 8     | Video frame analysis               |
| 9     | Testing and error handling         |
| 10    | Documentation and deployment       |

## 9. Current Status

**Status:** Architecture planning

The system design is preliminary and will be refined as detection providers, implementation constraints, and testing results are evaluated.
