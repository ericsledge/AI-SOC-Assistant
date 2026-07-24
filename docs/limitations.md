# Current Limitations

## Local Language Model

The application uses a locally hosted Ollama model.

Smaller local models generally produce lower-quality responses than larger cloud-hosted language models.

---

## Knowledge Base Limitations

The assistant can only answer questions using information contained within the indexed cybersecurity documents.

Topics outside the knowledge base may produce incomplete or inaccurate responses.

---

## Retrieval Limitations

Semantic retrieval is not perfect.

Relevant document chunks may occasionally be missed or ranked lower than less relevant chunks.

---

## No Real-Time Threat Intelligence

The assistant does not retrieve live threat intelligence.

It cannot provide current information about newly discovered vulnerabilities, active attacks, or recent CVEs unless those documents have been added to the knowledge base and re-indexed.

---

## Authentication

The current implementation does not include user authentication or role-based access control.

The application is intended for local educational use.

---

## Production Deployment

This project has not been deployed to a production environment.

Additional work would be required for scalability, monitoring, security hardening, and deployment.

---

## Analyst Review

The AI SOC Analyst Assistant is intended to support cybersecurity analysts.

Responses should always be reviewed by a qualified analyst before being used for operational or incident response decisions.