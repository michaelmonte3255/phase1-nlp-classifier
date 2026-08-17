Phishing URL Classifier

Problem:

Phishing attacks are some of the most common social enginerring attacks in cybersecurity. These attacks rely on malicious URLs designed to look legitimate and trick the user into giving sensitive information. This project is a classifier that predicts whether a URL is phishing or legitimate based on the URL string alone meaning there is no need to visit the site or analyze page content. The model is served as a live API, deployed on AWS.

Data
Source: real-world URL dataset aggregating OpenPhish, URLhaus, and Tranco which contained actual phishing URLs and actual legitimate site rankings.
7,658 training rows / 3,772 test rows, pre-split, perfectly balanced (3,829 phishing / 3,829 legitimate).
Only the raw url string and status label were used; the dataset's 89 pre-engineered features were intentionally not used, so every feature in this project is self-derived and explainable.
EDA surfaced real, interpretable patterns: phishing URLs disproportionately contain credential-harvesting language (login, update, secureupdate), brand-impersonation typosquats (appleld — a lowercase "l" swapped for capital "I"), and abuse of trusted cloud domains (appspot) to evade blocklists.


Model choices
Features: Used TF-IDF on the URL string, combined with hand-built structural features (URL length, digit count, HTTPS usage, presence of an IP address, dot/hyphen counts).
Baseline: Logistic Regression was chosen on purpose to create a fast, explainable starting point
Decision: shipped the Logistic Regression baseline. It matched the more complex models on this dataset while being faster to train, faster at inference, and fully explainable — a deliberate tradeoff, not a shortcut.


Metrics (Logistic Regression baseline):
- Precision (phishing): 0.92
- Recall (phishing): 0.90
- F1 (phishing): 0.91
- Accuracy: 0.91

Precision and recall are reported separately because they matter differently here: low recall means real phishing slips through indicating False Negatives. Low precision means legitimate sites get wrongly flagged indicating False Positives.

What I'd improve:

Have not fully evaluated the Random Forest and DistilBERT numbers above
Add features that require live lookups (domain age, DNS records, page rank) to catch patterns the URL string alone can't reveal — with a documented tradeoff, since those require external API calls at inference time.
Add automated tests for the /predict endpoint and a CI/CD pipeline to automate builds and deploys to ECR/EC2.
Move from a single EC2 instance to something that auto-restarts/scales (e.g. an Auto Scaling Group or ECS) for real production reliability.


Deployment:

FastAPI app → Docker container → Amazon ECR → AWS EC2 (IAM role for ECR access, security group restricting SSH to a single trusted IP).

--To run the docker
docker build -t phishing-classifier .
docker run -p 8000:8000 phishing-classifier

--To place a URL for the phishing classifier to classify
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"url": "http://secure-login-appleid-update.com"}'