# Go Examples — Bugfix

These examples demonstrate safe bugfix workflows in Go repositories.

---

## Example 1 — Nil Pointer Dereference

User request:
"Service crashes when optional metadata is missing."

### Branch

bugfix/STR-520-nil-metadata-check

### RED

```go
func TestBuildMetadata_NilInput(t *testing.T) {
	result := BuildMetadata(nil)

	assert.Equal(t, "", result.Name)
}
```

Run:

```bash
go test ./internal/metadata
```

Result:
- failing

### GREEN

```go
if metadata == nil {
	return Metadata{}
}
```

### Verification

```bash
go test ./internal/metadata
go test ./...
```

Result:
- passing
