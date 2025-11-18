# Screenshots

Phase 4: Visual Testing with Playwright

## Capturing Screenshots

```bash
# Capture API documentation screenshots
python screenshot_utility.py

# Run visual regression tests
pytest tests/e2e/test_visual_regression.py -v

# Or use make command
make screenshots
make visual-tests
```

## Screenshot Gallery

After capturing screenshots, view the gallery:

```bash
open screenshots/gallery.html
```

## Automated Screenshots

Screenshots are automatically captured for:
- API root endpoint
- Swagger UI documentation
- ReDoc documentation
- Health check JSON response

## Visual Regression Testing

Visual regression tests capture screenshots during E2E tests:
- `screenshots/tests/api_docs.png`
- `screenshots/tests/health_endpoint.png`
- `screenshots/tests/generated_ui.png`

## Metadata

Screenshot metadata is saved in `screenshot_metadata.json` including:
- URL captured
- Timestamp
- Page title
- File path

## CI/CD Integration

Screenshots can be captured in CI/CD pipeline and stored as artifacts for:
- Visual regression testing
- Documentation updates
- Release notes
