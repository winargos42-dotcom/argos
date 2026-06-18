---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/stream/gotchas.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\stream\gotchas.md
source_ext: .md
source_sha256: 17e6c4abb80560a6fbd761a434a6c8e8ecc26d7f74d666c2dd37522a83426171
text_sha256: 65ef0e0f81470833dea11179849d5bf78f695720286db5e5eebe7d8dcf77a1d4
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# gotchas.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/stream/gotchas.md`
- Extract: `text`
- SHA256: `17e6c4abb80560a6fbd761a434a6c8e8ecc26d7f74d666c2dd37522a83426171`

## Content

# Stream Gotchas

## Common Errors

### "ERR_NON_VIDEO"

**Cause:** Uploaded file is not a valid video format
**Solution:** Ensure file is in supported format (MP4, MKV, MOV, AVI, FLV, MPEG-2 TS/PS, MXF, LXF, GXF, 3GP, WebM, MPG, QuickTime)

### "ERR_DURATION_EXCEED_CONSTRAINT"

**Cause:** Video duration exceeds `maxDurationSeconds` constraint
**Solution:** Increase `maxDurationSeconds` in direct upload config or trim video before upload

### "ERR_FETCH_ORIGIN_ERROR"

**Cause:** Failed to download video from URL (upload from URL)
**Solution:** Ensure URL is publicly accessible, uses HTTPS, and video file is available

### "ERR_MALFORMED_VIDEO"

**Cause:** Video file is corrupted or improperly encoded
**Solution:** Re-encode video using FFmpeg or check source file integrity

### "ERR_DURATION_TOO_SHORT"

**Cause:** Video must be at least 0.1 seconds long
**Solution:** Ensure video has valid duration (not a single frame)

## Troubleshooting

### Video stuck in "inprogress" state
- **Cause**: Processing large/complex video
- **Solution**: Wait up to 5 minutes for processing; use webhooks instead of polling

### Signed URL returns 403
- **Cause**: Token expired or invalid signature
- **Solution**: Check expiration timestamp, verify JWK is correct, ensure clock sync

### Live stream not connecting
- **Cause**: Invalid RTMPS URL or stream key
- **Solution**: Use exact URL/key from API, ensure firewall allows outbound 443

### Webhook signature verification fails
- **Cause**: Incorrect secret or timestamp window
- **Solution**: Use exact secret from webhook setup, allow 5-minute timestamp drift

### Video uploads but isn't visible
- **Cause**: `requireSignedURLs` enabled without providing token
- **Solution**: Generate signed token or set `requireSignedURLs: false` for public videos

### Player shows infinite loading
- **Cause**: CORS issue with allowedOrigins
- **Solution**: Add your domain to `allowedOrigins` array

## Limits

| Resource | Limit |
|----------|-------|
| Max file size | 30 GB |
| Max frame rate | 60 fps (recommended) |
| Max duration per direct upload | Configurable via `maxDurationSeconds` |
| Token generation (API endpoint) | 1,000/day recommended (use signing keys for higher) |
| Live input outputs (simulcast) | 5 per live input |
| Webhook retry attempts | 5 (exponential backoff) |
| Webhook timeout | 30 seconds |
| Caption file size | 5 MB |
| Watermark image size | 2 MB |
| Metadata keys per video | Unlimited |
| Search results per page | Max 1,000 |

## Performance Issues

### Upload is slow
- **Cause**: Large file size or network constraints
- **Solution**: Use TUS resumable upload, compress video before upload, check bandwidth

### Playback buffering
- **Cause**: Network congestion or low bandwidth
- **Solution**: Use ABR (adaptive bitrate) with HLS/DASH, reduce max bitrate

### High processing time
- **Cause**: Complex video codec, high resolution
- **Solution**: Pre-encode with H.264 (most efficient), reduce resolution

## Type Safety

```typescript
// Error response type
interface StreamError {
  success: false;
  errors: Array<{
    code: number;
    message: string;
  }>;
}

// Handle errors
async function uploadWithErrorHandling(url: string, file: File) {
  const formData = new FormData();
  formData.append('file', file);
  const response = await fetch(url, { method: 'POST', body: formData });
  const result = await response.json();
  
  if (!result.success) {
    throw new Error(result.errors[0]?.message || 'Upload failed');
  }
  return result;
}
```

## Security Gotchas

1. **Never expose API token in frontend** - Use direct creator uploads
2. **Always verify webhook signatures** - Prevent spoofed notifications
3. **Set appropriate token expiration** - Short-lived for security
4. **Use requireSignedURLs for private content** - Prevent unauthorized access
5. **Whitelist allowedOrigins** - Prevent hotlinking/embedding on unauthorized sites

## In This Reference

- [README.md](./README.md) - Overview and quick start
- [configuration.md](./configuration.md) - Setup and config
- [api.md](./api.md) - On-demand video APIs
- [api-live.md](./api-live.md) - Live streaming APIs
- [patterns.md](./patterns.md) - Full-stack flows, best practices

## See Also

- [workers](../workers/) - Deploy Stream APIs securely

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
