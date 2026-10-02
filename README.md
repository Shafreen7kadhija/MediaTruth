# MediaTruth — AI Media Authenticity Analyzer

MediaTruth is an AI-powered media authenticity analysis platform designed to examine images and videos and estimate whether they are likely AI-generated or naturally captured.

The system combines AI-based detection with metadata inspection, provenance checks, and evidence-based analysis to provide users with an understandable assessment of uploaded media.

Rather than presenting detection as absolute truth, MediaTruth communicates uncertainty, confidence, and supporting evidence to help users make informed judgments.

## Problem Statement

With the increasing accessibility of generative AI tools, distinguishing AI-generated media from authentic photographs and videos has become increasingly challenging.

Existing detection tools may provide a prediction without explaining the evidence behind it, making it difficult for users to understand the reliability and limitations of the result.

MediaTruth aims to address this challenge by combining detection results with additional forensic signals and transparent explanations.

## Proposed Solution

MediaTruth provides a unified platform where users can upload images or videos and receive an authenticity analysis report.

The system is designed to:

* Analyze uploaded media using AI detection services.
* Inspect available metadata and provenance information.
* Combine multiple signals to produce an evidence-based assessment.
* Highlight uncertainty and conflicting results.
* Explain why a particular result was produced.
* Present results through a simple and user-friendly interface.

## Planned Features

* Image authenticity analysis
* Video authenticity analysis
* AI-generated media detection
* Metadata inspection
* Provenance and C2PA checks where available
* Evidence aggregation and confidence estimation
* Frame-level video analysis
* Explainable analysis reports
* Analysis history
* Report export

## Technology Stack

**Frontend**

* React
* TypeScript
* Tailwind CSS

**Backend**

* Python
* Flask

**Database**

* SQLite

**External Services**

* AI media detection API (to be selected after evaluating available providers)

**Development Tools**

* Visual Studio Code
* Git and GitHub

## Development Roadmap

1. Project research and architecture design
2. Detection service evaluation and integration planning
3. Backend setup and API development
4. Image upload and analysis
5. Metadata and provenance inspection
6. Evidence aggregation and explanation engine
7. Frontend development
8. Video frame analysis
9. Testing and error handling
10. Documentation and deployment

## Important Disclaimer

MediaTruth provides estimated authenticity assessments, not definitive proof of whether media is real or AI-generated.

Results may vary depending on the detection model, media quality, available metadata, and other factors. Users should interpret the results with appropriate caution.

## Project Status

**Status:** In Development

This project is being developed as a learning and portfolio project, with an emphasis on transparency, explainability, and responsible AI use.
