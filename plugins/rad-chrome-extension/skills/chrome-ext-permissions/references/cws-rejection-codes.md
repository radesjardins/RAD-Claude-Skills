# Chrome Web Store Rejection Codes

## Blue Family — Code Policy Violations

### Blue Argon — Remote Code
**Trigger:** Extension loads or executes code from external sources.
**Examples:** External `<script>` tags, `eval()`, `new Function()`, dynamically fetched JavaScript, SDK loaded from CDN.
**Prevention:**
- Bundle ALL dependencies locally via npm
- Remove all `eval()`, `new Function()`, `setTimeout(string)`, `setInterval(string)`
- Replace CDN-hosted libraries with local copies
- Audit npm packages for hidden `eval()` usage
- Use sandboxed iframes for unavoidable dynamic code

## Yellow Family — Packaging and Metadata

### Yellow Magnesium — Packaging/Functionality Issues
**Trigger:** Missing files, wrong paths, broken builds, non-functional extension.
**Examples:** Case-sensitive file path mismatches (Windows → Linux), missing icons, empty popup.
**Prevention:**
- Test packed `.zip` locally before submission
- Verify all file paths are case-correct (CWS reviewer runs on Linux)
- Ensure all declared resources exist in the package
- Test on a clean Chrome profile

### Yellow Zinc — Metadata Issues
**Trigger:** Missing icons, vague descriptions, keyword stuffing, misleading screenshots.
**Prevention:**
- Provide all required icon sizes (16, 32, 48, 128)
- Write clear, accurate descriptions
- Include representative screenshots
- No keyword spam in name or description
- Description must match actual functionality

## Purple Family — Permission and Privacy Violations

### Purple Potassium — Excessive Permissions
**Trigger:** Extension requests permissions it does not use, or requests overly broad permissions.
**Examples:** `<all_urls>` when extension only uses one site, `tabs` just to get current URL, permissions for unimplemented features.
**Prevention:**
- Audit every declared permission against actual code usage
- Replace broad permissions with narrow alternatives
- Use `activeTab` instead of `<all_urls>` where possible
- Move non-core permissions to `optional_permissions`
- Provide clear cause-and-effect justification in privacy tab

### Purple Lithium — User Data Privacy
**Trigger:** Extension handles user data without proper disclosure or privacy policy.
**Examples:** Missing privacy policy, collecting data without disclosure, unclear data handling.
**Prevention:**
- Provide working privacy policy URL that accurately describes data practices
- Disclose all data collection, usage, and sharing
- Ensure privacy policy is accessible (not behind login)
- Match privacy policy to actual extension behavior

### Purple Copper — Data Transmission Security
**Trigger:** Sensitive data transmitted insecurely.
**Examples:** HTTP instead of HTTPS, sensitive data in URL parameters or headers, unencrypted data transmission.
**Prevention:**
- Use HTTPS for ALL data transmission
- Never put sensitive data in URL query parameters
- Never put sensitive data in request headers that may be logged
- Encrypt sensitive payloads

## Red Family — Single Purpose Violations

### Red Magnesium — Multiple Unrelated Features
**Trigger:** Extension bundles unrelated functionalities.
**Prevention:** Each extension serves exactly one purpose. Split unrelated features into separate extensions.

### Red Copper — Undisclosed Features
**Trigger:** Extension has functionality not mentioned in its description.
**Prevention:** Description must accurately reflect ALL features.

### Red Lithium — Deceptive Behavior
**Trigger:** Extension behaves differently than described or expected.
**Prevention:** Ensure behavior matches marketing. No hidden functionality.

### Red Argon — New Tab/Homepage Override
**Trigger:** Extension overrides New Tab or homepage without proper disclosure.
**Prevention:** Use official URL Overrides API. Clearly disclose in description.

### Red Titanium — Code Obfuscation
**Trigger:** Deliberately obfuscated code (Base64-encoded logic, character encoding tricks).
**Prevention:** Use only standard minification. Never deliberately hide code functionality.

## Grey Family — Monetization Violations

### Grey Titanium — Affiliate Abuse
**Trigger:** Injecting affiliate cookies/codes without user knowledge or consent.
**Prevention:**
- Disclose affiliate usage clearly
- Only apply affiliate links after explicit user action
- Never inject affiliate codes automatically

## Review Timeline and Tips

- **Standard review:** 1-7 business days
- **Expedited review:** Include video proof and clear justification
- **Repeat rejections:** Address ALL issues before resubmission; each rejection extends review time

**Tips for faster review:**
1. Include a test video (30-60 seconds) demonstrating sensitive permission usage
2. Provide test credentials if extension requires login
3. Write specific cause-and-effect justifications (not vague explanations)
4. Link privacy policy prominently
5. Respond to reviewer feedback with specific changes made
