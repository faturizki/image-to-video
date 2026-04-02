"""
API Key Validation Test - Documentation & Usage Guide

This script validates whether all API keys used in the project are properly
configured and functional.

### Usage

#### Local Testing (without API keys - mock mode)
```bash
cd backend
python test_api_keys.py
```

Expected output:
```
✗ GEMINI: FAILED
  Message: API key not found in settings
✗ HUGGINGFACE: FAILED
  Message: API key not found in settings
```

#### Local Testing (with API keys)
```bash
# With .env file
cd backend
# Create or update .env with your keys
echo "GEMINI_API_KEY=your-key-here" >> .env
echo "HUGGINGFACE_API_KEY=your-key-here" >> .env
python test_api_keys.py
```

Or export as environment variables:
```bash
export GEMINI_API_KEY=your-key-here
export HUGGINGFACE_API_KEY=your-key-here
cd backend
python test_api_keys.py
```

#### GitHub Actions Testing
API keys should be configured as GitHub Secrets:
1. Go to your repository Settings → Secrets and variables → Actions
2. Add:
   - GEMINI_API_KEY: Your actual Gemini API key
   - HUGGINGFACE_API_KEY: Your actual Hugging Face API key

The CI/CD pipeline will automatically test these keys on each push/PR.

### API Key Validation Details

#### Gemini API
- **Endpoint**: Google Generative AI API
- **Test Method**: 
  1. Configure API with key
  2. Create GenerativeModel instance
  3. Send minimal test prompt ("Say 'test'...")
  4. Validate response is not empty
- **Success Criteria**: Can generate content without auth errors

#### Hugging Face API
- **Endpoint**: https://huggingface.co/api/whoami
- **Test Method**:
  1. Send authenticated GET request
  2. Check response status code
- **Success Criteria**: 200 OK response (authenticated and authorized)

### Troubleshooting

If you see:
- `API key not found in settings`: Key is not loaded from env/config
- `401 Unauthorized`: Key exists but authentication failed (invalid/expired key)
- `403 Forbidden`: Key authenticated but no permission to use API
- `Connection error`: Network issue or API endpoint unreachable

### What to Check

1. **API Key Format**: Make sure keys are pasted correctly (no extra spaces)
2. **Environment Variable Name**: Must match exactly:
   - `GEMINI_API_KEY` for Gemini
   - `HUGGINGFACE_API_KEY` for Hugging Face
3. **API Account Status**: Ensure accounts are active and not rate-limited
4. **Network Connectivity**: Check if you can reach API endpoints

### Integration with CI/CD

The test runs automatically in GitHub Actions:
1. After dependencies are installed
2. Tests run with `continue-on-error: true` to not block deployments
3. Failed tests are reported but don't stop the pipeline

To make it mandatory (fail pipeline if tests fail), remove `continue-on-error: true`
from `.github/workflows/ci-cd.yml`.

### Adding More API Keys

To add more API key tests:
1. Add API key to `config.py` (e.g., `new_api_key: Optional[str] = None`)
2. Add test method in `test_api_keys.py` (e.g., `test_new_api()`)
3. Call test method in `test_all_api_keys()` and add results
4. Update GitHub Actions secret if needed

### Security Notes

⚠️ **Important**:
- Never commit `.env` files with real API keys
- Never print API keys in logs
- Use GitHub Secrets for CI/CD environment
- Always use environment variables to pass keys
- Test script only prints keys as boolean (key exists or not)
"""
