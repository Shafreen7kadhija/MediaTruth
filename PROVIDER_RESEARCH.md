# MediaTruth — AI Detection Provider Research

## 1. Objective

The objective of this research is to identify a suitable external AI detection provider for MediaTruth.

The selected provider should support image and video analysis, return interpretable predictions, offer accessible developer documentation, and be suitable for a student portfolio project.

## 2. Providers Evaluated

### Sightengine

**Capabilities:**

* AI-generated image detection
* AI-generated video detection
* Deepfake detection
* Per-generator confidence scores
* Frame-level video analysis
* API integration through HTTP requests

**Pricing considerations:**

* Free plan available for testing and personal use.
* Paid plans available for higher usage.

**Advantages:**

* Supports both target media formats.
* Offers a practical starting point for development.
* Provides detailed model outputs that can support explainable reports.

**Limitations:**

* Detection results are probabilistic.
* Free-tier usage limits must be verified.
* External API availability and pricing may affect deployment.

Documentation: https://sightengine.com/docs/

Pricing: https://sightengine.com/pricing

### Hive

**Capabilities:**

* AI-generated image detection
* AI-generated video detection
* Deepfake classification
* Source classification
* Confidence scores

**Pricing considerations:**

* Free credits are available after adding a payment method.
* Usage-based pricing applies to detection requests.

**Advantages:**

* Supports multiple media formats.
* Provides detailed classification results.
* Offers an alternative provider for future evaluation.

**Limitations:**

* Free credits are conditional on adding a payment method.
* Usage costs should be considered before production deployment.

Documentation: https://docs.thehive.ai/docs/ai-image-and-video-detection

Pricing: https://thehive.ai/pricing

## 3. Comparison

| Criteria                                        | Sightengine            | Hive         |
| ----------------------------------------------- | ---------------------- | ------------ |
| Image detection                                 | Supported              | Supported    |
| Video detection                                 | Supported              | Supported    |
| Deepfake detection                              | Supported              | Supported    |
| Confidence scores                               | Available              | Available    |
| Free testing option                             | Free plan              | Free credits |
| Payment method required for stated free credits | Not stated as required | Yes          |
| Integration approach                            | REST API               | API          |

## 4. Initial Decision

Sightengine is selected as the initial detection provider for MediaTruth.

This is a provisional development decision based on its media-format support, testing accessibility, and compatibility with the planned architecture.

Hive will remain a potential alternative provider.

## 5. Integration Strategy

The backend will communicate with the detection provider through a dedicated service module.

The application will:

1. Accept and validate uploaded media.
2. Send the media to the selected provider.
3. Normalize the provider's response.
4. Extract relevant prediction scores.
5. Combine model output with metadata and provenance findings.
6. Generate an explainable analysis report.

The provider will be treated as one evidence source rather than the complete decision-making system.

## 6. Important Considerations

* No detection result will be presented as absolute proof.
* Missing metadata will not automatically indicate AI generation.
* Conflicting signals will be represented as uncertainty.
* API credentials will be stored securely on the backend.
* Usage limits and privacy requirements will be reviewed before deployment.

## 7. Status

**Research completed — initial provider selected.**

The next phase is to validate the provider's API access and design the backend integration.
