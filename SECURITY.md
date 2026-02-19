# 🔒 Security Guidelines

## Implemented Security Measures

### ✅ **1. Rate Limiting**
- **Library**: `slowapi`
- **Limit**: 10 requests per minute per IP address on `/api/discover` endpoint
- **Purpose**: Prevent API abuse and control OpenAI costs
- **Error Response**: HTTP 429 (Too Many Requests)

### ✅ **2. Input Validation**
- **Min length**: 10 characters (prevents spam)
- **Max length**: 500 characters (prevents abuse)
- **Language validation**: Only `en` or `es` accepted
- **Pydantic models**: Automatic type validation

### ✅ **3. CORS Configuration**
- **Development**: Allows `localhost:3000` and `localhost:3001`
- **Production**: Configured via `ALLOWED_ORIGINS` environment variable
- **Credentials**: Disabled (`allow_credentials=False`)
- **Methods**: Only `GET` and `POST`

### ✅ **4. Environment Variables**
- **OpenAI API Key**: Stored in `.env` file (not committed to Git)
- **.env.example**: Template provided for setup
- **Production**: Use Render's environment variables dashboard

### ✅ **5. Error Handling**
- LLM errors fallback to basic query
- Deezer API errors fallback to charts
- Generic error messages (no sensitive data leakage)
- Proper HTTP status codes

---

## 🚨 Important: Before Deployment

### **DO:**
1. ✅ Set `ALLOWED_ORIGINS` in Render environment variables to your frontend URL
2. ✅ Set `OPENAI_API_KEY` in Render (never commit it)
3. ✅ Monitor OpenAI usage dashboard regularly
4. ✅ Check Render logs for suspicious activity
5. ✅ Keep dependencies updated (`pip list --outdated`)

### **DON'T:**
1. ❌ Never commit `.env` file to Git (already in `.gitignore`)
2. ❌ Never expose OpenAI API key in frontend code
3. ❌ Don't increase rate limits unless necessary (costs!)
4. ❌ Don't disable CORS in production
5. ❌ Don't ignore 429 errors in production logs

---

## 🛡️ Production Deployment Checklist

### **Backend (Render)**
```bash
# Environment Variables to set in Render Dashboard:
OPENAI_API_KEY=sk-proj-...
ALLOWED_ORIGINS=https://your-app.vercel.app
ENVIRONMENT=production
```

### **Frontend (Vercel)**
```bash
# Environment Variables to set in Vercel Dashboard:
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

---

## 📊 Monitoring Recommendations

### **OpenAI Usage**
- Check usage at: https://platform.openai.com/usage
- Set budget alerts in OpenAI dashboard
- Monitor GPT-4o-mini token consumption

### **Render Logs**
```bash
# Watch for 429 errors (rate limit exceeded)
# Watch for 500 errors (server errors)
# Monitor response times
```

### **Security Headers** (Future Enhancement)
Consider adding:
- `helmet` middleware for security headers
- HTTPS-only enforcement
- Content Security Policy (CSP)

---

## 🐛 Known Limitations

1. **Rate limiting by IP**: Can be bypassed with VPNs
   - *Mitigation*: Monitor costs, consider user authentication
   
2. **No authentication**: Anyone can use the API
   - *Mitigation*: Rate limiting prevents major abuse
   
3. **Public API**: No user accounts or history
   - *Future*: Add OAuth for personalized features

---

## 📞 Incident Response

If you notice unusual activity:
1. Check Render logs for repeated 429 errors
2. Verify OpenAI usage hasn't spiked
3. Temporarily reduce rate limit if needed
4. Update `ALLOWED_ORIGINS` if unauthorized domains are making requests

---

## 🔐 API Key Rotation

If your OpenAI key is compromised:
1. Revoke old key at https://platform.openai.com/api-keys
2. Generate new key
3. Update Render environment variable
4. Restart backend service in Render

---

## 📝 Security Audit Log

| Date | Change | Reason |
|------|--------|--------|
| 2026-02-17 | Added rate limiting (10/min) | Prevent API abuse |
| 2026-02-17 | Added CORS environment config | Production security |
| 2026-02-17 | Created SECURITY.md | Documentation |

