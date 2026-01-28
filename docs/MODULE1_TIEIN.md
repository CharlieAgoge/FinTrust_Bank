# Module 1 tie-in: CIA triad and attack surface

This doc explains how the FinTrust Bank app supports Week 1 of the Cyber Agoge Bootcamp: mapping the CIA triad to real behaviour and outlining the attack surface for “think like a defender” exercises.

## CIA triad in the app

| Principle | Where it shows in FinTrust Bank |
|-----------|----------------------------------|
| **Confidentiality** | Only the logged-in user sees their balance and transfer history. Passwords are hashed (e.g. scrypt) and not logged. Session cookies are HttpOnly and SameSite. |
| **Integrity** | Transfer amounts are validated and applied in a single atomic step. The amount sent is exactly the amount received; no tampering mid-transfer. |
| **Availability** | The `/health` endpoint returns 200 for load balancers/orchestrators. Uptime and “can I log in and use the app?” map to availability. |

**In class:** Use the login flow (password in transit, token/session integrity) and the dashboard (balance visibility = confidentiality; “£100 stays £100” = integrity; health check = availability).

## Attack surface (Week 1 mapping)

Students can map “attack surfaces” by listing what is exposed and what data flows where.

### Endpoints and purpose

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/` | GET | no | Landing; link to login |
| `/login` | GET, POST | no | Authenticate; set session |
| `/logout` | GET, POST | no | Clear session |
| `/dashboard` | GET, POST | yes | View balance; submit transfer |
| `/health` | GET | no | Liveness/readiness for orchestration |

### Data flows to discuss

1. **Login** – Username/password from browser → server; session cookie set; password never stored in plaintext.
2. **Dashboard** – Session identifies user; balance and transfer form are server-rendered; transfer updates are validated and applied atomically.
3. **Health** – No sensitive data; suitable for external checks.

### Things to reinforce

- **Least privilege** – The app only has the access it needs (e.g. one SQLite DB, no unnecessary services).
- **Defence in depth** – Session + server-side checks; hashed passwords; safe defaults (e.g. HttpOnly, SameSite on cookies).
- **Authentication vs authorisation** – Login = who you are; dashboard and transfer = what you’re allowed to do (only your account).

## Next steps (Week 3+)

In **Week 3: Attack Mindset** you add OWASP Top 10, threat modelling, and vulnerability scanning. This repo can be extended with:

- A **lab** track: separate branch or `docs/labs/` with intentionally vulnerable variants (e.g. SQL injection, XSS, broken auth) for students to find and fix.
- **Semgrep** (or similar) runs in CI against the main branch to keep the “secure” baseline clean.
- **Threat models** for the same endpoints above (e.g. “What if an attacker tampers with the transfer amount in transit?”) using STRIDE or similar.

Keeping the Week 1 app small and clear makes it easier to contrast “secure by default” with later vulnerable lab versions.
